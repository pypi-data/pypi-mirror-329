from pydantic import BaseModel

from savant_models.user_management_models.enums.tab_permission_enum import TabPermissionEnum


class TabPermissions(BaseModel):
    permission: TabPermissionEnum = TabPermissionEnum.NOTHING
