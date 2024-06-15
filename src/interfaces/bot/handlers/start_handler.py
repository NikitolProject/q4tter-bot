from contextlib import suppress

from aiogram import Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.enums.parse_mode import ParseMode
from aiogram.types.message import Message

from src.domain.bot.handlers.handler_factory import HandlerFactory
from src.infrastructure.configs.enviroment import get_environment_variables
from src.application.services.message_service import MessageService
from src.application.services.user_service import UserService
from src.application.schemas.pydantic.message_schema import MessageSchema
from src.application.schemas.pydantic.user_schema import UserSchema

router = Router()


class StartHandler(HandlerFactory):

    def __init__(self, user_service: UserService, message_service: MessageService) -> None:
        self.config = get_environment_variables()
        self.user_service = user_service
        self.message_service = message_service

    async def handle(self, message: Message) -> None:
        if message.from_user.id not in [self.config.OWNER_TELEGRAM_ID, self.config.ADMIN_TELEGRAM_ID]:
            return await message.answer(
                "Напишите сообщение (с приложением, или без), которое вы хотите отправить в предложку"
            )

        keyboard = [[KeyboardButton(text="🧹 Очистить предложку")], [KeyboardButton(text="🚷 Banlist")]]
        keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        user = self.user_service.create(user_schema=UserSchema(user_id=message.bot.id, is_blocked=False))
        bot_message = await message.answer(
            "Это начало ленты! Для очистки БД нажмите кнопку ниже", 
            reply_markup=keyboard
        )
        self.message_service.create(
            MessageSchema(user_id=user.user_id, message_id=bot_message.message_id)
        )

    async def handle_clear_chat(self, message: Message) -> None:
        deleted_messages = []

        for user in self.user_service.list():

            for user_message in self.message_service.list(user_id=user.user_id):
                deleted_messages.append(user_message.message_id)
                self.message_service.delete(user_message.message_id)
            
            if not user.is_blocked:
                self.user_service.delete(user_id=user.user_id)
        
        with suppress(Exception):
            await message.bot.delete_messages(message.from_user.id, deleted_messages)

        keyboard = [[KeyboardButton(text="🧹 Очистить предложку")], [KeyboardButton(text="🚷 Banlist")]]
        keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        user = self.user_service.create(user_schema=UserSchema(user_id=message.bot.id, is_blocked=False))
        bot_message = await message.answer(
            "Это начало ленты! Для очистки БД нажмите кнопку ниже", 
            reply_markup=keyboard
        )
        self.message_service.create(
            MessageSchema(user_id=user.user_id, message_id=bot_message.message_id)
        )
        await message.delete()

    async def handle_ban_list(self, message: Message) -> None:
        text = "⛔️Список заблокированных пользователей:\n\n"

        for idx, user in enumerate(self.user_service.list()):
            if not user.is_blocked:
                continue

            user_entity = await message.bot.get_chat(user.user_id)
            text += f"{idx + 1}. [{user_entity.full_name}](tg://user?id={user.user_id}) `/unban {user.user_id}`\n"

        text += "\nЕсли вы хотите разблокировать пользователя - введите /unban <user-id>"
        await message.answer(text=text, parse_mode=ParseMode.MARKDOWN)
        await message.delete()

    def register(self, dp: Dispatcher) -> None:
        router.message(CommandStart())(self.handle)
        router.message(F.text == "🧹 Очистить предложку")(self.handle_clear_chat)
        router.message(F.text == "🚷 Banlist")(self.handle_ban_list)
        dp.include_router(router)
