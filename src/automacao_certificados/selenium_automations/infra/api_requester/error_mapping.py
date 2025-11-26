from http import HTTPStatus

from automacao_certificados.selenium_automations.core.exceptions import *

def map_error_response(route: str, status: int, body: dict):
    """
    Maps the error response from the API to the appropriate exception.

    :param route: The route of the API.
    :type route: str
    :param status: The status of the response.
    :type status: int
    :param body: The body of the response.
    :type body: dict
    :return: None.
    :rtype: None
    :raises RouteNotFoundError: If the route is not found.
    :raises NotFoundError: If the resource is not found.
    :raises BadRequestError: If the request is bad.
    :raises ConflictError: If there is a conflict.
    :raises UnexpectedError: If an unexpected error occurs.
    """
    if status in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED):
        raise ValueError(f"the response was sucessful: {status}")

    if status == HTTPStatus.NOT_FOUND:
        if body.get("detail") == "Not Found":
            raise RouteNotFoundError(route=route, message=f"Route not found: {route}")
        raise NotFoundError(route=route, message=body.get("message") or f"Resource not found. body response: {body}")

    if status == HTTPStatus.BAD_REQUEST:
        raise BadRequestError(route=route, message=body.get("message") or f"Bad request. body response: {body}")

    if status == HTTPStatus.CONFLICT:
        raise ConflictError(route=route, message=body.get("message") or f"Conflict error. body response: {body}")

    raise UnexpectedError(route=route, message=body.get("message") or f"Unexpected error. body response: {body}", status_code=status)



    