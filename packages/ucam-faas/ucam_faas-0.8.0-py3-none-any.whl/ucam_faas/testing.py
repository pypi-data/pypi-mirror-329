from . import _initialize_ucam_faas_app

try:
    from cloudevents.pydantic import CloudEvent
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pytest import fixture

    @fixture
    def event_app_test_client_factory():
        def _event_app_client(target, source=None):
            test_app = _initialize_ucam_faas_app(target, source, True)
            return test_app.test_client()

        return _event_app_client

    class CloudEventFactory(ModelFactory):
        __model__ = CloudEvent

        specversion = "1.0"

except ImportError:
    pass
