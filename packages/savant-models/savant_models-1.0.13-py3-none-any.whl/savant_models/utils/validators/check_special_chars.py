import logging
from fastapi import HTTPException

from savant_models.utils.response_bodies.response_message import ResponseMessage

logger = logging.getLogger("registry")


def check_special_chars(field: str) -> str:
    """
    Function will check for any special characters that could
    be used in mongo query and raise error if field contains
    any protected special character
    """
    special_char_list = ["$", "{", "}"]
    for char in special_char_list:
        if field and char in field:
            logger.info(f"Field contains '{char}' which is a protected character.")
            raise HTTPException(
                status_code=400,
                detail=ResponseMessage(
                    success=False,
                    message=f"Field contains '{char}' which is a protected character.",
                ).model_dump(),
            )

    return field
