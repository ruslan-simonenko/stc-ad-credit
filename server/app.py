from flask import Flask

from auth.auth_bp import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)


@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"
