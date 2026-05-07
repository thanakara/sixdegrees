from flask import Flask, jsonify, request, render_template
from werkzeug.exceptions import HTTPException

from sixdegrees.config import settings
from sixdegrees.app.extensions import close_driver
from sixdegrees.app.blueprints.main import bp as main_bp
from sixdegrees.app.blueprints.movie import bp as movie_bp
from sixdegrees.app.blueprints.person import bp as person_bp


def create_app() -> Flask:
    app = Flask(
        import_name=__name__,
        static_folder="static",
        template_folder="templates",
    )

    app.config["DEBUG"] = settings.debug
    app.config["ENV"] = settings.flask_env

    _register_blueprints(app)
    _register_error_handlers(app)
    _register_teardown(app)

    return app


def _register_blueprints(app: Flask) -> None:
    app.register_blueprint(main_bp)
    app.register_blueprint(movie_bp, url_prefix="/movie")
    app.register_blueprint(person_bp, url_prefix="/person")


def _register_error_handlers(app: Flask) -> None:
    def _wants_json() -> bool:
        return request.accept_mimetypes.best_match(
            ["application/json", "text/html"]
        ) == "application/json"  # fmt: skip

    def _error_response(code: int, name: str, description: str):
        if _wants_json():
            return jsonify(error=name, description=description), code

        return render_template(
            template_name_or_list="error.html",
            code=code,
            name=name,
            description=description,
        ), code

    @app.errorhandler(404)
    def not_found(e: HTTPException):
        return _error_response(
            code=404,
            name="Not found",
            description="The page you're looking for doesn't exist.",
        )

    @app.errorhandler(422)
    def unprocessable(e: HTTPException):
        return _error_response(
            code=422,
            name="Unprocessable",
            description="The request was well-formed but contained invalid data.",
        )

    @app.errorhandler(500)
    def server_error(e: HTTPException):
        return _error_response(
            code=500,
            name="Server error",
            description="Something went wrong on our end.",
        )


def _register_teardown(app: Flask) -> None:

    @app.teardown_appcontext
    def shutdown_driver(exception=None) -> None:
        close_driver()
