from pydantic import BaseModel


class MessageSchema(BaseModel):
    user_id: int
    message_id: int
