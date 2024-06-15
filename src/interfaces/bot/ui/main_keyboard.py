from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🚷", callback_data=f"ban-{user_id}"),
        InlineKeyboardButton(text="❌", callback_data=f"clear-{user_id}"),
        InlineKeyboardButton(text="❎", callback_data=f"delete"),
        InlineKeyboardButton(text="🗓", callback_data=f"confirm"),
        InlineKeyboardButton(text="🚹", url=f"tg://user?id={user_id}")
    )
    return builder.as_markup()
