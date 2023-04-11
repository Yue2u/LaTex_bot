from handlers.handlers_pipeline import HandlersPipeline
from handlers.convert import (
    convert_message,
    handle_albums,
    pictures_handler,
    stop_downloading_handler,
)
from handlers.new_project import np_start, np_title_handler, np_offset_input_handler
from handlers.edit_project import (
    get_project_title,
    offset_input_handler,
)


convert_pipeline = HandlersPipeline(
    "convert",
    (convert_message, (handle_albums, pictures_handler), stop_downloading_handler),
)
new_proj_pipeline = HandlersPipeline(
    "new_proj",
    (
        np_start,
        np_title_handler,
        np_offset_input_handler,
        (handle_albums, pictures_handler),
        stop_downloading_handler,
    ),
)
edit_proj_pipeline = HandlersPipeline(
    "edit_proj",
    (
        get_project_title,
        offset_input_handler,
        (handle_albums, pictures_handler),
        stop_downloading_handler,
    ),
)

pipelines_table = {
    "convert": convert_pipeline,
    "new_proj": new_proj_pipeline,
    "edit_proj": edit_proj_pipeline,
}
