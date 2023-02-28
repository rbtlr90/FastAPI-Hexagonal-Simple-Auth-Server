from typing import Protocol, runtime_checkable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, TimeoutError as DBTimeoutError

from app.application.port.users.outbound import AbstractUserRepository



@runtime_checkable
class UserUnitOfWork(Protocol):
    session: AsyncSession
    user_repository: AbstractUserRepository

    async def begin(self):
        raise NotImplementedError

    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError


class UserUnitOfWorkImpl(UserUnitOfWork):
    def __init__(self, session: AsyncSession, repository: AbstractUserRepository) -> None: # pylint: disable=W0231
        self.session = session
        self.user_repository = repository

    async def begin(self):
        await self.session.begin()

    async def commit(self):
        try:
            await self.session.commit()
            for obj in self.session:
                await self.session.refresh(obj)
            await self.session.flush()
        except IntegrityError as ie:
            await self.session.rollback()
            raise ie    # pylint: disable=W
        except DBTimeoutError as dte:
            await self.session.rollback()
            raise dte
        except SQLAlchemyError as sae:
            await self.session.rollback()
            raise sae

    async def rollback(self):
        await self.session.rollback()
