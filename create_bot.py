from aiogram import Bot, Dispatcher
from uploader_status import UploaderStatus
from handlers.user_handler import HandlerController
from my_storage import SimpleStorage
from utils import path_join
import aiohttp
import json

config = {}
with open("config.json") as cfg:
    config = json.load(cfg)


API_TOKEN = config.get("api_token", "")
USER_DATA = config.get("user_data", "")
DEBUG = config.get("debug", "")
SERVER_ADDRESS = config.get("server_address", "localhost:8000")
CONFIG_TEMPLATE = path_join(
    USER_DATA,
    "{}",
    "{}",
    "jsons",
    "config.json",
)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
upl_status = UploaderStatus()
hnd_ctrl = HandlerController()
sstorage = SimpleStorage()
client = aiohttp.ClientSession()
