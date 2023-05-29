from aiogram.utils import executor
from tg_bot.create_bot import dp
from tg_bot.handlers import main, tz_prog, tz_search, ro, rp, pz, pmi

if __name__ == "__main__":
    main.register_handlers(dp)

    tz_prog.register_handlers(dp)
    tz_search.register_handlers(dp)
    ro.register_handlers(dp)
    rp.register_handlers(dp)
    pz.register_handlers(dp)
    pmi.register_handlers(dp)

    executor.start_polling(dp, skip_updates=True)
