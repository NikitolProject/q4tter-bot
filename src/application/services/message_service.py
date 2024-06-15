from typing import List, Optional

from src.domain.models.message_model import MessageModel
from src.infrastructure.repositories.message_repository import MessageRepository
from src.application.schemas.pydantic.message_schema import MessageSchema


class MessageService:

    message_repository: MessageRepository

    def __init__(self, message_repository: MessageRepository = MessageRepository()) -> None:
        self.message_repository = message_repository

    def create(self, message_schema: MessageSchema) -> MessageModel:
        return self.message_repository.create(
            MessageModel(
                user_id=message_schema.user_id,
                message_id=message_schema.message_id
            )
        )

    def get(self, message_id: int) -> Optional[MessageModel]:
        return self.message_repository.get(message_id=message_id)
    
    def list(self, user_id: int) -> List[MessageModel]:
        return self.message_repository.list(user_id=user_id)
    
    def update(self, message_id: int, message_schema: MessageSchema) -> MessageModel:
        return self.message_repository.update(
            message_id=message_id,
            message=MessageModel(
                user_id=message_schema.user_id,
                message_id=message_id
            )
        )
    
    def delete(self, message_id: int) -> None:
        return self.message_repository.delete(
            self.message_repository.get(message_id=message_id)
        )
