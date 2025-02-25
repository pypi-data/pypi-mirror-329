

from dataclasses import dataclass
import io
import json
import pathlib
import ssl
from typing import IO, BinaryIO, Optional, TypeAlias, TypedDict, Union
import typing
import urllib.parse as urllib_parse
import pandas

import pyarrow.feather as feather

from invariant_client import pysdk
from invariant_client.bindings.invariant_instance_client.api.organization.ui_status_organization_name_api_v_1_ui_get import sync_detailed as ui_status_organization_name_api_v_1_ui_get

from invariant_client.bindings.invariant_instance_client.client import AuthenticatedClient as InstanceAuthenticatedClient
from invariant_client.bindings.invariant_instance_client import models
from invariant_client.bindings.invariant_instance_client import types
from invariant_client.bindings.invariant_instance_client.api.organization.list_reports_organization_name_api_v_1_reports_get import sync_detailed as list_reports_organization_name_api_v_1_reports_get
from invariant_client.bindings.invariant_instance_client.api.organization.refresh_organization_name_api_v1_refresh_post import sync_detailed as refresh_organization_name_api_v1_refresh_post
from invariant_client.bindings.invariant_instance_client.models.file_index import FileIndex
from invariant_client.bindings.invariant_instance_client.models.report_text_summary_request import ReportTextSummaryRequest
from invariant_client.bindings.invariant_login_client.client import AuthenticatedClient as LoginAuthenticatedClient, Client as LoginClient
from invariant_client.bindings.invariant_instance_client.api.organization.upload_snapshot_organization_name_api_v_1_uploadsnapshot_post import sync_detailed as upload_snapshot_organization_name_api_v_1_uploadsnapshot_post
from invariant_client.bindings.invariant_instance_client.api.organization.upload_snapshot_status_organization_name_api_v_1_uploadsnapshot_status_get import sync_detailed as upload_snapshot_status_organization_name_api_v_1_uploadsnapshot_status_get
from invariant_client.bindings.invariant_instance_client.api.organization.get_report_summary_organization_name_api_v_1_reports_report_id_summary_get import sync_detailed as get_report_summary_organization_name_api_v_1_reports_report_id_summary_get
from invariant_client.bindings.invariant_instance_client.api.organization.get_report_summary_text_summary_organization_name_api_v_1_reports_report_id_summary_text_get import sync_detailed as get_report_summary_text_summary_organization_name_api_v_1_reports_report_id_summary_text_get
from invariant_client.bindings.invariant_instance_client.api.organization.get_report_organization_name_api_v_1_reports_report_id_get import _get_kwargs as get_report_organization_name_api_v_1_reports_report_id_get__get_kwargs
from invariant_client.bindings.invariant_instance_client.api.organization.get_report_text_summary_organization_name_api_v_1_reports_report_id_text_get import sync_detailed as get_report_text_summary_organization_name_api_v_1_reports_report_id_text_get

from invariant_client.bindings.invariant_login_client.api.login.get_instances_api_v1_login_get_instances_post import sync_detailed as get_instances_api_v1_login_get_instances_post
from invariant_client.bindings.invariant_login_client.models.base_error_response import BaseErrorResponse
from invariant_client.bindings.invariant_login_client.models.validation_error_response import ValidationErrorResponse



DOMAIN_NAME = "https://prod.invariant.tech"


class NoOrganization(Exception):
    """Credentials must be paired with an organization name."""


ErrorResponseType: TypeAlias = BaseErrorResponse | ValidationErrorResponse


class RemoteError(Exception):
    """Generic server-side or connection error."""


class AuthorizationException(Exception):
    """Server authentication rejected."""


class Settings(TypedDict):
    debug: bool


