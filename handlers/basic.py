from create_bot import hnd_ctrl
from aiogram import types
from .convert import handle_albums
from .list_projects import list_projects_handler, register_callback_handlers
from .edit_project import register_edit_proj_callback_handlers
from .new_proj import register_new_proj_callback_handlers


def register_basic_handlers(dp):
    dp.register_message_handler(start_message, commands=["start", "help"])
    dp.register_message_handler(convert_handler, commands=["convert"])
    dp.register_message_handler(new_proj_handler, commands=["new_project"])
    dp.register_message_handler(show_projects, commands=["show_projects"])
    dp.register_message_handler(
        handle_albums, is_media_group=True, content_types=[types.ContentType.ANY]
    )
    dp.register_message_handler(basic_handler, content_types=[types.ContentType.ANY])

    register_callback_handlers(dp)
    register_edit_proj_callback_handlers(dp)
    register_new_proj_callback_handlers(dp)


async def start_message(message):
    msg = "Hi!\n"
    msg += "This bot can transform your picture conspetcs into LaTex docs\n"
    msg += "Just type /convert to start"
    await message.answer(msg)


async def convert_handler(message):
    user_id = message.chat.id

    hnd_ctrl.set_pipeline(user_id, "convert")
    handler = hnd_ctrl.get_handler(user_id)
    hnd_ctrl.next_handler(user_id)

    await handler(message)


async def show_projects(message):
    await list_projects_handler(message)


async def new_proj_handler(message):
    user_id = message.chat.id

    hnd_ctrl.set_pipeline(user_id, "new_proj")
    handler = hnd_ctrl.get_handler(user_id)
    hnd_ctrl.next_handler(user_id)

    await handler(message)


async def basic_handler(message):  # TODO: put handling of every pipeline to function
    user_id = message.chat.id

    if hnd_ctrl.get_handler_type(user_id) is None:
        await message.answer("Type /help to know what i can do!")
        return

    if hnd_ctrl.get_handler_type(user_id) == "convert":
        if message.text == "/stop":
            hnd_ctrl.next_handler(user_id)
            handler = hnd_ctrl.get_handler(user_id)
            hnd_ctrl.complete_pipeline(user_id)
            await handler(message)
            return
        mgr_handler, picture_handler = hnd_ctrl.get_handler(user_id)
        if message.photo:
            await picture_handler(message)
        return

    if hnd_ctrl.get_handler_type(user_id) == "new_proj":
        if message.text == "/stop":
            hnd_ctrl.next_handler(user_id)
            handler = hnd_ctrl.get_handler(user_id)
            hnd_ctrl.complete_pipeline(user_id)
            await handler(message)
            return
        handler = hnd_ctrl.get_handler(user_id)
        if isinstance(handler, tuple):
            if message.photo:
                await handler[1](message)
        else:
            hnd_ctrl.next_handler(user_id)
            await handler(message)

    if hnd_ctrl.get_handler_type(user_id) == "edit_proj":
        if message.text == "/stop":
            hnd_ctrl.next_handler(user_id)
            handler = hnd_ctrl.get_handler(user_id)
            hnd_ctrl.complete_pipeline(user_id)
            await handler(message)
            return
        handler = hnd_ctrl.get_handler(user_id)
        if isinstance(handler, tuple):
            if message.photo:
                handler = handler[1]
                await handler(message)
        else:
            hnd_ctrl.next_handler(user_id)
            await handler(message)
