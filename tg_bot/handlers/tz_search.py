from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from tg_bot.messages import tz, main
from tg_bot.fsm.tz_search import TzSearch

import templater.parser as p
from templater.main import compile_tex
from .main import check_enter


async def start(msg: types.Message):
    await TzSearch.student.set()
    await msg.answer(main.user)


@check_enter
async def user(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user'] = await p.user_parser(msg.text)
    await TzSearch.next()
    await msg.answer(tz.terms)


@check_enter
async def terms(msg: types.Message, state: FSMContext):
    arr = []
    for line in msg.text.split('\n'):
        arr.append(await p.item_parser(line))
    async with state.proxy() as data:
        data['terms'] = arr
    await TzSearch.next()
    await msg.answer(tz.intro)


@check_enter
async def introduction(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['intro'] = msg.text
    await TzSearch.next()
    await msg.answer(tz.analogs)


@check_enter
async def sources_review(msg: types.Message, state: FSMContext):
    arr = []
    for line in msg.text.split('\n'):
        arr.append(await p.item_parser(line))
    async with state.proxy() as data:
        data['sources_review'] = arr
    await TzSearch.next()
    await msg.answer(tz.sources_summary)


@check_enter
async def sources_summary(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sources_summary'] = msg.text
    await TzSearch.next()
    await msg.answer(tz.func_requirements)


@check_enter
async def intermediate_results(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['intermediate_results'] = msg.text.split('\n')
    await TzSearch.next()
    await msg.answer(tz.plan)


@check_enter
async def plan(msg: types.Message, state: FSMContext):
    arr = []
    for line in msg.text.split('\n'):
        arr.append(await p.plan_parser(line))
    async with state.proxy() as data:
        data['plan'] = arr
        await msg.answer_document(open(await compile_tex(data, 'project/templater/template/tz_search.tex'), 'rb'))
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['tz_search', 'ТЗ_И'])
    dp.register_message_handler(user, state=TzSearch.student)
    dp.register_message_handler(terms, state=TzSearch.terms)
    dp.register_message_handler(introduction, state=TzSearch.introduction)
    dp.register_message_handler(sources_review, state=TzSearch.sources_review)
    dp.register_message_handler(sources_summary, state=TzSearch.sources_summary)
    dp.register_message_handler(intermediate_results, state=TzSearch.intermediate_results)
    dp.register_message_handler(plan, state=TzSearch.plan)
