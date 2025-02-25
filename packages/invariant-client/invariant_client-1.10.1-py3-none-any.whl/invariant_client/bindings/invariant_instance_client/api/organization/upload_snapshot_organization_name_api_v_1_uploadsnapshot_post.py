from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.challenge_response import ChallengeResponse
from typing import cast, Union
from ...models.validation_error_response import ValidationErrorResponse
from typing import Dict
from typing import cast
from ...models.upload_snapshot_response import UploadSnapshotResponse
from ...types import UNSET, Unset
from ...models.base_error_response import BaseErrorResponse
from ...models.body_upload_snapshot_organization_name_api_v1_uploadsnapshot_post import (
    BodyUploadSnapshotOrganizationNameApiV1UploadsnapshotPost,
)
from typing import Union


def _get_kwargs(
    organization_name: str,
    *,
    multipart_data: BodyUploadSnapshotOrganizationNameApiV1UploadsnapshotPost,
    network: Union[None, Unset, str] = UNSET,
    role: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    json_network: Union[None, Unset, str]
    if isinstance(network, Unset):
        json_network = UNSET

    else:
        json_network = network

    params["network"] = json_network

    json_role: Union[None, Unset, str]
    if isinstance(role, Unset):
        json_role = UNSET

    else:
        json_role = role

    params["role"] = json_role

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": "/{organization_name}/api/v1/uploadsnapshot/".format(
            organization_name=organization_name,
        ),
        "files": multipart_multipart_data,
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Any,
        BaseErrorResponse,
        ChallengeResponse,
        UploadSnapshotResponse,
        ValidationErrorResponse,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UploadSnapshotResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationErrorResponse.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ChallengeResponse.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = BaseErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
        response_413 = cast(Any, None)
        return response_413
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        Any,
        BaseErrorResponse,
        ChallengeResponse,
        UploadSnapshotResponse,
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
    multipart_data: BodyUploadSnapshotOrganizationNameApiV1UploadsnapshotPost,
    network: Union[None, Unset, str] = UNSET,
    role: Union[None, Unset, str] = UNSET,
) -> Response[
    Union[
        Any,
        BaseErrorResponse,
        ChallengeResponse,
        UploadSnapshotResponse,
        ValidationErrorResponse,
    ]
]:
    """Upload a network snapshot.

    Args:
        organization_name (str):
        network (Union[None, Unset, str]):
        role (Union[None, Unset, str]):
        multipart_data (BodyUploadSnapshotOrganizationNameApiV1UploadsnapshotPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BaseErrorResponse, ChallengeResponse, UploadSnapshotResponse, ValidationErrorResponse]]
    """

    kwargs = _get_kwargs(
        organization_name=organization_name,
        multipart_data=multipart_data,
        network=network,
        role=role,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_name: str,
    *,
    client: AuthenticatedClient,
    multipart_data: BodyUploadSnapshotOrganizationNameApiV1UploadsnapshotPost,
    network: Union[None, Unset, str] = UNSET,
    role: Union[None, Unset, str] = UNSET,
) -> Optional[
    Union[
        Any,
        BaseErrorResponse,
        ChallengeResponse,
        UploadSnapshotResponse,
        ValidationErrorResponse,
    ]
]:
    """Upload a network snapshot.

    Args:
        organization_name (str):
        network (Union[None, Unset, str]):
        role (Union[None, Unset, str]):
        multipart_data (BodyUploadSnapshotOrganizationNameApiV1UploadsnapshotPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BaseErrorResponse, ChallengeResponse, UploadSnapshotResponse, ValidationErrorResponse]
    """

    return sync_detailed(
        organization_name=organization_name,
        client=client,
        multipart_data=multipart_data,
        network=network,
        role=role,
    ).parsed


async def asyncio_detailed(
    organization_name: str,
    *,
    client: AuthenticatedClient,
    multipart_data: BodyUploadSnapshotOrganizationNameApiV1UploadsnapshotPost,
    network: Union[None, Unset, str] = UNSET,
    role: Union[None, Unset, str] = UNSET,
) -> Response[
    Union[
        Any,
        BaseErrorResponse,
        ChallengeResponse,
        UploadSnapshotResponse,
        ValidationErrorResponse,
    ]
]:
    """Upload a network snapshot.

    Args:
        organization_name (str):
        network (Union[None, Unset, str]):
        role (Union[None, Unset, str]):
        multipart_data (BodyUploadSnapshotOrganizationNameApiV1UploadsnapshotPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BaseErrorResponse, ChallengeResponse, UploadSnapshotResponse, ValidationErrorResponse]]
    """

    kwargs = _get_kwargs(
        organization_name=organization_name,
        multipart_data=multipart_data,
        network=network,
        role=role,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_name: str,
    *,
    client: AuthenticatedClient,
    multipart_data: BodyUploadSnapshotOrganizationNameApiV1UploadsnapshotPost,
    network: Union[None, Unset, str] = UNSET,
    role: Union[None, Unset, str] = UNSET,
) -> Optional[
    Union[
        Any,
        BaseErrorResponse,
        ChallengeResponse,
        UploadSnapshotResponse,
        ValidationErrorResponse,
    ]
]:
    """Upload a network snapshot.

    Args:
        organization_name (str):
        network (Union[None, Unset, str]):
        role (Union[None, Unset, str]):
        multipart_data (BodyUploadSnapshotOrganizationNameApiV1UploadsnapshotPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BaseErrorResponse, ChallengeResponse, UploadSnapshotResponse, ValidationErrorResponse]
    """

    return (
        await asyncio_detailed(
            organization_name=organization_name,
            client=client,
            multipart_data=multipart_data,
            network=network,
            role=role,
        )
    ).parsed
