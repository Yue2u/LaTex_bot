from create_bot import client
import base64
from utils import path_join
import json
from utils import basement, create_folder, path_join, files_in_dir
import os


def base64_encode(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


async def recognize(images_path, url):
    encoded_images = {}

    for idx, image in enumerate(os.listdir(images_path)):
        encoded = base64_encode(path_join(images_path, image))
        encoded_images[idx] = encoded

    data = json.dumps(encoded_images, indent=4, ensure_ascii=False)
    async with client.post(
        url + "/process", data=data, headers={"ngrok-skip-browser-warning": "1"}
    ) as resp:
        if resp.status != 200:
            raise ValueError("Something went wrong. Try later")
        text = await resp.text()
        text = text[1:-1].replace("\\", "")
        tokens = json.loads(text)

        result = []
        for item in tokens["data"]:
            t, data = item["type"], item["data"]
            if t != 2:
                result.append((data, t))
            else:
                proj_path = basement(images_path)
                create_folder(path_join(proj_path, "images_in_use"))
                files_amount = files_in_dir(path_join(proj_path, "images_in_use"))
                with open(
                    path_join(proj_path, "images_in_use", f"img{files_amount}.png"),
                    "wb",
                ) as f:
                    f.write(base64.b64decode(data.encode("utf-8")))
                result.append(
                    (path_join(proj_path, "images_in_use", f"img{files_amount}.png"), t)
                )
        return result