@dataclass
class AccessCredential:
    """An invariant access credential."""

    access_token: Optional[str]
    refresh_token: Optional[str]
    organization_name: str

    @classmethod
    def from_env(cls, env_data: dict[str, str], base_url: Optional[str] = None, verify_ssl: Optional[str | bool | ssl.SSLContext] = None) -> Optional['AccessCredential']:
        access_token = env_data.get(cls.INVARIANT_ACCESS_TOKEN)
        refresh_token = env_data.get(cls.INVARIANT_API_TOKEN)
        organization_name = env_data.get(cls.INVARIANT_ORGANIZATION_NAME)
        return cls.build(organization_name, access_token, refresh_token, base_url=base_url, verify_ssl=verify_ssl)

    @classmethod
    def from_file(cls, file_path: 'typing.Union[pathlib.Path, str]', base_url: Optional[str] = None, verify_ssl: Optional[str | bool | ssl.SSLContext] = None) -> Optional['AccessCredential']:
        with open(file_path, "r") as f:
            data: dict = json.load(f)
        access_token = data.get(cls.INVARIANT_ACCESS_TOKEN)
        refresh_token = data.get(cls.INVARIANT_API_TOKEN)
        organization_name = data.get(cls.INVARIANT_ORGANIZATION_NAME)
        return cls.build(organization_name, access_token, refresh_token, base_url=base_url, verify_ssl=verify_ssl)

    @classmethod
    def build(cls, organization_name: str, access_token: Optional[str] = None, refresh_token: Optional[str] = None, base_url: Optional[str] = None, verify_ssl: Optional[str | bool | ssl.SSLContext] = None):
        # if access_token, try it (get ui? org?)
        # - if error and no RT, error to user
        # if refresh_token, but no organization_name, error to user
        # if refresh_token, try it, and error to user if error
        # otherwise just return None
        if not (organization_name or access_token or refresh_token):
            return None

        error: Exception = None
        verify_ssl = verify_ssl or ssl.create_default_context()
        if not organization_name:
            raise NoOrganization("INVARIANT_ORGANIZATION_NAME must be given.")
        if access_token:
            creds = cls(access_token=access_token, refresh_token=None, organization_name=organization_name)
            client = pysdk.Invariant(creds=creds, settings={}, base_url=base_url, verify_ssl=verify_ssl)
            try:
                client.status() # Will throw if access token is no good
                return creds
            except RemoteError as r_error:
                error = r_error
            # try it
            # try to set organization_name
            # if error and no RT, error to user
            # if error and RT, pass thru to RT
        if refresh_token:
            creds = cls(refresh_token=refresh_token, organization_name=organization_name, access_token=None)
            base_url = base_url or DOMAIN_NAME
            client = pysdk.InvariantLogin(settings={}, creds=creds, base_url=base_url, verify_ssl=verify_ssl)
            try:
                sdk = client.to_instance_sdk(verify_ssl)
                return sdk.creds
            except RemoteError as r_error:
                error = r_error

        if error:
            raise error

    def to_json(self) -> str:
        data = {}
        if self.access_token:
            data[AccessCredential.INVARIANT_ACCESS_TOKEN] = self.access_token
        if self.refresh_token:
            data[AccessCredential.INVARIANT_API_TOKEN] = self.refresh_token
        if self.organization_name:
            data[AccessCredential.INVARIANT_ORGANIZATION_NAME] = self.organization_name
        return json.dumps(data)


AccessCredential.INVARIANT_ACCESS_TOKEN = 'INVARIANT_ACCESS_TOKEN'
AccessCredential.INVARIANT_API_TOKEN = 'INVARIANT_API_TOKEN'
AccessCredential.INVARIANT_ORGANIZATION_NAME = 'INVARIANT_ORGANIZATION_NAME'


