from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from tg_bot.messages import ro, main
from tg_bot.fsm.ro import RO

import templater.parser as p
from templater.parser import named_list_parser
from templater.main import compile_tex
from .main import check_enter


async def start(msg: types.Message):
    await RO.student.set()
    await msg.answer(main.user)


@check_enter
async def user(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user'] = await p.user_parser(msg.text)
    await RO.next()
    await msg.answer(ro.func_purpose)


@check_enter
async def func_purpose(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['func_purpose'] = msg.text
    await RO.next()
    await msg.answer(ro.use_purpose)


@check_enter
async def use_purpose(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['use_purpose'] = msg.text
    await RO.next()
    await msg.answer(ro.func_desc)


@check_enter
async def func_desc(msg: types.Message, state: FSMContext):
    arr = []
    for line in msg.text.split('\n'):
        arr.append(await p.item_parser(line))
    async with state.proxy() as data:
        data['func_desc'] = arr
    await RO.next()
    await msg.answer(ro.pc_condition)


@check_enter
async def pc_cond(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pc_cond'] = msg.text.split('\n')
    await RO.next()
    await msg.answer(ro.prog_condition)


@check_enter
async def prog_cond(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['prog_cond'] = msg.text.split('\n')
    await RO.next()
    await msg.answer(ro.user_condition)


@check_enter
async def user_cond(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_cond'] = msg.text.split('\n')
    await RO.next()
    await msg.answer(ro.program_start)


@check_enter
async def program_start(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['program_start'] = msg.text
    await RO.next()
    await msg.answer(ro.func_work)


@check_enter
async def func_work(msg: types.Message, state: FSMContext):
    arr = []
    for line in msg.text.split('\n'):
        arr.append(await p.item_parser(line))
    async with state.proxy() as data:
        if len(arr) != len(data['func_desc']):
            await msg.answer(main.error)
            return
        data['func_work'] = arr
    await RO.next()
    await msg.answer(ro.program_end)


@check_enter
async def program_end(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['program_end'] = msg.text
    await RO.next()
    await msg.answer(ro.msg)


@check_enter
async def msgs(msg: types.Message, state: FSMContext):
    arr = []
    for block in msg.text.split('\n/sep\n'):
        arr.append(await p.named_list_parser(block))
        if len(arr[-1].items) != 3:
            await msg.answer(main.error)
            return
    async with state.proxy() as data:
        data['msgs'] = arr
        await msg.answer_document(open(await compile_tex(data, 'project/templater/template/ro.tex'), 'rb'))
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['ro', 'РО'])
    dp.register_message_handler(user, state=RO.student)
    dp.register_message_handler(func_purpose, state=RO.func_purpose)
    dp.register_message_handler(use_purpose, state=RO.use_purpose)
    dp.register_message_handler(func_desc, state=RO.func_desc)
    dp.register_message_handler(pc_cond, state=RO.pc_condition)
    dp.register_message_handler(prog_cond, state=RO.prog_condition)
    dp.register_message_handler(user_cond, state=RO.user_condition)
    dp.register_message_handler(program_start, state=RO.program_start)
    dp.register_message_handler(func_work, state=RO.func_work)
    dp.register_message_handler(program_end, state=RO.program_end)
    dp.register_message_handler(msgs, state=RO.messages)
