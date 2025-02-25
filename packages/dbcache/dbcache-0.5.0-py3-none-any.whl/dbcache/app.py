from flask import Flask

from dbcache.http import kvstore_httpapi


def make_app(uri, *stores):
    app = Flask(__name__)
    api = kvstore_httpapi(uri, *stores)
    app.register_blueprint(
        api.bp
    )
    return app
