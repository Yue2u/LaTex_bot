from create_bot import upl_status, bot, USER_DATA, CONFIG_TEMPLATE, hnd_ctrl, sstorage
from utils import path_join, create_folder
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from json_config import set_font_size, set_indent_size, init_project_config


def register_new_proj_callback_handlers(dp):
    dp.register_callback_query_handler(
        np_edit_offset_callback_handler, lambda c: c.data == "np_edit_offset"
    )
    dp.register_callback_query_handler(
        np_edit_font_size_callback_handler, lambda c: c.data == "np_edit_font_size"
    )
    dp.register_callback_query_handler(np_skip, lambda c: c.data == "np_edit_skip")
    dp.register_callback_query_handler(
        np_small_font_size, lambda c: c.data == "np_small_font_size"
    )
    dp.register_callback_query_handler(
        np_medium_font_size, lambda c: c.data == "np_medium_font_size"
    )
    dp.register_callback_query_handler(
        np_large_font_size, lambda c: c.data == "np_large_font_size"
    )


async def np_start(message):
    await message.answer("Enter new project title")


async def np_title_handler(message):
    title = message.text
    user_id = message.chat.id

    path = path_join(USER_DATA, user_id, title)
    create_folder(path)

    upl_status.start_upload(user_id, path_join(USER_DATA, user_id, title, "images"))
    sstorage.set_data(user_id, "editable_project", title)
    init_project_config(CONFIG_TEMPLATE.format(user_id, title))

    ikbm = InlineKeyboardMarkup().row(
        InlineKeyboardButton("Offset", callback_data="np_edit_offset"),
        InlineKeyboardButton("Font size", callback_data="np_edit_font_size"),
        InlineKeyboardButton("Skip", callback_data="np_edit_skip"),
    )

    await message.answer("Do you want to change pdf options?", reply_markup=ikbm)


async def project_message(user_id):
    msg = "Project successfully created\n"
    msg += "Send pictures of conspect in right order, please.\n"
    msg += "Type /stop to stop uploading files"
    await bot.send_message(user_id, msg)


async def np_skip(callback_q):
    user_id = callback_q.from_user.id

    hnd_ctrl.next_handler(user_id)

    await bot.answer_callback_query(callback_q.id)
    await project_message(user_id)


async def np_edit_offset_callback_handler(callback_q):
    user_id = callback_q.from_user.id

    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(user_id, "Input document offset in mm")


async def np_offset_input_handler(message):
    user_id = message.chat.id

    text = message.text
    if not text.isdigit() or int(text) < 0:
        await message.answer("Input is not a number or less than 0, try again please")
        return

    path = CONFIG_TEMPLATE.format(
        user_id, sstorage.get_data(user_id, "editable_project")
    )
    set_indent_size(path, int(text))

    await message.answer(f"Indent size set to {int(text)} mm")
    await project_message(user_id)


async def np_edit_font_size_callback_handler(callback_q):
    user_id = callback_q.from_user.id
    await bot.answer_callback_query(callback_q.id)

    inkm = InlineKeyboardMarkup().row(
        InlineKeyboardButton("Small", callback_data="np_small_font_size"),
        InlineKeyboardButton("Medium", callback_data="np_medium_font_size"),
        InlineKeyboardButton("Large", callback_data="np_large_font_size"),
    )

    await bot.send_message(user_id, "Choose font size", reply_markup=inkm)


async def np_small_font_size(callback_q):
    user_id = callback_q.from_user.id
    path = CONFIG_TEMPLATE.format(
        user_id, sstorage.get_data(user_id, "editable_project")
    )
    set_font_size(path, "small")

    hnd_ctrl.next_handler(user_id)

    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(user_id, "Font size changed to small")
    await project_message(user_id)


async def np_medium_font_size(callback_q):
    user_id = callback_q.from_user.id
    path = CONFIG_TEMPLATE.format(
        user_id, sstorage.get_data(user_id, "editable_project")
    )
    set_font_size(path, "medium")

    hnd_ctrl.next_handler(user_id)

    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(user_id, "Font size changed to medium")
    await project_message(user_id)


async def np_large_font_size(callback_q):
    user_id = callback_q.from_user.id
    path = CONFIG_TEMPLATE.format(
        user_id, sstorage.get_data(user_id, "editable_project")
    )
    set_font_size(path, "large")

    hnd_ctrl.next_handler(user_id)

    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(user_id, "Font size changed to large")
    await project_message(user_id)
