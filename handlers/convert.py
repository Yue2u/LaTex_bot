from aiogram import types
from utils import (
    files_in_dir,
    get_ext,
    path_join,
    create_folder,
    recreate_folder,
    basement,
    suffix,
)
from json_config import init_project_config
from tex_to_pdf import make_pdf
from create_bot import bot, upl_status, USER_DATA
from text_to_tex import add_section, build_document


def register_convert_handlers(dp):
    dp.register_message_handler(stop_downloading_handler, commands=["stop"])
    dp.register_message_handler(convert_message, commands=["convert"])
    dp.register_message_handler(
        handle_albums, is_media_group=True, content_types=[types.ContentType.ANY]
    )
    dp.register_message_handler(
        pictures_handler,
        content_types=[types.ContentType.PHOTO, types.ContentType.DOCUMENT],
    )


async def convert_message(message: types.Message):
    user_id = message.chat.id
    upl_status.start_upload(user_id, path_join(USER_DATA, user_id, "tmp"))

    recreate_folder(path_join(upl_status.get_path(user_id), "images"))
    init_project_config(
        path_join(upl_status.get_path(message.chat.id), "jsons", "config.json")
    )

    msg = "Send pictures of conspect in right order, please.\n"
    msg += "Type /stop to stop uploading files"
    print("Started uploading pictures...")
    await message.answer(msg)


def convert_text_to_pdf(user_id):
    # TODO: define text file place
    paragraphs = []
    title = ""
    proj_name = suffix(upl_status.get_path())

    add_section(user_id, proj_name, title, paragraphs)

    build_document(user_id, proj_name)


async def stop_downloading_handler(message):  # TODO: make convertation
    upl_status.stop_upload(message.chat.id)

    msg = "Stopped saving conspect pictures\n"
    msg += f"Uploaded {upl_status.uploads_count(message.chat.id)} pictures"
    await message.answer(msg)
    await message.answer("Converting...")

    # convert_text_to_pdf(message.chat.id)


async def save_files(files_id, user_id, path):
    create_folder(path)
    start_point = 1 + files_in_dir(path)

    for n, file_id in enumerate(files_id, start_point):
        file = await bot.get_file(file_id)
        ext = get_ext(file.file_path)
        await bot.download_file(file.file_path, path_join(path, f"{n}.{ext}"))
    upl_status.add_uploads(user_id, len(files_id))


async def handle_albums(message: types.Message, album):
    """This handler will receive a complete album of any type."""
    if not upl_status.is_uploading(message.chat.id):
        return

    print("Started saving album...")

    files_id = []
    media_group = types.MediaGroup()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            # We can also add a caption by specifying `"caption":"text"`
            media_group.attach({"media": file_id, "type": obj.content_type})
            files_id.append(file_id)
        except ValueError:
            return await message.answer(
                "This type of album is not supported by aiogram."
            )
    user_id = message.chat.id
    await save_files(
        files_id, user_id, path_join(upl_status.get_path(user_id), "images")
    )


async def pictures_handler(message):
    if not upl_status.is_uploading(message.chat.id):
        return
    photo = message.photo[-1] if message.photo else message.document
    print("Started saving...")
    user_id = message.chat.id
    await save_files(
        [photo.file_id], user_id, path_join(upl_status.get_path(user_id), "images")
    )
