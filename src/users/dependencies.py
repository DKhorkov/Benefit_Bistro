from fastapi import Depends
from typing import List

from src.users.exceptions import InvalidPasswordError, UserAlreadyExistsError
from src.users.models import UserModel
from src.security.models import JWTDataModel
from src.users.schemas import LoginUserScheme, RegisterUserScheme
from src.users.utils import oauth2_scheme, verify_password
from src.users.service import UsersService
from src.users.units_of_work import SQLAlchemyUsersUnitOfWork
from src.security.utils import parse_jwt_token


async def register_user(user_data: RegisterUserScheme) -> UserModel:
    """
    Registers a new user, if user with provided credentials doesn't exist.
    """

    users_service: UsersService = UsersService(uow=SQLAlchemyUsersUnitOfWork())
    if await users_service.check_user_existence(email=user_data.email, username=user_data.username):
        raise UserAlreadyExistsError

    user: UserModel = await users_service.register_user(user_data=user_data)
    await user.protect_password()
    return user


async def login_user(user_data: LoginUserScheme) -> UserModel:
    """
    Logs in a user with provided credentials, if credentials are valid.
    """

    users_service: UsersService = UsersService(uow=SQLAlchemyUsersUnitOfWork())

    user: UserModel
    if await users_service.check_user_existence(email=user_data.username):
        user = await users_service.get_user_by_email(email=user_data.username)
    else:
        user = await users_service.get_user_by_username(username=user_data.username)

    if not await verify_password(user_data.password, user.password):
        raise InvalidPasswordError

    await user.protect_password()
    return user


async def authenticate_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    """
    Authenticates user according to provided JWT token, if token is valid and hadn't expired.
    """

    jwt_data: JWTDataModel = await parse_jwt_token(token=token)
    users_service: UsersService = UsersService(uow=SQLAlchemyUsersUnitOfWork())
    user: UserModel = await users_service.authenticate_user(jwt_data=jwt_data)
    await user.protect_password()
    return user


async def verify_user_email(token: str) -> UserModel:
    """
    Confirms, that the provided by user email belongs to him according provided JWT token.
    """

    jwt_data: JWTDataModel = await parse_jwt_token(token=token)
    users_service: UsersService = UsersService(uow=SQLAlchemyUsersUnitOfWork())
    user: UserModel = await users_service.verify_user_email(jwt_data=jwt_data)
    await user.protect_password()
    return user


async def get_all_users() -> List[UserModel]:
    users_service: UsersService = UsersService(uow=SQLAlchemyUsersUnitOfWork())
    users: List[UserModel] = await users_service.get_all_users()
    for user in users:
        await user.protect_password()

    return users