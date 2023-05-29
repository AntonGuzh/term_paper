from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from tg_bot.messages import tz, main
from tg_bot.fsm.tz_prog import TzProg

import templater.parser as p
from templater.parser import named_list_parser
from templater.main import compile_tex
from .main import check_enter


async def start(msg: types.Message):
    await TzProg.student.set()
    await msg.answer(main.user)


@check_enter
async def user(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user'] = await p.user_parser(msg.text)
    await TzProg.next()
    await msg.answer(tz.terms)


@check_enter
async def terms(msg: types.Message, state: FSMContext):
    arr = []
    for line in msg.text.split('\n'):
        arr.append(await p.item_parser(line))
    async with state.proxy() as data:
        data['terms'] = arr
    await TzProg.next()
    await msg.answer(tz.intro)


@check_enter
async def introduction(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['intro'] = msg.text
    await TzProg.next()
    await msg.answer(tz.analogs)


@check_enter
async def analogs_review(msg: types.Message, state: FSMContext):
    arr = []
    for line in msg.text.split('\n'):
        arr.append(await p.item_parser(line))
    async with state.proxy() as data:
        data['analogs_review'] = arr
    await TzProg.next()
    await msg.answer(tz.analogs_summary)


@check_enter
async def analogs_summary(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['analogs_summary'] = msg.text
    await TzProg.next()
    await msg.answer(tz.sources)


@check_enter
async def sources_review(msg: types.Message, state: FSMContext):
    arr = []
    for line in msg.text.split('\n'):
        arr.append(await p.item_parser(line))
    async with state.proxy() as data:
        data['sources_review'] = arr
    await TzProg.next()
    await msg.answer(tz.sources_summary)


@check_enter
async def sources_summary(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sources_summary'] = msg.text
    await TzProg.next()
    await msg.answer(tz.func_requirements)


@check_enter
async def func_req(msg: types.Message, state: FSMContext):
    arr = []
    for block in msg.text.split('\n/sep\n'):
        arr.append(await named_list_parser(block))
    async with state.proxy() as data:
        data['func_req'] = arr
    await TzProg.next()
    await msg.answer(tz.non_func_requirements)


@check_enter
async def non_func_req(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['non_func_req'] = msg.text.split('\n')
    await TzProg.next()
    await msg.answer(tz.tech)


@check_enter
async def stack(msg: types.Message, state: FSMContext):
    arr = []
    for line in msg.text.split('\n'):
        arr.append(await p.item_parser(line))
    async with state.proxy() as data:
        data['technologies'] = arr
    await TzProg.next()
    await msg.answer(tz.arch)


@check_enter
async def arch(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['architecture'] = msg.text
    await TzProg.next()
    await msg.answer(tz.int_res)


@check_enter
async def intermediate_results(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['intermediate_results'] = msg.text.split('\n')
    await TzProg.next()
    await msg.answer(tz.plan)


@check_enter
async def plan(msg: types.Message, state: FSMContext):
    arr = []
    for line in msg.text.split('\n'):
        arr.append(await p.plan_parser(line))
    async with state.proxy() as data:
        data['plan'] = arr
        await msg.answer_document(open(await compile_tex(data, 'project/templater/template/tz_prog.tex'), 'rb'))
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['tz_prog', 'ТЗ_П'])
    dp.register_message_handler(user, state=TzProg.student)
    dp.register_message_handler(terms, state=TzProg.terms)
    dp.register_message_handler(introduction, state=TzProg.introduction)
    dp.register_message_handler(analogs_review, state=TzProg.analogs_review)
    dp.register_message_handler(analogs_summary, state=TzProg.analogs_summary)
    dp.register_message_handler(sources_review, state=TzProg.sources_review)
    dp.register_message_handler(sources_summary, state=TzProg.sources_summary)
    dp.register_message_handler(func_req, state=TzProg.func_requirements)
    dp.register_message_handler(non_func_req, state=TzProg.non_func_requirements)
    dp.register_message_handler(stack, state=TzProg.stack)
    dp.register_message_handler(arch, state=TzProg.architecture)
    dp.register_message_handler(intermediate_results, state=TzProg.intermediate_results)
    dp.register_message_handler(plan, state=TzProg.plan)
