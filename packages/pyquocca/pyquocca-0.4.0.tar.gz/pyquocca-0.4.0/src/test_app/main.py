from flask import Flask, jsonify
from pyquocca.logging import setup_dev_server_logging
from pyquocca.mysql import FlaskMySQL

app = Flask(__name__)

# db = FlaskPostgres()
db = FlaskMySQL()


@app.route("/")
def index():
    app.logger.info("Did a thing!")
    return jsonify(db.fetch_all("SELECT * FROM posts;"))


@app.route("/500")
def error():
    raise Exception("Oops!")


if __name__ == "__main__":
    setup_dev_server_logging()
    app.run(debug=True, host="0.0.0.0", port=8000)
