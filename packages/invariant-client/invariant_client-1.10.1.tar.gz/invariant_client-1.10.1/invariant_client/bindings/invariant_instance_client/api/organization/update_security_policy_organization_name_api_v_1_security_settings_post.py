from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.challenge_response import ChallengeResponse
from typing import cast, Union
from ...models.modify_allow_outbound_invitations_request import (
    ModifyAllowOutboundInvitationsRequest,
)
from ...models.modify_default_login_methods_request import (
    ModifyDefaultLoginMethodsRequest,
)
from ...models.validation_error_response import ValidationErrorResponse
from typing import Dict
from ...models.modify_allow_inbound_invitations_request import (
    ModifyAllowInboundInvitationsRequest,
)
from typing import cast
from ...models.base_error_response import BaseErrorResponse


def _get_kwargs(
    organization_name: str,
    *,
    json_body: Union[
        "ModifyAllowInboundInvitationsRequest",
        "ModifyAllowOutboundInvitationsRequest",
        "ModifyDefaultLoginMethodsRequest",
    ],
) -> Dict[str, Any]:
    json_json_body: Dict[str, Any]

    if isinstance(json_body, ModifyAllowInboundInvitationsRequest):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, ModifyAllowOutboundInvitationsRequest):
        json_json_body = json_body.to_dict()

    else:
        json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/{organization_name}/api/v1/security-settings".format(
            organization_name=organization_name,
        ),
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
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = BaseErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ChallengeResponse.from_dict(response.json())

        return response_401
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
    organization_name: str,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "ModifyAllowInboundInvitationsRequest",
        "ModifyAllowOutboundInvitationsRequest",
        "ModifyDefaultLoginMethodsRequest",
    ],
) -> Response[
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
]:
    """Update security policy

    Args:
        organization_name (str):
        json_body (Union['ModifyAllowInboundInvitationsRequest',
            'ModifyAllowOutboundInvitationsRequest', 'ModifyDefaultLoginMethodsRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]]
    """

    kwargs = _get_kwargs(
        organization_name=organization_name,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_name: str,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "ModifyAllowInboundInvitationsRequest",
        "ModifyAllowOutboundInvitationsRequest",
        "ModifyDefaultLoginMethodsRequest",
    ],
) -> Optional[
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
]:
    """Update security policy

    Args:
        organization_name (str):
        json_body (Union['ModifyAllowInboundInvitationsRequest',
            'ModifyAllowOutboundInvitationsRequest', 'ModifyDefaultLoginMethodsRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
    """

    return sync_detailed(
        organization_name=organization_name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    organization_name: str,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "ModifyAllowInboundInvitationsRequest",
        "ModifyAllowOutboundInvitationsRequest",
        "ModifyDefaultLoginMethodsRequest",
    ],
) -> Response[
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
]:
    """Update security policy

    Args:
        organization_name (str):
        json_body (Union['ModifyAllowInboundInvitationsRequest',
            'ModifyAllowOutboundInvitationsRequest', 'ModifyDefaultLoginMethodsRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]]
    """

    kwargs = _get_kwargs(
        organization_name=organization_name,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_name: str,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "ModifyAllowInboundInvitationsRequest",
        "ModifyAllowOutboundInvitationsRequest",
        "ModifyDefaultLoginMethodsRequest",
    ],
) -> Optional[
    Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
]:
    """Update security policy

    Args:
        organization_name (str):
        json_body (Union['ModifyAllowInboundInvitationsRequest',
            'ModifyAllowOutboundInvitationsRequest', 'ModifyDefaultLoginMethodsRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BaseErrorResponse, ChallengeResponse, ValidationErrorResponse]
    """

    return (
        await asyncio_detailed(
            organization_name=organization_name,
            client=client,
            json_body=json_body,
        )
    ).parsed
