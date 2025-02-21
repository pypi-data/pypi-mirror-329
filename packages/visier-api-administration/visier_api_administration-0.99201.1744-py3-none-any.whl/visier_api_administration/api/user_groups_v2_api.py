# coding: utf-8

"""
    Visier Administration APIs

    Visier APIs for managing your tenant or tenants in Visier. You can programmatically manage user accounts in Visier, the profiles and permissions assigned to users, and to make changes in projects and publish projects to production. Administrating tenant users can use administration APIs to manage their analytic tenants and consolidated analytics tenants.<br>**Note:** If you submit API requests for changes that cause a project to publish to production (such as assigning permissions to users or updating permissions), each request is individually published to production, resulting in hundreds or thousands of production versions. We recommend that you use the `ProjectID` request header to make changes in a project, if `ProjectID` is available for the API endpoint.

    The version of the OpenAPI document: 22222222.99201.1744
    Contact: alpine@visier.com

    Please note that this SDK is currently in beta.
    Functionality and behavior may change in future releases.
    We encourage you to provide feedback and report any issues encountered during your use.
"""  # noqa: E501

import warnings
from pydantic import validate_call, Field, StrictFloat, StrictStr, StrictInt
from typing import Any, Dict, List, Optional, Tuple, Union
from typing_extensions import Annotated

from visier_api_core import ApiClient, ApiResponse, RequestSerialized, RESTResponseType

from pydantic import Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Optional
from typing_extensions import Annotated
from visier_api_administration.models.delete_user_group_v2_request import DeleteUserGroupV2Request
from visier_api_administration.models.user_group_change_definition_dto import UserGroupChangeDefinitionDTO
from visier_api_administration.models.user_group_change_response_dto import UserGroupChangeResponseDTO
from visier_api_administration.models.user_group_delete_response_dto import UserGroupDeleteResponseDTO
from visier_api_administration.models.user_group_single_delete_response_dto import UserGroupSingleDeleteResponseDTO
from visier_api_administration.models.user_groups_change_dto import UserGroupsChangeDTO
from visier_api_administration.models.user_groups_delete_request_dto import UserGroupsDeleteRequestDTO
import visier_api_administration.models


