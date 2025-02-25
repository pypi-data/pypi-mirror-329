from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.consume_invite_request import ConsumeInviteRequest
from ...models.consume_invite_response import ConsumeInviteResponse
from ...models.validation_error_response import ValidationErrorResponse
from typing import Dict
from ...models.challenge_response import ChallengeResponse


def _get_kwargs(
    *,
    json_body: ConsumeInviteRequest,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v1/login/consume_invitation",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ChallengeResponse, ConsumeInviteResponse, ValidationErrorResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ConsumeInviteResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationErrorResponse.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ChallengeResponse.from_dict(response.json())

        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ChallengeResponse, ConsumeInviteResponse, ValidationErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: ConsumeInviteRequest,
) -> Response[Union[ChallengeResponse, ConsumeInviteResponse, ValidationErrorResponse]]:
    """Consume an invitation link.

     Consume an invitation link, granting access to the target org/user. Security policy
    may constrain the current login from joining external accounts.

    Args:
        json_body (ConsumeInviteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChallengeResponse, ConsumeInviteResponse, ValidationErrorResponse]]
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
    json_body: ConsumeInviteRequest,
) -> Optional[Union[ChallengeResponse, ConsumeInviteResponse, ValidationErrorResponse]]:
    """Consume an invitation link.

     Consume an invitation link, granting access to the target org/user. Security policy
    may constrain the current login from joining external accounts.

    Args:
        json_body (ConsumeInviteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChallengeResponse, ConsumeInviteResponse, ValidationErrorResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: ConsumeInviteRequest,
) -> Response[Union[ChallengeResponse, ConsumeInviteResponse, ValidationErrorResponse]]:
    """Consume an invitation link.

     Consume an invitation link, granting access to the target org/user. Security policy
    may constrain the current login from joining external accounts.

    Args:
        json_body (ConsumeInviteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChallengeResponse, ConsumeInviteResponse, ValidationErrorResponse]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: ConsumeInviteRequest,
) -> Optional[Union[ChallengeResponse, ConsumeInviteResponse, ValidationErrorResponse]]:
    """Consume an invitation link.

     Consume an invitation link, granting access to the target org/user. Security policy
    may constrain the current login from joining external accounts.

    Args:
        json_body (ConsumeInviteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChallengeResponse, ConsumeInviteResponse, ValidationErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
