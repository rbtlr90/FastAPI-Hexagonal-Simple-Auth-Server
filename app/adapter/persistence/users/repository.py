from typing import List, Optional
import traceback
import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import func
from sqlalchemy import insert, update
from sqlalchemy.orm.exc import NoResultFound

from app.adapter.api.users.requests import UserCreateRequest
from app.adapter.persistence.users.schema import UserSchema
from app.application.port.users.outbound import AbstractUserRepository
from app.domain.users.entity import User
from app.logger import logger


class UserRepositoryImpl(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def create_one_user(self, user_info: UserCreateRequest) -> Optional[User]:
        try:
            now = datetime.datetime.utcnow()
            created_user = UserSchema(
                id=None,
                user_id=user_info.user_id,
                email_address=user_info.email_address,
                password=user_info.password,
                role=user_info.role
            )
            logger.info(f"created user in respository: {created_user}")
            # await self.session.add(created_user)
            self.session.add(created_user)
            return created_user.to_domain()
        # except IntegrityError as ie:
        #     logger.error({"message": "conflict"})
        #     logger.error(ie)
        #     return None
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc(limit=None))
            raise

    async def get_one_user_by_user_id(self, user_id: str) -> Optional[User]:
        try:
            query = await self.session.execute(
                select(UserSchema).where(UserSchema.user_id == user_id)
            )
            user_scheme = query.one()[0]
            return user_scheme.to_domain()
            # return [user_scheme.to_domain for user_scheme in user_schemes]
        except NoResultFound:
            return None
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc(limit=None))
            raise

    async def get_user_list_paging(self, offset: int, limit: int, order: str) -> List[Optional[User]]:
        try:
            if order == 'desc':
                query = await self.session\
                            .execute(select(UserSchema)\
                                .offset(offset).limit(limit)\
                                    .order_by(UserSchema.id.desc())
                                )
            else:
                query = await self.session\
                            .execute(select(UserSchema)\
                                .offset(offset).limit(limit)\
                                    .order_by(UserSchema.id)
                                )
            # return query.scalars().all()
            user_schemes = query.scalars().all()
            return [user_scheme.to_domain() for user_scheme in user_schemes]
        except NoResultFound:
            return []
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc(limit=None))
            raise

    # async def set_session_id_to_user(self, user_id: str, session_id: str) -> bool:
    #     try:
    #         await self.session.execute(update(UserSchema).
    #                                     where(UserSchema.user_id == user_id).
    #                                     values(session_id=session_id))
    #         return True
    #     except Exception as e:
    #         logger.error(e)
    #         logger.error(traceback.format_exc(limit=None))
    #         return False

    # async def unset_session_id_from_user(self, user_id: str, session_id: str) -> bool:
    #     try:
    #         await self.session.execute(update(UserSchema).
    #                                     where(UserSchema.user_id == user_id).
    #                                     values(session_id=None))
    #         return True
    #     except Exception as e:
    #         logger.error(e)
    #         logger.error(traceback.format_exc(limit=None))
    #         return False
