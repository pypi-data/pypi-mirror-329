from pydantic import BaseModel

from savant_models.process_updates_models.enums.privilege_enum import PrivilegeEnum
from savant_models.user_management_models.enums.tab_permission_enum import TabPermissionEnum


class Privilege(BaseModel):
    privilege_type: PrivilegeEnum
    permission: TabPermissionEnum
