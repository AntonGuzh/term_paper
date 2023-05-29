from aiogram.dispatcher.filters.state import State, StatesGroup


class PZ(StatesGroup):
    student = State()
    intro = State()
    purpose = State()
    space = State()
    task = State()
    algo_desc = State()
    func_desc = State()
    communicate = State()
    pc_cond = State()
    prog_cond = State()
    wait = State()
    sources = State()
    sources_summary = State()
