import os
import json
import logging
from datetime import datetime
from typing import Optional
from httpx import Response as HttpResponse
from elog_cli.elog_management_backend_client.client import AuthenticatedClient
from elog_cli.elog_management_backend_client.types import File, Response, UNSET
from elog_cli.elog_management_backend_client.models import (
    ApiResultResponseString, 
    ApiResultResponseListLogbookDTO, 
    ApiResultResponseEntryDTO, 
    ApiResultResponseLogbookDTO,
    ApiResultResponseBoolean,
    NewEntryWithAttachmentBody, 
    NewEntryDTO, 
    LogbookDTO, 
    EntryDTO, 
    UpdateTagDTO, 
    NewTagDTO,
    TagDTO,
    AuthorizationCache,
    EntrySummaryDTO
)
from elog_cli.elog_management_backend_client.api.entries_controller import get_full,search, update_entry_attachment_preview
from elog_cli.elog_management_backend_client.api.entries_controller_v_2 import new_entry_with_attachment
from elog_cli.elog_management_backend_client.api.logbooks_controller import get_all_logbook, get_logbook, create_tag as create_tag_api, update_tag as update_tag_api

__all__ = [
    "ElogApi",
    "ElogAPIError"
    # do not include _check_for_auth_manager_definition
]

class ElogAPIError(Exception):
    def __init__(self, http_resposne:HttpResponse):
        http_status_descriptions = {
            400: "Bad Request: The server could not understand the request due to invalid syntax.",
            401: "Unauthorized: The client must authenticate itself to get the requested response.",
            403: "Forbidden: The client does not have access rights to the content.",
            404: "Not Found: The server can not find the requested resource.",
            500: "Internal Server Error: The server has encountered a situation it doesn't know how to handle.",
            502: "Bad Gateway: The server, while acting as a gateway or proxy, received an invalid response from the upstream server.",
            503: "Service Unavailable: The server is not ready to handle the request.",
            504: "Gateway Timeout: The server, while acting as a gateway or proxy, did not get a response in time from the upstream server."
        }
        description = http_status_descriptions.get(http_resposne.status_code, "Unknown HTTP Error")
        try:
            error_content = json.loads(http_resposne.content)
            if isinstance(error_content, dict) and "errorMessage" in error_content:
                description = error_content["errorMessage"]
        except json.JSONDecodeError:
            pass
        
        super().__init__(f"HTTP Error: {http_resposne.status_code}\nDescription: {description}")

    def is_http_error(self) -> bool:
        return self.http_status is not None

    def is_api_error(self) -> bool:
        return self.http_status is None

