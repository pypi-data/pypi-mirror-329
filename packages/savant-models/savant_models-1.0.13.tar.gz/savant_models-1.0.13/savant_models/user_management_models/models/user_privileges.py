from typing import Optional
from pydantic import BaseModel, field_validator

from savant_models.user_management_models.enums.tab_permission_enum import TabPermissionEnum
from savant_models.user_management_models.models.tab_permissions import TabPermissions


class UserPrivileges(BaseModel):
    batches: Optional[TabPermissions] = TabPermissions()
    projects: Optional[TabPermissions] = TabPermissions()
    admin: Optional[TabPermissions] = TabPermissions()
    file_uploads: Optional[TabPermissions] = TabPermissions()
    labels: Optional[TabPermissions] = TabPermissions()
    profiles: Optional[TabPermissions] = TabPermissions()
    videos: Optional[TabPermissions] = TabPermissions()

    @field_validator('projects')
    def check_special_chars(cls, v: Optional[TabPermissions]):
        if v and v.permission not in {TabPermissionEnum.NOTHING, TabPermissionEnum.TEAMS, TabPermissionEnum.EVERYTHING}:
            raise ValueError('Invalid value for projects. Allowed values are: nothing, teams, everything.')
        return v
