import pytest

from automacao_certificados.selenium_automations.infra.api_requester.error_mapping import map_error_response
from automacao_certificados.selenium_automations.core.exceptions import *

class TestNotFoundMapping:
    
    def test_if_raises_route_not_found_error(
        self,
    ):
        with pytest.raises(RouteNotFoundError) as e:
            map_error_response(
                route="test route",
                status=404,
                body={"detail": "Not Found"}
            )


    def test_if_raises_not_found_error_with_message(
        self,
    ):
        with pytest.raises(NotFoundError) as e:
            map_error_response(
                route="test route",
                status=404,
                body={"message": "not found resource"}
            )

        assert e.value.message == "not found resource"

    def test_if_raises_not_found_error_without_message(
        self,
    ):
        with pytest.raises(NotFoundError) as e:
            map_error_response(
                route="test route",
                status=404,
                body={}
            )

class TestBadrRequestMapping:
    def test_if_raises_bad_request_error_with_message(
        self,
    ):
        with pytest.raises(BadRequestError) as e:
            map_error_response(
                route="test route",
                status=400,
                body={"message": "bad request message"}
            )

        assert e.value.message == "bad request message"

    def test_if_raises_bad_request_error_without_message(
        self,
    ):
        with pytest.raises(BadRequestError) as e:
            map_error_response(
                route="test route",
                status=400,
                body={}
            )

class TestConflictMapping:
    def test_if_raises_conflict_error_with_message(
        self,
    ):
        with pytest.raises(ConflictError) as e:
            map_error_response(
                route="test route",
                status=409,
                body={"message": "conflict message"}
            )

        assert e.value.message == "conflict message"

    def test_if_raises_conflict_error_without_message(
        self,
    ):
        with pytest.raises(ConflictError) as e:
            map_error_response(
                route="test route",
                status=409,
                body={}
            )

class TestUnexpectedMapping:
    def test_if_raises_unexpected_error_with_message(
        self,
    ):
        with pytest.raises(UnexpectedError) as e:
            map_error_response(
                route="test route",
                status=500,
                body={"message": "unexpected error message"}
            )
        assert e.value.message == "unexpected error message"

    def test_if_raises_unexpected_error_without_message(
        self,
    ):
        with pytest.raises(UnexpectedError) as e:
            map_error_response(
                route="test route",
                status=500,
                body={}
            )
        assert e.value.message == "Unexpected error. body response: {}"

    def test_if_raises_unexpected_error_with_status_code(
        self,
    ):
        with pytest.raises(UnexpectedError) as e:
            map_error_response(
                route="test route",
                status=500,
                body={"message": "unexpected error message"}
            )
        assert e.value.status_code == 500
        