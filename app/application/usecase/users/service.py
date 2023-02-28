from typing import Optional, List

from app.adapter.api.users.requests import UserCreateRequest
from app.application.port.users.inbound import AbstractUserUsecase
from app.application.usecase.users.unit_of_work import UserUnitOfWork
from app.adapter.persistence.users.schema import UserSchema
from app.domain.users.entity import User
from app.logger import logger


class UserUsecaseImpl(AbstractUserUsecase):
    def __init__(self, uow: UserUnitOfWork):
        self.uow = uow

    async def create_one_user(self, user_info: UserCreateRequest) -> Optional[User]:
        await self.uow.begin()
        
        hashed_password = User.get_hashed_password(user_info.password)
        user_info.password = hashed_password
        created_user = await self.uow.user_repository.\
                                    create_one_user(user_info)
        await self.uow.commit()
        return created_user
    
    async def get_users_with_paging(self, offset: int, limit: int, order: str)\
                                                                        -> List[Optional[User]]:
        await self.uow.begin()

        users = await self.uow.user_repository.get_user_list_paging(offset, limit, order)
        logger.info(f'user list in service:\n{users}')
        return users
    
    async def get_one_user_by_user_id(self, user_id: str) -> Optional[User]:
        user = await self.uow.user_repository.\
                                            get_one_user_by_user_id(user_id=user_id)
        return user
