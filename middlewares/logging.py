from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
import json
from datetime import datetime


class StatMiddleware(BaseMiddleware):

    def __init__(self):
        super(StatMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        with open("log.txt", "a") as f:
            f.write(f"{datetime.now()}:\n")
            f.write(json.dumps(json.loads(str(message)), indent=4))
            f.write("\n\n")
