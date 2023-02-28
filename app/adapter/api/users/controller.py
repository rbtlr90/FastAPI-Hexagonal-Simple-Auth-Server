import traceback

from fastapi import Depends, Header, HTTPException, status, APIRouter
from sqlalchemy.exc import IntegrityError

from app.loader import get_session
from app.logger import logger
from app.adapter.api.users.requests import UserCreateRequest, UserListQuery
from app.adapter.api.users.responses import UserCreateResponse, UserListResponse
from app.adapter.api.users.dependencies import user_use_case
from app.adapter.api.auth.dependencies import auth_use_case
from app.domain.users.exceptions import (bad_request_exception, unauthorized_exception,
                                        forbidden_exception, not_found_exception,
                                        conflict_exception)

router = APIRouter(
    prefix="/api/v1/user",
    responses={
        400: {"detail": "Bad Request"},
        404: {"detail": "Not Found"},
        500: {"detail": "Internal Server Error"},
    }
)

@router.post("",
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreateResponse,
    responses={
        403: {"detail": "Forbidden"}
    }
)
async def create_one_user(user_create_info: UserCreateRequest,
                        user_usecase = Depends(user_use_case)):
    if user_create_info.role is None:
        user_create_info.role = 'user'
    try:
        created_user_entity = await user_usecase.create_one_user(user_create_info)
        return UserCreateResponse(
            user_id=created_user_entity.user_id,
            email_address=created_user_entity.email_address,
            role=created_user_entity.role
        )
    except IntegrityError as ie:
        raise conflict_exception from ie
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc(limit=None))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e

@router.get(
    "/users",
    response_model=UserListResponse,
    responses={
        401: {"detail": "Unauthorized"},
        403: {"detail": "Forbidden"}
    }
)
async def get_user_list_paging(user_list_query: UserListQuery = Depends(),
                        user_usecase = Depends(user_use_case),
                        token_usecase = Depends(auth_use_case),
                        authorization: str = Header(...)):
    token = authorization.split(" ")[-1]
    if not token_usecase.validate_token(token):
        raise unauthorized_exception

    try:
        user_list = await user_usecase.get_users_with_paging(user_list_query.offset,
                                                            user_list_query.limit,
                                                            user_list_query.order)
        return UserListResponse(
            users=[
                UserCreateResponse(
                    user_id=user.user_id,
                    email_address=user.email_address,
                    role=user.role
                ) 
                for user in user_list
            ]
        ) 
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc(limit=None))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e