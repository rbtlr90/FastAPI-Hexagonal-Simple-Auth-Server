import traceback

from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.logger import logger
from app.adapter.api.auth.requests import LoginInfo
from app.adapter.api.auth.responses import AccessToken, Token
from app.adapter.api.users.dependencies import user_use_case
from app.adapter.api.auth.dependencies import auth_use_case
from app.domain.users.exceptions import bad_request_exception, not_found_exception
from app.domain.tokens.exceptions import credential_exception

router = APIRouter(
    prefix="/api/v1/auth",
    responses={
        400: {"detail": "Bad Request"},
        500: {"detail": "Internal Server Error"},
    }
)

@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
)
async def login(login_info: LoginInfo,
                user_usecase = Depends(user_use_case),
                token_usecase = Depends(auth_use_case)):
    try:
        user = await user_usecase.get_one_user_by_user_id(login_info.user_id)
        if not user:
            return not_found_exception

        if not user.verify_password(login_info.password, user.password):
            return bad_request_exception

        access_token, refresh_token = token_usecase.login(user)
        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )

    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc(limit=None))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e

@router.get(
    "/refresh",
    response_model=AccessToken,
    status_code=status.HTTP_201_CREATED,
)
async def refresh_access_token(user_usecase = Depends(user_use_case),
                                token_usecase = Depends(auth_use_case),
                                authorization: str = Header(...)):
    token = authorization.split(" ")[-1]
    if not token_usecase.validate_token(token):
        raise credential_exception

    if token_usecase.get_token_type_from_token(token) != "refresh":
        raise bad_request_exception

    user_id = token_usecase.get_id_from_token(token)
    user = await user_usecase.get_one_user_by_user_id(user_id)
    if user is None:
        raise bad_request_exception

    return AccessToken(
        access_token=token_usecase.create_token(user, "access")
    )
