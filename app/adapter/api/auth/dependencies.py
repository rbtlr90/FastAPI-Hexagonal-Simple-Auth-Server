from app.application.port.tokens.inbound import AbstractTokenUsecase
from app.application.usecase.tokens.service import TokenUsecaseImpl


def auth_use_case() -> AbstractTokenUsecase:
    return TokenUsecaseImpl()