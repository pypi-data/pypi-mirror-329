from unittest.mock import patch

import pytest
from flask import Flask

from ucam_faas import FaaSGunicornApplication, cloud_event, raw_event
from ucam_faas.exceptions import UCAMFAASCouldNotProcess
from ucam_faas.testing import CloudEventFactory


# Raw events
@raw_event
def example_raw_event_no_exception(event):
    pass


@raw_event
def example_raw_event_handled_exception(event):
    raise UCAMFAASCouldNotProcess


@raw_event
def example_raw_event_unhandled_exception(event):
    raise Exception("Did not expect this")


# Cloud Events
@cloud_event
def example_cloud_event_no_exception(event):
    pass


@cloud_event
def example_cloud_event_handled_exception(event):
    raise UCAMFAASCouldNotProcess


@cloud_event
def example_cloud_event_unhandled_exception(event):
    raise Exception("Did not expect this")


def test_faas_gunicorn_application_bind():
    app = Flask(__name__)
    application = FaaSGunicornApplication(app, "0.0.0.0", "8080")

    with patch("gunicorn.app.base.BaseApplication.run") as mock_run:
        application.run()
        mock_run.assert_called_once()  # Ensures that the server's run method was indeed called


@pytest.mark.parametrize(
    "target_tuple",
    [
        (
            "example_raw_event_no_exception",
            "example_raw_event_handled_exception",
            "example_raw_event_unhandled_exception",
        ),
        (
            "example_cloud_event_no_exception",
            "example_cloud_event_handled_exception",
            "example_cloud_event_unhandled_exception",
        ),
    ],
)
def test_exceptions_raw_events(event_app_test_client_factory, target_tuple):
    this_file_path = "ucam_faas/tests/test_ucam_faas.py"

    # Both raw and cloud event functions except cloud eventd
    valid_cloud_event = CloudEventFactory.build().model_dump()

    # No exception
    test_client = event_app_test_client_factory(target=target_tuple[0], source=this_file_path)
    response = test_client.post("/", json=valid_cloud_event)
    assert response.status_code == 200

    # Handle exception
    test_client = event_app_test_client_factory(target=target_tuple[1], source=this_file_path)
    response = test_client.post("/", json=valid_cloud_event)
    assert response.status_code == 500
    assert "The function raised UCAMFAASCouldNotProcess" in response.data.decode()

    # Unhandled exception
    test_client = event_app_test_client_factory(target=target_tuple[2], source=this_file_path)
    response = test_client.post("/", json=valid_cloud_event)
    assert response.status_code == 500
