from create_bot import bot, hnd_ctrl, upl_status, sstorage, CONFIG_TEMPLATE, USER_DATA
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from json_config import set_font_size, set_indent_size
from text_to_tex import delete_section, build_document
from compress_zip import make_zip
from overleaf_upload import upload
from utils import path_join, list_articles, extract_proj_name


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
        delete_article_callback_handler, lambda c: c.data == "edit_del_article"
    )
    dp.register_callback_query_handler(
        get_source_callback_handler, lambda c: c.data == "edit_get_source"
    )
    dp.register_callback_query_handler(
        upload_overleaf_callback_handler, lambda c: c.data == "edit_upload_overleaf"
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


async def is_working(user_id, callback_q):
    if not hnd_ctrl.is_pipelining(user_id):
        await bot.answer_callback_query(callback_q.id)
        await bot.send_message(user_id, "There isn't any project in work now")
        return False
    return True


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

    msg1 = f"Start managing project '{message.text}'\n"
    msg2 = "Choose option to edit"

    inkm = (
        InlineKeyboardMarkup()
        .row(
            InlineKeyboardButton("Offset", callback_data="edit_offset"),
            InlineKeyboardButton("Font size", callback_data="edit_font_size"),
        )
        .row(
            InlineKeyboardButton("Add pages", callback_data="edit_add_pages"),
            InlineKeyboardButton("Delete article", callback_data="edit_del_article"),
        )
        .row(
            InlineKeyboardButton("Get source code", callback_data="edit_get_source"),
            InlineKeyboardButton("Upload to overleaf", callback_data="edit_upload_overleaf")
        )
    )

    await message.answer(msg1, reply_markup=ReplyKeyboardRemove())
    await message.answer(msg2, reply_markup=inkm)


async def add_pages_callback_handler(callback_q):
    user_id = callback_q.from_user.id

    if not await is_working(user_id, callback_q):
        return

    hnd_ctrl.next_handler(user_id)
    hnd_ctrl.next_handler(user_id)
    hnd_ctrl.next_handler(user_id)

    upl_status.start_upload(
        user_id,
        path_join(USER_DATA, user_id, sstorage.get_data(user_id, "editable_project")),
    )

    msg = "Send additional images to add it to the end\n"
    msg += "Type /stop to stop uploading files"

    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(user_id, msg)


async def delete_article_callback_handler(callback_q):
    user_id = callback_q.from_user.id

    if not await is_working(user_id, callback_q):
        return

    hnd_ctrl.next_handler(user_id)

    msg = "Choose title to delete from the list below:\n"

    path = CONFIG_TEMPLATE.format(
        user_id, sstorage.get_data(user_id, "editable_project")
    )

    articles = list_articles(path)
    sstorage.set_data(user_id, "articles_list", articles)
    msg += "\n".join([f'"{art}"' for art in articles])

    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(user_id, msg)


async def delete_article_handler(message):
    user_id = message.chat.id
    articles_list = sstorage.get_data(user_id, "articles_list")

    if message.text not in articles_list:
        hnd_ctrl.complete_pipeline(user_id)
        await message.answer(f'There is no article "{message.text}", try again')
        return

    proj_name = sstorage.get_data(user_id, "editable_project")

    delete_section(
        user_id, sstorage.get_data(user_id, "editable_project"), message.text
    )
    build_document(user_id, sstorage.get_data(user_id, "editable_project"))
    hnd_ctrl.complete_pipeline(user_id)

    await message.answer(
        f'Article "{message.text}" successfully deleted\nSending file...'
    )
    await message.answer_document(
        open(path_join(USER_DATA, user_id, proj_name, proj_name + ".pdf"), "rb")
    )


async def get_source_callback_handler(callback_q):
    user_id = callback_q.from_user.id

    if not await is_working(user_id, callback_q):
        return

    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(user_id, "Making zip of source files...")
    zip_path = make_zip(user_id, sstorage.get_data(user_id, "editable_project"))
    await bot.send_document(user_id, open(zip_path, "rb"))


async def upload_overleaf_callback_handler(callback_q):
    user_id = callback_q.from_user.id

    if not await is_working(user_id, callback_q):
        return

    hnd_ctrl.next_handler(user_id)
    hnd_ctrl.next_handler(user_id)

    await bot.answer_callback_query(callback_q.id)
    msg = 'Enter your overleaf email and password (we don\'t save it anywhere) in next format:\n'
    msg += '"email password" (email whitespace password)'
    await bot.send_message(user_id, msg)


async def overleaf_login_handler(message):
    user_id = message.chat.id

    data = message.text.split(' ')
    if len(data) != 2:
        hnd_ctrl.complete_pipeline(user_id)
        await message.answer("Wrong format. Try again")
        return

    email, password = data

    make_zip(user_id, sstorage.get_data(user_id, "editable_project"))
    try:
        upload(email, password, user_id, sstorage.get_data(user_id, "editable_project"))
    except Exception as ex:
        print(ex)
        hnd_ctrl.complete_pipeline(user_id)
        await message.answer("Something went wrong...\nTry again later.")
        return

    hnd_ctrl.complete_pipeline(user_id)
    await message.answer("Your project was successfully uploaded to overleaf!")


async def edit_offset_callback_handler(callback_q):
    user_id = callback_q.from_user.id

    if not await is_working(user_id, callback_q):
        return

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

    if not await is_working(user_id, callback_q):
        return

    await bot.answer_callback_query(callback_q.id)

    inkm = InlineKeyboardMarkup().row(
        InlineKeyboardButton("Small", callback_data="set_small_font_size"),
        InlineKeyboardButton("Medium", callback_data="set_medium_font_size"),
        InlineKeyboardButton("Large", callback_data="set_large_font_size"),
    )

    await bot.send_message(user_id, "Choose font size", reply_markup=inkm)


async def small_font_size(callback_q):
    user_id = callback_q.from_user.id

    if not await is_working(user_id, callback_q):
        return

    path = CONFIG_TEMPLATE.format(
        user_id, sstorage.get_data(user_id, "editable_project")
    )
    set_font_size(path, "small")

    hnd_ctrl.complete_pipeline(user_id)

    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(user_id, "Font size changed to small")


async def medium_font_size(callback_q):
    user_id = callback_q.from_user.id

    if not await is_working(user_id, callback_q):
        return

    path = CONFIG_TEMPLATE.format(
        user_id, sstorage.get_data(user_id, "editable_project")
    )
    set_font_size(path, "medium")

    hnd_ctrl.complete_pipeline(user_id)

    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(user_id, "Font size changed to medium")


async def large_font_size(callback_q):
    user_id = callback_q.from_user.id

    if not await is_working(user_id, callback_q):
        return

    path = CONFIG_TEMPLATE.format(
        user_id, sstorage.get_data(user_id, "editable_project")
    )
    set_font_size(path, "large")

    hnd_ctrl.complete_pipeline(user_id)

    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(user_id, "Font size changed to large")
