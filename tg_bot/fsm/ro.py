from aiogram.dispatcher.filters.state import State, StatesGroup


class RO(StatesGroup):
    student = State()
    func_purpose = State()
    use_purpose = State()
    func_desc = State()
    pc_condition = State()
    prog_condition = State()
    user_condition = State()
    program_start = State()
    func_work = State()
    program_end = State()
    messages = State()
