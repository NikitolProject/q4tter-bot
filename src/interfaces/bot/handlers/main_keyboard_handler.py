from contextlib import suppress

from aiogram import Dispatcher, Router, F
from aiogram.types import (
    CallbackQuery, ContentType
)
from aiogram.types.message import Message

from src.domain.bot.handlers.handler_factory import HandlerFactory
from src.infrastructure.configs.enviroment import get_environment_variables
from src.application.services.message_service import MessageService
from src.application.services.user_service import UserService
from src.application.schemas.pydantic.message_schema import MessageSchema
from src.application.schemas.pydantic.user_schema import UserSchema

router = Router()


class MainKeyboardHandler(HandlerFactory):

    def __init__(self, user_service: UserService, message_service: MessageService) -> None:
        self.config = get_environment_variables()
        self.user_service = user_service
        self.message_service = message_service

    async def handle(self, _: Message) -> None:
        """
        Since this handler handles several callbacks at once - the main function remains undefined
        """

    async def handle_ban_button(self, callback: CallbackQuery) -> None:
        user_id = int(callback.data.replace("ban-", ""))
        deleted_messages = []

        for message in self.message_service.list(user_id=user_id):
            deleted_messages.append(message.message_id)
            self.message_service.delete(message_id=message.message_id)
        
        with suppress(Exception):
            await callback.bot.delete_messages(
                chat_id=callback.message.chat.id, message_ids=deleted_messages
            )
        
        self.user_service.update(
            user_id=user_id, 
            user_schema=UserSchema(user_id=user_id, is_blocked=True)
        )

    async def handle_clear_button(self, callback: CallbackQuery) -> None:
        user_id = int(callback.data.replace("clear-", ""))
        deleted_messages = []

        for message in self.message_service.list(user_id=user_id):
            deleted_messages.append(message.message_id)
            self.message_service.delete(message_id=message.message_id)
        
        await callback.bot.delete_messages(chat_id=callback.message.chat.id, message_ids=deleted_messages)

    async def handle_delete_button(self, callback: CallbackQuery) -> None:
        self.message_service.delete(message_id=callback.message.message_id)
        await callback.message.delete()

    async def handle_confirm_button(self, callback: CallbackQuery) -> None:
        if callback.message.content_type == ContentType.TEXT:
            await callback.bot.send_message(
                chat_id=self.config.OUTPUT_CHAT_TELEGRAM_ID,
                text="\n\n".join(callback.message.text.split("\n\n")[:-1])
            )

        if callback.message.content_type in [ContentType.PHOTO, ContentType.VIDEO]:            
            if "\n\n" not in callback.message.caption:
                caption = " "
            else:
                caption = "\n\n".join(callback.message.caption.split("\n\n")[:-1])

            await callback.bot.copy_message(
                chat_id=self.config.OUTPUT_CHAT_TELEGRAM_ID,
                from_chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                caption=caption,
                reply_markup=None
            )

        self.message_service.delete(message_id=callback.message.message_id)
        await callback.message.delete()

    def register(self, dp: Dispatcher) -> None:
        router.callback_query(F.data.startswith("ban-"))(self.handle_ban_button)
        router.callback_query(F.data.startswith("clear-"))(self.handle_clear_button)
        router.callback_query(F.data == "delete")(self.handle_delete_button)
        router.callback_query(F.data == "confirm")(self.handle_confirm_button)
        dp.include_router(router)
