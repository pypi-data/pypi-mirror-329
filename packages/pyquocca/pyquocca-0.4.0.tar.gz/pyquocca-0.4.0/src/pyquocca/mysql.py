import logging
import os
import time
from typing import Any, Optional, Union

from flask import Flask, g
from pymysql import Connection
from pymysql.cursors import DictCursor

from pyquocca.envvars import to_env_var


class LoggingDictCursor(DictCursor):
    def execute(
        self,
        query,
        args=None,
    ):
        logger = logging.getLogger("pyquocca.mysql")

        start = time.monotonic_ns()
        try:
            result = super().execute(query, args)
            duration_ns = time.monotonic_ns() - start
        except Exception as exc:
            logger.error(
                "`%(query)s` with params `%(params)s` caused an error",
                {"query": query, "params": args},
            )
            raise exc

        logger.debug(
            "`%(query)s` with params `%(params)s` ran in %(duration_us).3f us",
            {"query": query, "params": args, "duration_us": duration_ns / 1000},
        )

        return result


def connect(name: str = "mysql"):
    """Connects to a MySQL database resource using provided environment variables
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
        f"Environment variables for MySQL resource `{name}` not found (e.g. `{env_prefix}_HOST`)."
    )

    return Connection(
        host=host,
        database=database,
        user=user,
        password=password,
        cursorclass=LoggingDictCursor,
    )


def execute(
    connection: Connection,
    sql: str,
    values: Optional[Union[tuple, list]] = None,
) -> LoggingDictCursor:
    """Executes an SQL query against a database connection."""
    cursor = connection.cursor()
    cursor.execute(sql, values)
    return cursor


def fetch_one(connection: Connection, sql: str, values=None) -> dict[str, Any] | None:
    """Executes an SQL query and calls `cursor.fetchone()` automatically."""
    with connection.cursor() as cursor:
        cursor.execute(sql, values)
        return cursor.fetchone()


def fetch_all(connection: Connection, sql: str, values=None) -> list[dict[str, Any]]:
    """Executes an SQL query and calls `cursor.fetchall()` automatically."""
    with connection.cursor() as cursor:
        cursor.execute(sql, values)
        return list(cursor.fetchall())


class UninitialisedError(Exception):
    pass


class FlaskMySQL:
    """Flask extension to add basic DB transaction usage to requests using MySQL. Each request gets a new connection
    and automatically commits or rolls back (if there is an unhandled exception) the entire transaction at
    the end of the request.
    """

    app: Optional[Flask]

    def __init__(self, name: str = "mysql", app: Optional[Flask] = None):
        self.name = name

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
        # g._mysql_connections is a dictionary of database names to connections.
        try:
            assert type(g._mysql_connections) is dict
            return g._mysql_connections
        except (AttributeError, AssertionError):
            g._mysql_connections = {}
            return g._mysql_connections

    def _get_connection(self) -> Connection | None:
        connections = self._get_connections_dict()
        if self.name not in connections:
            return None
        return connections[self.name]

    def _get_or_create_connection(self) -> Connection:
        db = self._get_connection()
        if db is None:
            db = connect(self.name)
            self._get_connections_dict()[self.name] = db
        return db

    def _teardown_request(self, exception: Optional[BaseException]):
        db = self._get_connection()

        if db is not None:
            if exception is None:
                db.commit()
                db.close()
            else:
                db.close()

            del self._get_connections_dict()[self.name]

    def execute(
        self,
        sql: str,
        values=None,
    ) -> LoggingDictCursor:
        """Executes an SQL query."""
        cursor = self._get_or_create_connection().cursor()
        cursor.execute(sql, values)
        return cursor

    def fetch_one(self, sql: str, values=None) -> dict[str, Any]:
        """Executes an SQL query and calls `cursor.fetchone()` automatically."""
        with self._get_or_create_connection().cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.fetchone()

    def fetch_all(self, sql: str, values=None) -> list[dict[str, Any]]:
        """Executes an SQL query and calls `cursor.fetchall()` automatically."""
        with self._get_or_create_connection().cursor() as cursor:
            cursor.execute(sql, values)
            return list(cursor.fetchall())