class Invariant:

    client: InstanceAuthenticatedClient
    creds: AccessCredential
    base_url: str

    def __init__(
            self,
            creds: AccessCredential,
            settings: dict,
            base_url: Optional[str] = None,
            verify_ssl: Optional[str | bool | ssl.SSLContext] = None,
            **kwargs):
        self.creds = creds
        self.settings = settings
        base_url = base_url or DOMAIN_NAME
        self.base_url = self.app_base_url(base_url)

        # Prefer to use the Python default SSL context over the HTTPX SSL context, which does not consider system trust roots
        # Users can revert to the HTTPX SSL context with 'verify_ssl=True'
        verify_ssl = verify_ssl or ssl.create_default_context()
        self.client = InstanceAuthenticatedClient(
            self.base_url,
            token=creds.access_token,
            verify_ssl=verify_ssl,
            **kwargs)
    
    @staticmethod
    def app_base_url(base_domain_name: str) -> str:
        url = urllib_parse.urlparse(base_domain_name)
        url = url._replace(netloc=f'app.{url.netloc}')
        return url.geturl()
    
    def upload_snapshot(
            self,
            source: 'Union[IO, BinaryIO]',
            network: Optional[str] = None,
            role: Optional[str] = None,
            compare_to: Optional[str] = None) -> models.UploadSnapshotResponse:
        """Zip and upload the current folder. Display a summary of processing results when complete."""
        response = upload_snapshot_organization_name_api_v_1_uploadsnapshot_post(
            self.creds.organization_name,
            client=self.client,
            multipart_data=models.BodyUploadSnapshotOrganizationNameApiV1UploadsnapshotPost(
                file=types.File(
                    payload=source,
                    file_name="snapshot_upload.zip",
                    mime_type="application/zip"
                )
            ),
            network=network,
            role=role)
        response = response.parsed
        # TODO idiom should be to examine error responses by status code as we do in the UI
        # Note that DNS NX_DOMAIN error actually raises httpx.ConnectError (-2: Name or service not known) at request time
        # Connection refused also raises httpx.ConnectError (111: Connection refused)
        if not response:
            raise RemoteError(f"Unable to connect to {self.base_url}")
        if isinstance(response, models.ChallengeResponse):
            raise AuthorizationException(f"{response.title}: {response.detail}")
        if not isinstance(response, models.UploadSnapshotResponse):
            raise RemoteError(response)
        return response
    
    def upload_is_running(self, uuid: str) -> models.UploadSnapshotStatusResponse:
        response = upload_snapshot_status_organization_name_api_v_1_uploadsnapshot_status_get(
            self.creds.organization_name,
            client=self.client,
            uuid=uuid,
        )
        response = response.parsed
        if not response:
            raise RemoteError(f"Unable to connect to {self.base_url}")
        if isinstance(response, models.ChallengeResponse):
            raise AuthorizationException(f"{response.title}: {response.detail}")
        if not isinstance(response, models.UploadSnapshotStatusResponse):
            raise RemoteError(response)
        return response

    def list_snapshots(
            self,
            filter_session: bool = None,
            filter_net: str = None,
            filter_role: str = None,
            limit: int = None) -> models.ListReportsResponse:
        kwargs = {}
        if filter_session:
            kwargs['filter_session'] = 1
        if filter_net:
            kwargs['filter_net'] = filter_net
        if filter_role:
            kwargs['filter_role'] = filter_role
        if limit:
            kwargs['limit'] = limit
        response = list_reports_organization_name_api_v_1_reports_get(
            self.creds.organization_name,
            client=self.client,
            **kwargs)
        response = response.parsed
        if not response:
            raise RemoteError(f"Unable to connect to {self.base_url}")
        if isinstance(response, models.ChallengeResponse):
            raise AuthorizationException(f"{response.title}: {response.detail}")
        if not isinstance(response, models.ListReportsResponse):
            raise RemoteError(response)
        return response

    def snapshot_detail(
            self,
            report_uuid: str) -> models.GetReportSummaryResponse:
        response = get_report_summary_organization_name_api_v_1_reports_report_id_summary_get(self.creds.organization_name, report_uuid, client=self.client)
        response = response.parsed
        if not response:
            raise RemoteError(f"Unable to connect to {self.base_url}")
        if isinstance(response, models.ChallengeResponse):
            raise AuthorizationException(f"{response.title}: {response.detail}")
        if not isinstance(response, models.GetReportSummaryResponse):
            raise RemoteError(response)
        return response

    def snapshot_detail_text(
            self,
            report_uuid: str,
            json_mode: bool
        ) -> models.ReportTextSummaryResponse:
        json_body = ReportTextSummaryRequest(
            traces=False,
            mode='json' if json_mode else 'text')
        response = get_report_summary_text_summary_organization_name_api_v_1_reports_report_id_summary_text_get(
            self.creds.organization_name,
            report_uuid,
            client=self.client,
            json_body=json_body)
        response = response.parsed
        if not response:
            raise RemoteError(f"Unable to connect to {self.base_url}")
        if isinstance(response, models.ChallengeResponse):
            raise AuthorizationException(f"{response.title}: {response.detail}")
        if not isinstance(response, models.ReportTextSummaryResponse):
            raise RemoteError(response)
        return response

    def snapshot_file(
            self,
            file_locator: FileIndex | str) -> pandas.DataFrame:
        """Download a remote file as a pandas DataFrame."""
        if isinstance(file_locator, str):
            file_uuids = [file_locator]
        elif isinstance(file_locator, FileIndex):
            file_uuids = file_locator.all_files
        else:
            raise ValueError('Unsupported file locator format. You may a newer client version.')

        responses: list[pandas.DataFrame] = []
        for file_uuid in file_uuids:
            kwargs = get_report_organization_name_api_v_1_reports_report_id_get__get_kwargs(
                organization_name=self.creds.organization_name,
                report_id=file_uuid,
            )
            response = self.client.get_httpx_client().request(
                **kwargs,
            )

            # TODO approach checking for errors more carefully as the expected value is not JSON
            if not response:
                raise RemoteError(f"Unable to connect to {self.base_url}")
            # if isinstance(response, models.ChallengeResponse):
            #     raise AuthorizationException(f"{response.title}: {response.detail}")
            # if isinstance(response, models.BaseErrorResponse):
            #     raise RemoteError(response)
            file_df = feather.read_feather(io.BytesIO(response.content))
            responses.append(file_df)
        combined_df = pandas.concat(responses)
        return combined_df

    def show(
            self,
            snapshot: str,
            file: str):
        pass

    def show_solution(
            self,
            snapshot: str,
            solution: str):
        pass

    def status(self) -> models.UIStatusResponse:
        if not self.creds or not self.creds.access_token:
            raise ValueError("status requires an access token.")
        response = ui_status_organization_name_api_v_1_ui_get(self.creds.organization_name, client=self.client)
        response = response.parsed
        if not response:
            raise RemoteError(f"Unable to connect to {self.base_url}")
        if isinstance(response, models.ChallengeResponse):
            raise AuthorizationException(f"{response.title}: {response.detail}")
        if not isinstance(response, models.UIStatusResponse):
            raise RemoteError(response)
        return response


