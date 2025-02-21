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


import unittest

import visier_api_administration.models
from visier_api_administration.models.permissions_to_user_group_for_tenant_dto import PermissionsToUserGroupForTenantDTO

class TestPermissionsToUserGroupForTenantDTO(unittest.TestCase):
    """PermissionsToUserGroupForTenantDTO unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PermissionsToUserGroupForTenantDTO:
        """Test PermissionsToUserGroupForTenantDTO
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """

        if include_optional:
            return PermissionsToUserGroupForTenantDTO(
                message = '',
                status = '',
                tenant_code = '',
                user_groups = [
                    visier_api_administration.models.user_group_get_api_response_dto.UserGroupGetAPIResponseDTO(
                        display_name = '', 
                        permissions = [
                            visier_api_administration.models.permission_response_dto.PermissionResponseDTO(
                                display_name = '', 
                                permission_id = '', )
                            ], 
                        user_group_id = '', )
                    ]
            )
        else:
            return PermissionsToUserGroupForTenantDTO(
        )

    def testPermissionsToUserGroupForTenantDTO(self):
        """Test PermissionsToUserGroupForTenantDTO"""
        def validate_instance(instance):
            PermissionsToUserGroupForTenantDTO.model_validate(inst_req_only)
            instance_deserialized = PermissionsToUserGroupForTenantDTO.from_dict(instance.to_dict())
            assert instance == instance_deserialized

        inst_req_only = self.make_instance(include_optional=False)
        validate_instance(inst_req_only)

        inst_req_and_optional = self.make_instance(include_optional=True)
        validate_instance(inst_req_and_optional)

if __name__ == '__main__':
    unittest.main()
