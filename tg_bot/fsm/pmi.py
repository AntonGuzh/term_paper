from aiogram.dispatcher.filters.state import State, StatesGroup


class PMI(StatesGroup):
    student = State()
    space = State()
    goal = State()
    prog_requirements = State()
    doc_requirements = State()
    pc_sources = State()
    prog_sources = State()
    steps = State()
    quantity = State()
    quality = State()
    conditions = State()
    methods = State()
