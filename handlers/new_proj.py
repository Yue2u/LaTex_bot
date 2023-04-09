from create_bot import upl_status, USER_DATA
from .utils import path_join, create_folder


async def new_proj_start(message):
    await message.answer("Enter new project title")


async def new_proj_title_handler(message):
    title = message.text
    user_id = message.chat.id

    path = path_join(USER_DATA, user_id, title)
    await create_folder(path)
    upl_status.start_upload(user_id, path_join(USER_DATA, user_id, title, "images"))

    msg = "Project successfully created\n"
    msg += "Send pictures of conspect in right order, please.\n"
    msg += "Type /stop to stop uploading files"
    await message.answer(msg)
