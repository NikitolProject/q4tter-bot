from sqlalchemy import (
    Column, Integer, BigInteger,
    Boolean, PrimaryKeyConstraint
)
from src.domain.models.base_model import entity_meta


class UserModel(entity_meta):
    __tablename__ = "users"

    id = Column(Integer)
    user_id = Column(BigInteger, nullable=False)
    is_blocked = Column(Boolean, nullable=False)

    PrimaryKeyConstraint(id)

    def normalize(self) -> dict:
        return {
            "id": int(self.id.__str__()),
            "user_id": int(self.user_id.__str__()),
            "is_blocked": bool(self.is_blocked.__str__())
        }
