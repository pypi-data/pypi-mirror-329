#  Copyright 2024 Palantir Technologies, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from __future__ import annotations

import warnings
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Union

import pydantic
from annotated_types import Len
from typing_extensions import Annotated
from typing_extensions import TypedDict
from typing_extensions import deprecated
from typing_extensions import overload

from foundry._core import ApiClient
from foundry._core import ApiResponse
from foundry._core import Auth
from foundry._core import BinaryStream
from foundry._core import Config
from foundry._core import RequestInfo
from foundry._core import ResourceIterator
from foundry._core import StreamingContextManager
from foundry._core.utils import maybe_ignore_preview
from foundry._errors import handle_unexpected
from foundry.v2.admin import errors as admin_errors
from foundry.v2.admin.group_membership import GroupMembershipClient
from foundry.v2.admin.models._get_user_markings_response import GetUserMarkingsResponse
from foundry.v2.admin.models._get_users_batch_request_element import (
    GetUsersBatchRequestElement,
)  # NOQA
from foundry.v2.admin.models._get_users_batch_request_element_dict import (
    GetUsersBatchRequestElementDict,
)  # NOQA
from foundry.v2.admin.models._get_users_batch_response import GetUsersBatchResponse
from foundry.v2.admin.models._list_users_response import ListUsersResponse
from foundry.v2.admin.models._search_users_response import SearchUsersResponse
from foundry.v2.admin.models._user import User
from foundry.v2.admin.models._user_search_filter import UserSearchFilter
from foundry.v2.admin.models._user_search_filter_dict import UserSearchFilterDict
from foundry.v2.admin.user_provider_info import UserProviderInfoClient
from foundry.v2.core.models._page_size import PageSize
from foundry.v2.core.models._page_token import PageToken
from foundry.v2.core.models._preview_mode import PreviewMode
from foundry.v2.core.models._principal_id import PrincipalId


