from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from tg_bot.messages import rp, main
from tg_bot.fsm.rp import RP

import templater.parser as p
from templater.parser import named_list_parser
from templater.main import compile_tex
from .main import check_enter


async def start(msg: types.Message):
    await RP.student.set()
    await msg.answer(main.user)


@check_enter
async def user(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user'] = await p.user_parser(msg.text)
    await RP.next()
    await msg.answer(rp.func_purpose)


@check_enter
async def func_purpose(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['func_purpose'] = msg.text
    await RP.next()
    await msg.answer(rp.use_purpose)


@check_enter
async def use_purpose(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['use_purpose'] = msg.text
    await RP.next()
    await msg.answer(rp.func_desc)


@check_enter
async def func_desc(msg: types.Message, state: FSMContext):
    arr = []
    for line in msg.text.split('\n'):
        arr.append(await p.item_parser(line))
    async with state.proxy() as data:
        data['func_desc'] = arr
    await RP.next()
    await msg.answer(rp.pc_condition)


@check_enter
async def pc_cond(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pc_cond'] = msg.text.split('\n')
    await RP.next()
    await msg.answer(rp.prog_condition)


@check_enter
async def prog_cond(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['prog_cond'] = msg.text.split('\n')
    await RP.next()
    await msg.answer(rp.user_condition)


@check_enter
async def user_cond(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_cond'] = msg.text.split('\n')
    await RP.next()
    await msg.answer(rp.schedule)


@check_enter
async def schedule(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['schedule'] = msg.text
    await RP.next()
    await msg.answer(rp.ctrl)


@check_enter
async def ctrl(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ctrl'] = msg.text
    await RP.next()
    await msg.answer(rp.program_start)


@check_enter
async def program_start(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['program_start'] = msg.text
    await RP.next()
    await msg.answer(rp.func_work)


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
    await RP.next()
    await msg.answer(rp.program_end)


@check_enter
async def program_end(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['program_end'] = msg.text
    await RP.next()
    await msg.answer(rp.inout)


@check_enter
async def inout(msg: types.Message, state: FSMContext):
    if len(msg.text.split('\n')) != 2:
        await msg.answer(main.error)
        return
    async with state.proxy() as data:
        data['inout'] = msg.text.split('\n')
    await RP.next()
    await msg.answer(rp.msg)


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
        await msg.answer_document(open(await compile_tex(data, 'project/templater/template/rp.tex'), 'rb'))
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['rp', 'РП'])
    dp.register_message_handler(user, state=RP.student)
    dp.register_message_handler(func_purpose, state=RP.func_purpose)
    dp.register_message_handler(use_purpose, state=RP.use_purpose)
    dp.register_message_handler(func_desc, state=RP.func_desc)
    dp.register_message_handler(pc_cond, state=RP.pc_condition)
    dp.register_message_handler(prog_cond, state=RP.prog_condition)
    dp.register_message_handler(user_cond, state=RP.user_condition)
    dp.register_message_handler(schedule, state=RP.schedule)
    dp.register_message_handler(ctrl, state=RP.ctrl)
    dp.register_message_handler(program_start, state=RP.program_start)
    dp.register_message_handler(func_work, state=RP.func_work)
    dp.register_message_handler(program_end, state=RP.program_end)
    dp.register_message_handler(inout, state=RP.inout)
    dp.register_message_handler(msgs, state=RP.messages)
