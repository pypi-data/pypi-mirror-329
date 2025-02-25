import os.path

import click
import flask
import functions_framework
import gunicorn.app.base
from cloudevents.http.event import CloudEvent
from ucam_observe import get_structlog_logger
from ucam_observe.gunicorn import logconfig_dict
from werkzeug.exceptions import InternalServerError

from .exceptions import UCAMFAASException

# As well as making a logger available this should setup logging before the flask app is created
logger = get_structlog_logger(__name__)


def _common_function_wrapper(function):
    def _common_function_wrapper_internal(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except UCAMFAASException as exception:
            exception_name = exception.__class__.__name__

            logger.warning("function_failed_gracefully", exception_name=exception_name)

            raise InternalServerError(description=f"The function raised {exception_name}.")

        except Exception as exception:
            exception_name = exception.__class__.__name__

            logger.error("function_failed_uncaught_exception", exception_name=exception_name)

            # FIXME dump stack trace into logs for unhandled exception

            raise exception

    return _common_function_wrapper_internal


def raw_event(function):
    @_common_function_wrapper
    def _raw_event_internal(request: flask.Request) -> flask.typing.ResponseReturnValue:
        return_value = function(request.data)

        if return_value is not None:
            return return_value

        return "", 200

    _raw_event_internal.__name__ = function.__name__
    _raw_event_internal = functions_framework.http(_raw_event_internal)

    _raw_event_internal.__wrapped__ = function

    return _raw_event_internal


def cloud_event(function):
    @_common_function_wrapper
    def _cloud_event_internal(event: CloudEvent) -> None:
        return function(event.data)

    _cloud_event_internal.__name__ = function.__name__
    _cloud_event_internal = functions_framework.cloud_event(_cloud_event_internal)

    _cloud_event_internal.__wrapped__ = function
    return _cloud_event_internal


class FaaSGunicornApplication(gunicorn.app.base.Application):
    def __init__(self, app, host, port):
        self.host = host
        self.port = port
        self.app = app

        self.options = {
            "bind": "%s:%s" % (host, port),
            "workers": os.environ.get("WORKERS", 2),
            "threads": os.environ.get("THREADS", (os.cpu_count() or 1) * 4),
            "timeout": 0,
            "limit_request_line": 0,
            "logconfig_dict": logconfig_dict,
        }

        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key, value)

    def load(self):
        return self.app


def _initialize_ucam_faas_app(target, source, debug):
    app = functions_framework.create_app(target, source)

    app.logger.info("flask_app_created")

    @app.route("/healthy")
    @app.route("/status")
    def get_status():
        return "ok"

    return app


def run_ucam_faas(target, source, host, port, debug):  # pragma: no cover
    app = _initialize_ucam_faas_app(target, source, debug)
    if debug:
        app.run(host, port, debug)
    else:
        server = FaaSGunicornApplication(app, host, port)
        server.run()


@click.command()
@click.option("--target", envvar="FUNCTION_TARGET", type=click.STRING, required=True)
@click.option("--source", envvar="FUNCTION_SOURCE", type=click.Path(), default=None)
@click.option("--host", envvar="HOST", type=click.STRING, default="0.0.0.0")
@click.option("--port", envvar="PORT", type=click.INT, default=8080)
@click.option("--debug", envvar="DEBUG", is_flag=True)
def _cli(target, source, host, port, debug):  # pragma: no cover
    run_ucam_faas(target, source, host, port, debug)
