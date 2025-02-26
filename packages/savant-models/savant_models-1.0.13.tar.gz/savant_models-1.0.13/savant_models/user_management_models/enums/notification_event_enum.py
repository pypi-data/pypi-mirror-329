from enum import StrEnum


class NotificationEventEnum(StrEnum):
    SEQUENCE_ASSIGNED_TO_USER = "sequence_assigned_to_user"
    TEAM_ASSIGNED_TO_MANAGED_BATCH = "team_assigned_to_batch"
    BATCH_COMPLETED = "batch_completed"
    COMMENT_ADDED = "comment_added"
