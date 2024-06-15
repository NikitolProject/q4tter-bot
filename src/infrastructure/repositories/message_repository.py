from typing import List, Optional

from sqlalchemy.orm import Session, lazyload

from src.infrastructure.configs.database import get_db_connection
from src.domain.repositories.repository_meta import RepositoryMeta
from src.domain.models.message_model import MessageModel


class MessageRepository(RepositoryMeta):

    db: Session

    def __init__(self, db: Session = get_db_connection().__next__()) -> None:
        self.db = db

    def list(self, user_id: int) -> List[MessageModel]:
        query = self.db.query(MessageModel)
        query = query.filter_by(user_id=user_id)

        return query.all()

    def get(self, message_id: int) -> Optional[MessageModel]:
        return self.db.query(MessageModel).filter_by(message_id=message_id).first()

    def create(self, message: MessageModel) -> MessageModel:
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def update(self, message_id: int, message: MessageModel) -> MessageModel:
        old_message = self.get(message_id)
        old_message.user_id = message.user_id
        self.db.merge(old_message)
        self.db.commit()
        return message

    def delete(self, message: MessageModel) -> None:
        self.db.delete(message)
        self.db.commit()
        self.db.flush()
