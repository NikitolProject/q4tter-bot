from abc import abstractmethod
from typing import TypeVar

from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext


#################################
#  Abstract Class for Handler   #
#################################
class HandlerFactory:

    @abstractmethod
    async def handle(self, message: types.Message, state: FSMContext) -> None:
        pass

    @abstractmethod
    def register(self, dp: Dispatcher) -> None:
        pass
