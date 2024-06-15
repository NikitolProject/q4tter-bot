from sqlalchemy import (
    Column, Integer, BigInteger,
    PrimaryKeyConstraint
)
from src.domain.models.base_model import entity_meta


class MessageModel(entity_meta):
    __tablename__ = "messages"

    id = Column(Integer)
    user_id = Column(BigInteger, nullable=False)
    message_id = Column(BigInteger, nullable=False)

    PrimaryKeyConstraint(id)

    def normalize(self) -> dict:
        return {
            "id": int(self.id.__str__()),
            "user_id": int(self.client_id.__str__()),
            "message_id": int(self.message_id.__str__())
        }