class InvariantLogin:

    client: LoginAuthenticatedClient
    login_client: LoginAuthenticatedClient
    creds: AccessCredential
    login_creds: AccessCredential
    base_url: str

    def __init__(
            self,
            settings: dict,
            creds: Optional[AccessCredential] = None,
            login_session_creds: Optional[AccessCredential] = None,
            base_url: Optional[str] = None,
            verify_ssl: Optional[str | bool | ssl.SSLContext] = None,
            **kwargs):
        self.creds = creds
        self.login_creds = login_session_creds
        self.settings = settings
        self.base_url = base_url or DOMAIN_NAME

        # Prefer to use the Python default SSL context over the HTTPX SSL context, which does not consider system trust roots
        # Users can revert to the HTTPX SSL context with 'verify_ssl=True'
        verify_ssl = verify_ssl or ssl.create_default_context()

        # Three credential modes for the login service: no creds, login session, and refresh token
        if creds.refresh_token:
            self.client = LoginClient(
                self.base_url,
                cookies={'refresh_token_cookie': creds.refresh_token},
                verify_ssl=verify_ssl,
                **kwargs)
        elif login_session_creds:
            self.login_client = LoginAuthenticatedClient(
                self.base_url,
                token=login_session_creds.access_token,
                verify_ssl=verify_ssl,
                **kwargs)
        else:
            self.login_client = LoginClient(
                self.base_url,
                verify_ssl=verify_ssl,
                **kwargs)

    def get_instances(self):
        if not self.creds or not self.creds.refresh_token:
            raise ValueError("get_instances requires a refresh token.")
        response = get_instances_api_v1_login_get_instances_post(client=self.client)
        response = response.parsed
        if not response:
            raise RemoteError(f"Unable to connect to {self.base_url}")
        if isinstance(response, models.ChallengeResponse):
            raise AuthorizationException(f"{response.title}: {response.detail}")
        if not isinstance(response, list):
            raise RemoteError(response)
        return response

    def to_instance_sdk(self, verify_ssl: str | bool | ssl.SSLContext = True):
        if not self.creds or not self.creds.refresh_token or not self.creds.organization_name:
            raise ValueError("to_instance_sdk requires a refresh token and organization name.")
        base_url = Invariant.app_base_url(self.base_url)
        client = LoginClient(
            base_url,
            cookies={'refresh_token_cookie': self.creds.refresh_token},
            verify_ssl=verify_ssl)

        response = refresh_organization_name_api_v1_refresh_post(organization_name=self.creds.organization_name, client=client)
        response = response.parsed
        if not response:
            raise RemoteError(f"Unable to connect to {self.base_url}")
        if isinstance(response, models.ChallengeResponse):
            raise AuthorizationException(f"{response.title}: {response.detail}")
        if not isinstance(response, models.RefreshResponse):
            raise RemoteError(response)

        new_creds = AccessCredential(
            response.access_token,
            refresh_token=self.creds.refresh_token,
            organization_name=self.creds.organization_name)
        return Invariant(
            creds=new_creds,
            settings=self.settings,
            base_url=self.base_url,
            verify_ssl=verify_ssl)
