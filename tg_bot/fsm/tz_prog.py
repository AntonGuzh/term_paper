from aiogram.dispatcher.filters.state import State, StatesGroup


class TzProg(StatesGroup):
    student = State()
    terms = State()
    introduction = State()
    analogs_review = State()
    analogs_summary = State()
    sources_review = State()
    sources_summary = State()
    func_requirements = State()
    non_func_requirements = State()
    stack = State()
    architecture = State()
    intermediate_results = State()
    plan = State()
