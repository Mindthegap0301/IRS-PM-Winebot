import logging
from os import environ
from dotenv import load_dotenv

from flask import Flask, request as req, render_template, send_from_directory
from flask_restful import Api
from flask_cors import CORS, cross_origin

from app.config import config as app_config
from app.routes import initialize_routes

from app.errors import errors
from app.db import db

from flask_seeder import FlaskSeeder
#配置和初始化flask，包括设置路由、数据库、cors支持

def register_paths(app):
    @app.route("/")
    def index():
        return send_from_directory("static", "index.html")

    @app.route("/<path:path>")
    def files(path):
        return send_from_directory("static", path)


def register_extensions(app):
    db.init_app(app)
    # Seed DB
    seeder = FlaskSeeder()
    seeder.init_app(app, db)


def create_app():
    load_dotenv()
    APPLICATION_ENV = get_environment()
    conf = app_config[APPLICATION_ENV]
    app = Flask(conf.APP_NAME)
    app.config.from_object(conf)

    register_paths(app)

    register_extensions(app)

    # CORS
    CORS(app, allow_headers=[
        "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        supports_credentials=True)
    app.config['CORS_HEADERS'] = 'Content-Type'

    api = Api(app, errors=errors)
    initialize_routes(api)

    app.logger.setLevel(logging.NOTSET)

    return app


def get_environment():
    return environ.get('APPLICATION_ENV') or 'development'