class ElogApi():
    def __init__(self, endpoint:str):
        self._client = None
        self._endpoint = endpoint
        self._logger = logging.getLogger(__name__)

    def __del__(self):
        self._logger.debug("ElogApi object is deleted")
        self._client = None

    def set_authentication_token(self, token: str):
        """ Set the authentication token """
        self._token = token

    def _checkManager(self):
        if self._auth_manager is None:
            raise ElogAPIError("AuthManager is not initialized")

    def get_authenticated_client(self):
        """ Get the authenticated client """
        self._checkManager
        if self._token is None:
            raise ElogAPIError("Authentication token is not set")
        if self._endpoint is None:
            raise ElogAPIError("Endpoint is not set")
        
        self._logger.debug(f"Use url {self._endpoint}")
        if self._client is None:
            self._client = AuthenticatedClient(
                base_url = self._endpoint, 
                token=self._token,
                prefix="",
                auth_header_name="x-vouch-idp-accesstoken",
                # httpx_args={"event_hooks": {"request": [log_request], "response": [log_response]}}
            )
        return self._client

    def set_prodution(self, prod: bool):
        """ let the library operate on production end point or not """
        self._checkManager
        self._auth_manager.setEnvironment(prod)

    def create_entry(self, new_entry_dto:NewEntryDTO, attachments:list[str]) -> str:
        """
        Create a new entry with a title, text, tags and attachments.
        on success the id of the new entry is returned
        """
        client = self.get_authenticated_client()
        body = NewEntryWithAttachmentBody(
            entry=new_entry_dto,
            files=[
                File(
                    payload=open(attachment, "rb").read(), 
                    file_name=os.path.basename(attachment),  # Extract only the filename
                    mime_type="application/octet-stream"
                )
                for attachment in attachments]
        )
        result: Response[ApiResultResponseString] = new_entry_with_attachment.sync_detailed(client=client, body=body)
        if result.status_code == 201:
            if result.parsed.error_code == 0:
                return result.parsed.payload
            else:
                raise ElogAPIError(f"Error: {result.parsed.error_message}")
        else:
            raise ElogAPIError(result)

    def list_logbooks(self) -> list[LogbookDTO]:
        """List all logbooks"""
        client = self.get_authenticated_client()
        all_logbook_result: Response[ApiResultResponseListLogbookDTO] = get_all_logbook.sync_detailed(client=client)
        if all_logbook_result.status_code == 200:
            if all_logbook_result.parsed.error_code == 0:
                return all_logbook_result.parsed.payload
            else:
                raise ElogAPIError(f"Error: {all_logbook_result.parsed.error_message}")
        else:
            raise ElogAPIError(all_logbook_result)
        
    def list_entries(self, limit:Optional[int] = 10, context:Optional[int] = None, logbooks:list[int] = None, anchor:Optional[str] = None, end_date:datetime = None) -> list[EntrySummaryDTO]:
        """List all logbooks"""
        client = self.get_authenticated_client()
        all_logbook_result: Response[ApiResultResponseListLogbookDTO] = search.sync_detailed(
            client=client,
            authorization_cache=AuthorizationCache(),
            limit=limit if limit is not None else 10,
            context_size=context if context is not None else 10,
            anchor=anchor if anchor is not None else UNSET,
            end_date=end_date if end_date is not None else UNSET,
            logbooks=logbooks if logbooks is not None else UNSET
        )
        if all_logbook_result.status_code == 200:
            if all_logbook_result.parsed.error_code == 0:
                return all_logbook_result.parsed.payload
            else:
                raise ElogAPIError(f"Error: {all_logbook_result.parsed.error_message}")
        else:
            raise ElogAPIError(all_logbook_result)

    def get_full_logbook(self, logbook_id: str) -> LogbookDTO:
        """Show the full information of the logbook identified by LOGBOOKS"""
        client = self.get_authenticated_client()
        full_logbook_result: Response[ApiResultResponseLogbookDTO] = get_logbook.sync_detailed(client=client, logbook_id=logbook_id, include_authorizations=True)
        if full_logbook_result.status_code == 200:
            if full_logbook_result.parsed.error_code == 0:
                return full_logbook_result.parsed.payload
            else:
                raise ElogAPIError(f"Error: {full_logbook_result.parsed.error_message}")
        else:
            raise ElogAPIError(full_logbook_result)

    def update_entry_attachments(self, entry_id: str)->bool:
        """Update the attachments of the entry identified by entry_id"""
        client = self.get_authenticated_client()
        api_result: Response[ApiResultResponseBoolean] = update_entry_attachment_preview.sync_detailed(client=client, id=entry_id)
        if api_result.status_code == 200:
            if api_result.parsed.error_code == 0:
                return api_result.parsed.payload
            else:
                raise ElogAPIError(f"Error: {api_result.parsed.error_message}")
        else:
            raise ElogAPIError(api_result)

    def get_full_entry(self, entry_id: str)->EntryDTO:
        """Show the full information of the entry identified by entry_id"""
        client = self.get_authenticated_client()
        full_entry_result: Response[ApiResultResponseEntryDTO] = get_full.sync_detailed(
            client=client, 
            entry_id=entry_id,
            include_follow_ups=True,
            include_following_ups=True,
            include_history=True,
            include_references=True,
            include_referenced_by=True,
            include_superseded_by=True,
            authorization_cache=AuthorizationCache()
        )
        if full_entry_result.status_code == 200:
            if full_entry_result.parsed.error_code == 0:
                return full_entry_result.parsed.payload
            else:
                raise ElogAPIError(f"Error: {full_entry_result.parsed.error_message}")
        else:
            raise ElogAPIError(full_entry_result)

    def create_tag(self, logbook_id: str, new_tag_dto:NewTagDTO)->str:
        """
        Create a new tag with a name and description.
        on success the id of the new tag is returned
        """
        client = self.get_authenticated_client()
        response = create_tag_api.sync_detailed(client=client, logbook_id=logbook_id, body=new_tag_dto)
        if response.status_code == 201:
            if response.parsed.error_code == 0:
                return response.parsed.payload
            else:
                raise ElogAPIError(f"Error: {response.parsed.error_message}")
        else:
            raise ElogAPIError(response)

    def update_tag(self, logbook_id: str, tag_id: str, update_tag_dto:UpdateTagDTO)->TagDTO:
        """
        Update a tag with a name and description.
        On success the updated tag is returned
        """
        client = self.get_authenticated_client()
        response = update_tag_api.sync_detailed(client=client, logbook_id=logbook_id, tag_id=tag_id, body=update_tag_dto)
        if response.status_code == 200:
            if response.parsed.error_code == 0:
                return response.parsed.payload
            else:
                raise ElogAPIError(f"Error: {response.parsed.error_message}")
        else:
            raise ElogAPIError(response)