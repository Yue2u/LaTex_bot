from aiogram import executor
from album_middleware import AlbumMiddleware
from handlers.basic import register_basic_handlers
from create_bot import dp, hnd_ctrl
from pipelines import pipelines_table


if __name__ == "__main__":
    dp.middleware.setup(AlbumMiddleware())
    register_basic_handlers(dp)
    hnd_ctrl.set_pipelines_table(pipelines_table)
    executor.start_polling(dp, skip_updates=True)
