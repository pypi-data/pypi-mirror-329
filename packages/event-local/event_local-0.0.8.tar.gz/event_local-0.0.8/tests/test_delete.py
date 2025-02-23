from http import HTTPStatus

from python_sdk_remote.http_response import create_authorization_http_headers
from user_context_remote.user_context import UserContext

from src.events_local import EventsLocal
from src.handler import deleteHandler

user_jwt = UserContext().get_user_jwt()


class TestDelete:
    def test_valid_id(self):
        event = {
            "pathParameters": {"eventId": EventsLocal().get_test_event_id()},
            "headers": create_authorization_http_headers(user_jwt),
        }
        response = deleteHandler(event, None)
        assert response["statusCode"] == HTTPStatus.OK.value
        assert response["body"] == '{"message": "Event deleted successfully"}'

    def test_invalid_id(self):
        event = {
            "pathParameters": {"eventId": "invalid"},
            "headers": create_authorization_http_headers(user_jwt),
        }
        response = deleteHandler(event, None)
        assert response["statusCode"] != HTTPStatus.OK.value
        # Add event_id number
        assert '{"error": ' in response["body"]
