from datetime import datetime, timedelta
from typing import Optional, List

from pydantic import model_validator, ConfigDict, EmailStr, Field

from savant_models.teams_management_models.models.user_team import UserTeam
from savant_models.user_management_models.enums.notification_event_enum import NotificationEventEnum
from savant_models.user_management_models.enums.user_status_enum import UserStatusEnum
from savant_models.user_management_models.models.user_privileges import UserPrivileges
from savant_models.utils.base import BaseModel, PyObjectId
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus



class User(BaseModel):
    """Whole user information in the database."""
    id: PyObjectId = Field(alias="_id")
    email: EmailStr
    name: str
    hashed_password: str
    is_active: bool
    is_internal_manager: bool
    is_external_manager: bool
    is_internal_annotator: bool
    is_external_annotator: bool
    is_ml_engineer: bool
    is_researcher: Optional[bool] = False
    is_superuser: bool
    organisation_id: PyObjectId
    teams: Optional[List[UserTeam]] = []
    invite_sent: Optional[bool] = True
    date_sent: Optional[datetime] = None
    date_created: Optional[datetime] = None
    status: Optional[UserStatusEnum] = UserStatusEnum.ACTIVE
    verified_email: Optional[bool] = True
    privileges: Optional[UserPrivileges] = UserPrivileges()
    last_logged_in: Optional[datetime] = None
    notifications: Optional[List[NotificationEventEnum]] = []
    password_last_set: Optional[datetime] = None
    old_passwords: Optional[List[str]] = []
    rate_limit: bool = True

    @model_validator(mode='before')
    @classmethod
    def set_status(cls, values):
        invite_sent = values.get("invite_sent")
        date_sent = values.get("date_sent")
        verified_email = values.get("verified_email")
        is_active = values.get("is_active")
        if date_sent:
            time_delta = datetime.now() - date_sent
            if verified_email and is_active:
                values["status"] = UserStatusEnum.ACTIVE
            elif not is_active:
                values["status"] = UserStatusEnum.INACTIVE
            elif invite_sent and time_delta > timedelta(days=2):
                values["status"] = UserStatusEnum.EXPIRED
            elif invite_sent and time_delta < timedelta(days=2):
                values["status"] = UserStatusEnum.PENDING

        return values

    def get_dict(self):
        return dict(
            id=str(self.id),
            email=self.email,
            name=self.name,
            hashed_password=self.hashed_password,
            is_active=self.is_active,
            is_internal_manager=self.is_internal_manager,
            is_external_manager=self.is_external_manager,
            is_internal_annotator=self.is_internal_annotator,
            is_external_annotator=self.is_external_annotator,
            is_ml_engineer=self.is_ml_engineer,
            is_superuser=self.is_superuser,
            organisation_id=str(self.organisation_id),
            teams=self.convert_teams(),
            status=self.status,
            verified_email=self.verified_email,
            privileges=self.privileges.model_dump(),
            password_last_set=self.password_last_set.isoformat() if self.password_last_set else None,
            rate_limit=self.rate_limit
        )

    def convert_teams(self) -> dict:
        new_teams = []
        if self.teams:
            for team in self.teams:
                team = {"id": str(team.id), "name": team.name}
                new_teams.append(team)
            # self.teams = new_teams
        return new_teams

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})

