from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, status
from fastapi.responses import Response, RedirectResponse, JSONResponse

from src.auth.models import UserModel
from src.auth.config import RouterConfig, URLPathsConfig, URLNamesConfig, cookies_config
from src.celery.tasks.auth_tasks import send_verify_email_message
from src.security.models import JWTDataModel
from src.security.utils import create_jwt_token
from src.auth.dependencies import (
    login_user,
    register_user,
    authenticate_user,
    verify_user_email
)


router = APIRouter(
    prefix=RouterConfig.PREFIX,
    tags=RouterConfig.tags_list(),
)


@router.post(
    path=URLPathsConfig.REGISTER,
    response_class=JSONResponse,
    name=URLNamesConfig.REGISTER,
    status_code=status.HTTP_201_CREATED,
    response_model=UserModel
)
async def register(user: UserModel = Depends(register_user)):
    send_verify_email_message.delay(user_data=await user.to_dict())
    return user


@router.get(
    path=URLPathsConfig.VERIFY_EMAIL,
    response_class=Response,
    name=URLNamesConfig.VERIFY_EMAIL,
    status_code=status.HTTP_204_NO_CONTENT
)
async def verify_email(user: UserModel = Depends(verify_user_email)):   # Using this style for correct Dependency work
    pass


@router.post(
    path=URLPathsConfig.LOGIN,
    response_class=Response,
    name=URLNamesConfig.LOGIN,
    status_code=status.HTTP_204_NO_CONTENT
)
async def login(user: UserModel = Depends(login_user)):
    jwt_data: JWTDataModel = JWTDataModel(user_id=user.id)
    token: str = await create_jwt_token(jwt_data=jwt_data)
    response: Response = Response()
    response.set_cookie(
        key=cookies_config.COOKIES_KEY,
        value=token,
        secure=cookies_config.SECURE_COOKIES,
        httponly=cookies_config.HTTP_ONLY,
        expires=datetime.now(tz=timezone.utc) + timedelta(days=cookies_config.COOKIES_LIFESPAN_DAYS),
        samesite=cookies_config.SAME_SITE
    )
    return response


@router.get(
    path=URLPathsConfig.LOGOUT,
    response_class=Response,
    name=URLNamesConfig.LOGOUT,
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout():
    response: Response = Response()
    response.delete_cookie(
        key=cookies_config.COOKIES_KEY,
        secure=cookies_config.SECURE_COOKIES,
        httponly=cookies_config.HTTP_ONLY,
        samesite=cookies_config.SAME_SITE
    )
    return response


@router.get(
    path=URLPathsConfig.ME,
    response_class=JSONResponse,
    response_model=UserModel,
    name=URLNamesConfig.ME,
    status_code=status.HTTP_200_OK
)
async def get_my_account(user: UserModel = Depends(authenticate_user)):
    return user
