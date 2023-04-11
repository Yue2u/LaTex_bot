from create_bot import bot, hnd_ctrl, upl_status, sstorage, CONFIG_TEMPLATE, USER_DATA
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from json_config import set_font_size, set_indent_size
from utils import path_join


def register_edit_proj_callback_handlers(dp):
    dp.register_callback_query_handler(
        edit_offset_callback_handler, lambda c: c.data == "edit_offset"
    )
    dp.register_callback_query_handler(
        edit_font_size_callback_handler, lambda c: c.data == "edit_font_size"
    )
    dp.register_callback_query_handler(
        add_pages_callback_handler, lambda c: c.data == "edit_add_pages"
    )
    dp.register_callback_query_handler(
        small_font_size, lambda c: c.data == "set_small_font_size"
    )
    dp.register_callback_query_handler(
        medium_font_size, lambda c: c.data == "set_medium_font_size"
    )
    dp.register_callback_query_handler(
        large_font_size, lambda c: c.data == "set_large_font_size"
    )


async def get_project_title(message):
    user_id = message.chat.id

    projects = sstorage.get_data(user_id, "projects_list")
    if message.text not in projects:
        await message.answer(
            "You choosed wrong project, returning back",
            reply_markup=ReplyKeyboardRemove(),
        )
        hnd_ctrl.complete_pipeline(user_id)
        return

    sstorage.set_data(user_id, "editable_project", message.text)

    msg1 = f"Start editing project '{message.text}'\n"
    msg2 = "Choose option to edit"

    inkm = InlineKeyboardMarkup().row(
        InlineKeyboardButton("Offset", callback_data="edit_offset"),
        InlineKeyboardButton("Font size", callback_data="edit_font_size"),
        InlineKeyboardButton("Add pages", callback_data="edit_add_pages"),
    )

    await message.answer(msg1, reply_markup=ReplyKeyboardRemove())
    await message.answer(msg2, reply_markup=inkm)


async def add_pages_callback_handler(callback_q):
    user_id = callback_q.from_user.id

    hnd_ctrl.next_handler(user_id)

    upl_status.start_upload(
        user_id,
        path_join(USER_DATA, user_id, sstorage.get_data(user_id, "editable_project")),
    )

    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(user_id, "Send additional images to add it to the end")


async def edit_offset_callback_handler(callback_q):
    user_id = callback_q.from_user.id

    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(user_id, "Input document offset in mm")


async def offset_input_handler(message):
    user_id = message.chat.id

    text = message.text
    if not text.isdigit() or int(text) < 0:
        await message.answer("Input is not a number or less than 0, try again please")
        return

    path = CONFIG_TEMPLATE.format(
        user_id, sstorage.get_data(user_id, "editable_project")
    )
    set_indent_size(path, int(text))
    hnd_ctrl.complete_pipeline(user_id)

    await message.answer(f"Indent size set to {int(text)} mm, returning back")


async def edit_font_size_callback_handler(callback_q):
    user_id = callback_q.from_user.id
    await bot.answer_callback_query(callback_q.id)

    inkm = InlineKeyboardMarkup().row(
        InlineKeyboardButton("Small", callback_data="set_small_font_size"),
        InlineKeyboardButton("Medium", callback_data="set_medium_font_size"),
        InlineKeyboardButton("Large", callback_data="set_large_font_size"),
    )

    await bot.send_message(user_id, "Choose font size", reply_markup=inkm)


async def small_font_size(callback_q):
    user_id = callback_q.from_user.id
    path = CONFIG_TEMPLATE.format(
        user_id, sstorage.get_data(user_id, "editable_project")
    )
    set_font_size(path, "small")

    hnd_ctrl.complete_pipeline(user_id)

    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(user_id, "Font size changed to small")


async def medium_font_size(callback_q):
    user_id = callback_q.from_user.id
    path = CONFIG_TEMPLATE.format(
        user_id, sstorage.get_data(user_id, "editable_project")
    )
    set_font_size(path, "medium")

    hnd_ctrl.complete_pipeline(user_id)

    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(user_id, "Font size changed to medium")


async def large_font_size(callback_q):
    user_id = callback_q.from_user.id
    path = CONFIG_TEMPLATE.format(
        user_id, sstorage.get_data(user_id, "editable_project")
    )
    set_font_size(path, "large")

    hnd_ctrl.complete_pipeline(user_id)

    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(user_id, "Font size changed to large")
