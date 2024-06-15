from aiogram import Bot, Dispatcher

from src.infrastructure.configs.database import get_db_connection
from src.infrastructure.configs.enviroment import get_environment_variables
from src.infrastructure.repositories.message_repository import MessageRepository
from src.infrastructure.repositories.user_repository import UserRepository

from src.application.services.message_service import MessageService
from src.application.services.user_service import UserService

from src.domain.models.base_model import init

from src.interfaces.bot.handlers.start_handler import StartHandler
from src.interfaces.bot.handlers.message_handler import MessageHandler
from src.interfaces.bot.handlers.main_keyboard_handler import MainKeyboardHandler
from src.interfaces.bot.handlers.unban_command_handler import UnbanCommandHandler

config = get_environment_variables()
bot = Bot(config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


async def main() -> None:
    init()

    connection = get_db_connection().__next__()
    message_repository = MessageRepository(connection)
    user_repository = UserRepository(connection)

    message_service = MessageService(message_repository)
    user_service = UserService(user_repository)

    StartHandler(user_service=user_service, message_service=message_service).register(dp)
    UnbanCommandHandler(user_service=user_service, message_service=message_service).register(dp)

    # IMPORTANT! MessageHandler MUST be below all command handlers
    MessageHandler(user_service=user_service, message_service=message_service).register(dp)
    MainKeyboardHandler(user_service=user_service, message_service=message_service).register(dp)

    await dp.start_polling(bot)
