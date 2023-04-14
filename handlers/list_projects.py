from create_bot import bot, USER_DATA, sstorage, hnd_ctrl
from utils import list_projects, path_join
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


def register_list_projects_callback_handlers(dp):
    dp.register_callback_query_handler(
        edit_projects_callback, lambda c: c.data == "edit_project"
    )


async def list_projects_handler(message):  # TODO: add pagination
    user_id = message.chat.id
    projects = list_projects(path_join(USER_DATA, user_id))
    msg = "Your projects:\n" + "\n".join(projects)

    ikb = InlineKeyboardButton("Edit projects", callback_data="edit_project")
    ikbm = InlineKeyboardMarkup().add(ikb)

    sstorage.set_data(user_id, "projects_list", projects)
    await message.answer(msg, reply_markup=ikbm)


async def edit_projects_callback(callback_q):
    await bot.answer_callback_query(callback_q.id)
    
    user_id = callback_q.from_user.id
    projects = sstorage.get_data(user_id, "projects_list")

    msg = "Chooose project for editing:\n"

    ikbm = ReplyKeyboardMarkup(resize_keyboard=True)
    for proj in projects:
        ikbm.insert(KeyboardButton(proj))

    hnd_ctrl.set_pipeline(user_id, "edit_proj")

    await bot.send_message(user_id, text=msg, reply_markup=ikbm)
