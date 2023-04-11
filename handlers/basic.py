from create_bot import hnd_ctrl
from aiogram import types
from .convert import handle_albums
from .list_projects import list_projects_handler, register_callback_handlers
from .edit_project import register_edit_proj_callback_handlers
from .new_project import register_new_proj_callback_handlers


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
    msg += "This bot can transform your picture conspetcs into LaTex docs and store them\n"
    msg += "Type /convert to make temporary project\n"
    msg += "Type /new_project to create titled project and handle its options\n"
    msg += "Type /show_projects to look at projects you created"
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


async def none_pipeline_handler(message):
    await message.answer("Type /help to know what i can do!")


async def convert_pipeline_handler(message):
    user_id = message.chat.id

    if message.text == "/stop":
        hnd_ctrl.next_handler(user_id)
        handler = hnd_ctrl.get_handler(user_id)
        hnd_ctrl.complete_pipeline(user_id)
        await handler(message)
        return
    mgr_handler, picture_handler = hnd_ctrl.get_handler(user_id)
    if message.photo:
        await picture_handler(message)


async def new_proj_pipeline_handler(message):
    user_id = message.chat.id

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


async def edit_proj_pipeline_handler(message):
    user_id = message.chat.id

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


async def basic_handler(message):
    user_id = message.chat.id
    pipeline_type = hnd_ctrl.get_handler_type(user_id)

    pipeline_dict = {
        None: none_pipeline_handler,
        "convert": convert_pipeline_handler,
        "new_proj": new_proj_pipeline_handler,
        "edit_proj": edit_proj_pipeline_handler
    }

    await pipeline_dict[pipeline_type](message)
