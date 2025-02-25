from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from typing import cast
from ...models.base_error_response import BaseErrorResponse
from ...models.validation_error_response import ValidationErrorResponse
from ...models.fulfill_client_login_request import FulfillClientLoginRequest
from typing import Dict
from ...models.challenge_response import ChallengeResponse


def _get_kwargs(
    *,
    json_body: FulfillClientLoginRequest,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v1/fulfill_client_login",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationErrorResponse.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ChallengeResponse.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = BaseErrorResponse.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = BaseErrorResponse.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: FulfillClientLoginRequest,
) -> Response[
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
]:
    """Fullfil a client login session.

     Resolve a client login session to a specific access token + org using a refresh token.

    Args:
        json_body (FulfillClientLoginRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: FulfillClientLoginRequest,
) -> Optional[
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
]:
    """Fullfil a client login session.

     Resolve a client login session to a specific access token + org using a refresh token.

    Args:
        json_body (FulfillClientLoginRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: FulfillClientLoginRequest,
) -> Response[
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
]:
    """Fullfil a client login session.

     Resolve a client login session to a specific access token + org using a refresh token.

    Args:
        json_body (FulfillClientLoginRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: FulfillClientLoginRequest,
) -> Optional[
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
]:
    """Fullfil a client login session.

     Resolve a client login session to a specific access token + org using a refresh token.

    Args:
        json_body (FulfillClientLoginRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
