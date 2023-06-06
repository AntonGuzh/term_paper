from aiogram import Dispatcher, types
from tg_bot.messages import main
from aiogram.dispatcher import FSMContext

from templater.parser import base_parser


async def start(msg: types.Message):
    await msg.answer(main.start)


def check_enter(handler):
    async def checker(msg: types.Message, state: FSMContext):
        try:
            msg.text = await base_parser(msg.text)
            await handler(msg, state)
        except BaseException as e:
            await msg.answer(main.error)

    return checker


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'], commands_prefix='/')
