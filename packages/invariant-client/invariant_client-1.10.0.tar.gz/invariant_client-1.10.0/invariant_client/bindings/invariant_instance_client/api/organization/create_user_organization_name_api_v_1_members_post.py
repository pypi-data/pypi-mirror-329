from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.challenge_response import ChallengeResponse
from ...models.invite_response import InviteResponse
from typing import Union
from ...models.invite_user_request import InviteUserRequest
from ...models.validation_error_response import ValidationErrorResponse
from typing import Dict
from ...models.base_error_response import BaseErrorResponse
from ...models.create_managed_user_request import CreateManagedUserRequest
from ...models.create_member_response import CreateMemberResponse


def _get_kwargs(
    organization_name: str,
    *,
    json_body: Union["CreateManagedUserRequest", "InviteUserRequest"],
) -> Dict[str, Any]:
    json_json_body: Dict[str, Any]

    if isinstance(json_body, CreateManagedUserRequest):
        json_json_body = json_body.to_dict()

    else:
        json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/{organization_name}/api/v1/members".format(
            organization_name=organization_name,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        BaseErrorResponse,
        ChallengeResponse,
        Union["CreateMemberResponse", "InviteResponse"],
        ValidationErrorResponse,
    ]
]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(
            data: object,
        ) -> Union["CreateMemberResponse", "InviteResponse"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = CreateMemberResponse.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = InviteResponse.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

        return response_200
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
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = BaseErrorResponse.from_dict(response.json())

        return response_409
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        BaseErrorResponse,
        ChallengeResponse,
        Union["CreateMemberResponse", "InviteResponse"],
        ValidationErrorResponse,
    ]
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
    json_body: Union["CreateManagedUserRequest", "InviteUserRequest"],
) -> Response[
    Union[
        BaseErrorResponse,
        ChallengeResponse,
        Union["CreateMemberResponse", "InviteResponse"],
        ValidationErrorResponse,
    ]
]:
    """Add or invite a user.

    Args:
        organization_name (str):
        json_body (Union['CreateManagedUserRequest', 'InviteUserRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BaseErrorResponse, ChallengeResponse, Union['CreateMemberResponse', 'InviteResponse'], ValidationErrorResponse]]
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
    json_body: Union["CreateManagedUserRequest", "InviteUserRequest"],
) -> Optional[
    Union[
        BaseErrorResponse,
        ChallengeResponse,
        Union["CreateMemberResponse", "InviteResponse"],
        ValidationErrorResponse,
    ]
]:
    """Add or invite a user.

    Args:
        organization_name (str):
        json_body (Union['CreateManagedUserRequest', 'InviteUserRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BaseErrorResponse, ChallengeResponse, Union['CreateMemberResponse', 'InviteResponse'], ValidationErrorResponse]
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
    json_body: Union["CreateManagedUserRequest", "InviteUserRequest"],
) -> Response[
    Union[
        BaseErrorResponse,
        ChallengeResponse,
        Union["CreateMemberResponse", "InviteResponse"],
        ValidationErrorResponse,
    ]
]:
    """Add or invite a user.

    Args:
        organization_name (str):
        json_body (Union['CreateManagedUserRequest', 'InviteUserRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BaseErrorResponse, ChallengeResponse, Union['CreateMemberResponse', 'InviteResponse'], ValidationErrorResponse]]
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
    json_body: Union["CreateManagedUserRequest", "InviteUserRequest"],
) -> Optional[
    Union[
        BaseErrorResponse,
        ChallengeResponse,
        Union["CreateMemberResponse", "InviteResponse"],
        ValidationErrorResponse,
    ]
]:
    """Add or invite a user.

    Args:
        organization_name (str):
        json_body (Union['CreateManagedUserRequest', 'InviteUserRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BaseErrorResponse, ChallengeResponse, Union['CreateMemberResponse', 'InviteResponse'], ValidationErrorResponse]
    """

    return (
        await asyncio_detailed(
            organization_name=organization_name,
            client=client,
            json_body=json_body,
        )
    ).parsed
