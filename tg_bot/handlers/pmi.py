from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from tg_bot.messages import pmi, main
from tg_bot.fsm.pmi import PMI

import templater.parser as p
from templater.parser import named_list_parser
from templater.main import compile_tex
from .main import check_enter


async def start(msg: types.Message):
    await PMI.student.set()
    await msg.answer(main.user)


@check_enter
async def user(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user'] = await p.user_parser(msg.text)
    await PMI.next()
    await msg.answer(pmi.space)


@check_enter
async def space(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['space'] = msg.text
    await PMI.next()
    await msg.answer(pmi.goal)


@check_enter
async def goal(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['goal'] = msg.text
    await PMI.next()
    await msg.answer(pmi.prog_requirements)


@check_enter
async def prog_req(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['prog_req'] = msg.text.split('\n')
    await PMI.next()
    await msg.answer(pmi.doc_requirements)


@check_enter
async def doc_req(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['doc_req'] = msg.text.split('\n')
    await PMI.next()
    await msg.answer(pmi.pc_sources)


@check_enter
async def pc_source(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pc_source'] = msg.text.split('\n')
    await PMI.next()
    await msg.answer(pmi.prog_sources)


@check_enter
async def prog_source(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['prog_source'] = msg.text.split('\n')
    await PMI.next()
    await msg.answer(pmi.steps)


@check_enter
async def steps(msg: types.Message, state: FSMContext):
    arr = []
    for block in msg.text.split('\n/sep\n'):
        arr.append(await named_list_parser(block))
    async with state.proxy() as data:
        data['steps'] = arr
    await PMI.next()
    await msg.answer(pmi.quantity)


@check_enter
async def quantity(msg: types.Message, state: FSMContext):
    arr = []
    for line in msg.text.split('\n'):
        arr.append(await p.item_parser(line))
    async with state.proxy() as data:
        data['quantity'] = arr
    await PMI.next()
    await msg.answer(pmi.quality)


@check_enter
async def quality(msg: types.Message, state: FSMContext):
    arr = []
    for line in msg.text.split('\n'):
        arr.append(await p.item_parser(line))
    async with state.proxy() as data:
        data['quality'] = arr
    await PMI.next()
    await msg.answer(pmi.conditions)


@check_enter
async def conditions(msg: types.Message, state: FSMContext):
    arr = []
    for block in msg.text.split('\n/sep\n'):
        arr.append(await named_list_parser(block))
    async with state.proxy() as data:
        data['conditions'] = arr
    await PMI.next()
    await msg.answer(pmi.methods)


@check_enter
async def methods(msg: types.Message, state: FSMContext):
    arr = []
    for block in msg.text.split('\n/sep\n'):
        arr.append(await named_list_parser(block))
    async with state.proxy() as data:
        data['methods'] = arr
        await msg.answer_document(open(await compile_tex(data, 'project/templater/template/pmi.tex'), 'rb'))
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['pmi', 'ПМИ'])
    dp.register_message_handler(user, state=PMI.student)
    dp.register_message_handler(space, state=PMI.space)
    dp.register_message_handler(goal, state=PMI.goal)
    dp.register_message_handler(pc_source, state=PMI.pc_sources)
    dp.register_message_handler(prog_source, state=PMI.prog_sources)
    dp.register_message_handler(prog_req, state=PMI.prog_requirements)
    dp.register_message_handler(doc_req, state=PMI.doc_requirements)
    dp.register_message_handler(steps, state=PMI.steps)
    dp.register_message_handler(quantity, state=PMI.quantity)
    dp.register_message_handler(quality, state=PMI.quality)
    dp.register_message_handler(conditions, state=PMI.conditions)
    dp.register_message_handler(methods, state=PMI.methods)
