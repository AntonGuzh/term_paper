from aiogram.dispatcher.filters.state import State, StatesGroup


class RP(StatesGroup):
    student = State()
    func_purpose = State()
    use_purpose = State()
    func_desc = State()
    pc_condition = State()
    prog_condition = State()
    user_condition = State()
    schedule = State()
    ctrl = State()
    program_start = State()
    func_work = State()
    program_end = State()
    inout = State()
    messages = State()
