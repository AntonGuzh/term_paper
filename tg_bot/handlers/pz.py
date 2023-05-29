from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from tg_bot.messages import pz, main
from tg_bot.fsm.pz import PZ

import templater.parser as p
from templater.parser import named_list_parser
from templater.main import compile_tex
from .main import check_enter


async def start(msg: types.Message):
    await PZ.student.set()
    await msg.answer(main.user)


@check_enter
async def user(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user'] = await p.user_parser(msg.text)
    await PZ.next()
    await msg.answer(pz.intro)


@check_enter
async def intro(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['intro'] = msg.text
    await PZ.next()
    await msg.answer(pz.purpose)


@check_enter
async def purpose(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['purpose'] = msg.text
    await PZ.next()
    await msg.answer(pz.space)


@check_enter
async def space(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['space'] = msg.text
    await PZ.next()
    await msg.answer(pz.task)


@check_enter
async def task(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['task'] = msg.text
    await PZ.next()
    await msg.answer(pz.algo_desc)


@check_enter
async def algo(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['algo'] = msg.text
    await PZ.next()
    await msg.answer(pz.func_desc)


@check_enter
async def func(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['func'] = msg.text
    await PZ.next()
    await msg.answer(pz.communicate)


@check_enter
async def communicate(msg: types.Message, state: FSMContext):
    arr = []
    for block in msg.text.split('\n/sep\n'):
        arr.append(await named_list_parser(block))
    async with state.proxy() as data:
        data['communicate'] = arr
    await PZ.next()
    await msg.answer(pz.pc_cond)


@check_enter
async def pc_cond(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pc_cond'] = msg.text
    await PZ.next()
    await msg.answer(pz.prog_cond)


@check_enter
async def prog_cond(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['prog_cond'] = msg.text
    await PZ.next()
    await msg.answer(pz.wait)


@check_enter
async def wait(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['wait'] = msg.text
    await PZ.next()
    await msg.answer(pz.sources)


@check_enter
async def sources_review(msg: types.Message, state: FSMContext):
    arr = []
    for line in msg.text.split('\n'):
        arr.append(await p.item_parser(line))
    async with state.proxy() as data:
        data['sources_review'] = arr
    await PZ.next()
    await msg.answer(pz.sources_summary)


@check_enter
async def sources_summary(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sources_summary'] = msg.text
        await msg.answer_document(open(await compile_tex(data, 'project/templater/template/pz.tex'), 'rb'))
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['pz', 'ПЗ'])
    dp.register_message_handler(user, state=PZ.student)
    dp.register_message_handler(intro, state=PZ.intro)
    dp.register_message_handler(purpose, state=PZ.purpose)
    dp.register_message_handler(space, state=PZ.space)
    dp.register_message_handler(task, state=PZ.task)
    dp.register_message_handler(algo, state=PZ.algo_desc)
    dp.register_message_handler(func, state=PZ.func_desc)
    dp.register_message_handler(communicate, state=PZ.communicate)
    dp.register_message_handler(pc_cond, state=PZ.pc_cond)
    dp.register_message_handler(prog_cond, state=PZ.prog_cond)
    dp.register_message_handler(wait, state=PZ.wait)
    dp.register_message_handler(sources_review, state=PZ.sources)
    dp.register_message_handler(sources_summary, state=PZ.sources_summary)
