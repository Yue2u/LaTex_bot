from aiogram import Bot, Dispatcher
from uploader_status import UploaderStatus
from handlers.user_handler import HandlerController


API_TOKEN = "6228829336:AAF3API2d5KQTgpbjIlBuFZhrp55PgsApJw"
USER_DATA = "user_data"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
upl_status = UploaderStatus()
hnd_ctrl = HandlerController()
