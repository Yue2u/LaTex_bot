from aiogram import Bot, Dispatcher
from uploader_status import UploaderStatus
from handlers.user_handler import HandlerController
from my_storage import SimpleStorage
from utils import path_join


API_TOKEN = "6228829336:AAF3API2d5KQTgpbjIlBuFZhrp55PgsApJw"
USER_DATA = "user_data"
CONFIG_TEMPLATE = path_join(
    USER_DATA,
    "{}",
    "{}",
    "jsons",
    "config.json",
)
DEBUG = False

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
upl_status = UploaderStatus()
hnd_ctrl = HandlerController()
sstorage = SimpleStorage()
