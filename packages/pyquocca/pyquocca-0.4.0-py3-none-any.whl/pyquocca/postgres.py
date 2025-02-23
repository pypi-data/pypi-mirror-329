import atexit
import logging
import os
import time
from typing import Generic, Optional, TypeVar, cast

from flask import Flask, g
from psycopg import Connection, Cursor
from psycopg.abc import Params, Query
from psycopg.rows import RowFactory, dict_row
from psycopg_pool import ConnectionPool, NullConnectionPool

from pyquocca.envvars import to_env_var


class LoggingCursor(Cursor):
    def execute(
        self,
        query: Query,
        params: Optional[Params] = None,
        *,
        prepare: Optional[bool] = None,
        binary: Optional[bool] = None,
    ):
        logger = logging.getLogger("pyquocca.postgres")

        start = time.monotonic_ns()
        try:
            super().execute(query, params, prepare=prepare, binary=binary)
            duration_ns = time.monotonic_ns() - start
        except Exception as exc:
            logger.error(
                "`%(query)s` with params `%(params)s` caused an error",
                {"query": query, "params": params},
            )
            raise exc

        logger.debug(
            "`%(query)s` with params `%(params)s` ran in %(duration_us).3f us",
            {"query": query, "params": params, "duration_us": duration_ns / 1000},
        )

        return self


T = TypeVar("T")


def connect(
    name: str = "postgres",
    row_factory: RowFactory[T] = dict_row,
    pool: Optional[bool] = None,
) -> ConnectionPool[Connection[T]] | NullConnectionPool[Connection[T]]:
    """Connects to a PostgreSQL database resource using provided environment variables
    (e.g. `{name}_HOST`).
    """

    env_prefix = to_env_var(name)
    host = os.getenv(f"{env_prefix}_HOST")
    database = os.getenv(f"{env_prefix}_DB") or os.getenv(f"{env_prefix}_DATABASE")
    user = os.getenv(f"{env_prefix}_USER")
    password = os.getenv(f"{env_prefix}_PASS") or os.getenv(f"{env_prefix}_PASSWORD")

    assert (
        host is not None
        and database is not None
        and user is not None
        and password is not None
    ), (
        f"Environment variables for PostgreSQL resource `{name}` not found (e.g. `{env_prefix}_HOST`)."
    )

    if pool is None:
        pool = os.getenv("KUBERNETES_SERVICE_HOST") is not None
    PoolClass = (
        ConnectionPool[Connection[T]] if pool else NullConnectionPool[Connection[T]]
    )

    return PoolClass(
        connection_class=Connection[T],
        kwargs={
            "host": host,
            "dbname": database,
            "user": user,
            "password": password,
            "row_factory": row_factory,
            "cursor_factory": LoggingCursor,
        },
    )


def execute(
    pool: ConnectionPool[Connection[T]],
    sql: Query,
    values: Optional[Params] = None,
):
    """Executes an SQL query against a database connection."""
    with pool.connection() as connection:
        return connection.execute(sql, values)


def fetch_one(
    pool: ConnectionPool[Connection[T]],
    sql: Query,
    values: Optional[Params] = None,
):
    """Executes an SQL query and calls `cursor.fetchone()` automatically."""
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.fetchone()


def fetch_all(
    pool: ConnectionPool[Connection[T]],
    sql: Query,
    values: Optional[Params] = None,
):
    """Executes an SQL query and calls `cursor.fetchall()` automatically."""
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.fetchall()


class UninitialisedError(Exception):
    pass


class FlaskPostgres(Generic[T]):
    """Flask extension to add basic DB transaction usage to requests using Postgres. Each request gets a connection
    from the pool and automatically commits or rolls back (if there is an unhandled exception) the entire
    transaction at the end of the request.
    """

    app: Optional[Flask]

    def __init__(
        self,
        name: str = "postgres",
        app: Optional[Flask] = None,
        row_factory: RowFactory[T] = dict_row,
        pool: Optional[bool] = None,
    ):
        self.name = name
        self.pool = connect(name, row_factory=row_factory, pool=pool)
        self.pool.wait()

        atexit.register(self.pool.close)

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app = app
        app.teardown_request(self._teardown_request)

    def _get_connections_dict(self):
        if self.app is None:
            raise UninitialisedError(
                "This Flask extension has not been initialised with .init_app() yet (required for auto-commit)."
            )

        # g._postgres_connections is a dictionary of database names to connections.
        try:
            assert type(g._postgres_connections) is dict
            return g._postgres_connections
        except (AttributeError, AssertionError):
            g._postgres_connections = {}
            return g._postgres_connections

    def _get_connection(self):
        connections = self._get_connections_dict()
        if self.name not in connections:
            return None
        return cast(
            Connection[T],
            connections[self.name],
        )

    def _get_or_create_connection(self):
        conn = self._get_connection()
        if conn is None:
            conn = self.pool.getconn()
            self._get_connections_dict()[self.name] = conn
        return conn

    def _teardown_request(self, exception: Optional[BaseException]):
        conn = self._get_connection()

        if conn is not None:
            if exception is None:
                conn.commit()
            else:
                conn.rollback()

            self.pool.putconn(conn)
            del self._get_connections_dict()[self.name]

    def cursor(self):
        """Returns a DB-API cursor object."""
        return self._get_or_create_connection().cursor()

    def execute(
        self,
        sql: Query,
        values: Optional[Params] = None,
    ):
        """Executes an SQL query."""
        return self._get_or_create_connection().cursor().execute(sql, values)

    def fetch_one(
        self,
        sql: Query,
        values: Optional[Params] = None,
    ):
        """Executes an SQL query and calls `cursor.fetchone()` automatically."""
        with self.cursor() as cur:
            cur.execute(sql, values)
            return cur.fetchone()

    def fetch_all(
        self,
        sql: Query,
        values: Optional[Params] = None,
    ):
        """Executes an SQL query and calls `cursor.fetchall()` automatically."""
        with self.cursor() as cur:
            cur.execute(sql, values)
            return cur.fetchall()