class UserClient:
    """
    The API client for the User Resource.

    :param auth: Your auth configuration.
    :param hostname: Your Foundry hostname (for example, "myfoundry.palantirfoundry.com"). This can also include your API gateway service URI.
    :param config: Optionally specify the configuration for the HTTP session.
    """

    def __init__(
        self,
        auth: Auth,
        hostname: str,
        config: Optional[Config] = None,
    ):
        self._api_client = ApiClient(auth=auth, hostname=hostname, config=config)
        self.with_streaming_response = _UserClientStreaming(
            auth=auth, hostname=hostname, config=config
        )
        self.with_raw_response = _UserClientRaw(auth=auth, hostname=hostname, config=config)
        self.ProviderInfo = UserProviderInfoClient(auth=auth, hostname=hostname, config=config)
        self.GroupMembership = GroupMembershipClient(auth=auth, hostname=hostname, config=config)

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def delete(
        self,
        user_id: PrincipalId,
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> None:
        """
        Delete the User with the specified id.
        :param user_id: userId
        :type user_id: PrincipalId
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: None

        :raises DeleteUserPermissionDenied: Could not delete the User.
        """

        return self._api_client.call_api(
            RequestInfo(
                method="DELETE",
                resource_path="/v2/admin/users/{userId}",
                query_params={},
                path_params={
                    "userId": user_id,
                },
                header_params={},
                body=None,
                body_type=None,
                response_type=None,
                request_timeout=request_timeout,
                throwable_errors={
                    "DeleteUserPermissionDenied": admin_errors.DeleteUserPermissionDenied,
                },
            ),
        ).decode()

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def get(
        self,
        user_id: PrincipalId,
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> User:
        """
        Get the User with the specified id.
        :param user_id: userId
        :type user_id: PrincipalId
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: User

        :raises UserNotFound: The given User could not be found.
        """

        return self._api_client.call_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users/{userId}",
                query_params={},
                path_params={
                    "userId": user_id,
                },
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=User,
                request_timeout=request_timeout,
                throwable_errors={
                    "UserNotFound": admin_errors.UserNotFound,
                },
            ),
        ).decode()

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def get_batch(
        self,
        body: Annotated[
            List[Union[GetUsersBatchRequestElement, GetUsersBatchRequestElementDict]],
            Len(min_length=1, max_length=500),
        ],
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> GetUsersBatchResponse:
        """
        Execute multiple get requests on User.

        The maximum batch size for this endpoint is 500.
        :param body: Body of the request
        :type body: Annotated[List[Union[GetUsersBatchRequestElement, GetUsersBatchRequestElementDict]], Len(min_length=1, max_length=500)]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: GetUsersBatchResponse
        """

        return self._api_client.call_api(
            RequestInfo(
                method="POST",
                resource_path="/v2/admin/users/getBatch",
                query_params={},
                path_params={},
                header_params={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                body=body,
                body_type=Annotated[
                    List[GetUsersBatchRequestElementDict], Len(min_length=1, max_length=500)
                ],
                response_type=GetUsersBatchResponse,
                request_timeout=request_timeout,
                throwable_errors={},
            ),
        ).decode()

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def get_current(
        self,
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> User:
        """

        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: User

        :raises GetCurrentUserPermissionDenied: Could not getCurrent the User.
        """

        return self._api_client.call_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users/getCurrent",
                query_params={},
                path_params={},
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=User,
                request_timeout=request_timeout,
                throwable_errors={
                    "GetCurrentUserPermissionDenied": admin_errors.GetCurrentUserPermissionDenied,
                },
            ),
        ).decode()

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def get_markings(
        self,
        user_id: PrincipalId,
        *,
        preview: Optional[PreviewMode] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> GetUserMarkingsResponse:
        """
        Retrieve Markings that the user is currently a member of.
        :param user_id: userId
        :type user_id: PrincipalId
        :param preview: preview
        :type preview: Optional[PreviewMode]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: GetUserMarkingsResponse

        :raises GetMarkingsUserPermissionDenied: Could not getMarkings the User.
        """

        return self._api_client.call_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users/{userId}/getMarkings",
                query_params={
                    "preview": preview,
                },
                path_params={
                    "userId": user_id,
                },
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=GetUserMarkingsResponse,
                request_timeout=request_timeout,
                throwable_errors={
                    "GetMarkingsUserPermissionDenied": admin_errors.GetMarkingsUserPermissionDenied,
                },
            ),
        ).decode()

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def list(
        self,
        *,
        page_size: Optional[PageSize] = None,
        page_token: Optional[PageToken] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> ResourceIterator[User]:
        """
        Lists all Users.

        This is a paged endpoint. Each page may be smaller or larger than the requested page size. However, it is guaranteed that if there are more results available, the `nextPageToken` field will be populated. To get the next page, make the same request again, but set the value of the `pageToken` query parameter to be value of the `nextPageToken` value of the previous response. If there is no `nextPageToken` field in the response, you are on the last page.
        :param page_size: pageSize
        :type page_size: Optional[PageSize]
        :param page_token: pageToken
        :type page_token: Optional[PageToken]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: ResourceIterator[User]
        """

        return self._api_client.iterate_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users",
                query_params={
                    "pageSize": page_size,
                    "pageToken": page_token,
                },
                path_params={},
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=ListUsersResponse,
                request_timeout=request_timeout,
                throwable_errors={},
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def page(
        self,
        *,
        page_size: Optional[PageSize] = None,
        page_token: Optional[PageToken] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> ListUsersResponse:
        """
        Lists all Users.

        This is a paged endpoint. Each page may be smaller or larger than the requested page size. However, it is guaranteed that if there are more results available, the `nextPageToken` field will be populated. To get the next page, make the same request again, but set the value of the `pageToken` query parameter to be value of the `nextPageToken` value of the previous response. If there is no `nextPageToken` field in the response, you are on the last page.
        :param page_size: pageSize
        :type page_size: Optional[PageSize]
        :param page_token: pageToken
        :type page_token: Optional[PageToken]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: ListUsersResponse
        """

        warnings.warn(
            "The client.admin.User.page(...) method has been deprecated. Please use client.admin.User.list(...) instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        return self._api_client.call_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users",
                query_params={
                    "pageSize": page_size,
                    "pageToken": page_token,
                },
                path_params={},
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=ListUsersResponse,
                request_timeout=request_timeout,
                throwable_errors={},
            ),
        ).decode()

    @overload
    @deprecated(
        "Using the `stream` parameter is deprecated. Please use the `with_streaming_response` instead."
    )
    def profile_picture(
        self,
        user_id: PrincipalId,
        *,
        stream: Literal[True],
        chunk_size: Optional[int] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> BinaryStream:
        """

        :param user_id: userId
        :type user_id: PrincipalId
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param chunk_size: The number of bytes that should be read into memory for each chunk. If set to None, the data will become available as it arrives in whatever size is sent from the host.
        :type chunk_size: Optional[int]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: BinaryStream

        :raises GetProfilePictureOfUserPermissionDenied: Could not profilePicture the User.
        :raises InvalidProfilePicture: The user's profile picture is not a valid image
        """
        ...

    @overload
    def profile_picture(
        self,
        user_id: PrincipalId,
        *,
        stream: Literal[False] = False,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> bytes:
        """

        :param user_id: userId
        :type user_id: PrincipalId
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: bytes

        :raises GetProfilePictureOfUserPermissionDenied: Could not profilePicture the User.
        :raises InvalidProfilePicture: The user's profile picture is not a valid image
        """
        ...

    @overload
    @deprecated(
        "Using the `stream` parameter is deprecated. Please use the `with_streaming_response` instead."
    )
    def profile_picture(
        self,
        user_id: PrincipalId,
        *,
        stream: bool,
        chunk_size: Optional[int] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> Union[bytes, BinaryStream]:
        """

        :param user_id: userId
        :type user_id: PrincipalId
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param chunk_size: The number of bytes that should be read into memory for each chunk. If set to None, the data will become available as it arrives in whatever size is sent from the host.
        :type chunk_size: Optional[int]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: Union[bytes, BinaryStream]

        :raises GetProfilePictureOfUserPermissionDenied: Could not profilePicture the User.
        :raises InvalidProfilePicture: The user's profile picture is not a valid image
        """
        ...

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def profile_picture(
        self,
        user_id: PrincipalId,
        *,
        stream: bool = False,
        chunk_size: Optional[int] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> Union[bytes, BinaryStream]:
        """

        :param user_id: userId
        :type user_id: PrincipalId
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param chunk_size: The number of bytes that should be read into memory for each chunk. If set to None, the data will become available as it arrives in whatever size is sent from the host.
        :type chunk_size: Optional[int]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: Union[bytes, BinaryStream]

        :raises GetProfilePictureOfUserPermissionDenied: Could not profilePicture the User.
        :raises InvalidProfilePicture: The user's profile picture is not a valid image
        """

        if stream:
            warnings.warn(
                f"client.admin.User.profile_picture(..., stream=True, chunk_size={chunk_size}) is deprecated. Please use:\n\nwith client.admin.User.with_streaming_response.profile_picture(...) as response:\n    response.iter_bytes(chunk_size={chunk_size})\n",
                DeprecationWarning,
                stacklevel=2,
            )

        return self._api_client.call_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users/{userId}/profilePicture",
                query_params={},
                path_params={
                    "userId": user_id,
                },
                header_params={
                    "Accept": "application/octet-stream",
                },
                body=None,
                body_type=None,
                response_type=bytes,
                stream=stream,
                chunk_size=chunk_size,
                request_timeout=request_timeout,
                throwable_errors={
                    "GetProfilePictureOfUserPermissionDenied": admin_errors.GetProfilePictureOfUserPermissionDenied,
                    "InvalidProfilePicture": admin_errors.InvalidProfilePicture,
                },
            ),
        ).decode()

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def search(
        self,
        *,
        where: Union[UserSearchFilter, UserSearchFilterDict],
        page_size: Optional[PageSize] = None,
        page_token: Optional[PageToken] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> SearchUsersResponse:
        """

        :param where:
        :type where: Union[UserSearchFilter, UserSearchFilterDict]
        :param page_size:
        :type page_size: Optional[PageSize]
        :param page_token:
        :type page_token: Optional[PageToken]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: SearchUsersResponse

        :raises SearchUsersPermissionDenied: Could not search the User.
        """

        return self._api_client.call_api(
            RequestInfo(
                method="POST",
                resource_path="/v2/admin/users/search",
                query_params={},
                path_params={},
                header_params={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                body={
                    "where": where,
                    "pageSize": page_size,
                    "pageToken": page_token,
                },
                body_type=TypedDict(
                    "Body",
                    {  # type: ignore
                        "where": Union[UserSearchFilter, UserSearchFilterDict],
                        "pageSize": Optional[PageSize],
                        "pageToken": Optional[PageToken],
                    },
                ),
                response_type=SearchUsersResponse,
                request_timeout=request_timeout,
                throwable_errors={
                    "SearchUsersPermissionDenied": admin_errors.SearchUsersPermissionDenied,
                },
            ),
        ).decode()


class _UserClientRaw:
    """
    The API client for the User Resource.

    :param auth: Your auth configuration.
    :param hostname: Your Foundry hostname (for example, "myfoundry.palantirfoundry.com"). This can also include your API gateway service URI.
    :param config: Optionally specify the configuration for the HTTP session.
    """

    def __init__(
        self,
        auth: Auth,
        hostname: str,
        config: Optional[Config] = None,
    ):
        self._api_client = ApiClient(auth=auth, hostname=hostname, config=config)

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def delete(
        self,
        user_id: PrincipalId,
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> ApiResponse[None]:
        """
        Delete the User with the specified id.
        :param user_id: userId
        :type user_id: PrincipalId
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: ApiResponse[None]

        :raises DeleteUserPermissionDenied: Could not delete the User.
        """

        return self._api_client.call_api(
            RequestInfo(
                method="DELETE",
                resource_path="/v2/admin/users/{userId}",
                query_params={},
                path_params={
                    "userId": user_id,
                },
                header_params={},
                body=None,
                body_type=None,
                response_type=None,
                request_timeout=request_timeout,
                throwable_errors={
                    "DeleteUserPermissionDenied": admin_errors.DeleteUserPermissionDenied,
                },
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def get(
        self,
        user_id: PrincipalId,
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> ApiResponse[User]:
        """
        Get the User with the specified id.
        :param user_id: userId
        :type user_id: PrincipalId
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: ApiResponse[User]

        :raises UserNotFound: The given User could not be found.
        """

        return self._api_client.call_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users/{userId}",
                query_params={},
                path_params={
                    "userId": user_id,
                },
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=User,
                request_timeout=request_timeout,
                throwable_errors={
                    "UserNotFound": admin_errors.UserNotFound,
                },
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def get_batch(
        self,
        body: Annotated[
            List[Union[GetUsersBatchRequestElement, GetUsersBatchRequestElementDict]],
            Len(min_length=1, max_length=500),
        ],
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> ApiResponse[GetUsersBatchResponse]:
        """
        Execute multiple get requests on User.

        The maximum batch size for this endpoint is 500.
        :param body: Body of the request
        :type body: Annotated[List[Union[GetUsersBatchRequestElement, GetUsersBatchRequestElementDict]], Len(min_length=1, max_length=500)]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: ApiResponse[GetUsersBatchResponse]
        """

        return self._api_client.call_api(
            RequestInfo(
                method="POST",
                resource_path="/v2/admin/users/getBatch",
                query_params={},
                path_params={},
                header_params={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                body=body,
                body_type=Annotated[
                    List[GetUsersBatchRequestElementDict], Len(min_length=1, max_length=500)
                ],
                response_type=GetUsersBatchResponse,
                request_timeout=request_timeout,
                throwable_errors={},
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def get_current(
        self,
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> ApiResponse[User]:
        """

        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: ApiResponse[User]

        :raises GetCurrentUserPermissionDenied: Could not getCurrent the User.
        """

        return self._api_client.call_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users/getCurrent",
                query_params={},
                path_params={},
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=User,
                request_timeout=request_timeout,
                throwable_errors={
                    "GetCurrentUserPermissionDenied": admin_errors.GetCurrentUserPermissionDenied,
                },
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def get_markings(
        self,
        user_id: PrincipalId,
        *,
        preview: Optional[PreviewMode] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> ApiResponse[GetUserMarkingsResponse]:
        """
        Retrieve Markings that the user is currently a member of.
        :param user_id: userId
        :type user_id: PrincipalId
        :param preview: preview
        :type preview: Optional[PreviewMode]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: ApiResponse[GetUserMarkingsResponse]

        :raises GetMarkingsUserPermissionDenied: Could not getMarkings the User.
        """

        return self._api_client.call_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users/{userId}/getMarkings",
                query_params={
                    "preview": preview,
                },
                path_params={
                    "userId": user_id,
                },
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=GetUserMarkingsResponse,
                request_timeout=request_timeout,
                throwable_errors={
                    "GetMarkingsUserPermissionDenied": admin_errors.GetMarkingsUserPermissionDenied,
                },
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def list(
        self,
        *,
        page_size: Optional[PageSize] = None,
        page_token: Optional[PageToken] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> ApiResponse[ListUsersResponse]:
        """
        Lists all Users.

        This is a paged endpoint. Each page may be smaller or larger than the requested page size. However, it is guaranteed that if there are more results available, the `nextPageToken` field will be populated. To get the next page, make the same request again, but set the value of the `pageToken` query parameter to be value of the `nextPageToken` value of the previous response. If there is no `nextPageToken` field in the response, you are on the last page.
        :param page_size: pageSize
        :type page_size: Optional[PageSize]
        :param page_token: pageToken
        :type page_token: Optional[PageToken]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: ApiResponse[ListUsersResponse]
        """

        return self._api_client.call_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users",
                query_params={
                    "pageSize": page_size,
                    "pageToken": page_token,
                },
                path_params={},
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=ListUsersResponse,
                request_timeout=request_timeout,
                throwable_errors={},
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def page(
        self,
        *,
        page_size: Optional[PageSize] = None,
        page_token: Optional[PageToken] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> ApiResponse[ListUsersResponse]:
        """
        Lists all Users.

        This is a paged endpoint. Each page may be smaller or larger than the requested page size. However, it is guaranteed that if there are more results available, the `nextPageToken` field will be populated. To get the next page, make the same request again, but set the value of the `pageToken` query parameter to be value of the `nextPageToken` value of the previous response. If there is no `nextPageToken` field in the response, you are on the last page.
        :param page_size: pageSize
        :type page_size: Optional[PageSize]
        :param page_token: pageToken
        :type page_token: Optional[PageToken]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: ApiResponse[ListUsersResponse]
        """

        warnings.warn(
            "The client.admin.User.page(...) method has been deprecated. Please use client.admin.User.list(...) instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        return self._api_client.call_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users",
                query_params={
                    "pageSize": page_size,
                    "pageToken": page_token,
                },
                path_params={},
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=ListUsersResponse,
                request_timeout=request_timeout,
                throwable_errors={},
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def profile_picture(
        self,
        user_id: PrincipalId,
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> ApiResponse[bytes]:
        """

        :param user_id: userId
        :type user_id: PrincipalId
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: ApiResponse[bytes]

        :raises GetProfilePictureOfUserPermissionDenied: Could not profilePicture the User.
        :raises InvalidProfilePicture: The user's profile picture is not a valid image
        """

        return self._api_client.call_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users/{userId}/profilePicture",
                query_params={},
                path_params={
                    "userId": user_id,
                },
                header_params={
                    "Accept": "application/octet-stream",
                },
                body=None,
                body_type=None,
                response_type=bytes,
                request_timeout=request_timeout,
                throwable_errors={
                    "GetProfilePictureOfUserPermissionDenied": admin_errors.GetProfilePictureOfUserPermissionDenied,
                    "InvalidProfilePicture": admin_errors.InvalidProfilePicture,
                },
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def search(
        self,
        *,
        where: Union[UserSearchFilter, UserSearchFilterDict],
        page_size: Optional[PageSize] = None,
        page_token: Optional[PageToken] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> ApiResponse[SearchUsersResponse]:
        """

        :param where:
        :type where: Union[UserSearchFilter, UserSearchFilterDict]
        :param page_size:
        :type page_size: Optional[PageSize]
        :param page_token:
        :type page_token: Optional[PageToken]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: ApiResponse[SearchUsersResponse]

        :raises SearchUsersPermissionDenied: Could not search the User.
        """

        return self._api_client.call_api(
            RequestInfo(
                method="POST",
                resource_path="/v2/admin/users/search",
                query_params={},
                path_params={},
                header_params={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                body={
                    "where": where,
                    "pageSize": page_size,
                    "pageToken": page_token,
                },
                body_type=TypedDict(
                    "Body",
                    {  # type: ignore
                        "where": Union[UserSearchFilter, UserSearchFilterDict],
                        "pageSize": Optional[PageSize],
                        "pageToken": Optional[PageToken],
                    },
                ),
                response_type=SearchUsersResponse,
                request_timeout=request_timeout,
                throwable_errors={
                    "SearchUsersPermissionDenied": admin_errors.SearchUsersPermissionDenied,
                },
            ),
        )


class _UserClientStreaming:
    """
    The API client for the User Resource.

    :param auth: Your auth configuration.
    :param hostname: Your Foundry hostname (for example, "myfoundry.palantirfoundry.com"). This can also include your API gateway service URI.
    :param config: Optionally specify the configuration for the HTTP session.
    """

    def __init__(
        self,
        auth: Auth,
        hostname: str,
        config: Optional[Config] = None,
    ):
        self._api_client = ApiClient(auth=auth, hostname=hostname, config=config)

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def delete(
        self,
        user_id: PrincipalId,
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> StreamingContextManager[None]:
        """
        Delete the User with the specified id.
        :param user_id: userId
        :type user_id: PrincipalId
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: StreamingContextManager[None]

        :raises DeleteUserPermissionDenied: Could not delete the User.
        """

        return self._api_client.stream_api(
            RequestInfo(
                method="DELETE",
                resource_path="/v2/admin/users/{userId}",
                query_params={},
                path_params={
                    "userId": user_id,
                },
                header_params={},
                body=None,
                body_type=None,
                response_type=None,
                request_timeout=request_timeout,
                throwable_errors={
                    "DeleteUserPermissionDenied": admin_errors.DeleteUserPermissionDenied,
                },
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def get(
        self,
        user_id: PrincipalId,
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> StreamingContextManager[User]:
        """
        Get the User with the specified id.
        :param user_id: userId
        :type user_id: PrincipalId
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: StreamingContextManager[User]

        :raises UserNotFound: The given User could not be found.
        """

        return self._api_client.stream_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users/{userId}",
                query_params={},
                path_params={
                    "userId": user_id,
                },
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=User,
                request_timeout=request_timeout,
                throwable_errors={
                    "UserNotFound": admin_errors.UserNotFound,
                },
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def get_batch(
        self,
        body: Annotated[
            List[Union[GetUsersBatchRequestElement, GetUsersBatchRequestElementDict]],
            Len(min_length=1, max_length=500),
        ],
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> StreamingContextManager[GetUsersBatchResponse]:
        """
        Execute multiple get requests on User.

        The maximum batch size for this endpoint is 500.
        :param body: Body of the request
        :type body: Annotated[List[Union[GetUsersBatchRequestElement, GetUsersBatchRequestElementDict]], Len(min_length=1, max_length=500)]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: StreamingContextManager[GetUsersBatchResponse]
        """

        return self._api_client.stream_api(
            RequestInfo(
                method="POST",
                resource_path="/v2/admin/users/getBatch",
                query_params={},
                path_params={},
                header_params={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                body=body,
                body_type=Annotated[
                    List[GetUsersBatchRequestElementDict], Len(min_length=1, max_length=500)
                ],
                response_type=GetUsersBatchResponse,
                request_timeout=request_timeout,
                throwable_errors={},
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def get_current(
        self,
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> StreamingContextManager[User]:
        """

        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: StreamingContextManager[User]

        :raises GetCurrentUserPermissionDenied: Could not getCurrent the User.
        """

        return self._api_client.stream_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users/getCurrent",
                query_params={},
                path_params={},
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=User,
                request_timeout=request_timeout,
                throwable_errors={
                    "GetCurrentUserPermissionDenied": admin_errors.GetCurrentUserPermissionDenied,
                },
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def get_markings(
        self,
        user_id: PrincipalId,
        *,
        preview: Optional[PreviewMode] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> StreamingContextManager[GetUserMarkingsResponse]:
        """
        Retrieve Markings that the user is currently a member of.
        :param user_id: userId
        :type user_id: PrincipalId
        :param preview: preview
        :type preview: Optional[PreviewMode]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: StreamingContextManager[GetUserMarkingsResponse]

        :raises GetMarkingsUserPermissionDenied: Could not getMarkings the User.
        """

        return self._api_client.stream_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users/{userId}/getMarkings",
                query_params={
                    "preview": preview,
                },
                path_params={
                    "userId": user_id,
                },
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=GetUserMarkingsResponse,
                request_timeout=request_timeout,
                throwable_errors={
                    "GetMarkingsUserPermissionDenied": admin_errors.GetMarkingsUserPermissionDenied,
                },
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def list(
        self,
        *,
        page_size: Optional[PageSize] = None,
        page_token: Optional[PageToken] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> StreamingContextManager[ListUsersResponse]:
        """
        Lists all Users.

        This is a paged endpoint. Each page may be smaller or larger than the requested page size. However, it is guaranteed that if there are more results available, the `nextPageToken` field will be populated. To get the next page, make the same request again, but set the value of the `pageToken` query parameter to be value of the `nextPageToken` value of the previous response. If there is no `nextPageToken` field in the response, you are on the last page.
        :param page_size: pageSize
        :type page_size: Optional[PageSize]
        :param page_token: pageToken
        :type page_token: Optional[PageToken]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: StreamingContextManager[ListUsersResponse]
        """

        return self._api_client.stream_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users",
                query_params={
                    "pageSize": page_size,
                    "pageToken": page_token,
                },
                path_params={},
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=ListUsersResponse,
                request_timeout=request_timeout,
                throwable_errors={},
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def page(
        self,
        *,
        page_size: Optional[PageSize] = None,
        page_token: Optional[PageToken] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> StreamingContextManager[ListUsersResponse]:
        """
        Lists all Users.

        This is a paged endpoint. Each page may be smaller or larger than the requested page size. However, it is guaranteed that if there are more results available, the `nextPageToken` field will be populated. To get the next page, make the same request again, but set the value of the `pageToken` query parameter to be value of the `nextPageToken` value of the previous response. If there is no `nextPageToken` field in the response, you are on the last page.
        :param page_size: pageSize
        :type page_size: Optional[PageSize]
        :param page_token: pageToken
        :type page_token: Optional[PageToken]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: StreamingContextManager[ListUsersResponse]
        """

        warnings.warn(
            "The client.admin.User.page(...) method has been deprecated. Please use client.admin.User.list(...) instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        return self._api_client.stream_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users",
                query_params={
                    "pageSize": page_size,
                    "pageToken": page_token,
                },
                path_params={},
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=ListUsersResponse,
                request_timeout=request_timeout,
                throwable_errors={},
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def profile_picture(
        self,
        user_id: PrincipalId,
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> StreamingContextManager[bytes]:
        """

        :param user_id: userId
        :type user_id: PrincipalId
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: StreamingContextManager[bytes]

        :raises GetProfilePictureOfUserPermissionDenied: Could not profilePicture the User.
        :raises InvalidProfilePicture: The user's profile picture is not a valid image
        """

        return self._api_client.stream_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/admin/users/{userId}/profilePicture",
                query_params={},
                path_params={
                    "userId": user_id,
                },
                header_params={
                    "Accept": "application/octet-stream",
                },
                body=None,
                body_type=None,
                response_type=bytes,
                request_timeout=request_timeout,
                throwable_errors={
                    "GetProfilePictureOfUserPermissionDenied": admin_errors.GetProfilePictureOfUserPermissionDenied,
                    "InvalidProfilePicture": admin_errors.InvalidProfilePicture,
                },
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def search(
        self,
        *,
        where: Union[UserSearchFilter, UserSearchFilterDict],
        page_size: Optional[PageSize] = None,
        page_token: Optional[PageToken] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> StreamingContextManager[SearchUsersResponse]:
        """

        :param where:
        :type where: Union[UserSearchFilter, UserSearchFilterDict]
        :param page_size:
        :type page_size: Optional[PageSize]
        :param page_token:
        :type page_token: Optional[PageToken]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: StreamingContextManager[SearchUsersResponse]

        :raises SearchUsersPermissionDenied: Could not search the User.
        """

        return self._api_client.stream_api(
            RequestInfo(
                method="POST",
                resource_path="/v2/admin/users/search",
                query_params={},
                path_params={},
                header_params={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                body={
                    "where": where,
                    "pageSize": page_size,
                    "pageToken": page_token,
                },
                body_type=TypedDict(
                    "Body",
                    {  # type: ignore
                        "where": Union[UserSearchFilter, UserSearchFilterDict],
                        "pageSize": Optional[PageSize],
                        "pageToken": Optional[PageToken],
                    },
                ),
                response_type=SearchUsersResponse,
                request_timeout=request_timeout,
                throwable_errors={
                    "SearchUsersPermissionDenied": admin_errors.SearchUsersPermissionDenied,
                },
            ),
        )
