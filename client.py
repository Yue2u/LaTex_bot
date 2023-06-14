from create_bot import client
import base64
from utils import path_join
import json
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

    async with client.post(url + '/process', data=data, headers={"ngrok-skip-browser-warning": "1"}) as resp:
        if resp.status != 200:
            raise ValueError("Something went wrong. Try later")
        text = await resp.text()
        return json.loads(text)
