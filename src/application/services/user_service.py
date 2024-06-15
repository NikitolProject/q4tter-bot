from typing import List, Optional

from src.domain.models.user_model import UserModel
from src.infrastructure.repositories.user_repository import UserRepository
from src.application.schemas.pydantic.user_schema import UserSchema


class UserService:

    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository = UserRepository()) -> None:
        self.user_repository = user_repository

    def create(self, user_schema: UserSchema) -> UserModel:
        return self.user_repository.create(
            UserModel(
                user_id=user_schema.user_id,
                is_blocked=user_schema.is_blocked
            )
        )

    def get(self, user_id: int) -> Optional[UserModel]:
        return self.user_repository.get(user_id=user_id)
    
    def list(self) -> List[UserModel]:
        return self.user_repository.list()
    
    def update(self, user_id: int, user_schema: UserSchema) -> UserModel:
        return self.user_repository.update(
            user_id=user_id,
            user=UserModel(
                user_id=user_schema.user_id,
                is_blocked=user_schema.is_blocked
            )
        )
    
    def delete(self, user_id: int) -> None:
        return self.user_repository.delete(
            self.user_repository.get(user_id=user_id)
        )
