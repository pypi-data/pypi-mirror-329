import logging

from flask.logging import default_handler


def setup_dev_server_logging():
    # Log messages from everything (including pyquocca).
    root = logging.getLogger()
    root.addHandler(default_handler)
    root.setLevel("INFO")
    # Don't overwrite the format of the dev server.
    logging.getLogger("werkzeug").propagate = False
    # Log debugging for SQL.
    logging.getLogger("pyquocca.postgres").setLevel("DEBUG")
    logging.getLogger("pyquocca.mysql").setLevel("DEBUG")
