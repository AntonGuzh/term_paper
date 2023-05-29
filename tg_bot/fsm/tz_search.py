from aiogram.dispatcher.filters.state import State, StatesGroup


class TzSearch(StatesGroup):
    student = State()
    terms = State()
    introduction = State()
    sources_review = State()
    sources_summary = State()
    intermediate_results = State()
    plan = State()
