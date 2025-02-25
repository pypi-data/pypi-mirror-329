from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.base_error_response import BaseErrorResponse
from ...models.validation_error_response import ValidationErrorResponse
from typing import cast
from typing import Dict


def _get_kwargs(
    *,
    state: str,
    code: str,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    params["state"] = state

    params["code"] = code

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": "/api/v1/login/complete_sso_pkce",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BaseErrorResponse, ValidationErrorResponse]]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationErrorResponse.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = BaseErrorResponse.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, BaseErrorResponse, ValidationErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    state: str,
    code: str,
) -> Response[Union[Any, BaseErrorResponse, ValidationErrorResponse]]:
    """Retrieve the OpenID token using the OIDC PKCE state code. May issue a login cookie and create a user
    session.

    Args:
        state (str):
        code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BaseErrorResponse, ValidationErrorResponse]]
    """

    kwargs = _get_kwargs(
        state=state,
        code=code,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    state: str,
    code: str,
) -> Optional[Union[Any, BaseErrorResponse, ValidationErrorResponse]]:
    """Retrieve the OpenID token using the OIDC PKCE state code. May issue a login cookie and create a user
    session.

    Args:
        state (str):
        code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BaseErrorResponse, ValidationErrorResponse]
    """

    return sync_detailed(
        client=client,
        state=state,
        code=code,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    state: str,
    code: str,
) -> Response[Union[Any, BaseErrorResponse, ValidationErrorResponse]]:
    """Retrieve the OpenID token using the OIDC PKCE state code. May issue a login cookie and create a user
    session.

    Args:
        state (str):
        code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BaseErrorResponse, ValidationErrorResponse]]
    """

    kwargs = _get_kwargs(
        state=state,
        code=code,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    state: str,
    code: str,
) -> Optional[Union[Any, BaseErrorResponse, ValidationErrorResponse]]:
    """Retrieve the OpenID token using the OIDC PKCE state code. May issue a login cookie and create a user
    session.

    Args:
        state (str):
        code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BaseErrorResponse, ValidationErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            state=state,
            code=code,
        )
    ).parsed
