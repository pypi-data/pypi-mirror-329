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


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class ProjectDTO(BaseModel):
    """
    ProjectDTO
    """ # noqa: E501
    capabilities: Optional[List[StrictStr]] = Field(default=None, description="The current user's capabilities for the project. Users with `canWrite`, `canShare`, or `owner` capabilities can add and commit changes to the project.  **canRead**: The project has been shared to the user with `View` access.  **canWrite**: The project has been shared to the user with `Edit` access.  **canShare**: The project has been shared to the user with `Share` access.  **owner**: The user is the owner of the project.  Omit when creating a new project.")
    description: Optional[StrictStr] = Field(default=None, description="A description of the project.")
    id: Optional[StrictStr] = Field(default=None, description="The unique ID of the project. Omit when creating a new project.")
    name: Optional[StrictStr] = Field(default=None, description="An identifiable project name to display in Visier.")
    release_version: Optional[StrictStr] = Field(default=None, description="The release version of the project.", alias="releaseVersion")
    ticket_number: Optional[StrictStr] = Field(default=None, description="The change management ticket number of the project.", alias="ticketNumber")
    version_number: Optional[StrictInt] = Field(default=None, description="The version number of the project.", alias="versionNumber")
    __properties: ClassVar[List[str]] = ["capabilities", "description", "id", "name", "releaseVersion", "ticketNumber", "versionNumber"]

    @field_validator('capabilities')
    def capabilities_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        for i in value:
            if i not in set(['canRead', 'canWrite', 'canShare', 'owner']):
                raise ValueError("each list item must be one of ('canRead', 'canWrite', 'canShare', 'owner')")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of ProjectDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ProjectDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "capabilities": obj.get("capabilities"),
            "description": obj.get("description"),
            "id": obj.get("id"),
            "name": obj.get("name"),
            "releaseVersion": obj.get("releaseVersion"),
            "ticketNumber": obj.get("ticketNumber"),
            "versionNumber": obj.get("versionNumber")
        })
        return _obj


