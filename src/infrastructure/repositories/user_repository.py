from typing import List, Optional

from sqlalchemy.orm import Session, lazyload

from src.infrastructure.configs.database import get_db_connection
from src.domain.repositories.repository_meta import RepositoryMeta
from src.domain.models.user_model import UserModel


class UserRepository(RepositoryMeta):

    db: Session

    def __init__(self, db: Session = get_db_connection().__next__()) -> None:
        self.db = db

    def list(self) -> List[UserModel]:
        query = self.db.query(UserModel)

        return query.all()

    def get(self, user_id: int) -> Optional[UserModel]:
        return self.db.query(UserModel).filter_by(user_id=user_id).first()

    def create(self, user: UserModel) -> UserModel:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user_id: int, user: UserModel) -> UserModel:
        old_user = self.get(user_id)
        old_user.is_blocked = user.is_blocked
        self.db.merge(old_user)
        self.db.commit()
        return user

    def delete(self, user: UserModel) -> None:
        self.db.delete(user)
        self.db.commit()
        self.db.flush()