class UserGroupsV2Api:
    """
    This class provides methods to make requests to the Visier API.
    It uses the ApiClient to handle the HTTP requests and responses.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client


    @validate_call
    def create_user_groups(
        self,
        user_groups_change_dto: UserGroupsChangeDTO,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> UserGroupChangeResponseDTO:
        """Create multiple user groups

        Create new user groups. To specify the tenant in which to add new user groups, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header.   To specify the project in which to create new user groups, provide a project UUID in the `ProjectID` request header or `projectId` for each user group in the request body.

        :param user_groups_change_dto: (required)
        :type user_groups_change_dto: UserGroupsChangeDTO
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._create_user_groups_serialize(
            user_groups_change_dto=user_groups_change_dto,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupChangeResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_administration.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def create_user_groups_with_http_info(
        self,
        user_groups_change_dto: UserGroupsChangeDTO,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[UserGroupChangeResponseDTO]:
        """Create multiple user groups

        Create new user groups. To specify the tenant in which to add new user groups, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header.   To specify the project in which to create new user groups, provide a project UUID in the `ProjectID` request header or `projectId` for each user group in the request body.

        :param user_groups_change_dto: (required)
        :type user_groups_change_dto: UserGroupsChangeDTO
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._create_user_groups_serialize(
            user_groups_change_dto=user_groups_change_dto,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupChangeResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_administration.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def create_user_groups_without_preload_content(
        self,
        user_groups_change_dto: UserGroupsChangeDTO,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Create multiple user groups

        Create new user groups. To specify the tenant in which to add new user groups, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header.   To specify the project in which to create new user groups, provide a project UUID in the `ProjectID` request header or `projectId` for each user group in the request body.

        :param user_groups_change_dto: (required)
        :type user_groups_change_dto: UserGroupsChangeDTO
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._create_user_groups_serialize(
            user_groups_change_dto=user_groups_change_dto,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupChangeResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _create_user_groups_serialize(
        self,
        user_groups_change_dto,
        target_tenant_id,
        project_id,
        non_versioned,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        # process the header parameters
        if target_tenant_id is not None:
            _header_params['TargetTenantID'] = target_tenant_id
        if project_id is not None:
            _header_params['ProjectID'] = project_id
        if non_versioned is not None:
            _header_params['NonVersioned'] = non_versioned
        # process the form parameters
        # process the body parameter
        if user_groups_change_dto is not None:
            _body_params = user_groups_change_dto


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )

        # set the HTTP header `Content-Type`
        if _content_type:
            _header_params['Content-Type'] = _content_type
        else:
            _default_content_type = (
                self.api_client.select_header_content_type(
                    [
                        'application/json'
                    ]
                )
            )
            if _default_content_type is not None:
                _header_params['Content-Type'] = _default_content_type

        # authentication setting
        _auth_settings: List[str] = [
        ]

        return self.api_client.param_serialize(
            method='POST',
            resource_path='/v2/admin/user-groups',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )




    @validate_call
    def delete_user_group(
        self,
        user_group_id: Annotated[StrictStr, Field(description="The ID of user group to delete.")],
        delete_user_group_v2_request: DeleteUserGroupV2Request,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> UserGroupSingleDeleteResponseDTO:
        """Delete a user group

        Delete a specific user group. To specify the tenant in which to delete a user group, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header.   To specify the project in which to delete a user group, provide a project UUID in the `ProjectID` request header.

        :param user_group_id: The ID of user group to delete. (required)
        :type user_group_id: str
        :param delete_user_group_v2_request: (required)
        :type delete_user_group_v2_request: DeleteUserGroupV2Request
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._delete_user_group_serialize(
            user_group_id=user_group_id,
            delete_user_group_v2_request=delete_user_group_v2_request,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupSingleDeleteResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_administration.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def delete_user_group_with_http_info(
        self,
        user_group_id: Annotated[StrictStr, Field(description="The ID of user group to delete.")],
        delete_user_group_v2_request: DeleteUserGroupV2Request,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[UserGroupSingleDeleteResponseDTO]:
        """Delete a user group

        Delete a specific user group. To specify the tenant in which to delete a user group, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header.   To specify the project in which to delete a user group, provide a project UUID in the `ProjectID` request header.

        :param user_group_id: The ID of user group to delete. (required)
        :type user_group_id: str
        :param delete_user_group_v2_request: (required)
        :type delete_user_group_v2_request: DeleteUserGroupV2Request
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._delete_user_group_serialize(
            user_group_id=user_group_id,
            delete_user_group_v2_request=delete_user_group_v2_request,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupSingleDeleteResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_administration.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def delete_user_group_without_preload_content(
        self,
        user_group_id: Annotated[StrictStr, Field(description="The ID of user group to delete.")],
        delete_user_group_v2_request: DeleteUserGroupV2Request,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Delete a user group

        Delete a specific user group. To specify the tenant in which to delete a user group, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header.   To specify the project in which to delete a user group, provide a project UUID in the `ProjectID` request header.

        :param user_group_id: The ID of user group to delete. (required)
        :type user_group_id: str
        :param delete_user_group_v2_request: (required)
        :type delete_user_group_v2_request: DeleteUserGroupV2Request
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._delete_user_group_serialize(
            user_group_id=user_group_id,
            delete_user_group_v2_request=delete_user_group_v2_request,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupSingleDeleteResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _delete_user_group_serialize(
        self,
        user_group_id,
        delete_user_group_v2_request,
        target_tenant_id,
        project_id,
        non_versioned,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        if user_group_id is not None:
            _path_params['userGroupId'] = user_group_id
        # process the query parameters
        # process the header parameters
        if target_tenant_id is not None:
            _header_params['TargetTenantID'] = target_tenant_id
        if project_id is not None:
            _header_params['ProjectID'] = project_id
        if non_versioned is not None:
            _header_params['NonVersioned'] = non_versioned
        # process the form parameters
        # process the body parameter
        if delete_user_group_v2_request is not None:
            _body_params = delete_user_group_v2_request


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )

        # set the HTTP header `Content-Type`
        if _content_type:
            _header_params['Content-Type'] = _content_type
        else:
            _default_content_type = (
                self.api_client.select_header_content_type(
                    [
                        'application/json'
                    ]
                )
            )
            if _default_content_type is not None:
                _header_params['Content-Type'] = _default_content_type

        # authentication setting
        _auth_settings: List[str] = [
        ]

        return self.api_client.param_serialize(
            method='DELETE',
            resource_path='/v2/admin/user-groups/{userGroupId}',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )




    @validate_call
    def delete_user_groups(
        self,
        user_groups_delete_request_dto: UserGroupsDeleteRequestDTO,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> UserGroupDeleteResponseDTO:
        """Delete multiple user groups

        Delete user groups in bulk. To specify the tenant in which to delete user groups, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header.   To specify the project in which to delete user groups, provide a project UUID in the `ProjectID` request header or `projectId` for each user group in the request body.

        :param user_groups_delete_request_dto: (required)
        :type user_groups_delete_request_dto: UserGroupsDeleteRequestDTO
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._delete_user_groups_serialize(
            user_groups_delete_request_dto=user_groups_delete_request_dto,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupDeleteResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_administration.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def delete_user_groups_with_http_info(
        self,
        user_groups_delete_request_dto: UserGroupsDeleteRequestDTO,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[UserGroupDeleteResponseDTO]:
        """Delete multiple user groups

        Delete user groups in bulk. To specify the tenant in which to delete user groups, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header.   To specify the project in which to delete user groups, provide a project UUID in the `ProjectID` request header or `projectId` for each user group in the request body.

        :param user_groups_delete_request_dto: (required)
        :type user_groups_delete_request_dto: UserGroupsDeleteRequestDTO
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._delete_user_groups_serialize(
            user_groups_delete_request_dto=user_groups_delete_request_dto,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupDeleteResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_administration.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def delete_user_groups_without_preload_content(
        self,
        user_groups_delete_request_dto: UserGroupsDeleteRequestDTO,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Delete multiple user groups

        Delete user groups in bulk. To specify the tenant in which to delete user groups, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header.   To specify the project in which to delete user groups, provide a project UUID in the `ProjectID` request header or `projectId` for each user group in the request body.

        :param user_groups_delete_request_dto: (required)
        :type user_groups_delete_request_dto: UserGroupsDeleteRequestDTO
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._delete_user_groups_serialize(
            user_groups_delete_request_dto=user_groups_delete_request_dto,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupDeleteResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _delete_user_groups_serialize(
        self,
        user_groups_delete_request_dto,
        target_tenant_id,
        project_id,
        non_versioned,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        # process the header parameters
        if target_tenant_id is not None:
            _header_params['TargetTenantID'] = target_tenant_id
        if project_id is not None:
            _header_params['ProjectID'] = project_id
        if non_versioned is not None:
            _header_params['NonVersioned'] = non_versioned
        # process the form parameters
        # process the body parameter
        if user_groups_delete_request_dto is not None:
            _body_params = user_groups_delete_request_dto


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )

        # set the HTTP header `Content-Type`
        if _content_type:
            _header_params['Content-Type'] = _content_type
        else:
            _default_content_type = (
                self.api_client.select_header_content_type(
                    [
                        'application/json'
                    ]
                )
            )
            if _default_content_type is not None:
                _header_params['Content-Type'] = _default_content_type

        # authentication setting
        _auth_settings: List[str] = [
        ]

        return self.api_client.param_serialize(
            method='DELETE',
            resource_path='/v2/admin/user-groups',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )




    @validate_call
    def get_user_group(
        self,
        user_group_id: Annotated[StrictStr, Field(description="The ID of user group.")],
        var_with: Annotated[Optional[StrictStr], Field(description="Controls the amount of detail to return in the response. Omit to return detailed information.  * **permissions**: Include the user group's permissions.  * **users**: Include the users in the user group.  * **details**: Include all available information.")] = None,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> UserGroupChangeDefinitionDTO:
        """Retrieve the details of a user group

        Retrieve all available information about a specific user group.    <br>To specify the tenant in which to retrieve a user group, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header.   To specify the project in which to return a user group, provide a project UUID in the `ProjectID` request header.

        :param user_group_id: The ID of user group. (required)
        :type user_group_id: str
        :param var_with: Controls the amount of detail to return in the response. Omit to return detailed information.  * **permissions**: Include the user group's permissions.  * **users**: Include the users in the user group.  * **details**: Include all available information.
        :type var_with: str
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_user_group_serialize(
            user_group_id=user_group_id,
            var_with=var_with,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupChangeDefinitionDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_administration.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def get_user_group_with_http_info(
        self,
        user_group_id: Annotated[StrictStr, Field(description="The ID of user group.")],
        var_with: Annotated[Optional[StrictStr], Field(description="Controls the amount of detail to return in the response. Omit to return detailed information.  * **permissions**: Include the user group's permissions.  * **users**: Include the users in the user group.  * **details**: Include all available information.")] = None,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[UserGroupChangeDefinitionDTO]:
        """Retrieve the details of a user group

        Retrieve all available information about a specific user group.    <br>To specify the tenant in which to retrieve a user group, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header.   To specify the project in which to return a user group, provide a project UUID in the `ProjectID` request header.

        :param user_group_id: The ID of user group. (required)
        :type user_group_id: str
        :param var_with: Controls the amount of detail to return in the response. Omit to return detailed information.  * **permissions**: Include the user group's permissions.  * **users**: Include the users in the user group.  * **details**: Include all available information.
        :type var_with: str
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_user_group_serialize(
            user_group_id=user_group_id,
            var_with=var_with,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupChangeDefinitionDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_administration.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def get_user_group_without_preload_content(
        self,
        user_group_id: Annotated[StrictStr, Field(description="The ID of user group.")],
        var_with: Annotated[Optional[StrictStr], Field(description="Controls the amount of detail to return in the response. Omit to return detailed information.  * **permissions**: Include the user group's permissions.  * **users**: Include the users in the user group.  * **details**: Include all available information.")] = None,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Retrieve the details of a user group

        Retrieve all available information about a specific user group.    <br>To specify the tenant in which to retrieve a user group, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header.   To specify the project in which to return a user group, provide a project UUID in the `ProjectID` request header.

        :param user_group_id: The ID of user group. (required)
        :type user_group_id: str
        :param var_with: Controls the amount of detail to return in the response. Omit to return detailed information.  * **permissions**: Include the user group's permissions.  * **users**: Include the users in the user group.  * **details**: Include all available information.
        :type var_with: str
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_user_group_serialize(
            user_group_id=user_group_id,
            var_with=var_with,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupChangeDefinitionDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _get_user_group_serialize(
        self,
        user_group_id,
        var_with,
        target_tenant_id,
        project_id,
        non_versioned,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        if user_group_id is not None:
            _path_params['userGroupId'] = user_group_id
        # process the query parameters
        if var_with is not None:
            
            _query_params.append(('with', var_with))
            
        # process the header parameters
        if target_tenant_id is not None:
            _header_params['TargetTenantID'] = target_tenant_id
        if project_id is not None:
            _header_params['ProjectID'] = project_id
        if non_versioned is not None:
            _header_params['NonVersioned'] = non_versioned
        # process the form parameters
        # process the body parameter


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )


        # authentication setting
        _auth_settings: List[str] = [
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/v2/admin/user-groups/{userGroupId}',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )




    @validate_call
    def get_user_groups(
        self,
        var_with: Annotated[Optional[StrictStr], Field(description="Controls the amount of detail to return in the response. Omit to return basic information.  * **permissions**: Include the user group's permissions.  * **users**: Include the users in the user group.  * **details**: Include all available information.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The number of results to return. The maximum number of user groups to retrieve is 1000. The default is 100.")] = None,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> UserGroupsChangeDTO:
        """Retrieve a list of user groups

        Retrieve a collection of user groups. Use `with` to control the amount of detail returned in the response.  `with` supports these values:  * **permissions**: Include the user group's permissions.  * **users**: Include the users in the user group.  * **details**: Include all available information.   This API can return a maximum of 1000 user groups. The default number of user groups to return is 100.   To specify the project in which to return user groups, provide a project UUID in the `ProjectID` request header.   <br>To specify the tenant in which to retrieve user groups, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header.

        :param var_with: Controls the amount of detail to return in the response. Omit to return basic information.  * **permissions**: Include the user group's permissions.  * **users**: Include the users in the user group.  * **details**: Include all available information.
        :type var_with: str
        :param limit: The number of results to return. The maximum number of user groups to retrieve is 1000. The default is 100.
        :type limit: int
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_user_groups_serialize(
            var_with=var_with,
            limit=limit,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupsChangeDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_administration.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def get_user_groups_with_http_info(
        self,
        var_with: Annotated[Optional[StrictStr], Field(description="Controls the amount of detail to return in the response. Omit to return basic information.  * **permissions**: Include the user group's permissions.  * **users**: Include the users in the user group.  * **details**: Include all available information.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The number of results to return. The maximum number of user groups to retrieve is 1000. The default is 100.")] = None,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[UserGroupsChangeDTO]:
        """Retrieve a list of user groups

        Retrieve a collection of user groups. Use `with` to control the amount of detail returned in the response.  `with` supports these values:  * **permissions**: Include the user group's permissions.  * **users**: Include the users in the user group.  * **details**: Include all available information.   This API can return a maximum of 1000 user groups. The default number of user groups to return is 100.   To specify the project in which to return user groups, provide a project UUID in the `ProjectID` request header.   <br>To specify the tenant in which to retrieve user groups, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header.

        :param var_with: Controls the amount of detail to return in the response. Omit to return basic information.  * **permissions**: Include the user group's permissions.  * **users**: Include the users in the user group.  * **details**: Include all available information.
        :type var_with: str
        :param limit: The number of results to return. The maximum number of user groups to retrieve is 1000. The default is 100.
        :type limit: int
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_user_groups_serialize(
            var_with=var_with,
            limit=limit,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupsChangeDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_administration.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def get_user_groups_without_preload_content(
        self,
        var_with: Annotated[Optional[StrictStr], Field(description="Controls the amount of detail to return in the response. Omit to return basic information.  * **permissions**: Include the user group's permissions.  * **users**: Include the users in the user group.  * **details**: Include all available information.")] = None,
        limit: Annotated[Optional[StrictInt], Field(description="The number of results to return. The maximum number of user groups to retrieve is 1000. The default is 100.")] = None,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Retrieve a list of user groups

        Retrieve a collection of user groups. Use `with` to control the amount of detail returned in the response.  `with` supports these values:  * **permissions**: Include the user group's permissions.  * **users**: Include the users in the user group.  * **details**: Include all available information.   This API can return a maximum of 1000 user groups. The default number of user groups to return is 100.   To specify the project in which to return user groups, provide a project UUID in the `ProjectID` request header.   <br>To specify the tenant in which to retrieve user groups, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header.

        :param var_with: Controls the amount of detail to return in the response. Omit to return basic information.  * **permissions**: Include the user group's permissions.  * **users**: Include the users in the user group.  * **details**: Include all available information.
        :type var_with: str
        :param limit: The number of results to return. The maximum number of user groups to retrieve is 1000. The default is 100.
        :type limit: int
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_user_groups_serialize(
            var_with=var_with,
            limit=limit,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupsChangeDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _get_user_groups_serialize(
        self,
        var_with,
        limit,
        target_tenant_id,
        project_id,
        non_versioned,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        if var_with is not None:
            
            _query_params.append(('with', var_with))
            
        if limit is not None:
            
            _query_params.append(('limit', limit))
            
        # process the header parameters
        if target_tenant_id is not None:
            _header_params['TargetTenantID'] = target_tenant_id
        if project_id is not None:
            _header_params['ProjectID'] = project_id
        if non_versioned is not None:
            _header_params['NonVersioned'] = non_versioned
        # process the form parameters
        # process the body parameter


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )


        # authentication setting
        _auth_settings: List[str] = [
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/v2/admin/user-groups',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )




    @validate_call
    def patch_user_groups(
        self,
        user_groups_change_dto: UserGroupsChangeDTO,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> UserGroupChangeResponseDTO:
        """Patch multiple user groups

        Make partial changes to user groups. To specify the tenant in which to patch a user group, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header or `tenantCode` for each user group in the request body.   Unlike `PUT`, which completely replaces the user group definition, use `PATCH` to change specific fields in the user group without affecting omitted fields.   To specify the project in which to patch user groups, provide a project UUID in the `ProjectID` request header or `projectId` for each user group in the request body.

        :param user_groups_change_dto: (required)
        :type user_groups_change_dto: UserGroupsChangeDTO
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._patch_user_groups_serialize(
            user_groups_change_dto=user_groups_change_dto,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupChangeResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_administration.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def patch_user_groups_with_http_info(
        self,
        user_groups_change_dto: UserGroupsChangeDTO,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[UserGroupChangeResponseDTO]:
        """Patch multiple user groups

        Make partial changes to user groups. To specify the tenant in which to patch a user group, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header or `tenantCode` for each user group in the request body.   Unlike `PUT`, which completely replaces the user group definition, use `PATCH` to change specific fields in the user group without affecting omitted fields.   To specify the project in which to patch user groups, provide a project UUID in the `ProjectID` request header or `projectId` for each user group in the request body.

        :param user_groups_change_dto: (required)
        :type user_groups_change_dto: UserGroupsChangeDTO
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._patch_user_groups_serialize(
            user_groups_change_dto=user_groups_change_dto,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupChangeResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_administration.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def patch_user_groups_without_preload_content(
        self,
        user_groups_change_dto: UserGroupsChangeDTO,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Patch multiple user groups

        Make partial changes to user groups. To specify the tenant in which to patch a user group, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header or `tenantCode` for each user group in the request body.   Unlike `PUT`, which completely replaces the user group definition, use `PATCH` to change specific fields in the user group without affecting omitted fields.   To specify the project in which to patch user groups, provide a project UUID in the `ProjectID` request header or `projectId` for each user group in the request body.

        :param user_groups_change_dto: (required)
        :type user_groups_change_dto: UserGroupsChangeDTO
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._patch_user_groups_serialize(
            user_groups_change_dto=user_groups_change_dto,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupChangeResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _patch_user_groups_serialize(
        self,
        user_groups_change_dto,
        target_tenant_id,
        project_id,
        non_versioned,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        # process the header parameters
        if target_tenant_id is not None:
            _header_params['TargetTenantID'] = target_tenant_id
        if project_id is not None:
            _header_params['ProjectID'] = project_id
        if non_versioned is not None:
            _header_params['NonVersioned'] = non_versioned
        # process the form parameters
        # process the body parameter
        if user_groups_change_dto is not None:
            _body_params = user_groups_change_dto


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )

        # set the HTTP header `Content-Type`
        if _content_type:
            _header_params['Content-Type'] = _content_type
        else:
            _default_content_type = (
                self.api_client.select_header_content_type(
                    [
                        'application/json'
                    ]
                )
            )
            if _default_content_type is not None:
                _header_params['Content-Type'] = _default_content_type

        # authentication setting
        _auth_settings: List[str] = [
        ]

        return self.api_client.param_serialize(
            method='PATCH',
            resource_path='/v2/admin/user-groups',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )




    @validate_call
    def put_user_groups(
        self,
        user_groups_change_dto: UserGroupsChangeDTO,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> UserGroupChangeResponseDTO:
        """Update multiple user groups

        Update existing user groups. To specify the tenant in which to update a user group, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header or `tenantCode` for each user group in the request body.   When updating user groups, the user group definition in your API call replaces the prior definition. You must provide the entire definition in the `PUT` call. If you omit values from the update request, those values are removed from the user group. We recommend that you retrieve a user group's details before you update the user group with new values.    To specify the project in which to update user groups, provide a project UUID in the `ProjectID` request header or `projectId` for each user group in the request body.

        :param user_groups_change_dto: (required)
        :type user_groups_change_dto: UserGroupsChangeDTO
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._put_user_groups_serialize(
            user_groups_change_dto=user_groups_change_dto,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupChangeResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_administration.models,
            response_data=response_data,
            response_types_map=_response_types_map
        ).data


    @validate_call
    def put_user_groups_with_http_info(
        self,
        user_groups_change_dto: UserGroupsChangeDTO,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[UserGroupChangeResponseDTO]:
        """Update multiple user groups

        Update existing user groups. To specify the tenant in which to update a user group, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header or `tenantCode` for each user group in the request body.   When updating user groups, the user group definition in your API call replaces the prior definition. You must provide the entire definition in the `PUT` call. If you omit values from the update request, those values are removed from the user group. We recommend that you retrieve a user group's details before you update the user group with new values.    To specify the project in which to update user groups, provide a project UUID in the `ProjectID` request header or `projectId` for each user group in the request body.

        :param user_groups_change_dto: (required)
        :type user_groups_change_dto: UserGroupsChangeDTO
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._put_user_groups_serialize(
            user_groups_change_dto=user_groups_change_dto,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupChangeResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            model_package=visier_api_administration.models,
            response_data=response_data,
            response_types_map=_response_types_map
        )


    @validate_call
    def put_user_groups_without_preload_content(
        self,
        user_groups_change_dto: UserGroupsChangeDTO,
        target_tenant_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.")] = None,
        project_id: Annotated[Optional[StrictStr], Field(description="Optionally, specify a project in which to make the request.")] = None,
        non_versioned: Annotated[Optional[StrictBool], Field(description="If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Update multiple user groups

        Update existing user groups. To specify the tenant in which to update a user group, administrating tenants can provide an analytic tenant code in the `TargetTenantID` request header or `tenantCode` for each user group in the request body.   When updating user groups, the user group definition in your API call replaces the prior definition. You must provide the entire definition in the `PUT` call. If you omit values from the update request, those values are removed from the user group. We recommend that you retrieve a user group's details before you update the user group with new values.    To specify the project in which to update user groups, provide a project UUID in the `ProjectID` request header or `projectId` for each user group in the request body.

        :param user_groups_change_dto: (required)
        :type user_groups_change_dto: UserGroupsChangeDTO
        :param target_tenant_id: Optionally, specify the tenant that you want to execute the API call on. This defines the tenant that you're logged into. If omitted, the request uses the administrating tenant as the login tenant.
        :type target_tenant_id: str
        :param project_id: Optionally, specify a project in which to make the request.
        :type project_id: str
        :param non_versioned: If `true`, the API call executes on non-versioned artifacts and create/update actions take effect without a new production version. If `false`, the API call executes on versioned artifacts and create/update actions release a new production version. Default is `false`.<br>**Note:** <em>This header is in **limited availability**. If you are interested in using it, please contact your Customer Success Manager (CSM).</em>
        :type non_versioned: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._put_user_groups_serialize(
            user_groups_change_dto=user_groups_change_dto,
            target_tenant_id=target_tenant_id,
            project_id=project_id,
            non_versioned=non_versioned,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "UserGroupChangeResponseDTO",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _put_user_groups_serialize(
        self,
        user_groups_change_dto,
        target_tenant_id,
        project_id,
        non_versioned,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        # process the header parameters
        if target_tenant_id is not None:
            _header_params['TargetTenantID'] = target_tenant_id
        if project_id is not None:
            _header_params['ProjectID'] = project_id
        if non_versioned is not None:
            _header_params['NonVersioned'] = non_versioned
        # process the form parameters
        # process the body parameter
        if user_groups_change_dto is not None:
            _body_params = user_groups_change_dto


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )

        # set the HTTP header `Content-Type`
        if _content_type:
            _header_params['Content-Type'] = _content_type
        else:
            _default_content_type = (
                self.api_client.select_header_content_type(
                    [
                        'application/json'
                    ]
                )
            )
            if _default_content_type is not None:
                _header_params['Content-Type'] = _default_content_type

        # authentication setting
        _auth_settings: List[str] = [
        ]

        return self.api_client.param_serialize(
            method='PUT',
            resource_path='/v2/admin/user-groups',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )


