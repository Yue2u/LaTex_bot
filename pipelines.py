from handlers.handlers_pipeline import HandlersPipeline
from handlers.convert import (
    convert_message,
    handle_albums,
    pictures_handler,
    stop_downloading_handler,
)
from handlers.new_proj import new_proj_start, new_proj_title_handler


convert_pipeline = HandlersPipeline(
    "convert",
    (convert_message, (handle_albums, pictures_handler), stop_downloading_handler),
)
new_proj_pipeline = HandlersPipeline(
    "new_proj",
    (
        new_proj_start,
        new_proj_title_handler,
        (handle_albums, pictures_handler),
        stop_downloading_handler,
    ),
)

pipelines_table = {"convert": convert_pipeline, "new_proj": new_proj_pipeline}
