from contextlib import suppress

from aiogram import Dispatcher, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.enums.parse_mode import ParseMode
from aiogram.types.message import Message

from src.domain.bot.handlers.handler_factory import HandlerFactory
from src.infrastructure.configs.enviroment import get_environment_variables
from src.application.services.message_service import MessageService
from src.application.services.user_service import UserService
from src.application.schemas.pydantic.message_schema import MessageSchema
from src.application.schemas.pydantic.user_schema import UserSchema

router = Router()


class UnbanCommandHandler(HandlerFactory):

    def __init__(self, user_service: UserService, message_service: MessageService) -> None:
        self.config = get_environment_variables()
        self.user_service = user_service
        self.message_service = message_service

    async def handle(self, message: Message, command: CommandObject) -> None:
        print("JJNSNJDSNJDSJNDSJNJDSNJDSJSDJNDJNJDNSNJDSJNSD")
        if message.from_user.id not in [self.config.OWNER_TELEGRAM_ID, self.config.ADMIN_TELEGRAM_ID]:
            return None
                
        if command.args is None or not command.args.isdigit():
            return await message.answer("❌ Пожалуйста, введите команду в корректном виде: /unban <user-id>")

        user_id = int(command.args)
        user = self.user_service.get(user_id=user_id)

        if user is None:
            return await message.answer("❌ Пользователя нет в базе данных бота")
        
        if not user.is_blocked:
            return await message.answer("❌ Пользователя нет в чёрном списке бота")
        
        self.user_service.update(user_id=user_id, user_schema=UserSchema(user_id=user_id, is_blocked=False))
        await message.answer("✅ Пользователь успешно удалён из чёрного списка")
    
    def register(self, dp: Dispatcher) -> None:
        router.message(Command("unban"))(self.handle)
        dp.include_router(router)
