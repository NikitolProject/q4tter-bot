from aiogram import Dispatcher, Router
from aiogram.types import (
    KeyboardButton, ReplyKeyboardMarkup, ContentType
)
from aiogram.types.message import Message

from src.domain.bot.handlers.handler_factory import HandlerFactory
from src.infrastructure.configs.enviroment import get_environment_variables
from src.application.services.message_service import MessageService
from src.application.services.user_service import UserService
from src.application.schemas.pydantic.message_schema import MessageSchema
from src.application.schemas.pydantic.user_schema import UserSchema
from src.interfaces.bot.ui.main_keyboard import get_main_keyboard

router = Router()


class MessageHandler(HandlerFactory):

    def __init__(self, user_service: UserService, message_service: MessageService) -> None:
        self.config = get_environment_variables()
        self.user_service = user_service
        self.message_service = message_service

    async def handle(self, message: Message) -> None:
        if message.from_user.id in [self.config.OWNER_TELEGRAM_ID, self.config.ADMIN_TELEGRAM_ID]:
            if message.content_type == ContentType.TEXT and message.reply_to_message is not None:
                if message.reply_to_message.content_type == ContentType.TEXT:
                    from_user = message.reply_to_message.text.split("\n\n")[-1]

                    await message.bot.edit_message_text(
                        chat_id=message.from_user.id,
                        message_id=message.reply_to_message.message_id,
                        text=f"{message.text}\n\n{from_user}",
                        reply_markup=message.reply_to_message.reply_markup
                    )

                if message.reply_to_message.content_type in [ContentType.PHOTO, ContentType.VIDEO]:
                    from_user = message.reply_to_message.caption if message.reply_to_message.caption.startswith("✏️ ") else message.reply_to_message.caption.split("\n\n")[-1]

                    await message.bot.edit_message_caption(
                        chat_id=message.from_user.id,
                        message_id=message.reply_to_message.message_id,
                        caption=f"{message.text}\n\n{from_user}",
                        reply_markup=message.reply_to_message.reply_markup
                    )

                await message.answer("✅ Сообщение отредактировано")

            return None
        
        is_blocked = self.__is_blocked_user_in_database(user_id=message.from_user.id)

        if is_blocked:
            return await message.answer("❌ Вы в чёрном списке предложки")
        
        if message.content_type == ContentType.TEXT:
            new_message = await message.bot.send_message(
                chat_id=self.config.ADMIN_TELEGRAM_ID,
                text=f"{message.text}\n\n✏️ {message.from_user.first_name} {message.from_user.last_name}",
                reply_markup=get_main_keyboard(message.from_user.id)
            )
            self.__create_message_in_database(
                user_id=message.from_user.id, 
                message_id=new_message.message_id
            )

        if message.content_type in [ContentType.PHOTO, ContentType.VIDEO]:
            caption = f"{message.caption}\n\n" if message.caption is not None else ""

            new_message = await message.bot.copy_message(
                chat_id=self.config.ADMIN_TELEGRAM_ID,
                from_chat_id=message.from_user.id,
                message_id=message.message_id,
                caption=f"{caption}✏️ {message.from_user.first_name} {message.from_user.last_name}",
                reply_markup=get_main_keyboard(message.from_user.id)
            )
            self.__create_message_in_database(
                user_id=message.from_user.id, 
                message_id=new_message.message_id
            )

        await message.answer("✅ Ваше сообщение отправлено в предложку")

    # TODO: Remove this function
    async def test(self, message: Message) -> None:
        print(message.chat.id)

    def register(self, dp: Dispatcher) -> None:
        router.message(
            lambda message: message.content_type not in [ContentType.STICKER, ContentType.AUDIO] \
                and message.from_user.id == message.chat.id and message.text != "/start"
        )(self.handle)
        router.channel_post()(self.test)
        dp.include_router(router)

    def __is_blocked_user_in_database(self, user_id: int) -> bool:
        user = self.user_service.get(user_id=user_id)

        if user is None:
            user = self.user_service.create(UserSchema(user_id=user_id, is_blocked=False))
        
        return user.is_blocked

    def __create_message_in_database(self, user_id: int, message_id: int) -> None:
        self.message_service.create(MessageSchema(user_id=user_id, message_id=message_id))
