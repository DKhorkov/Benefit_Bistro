from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response

from src.groups.models import GroupModel
from src.groups.config import RouterConfig, URLPathsConfig, URLNamesConfig
from src.groups.dependencies import (
    create_group,
    delete_group,
    get_current_user_groups
)


router = APIRouter(
    prefix=RouterConfig.PREFIX,
    tags=RouterConfig.tags_list(),
)


@router.post(
    path=URLPathsConfig.CREATE_GROUP,
    response_class=JSONResponse,
    name=URLNamesConfig.CREATE_GROUP,
    response_model=GroupModel,
    status_code=status.HTTP_201_CREATED
)
async def create(group: GroupModel = Depends(create_group)):
    return group


@router.delete(
    path=URLPathsConfig.DELETE_GROUP,
    response_class=Response,
    name=URLNamesConfig.DELETE_GROUP,
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(deleted: None = Depends(delete_group)):  # Using this style for correct Dependency work
    pass


@router.get(
    path=URLPathsConfig.MY_GROUPS,
    response_class=JSONResponse,
    name=URLNamesConfig.MY_GROUPS,
    response_model=List[GroupModel],
    status_code=status.HTTP_200_OK
)
async def get_my_groups(groups: List[GroupModel] = Depends(get_current_user_groups)):
    return groups