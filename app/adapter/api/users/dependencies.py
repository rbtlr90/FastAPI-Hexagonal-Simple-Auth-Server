from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.loader import get_session
from app.adapter.persistence.users.repository import UserRepositoryImpl
from app.application.port.users.inbound import AbstractUserUsecase
from app.application.port.users.outbound import AbstractUserRepository
from app.application.usecase.users.unit_of_work import UserUnitOfWork, UserUnitOfWorkImpl
from app.application.usecase.users.service import UserUsecaseImpl

def user_use_case(db_session: AsyncSession = Depends(get_session)) -> AbstractUserUsecase:
    "Get usecase implementation class"
    user_repository: AbstractUserRepository = UserRepositoryImpl(db_session)
    uow: UserUnitOfWork = UserUnitOfWorkImpl(
        session=db_session,
        repository=user_repository,
    )
    return UserUsecaseImpl(uow)
