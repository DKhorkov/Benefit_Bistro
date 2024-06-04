from typing import List
from pydantic import BaseModel, field_validator

from src.groups.config import GroupValidationConfig
from src.groups.exceptions import GroupNameValidationError


class CreateGroupScheme(BaseModel):
    name: str

    @field_validator('name', mode='before')
    @classmethod
    def validate_group_name(cls, value: str) -> str:
        if not GroupValidationConfig.NAME_MIN_LENGTH <= len(value) <= GroupValidationConfig.NAME_MAX_LENGTH:
            raise GroupNameValidationError

        return value


class UpdateGroupMembersScheme(BaseModel):
    group_member_ids: List[int] = []
