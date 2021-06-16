import requests
import logging
import numpy as np
import cv2
from settings import HEADERS, OPEN_URL, VIDEO_URL, CERTIFI


def open_door():    # функция открытия двери
    result = requests.post(f'{OPEN_URL}', headers=HEADERS, json={"door": "left_door", "id": "7361"}, verify=CERTIFI)
    if result.status_code != 200:
        logging.error(f"Failed to open the door with status code {result.status_code}")
        print('nope')
        return False
    logging.warning(f"Door opened successfully in {result.elapsed.total_seconds()}sec")
    print('yep')
    return True


def get_video_url():     # функция получения видео-потока с камеры
    result = requests.get(VIDEO_URL, headers=HEADERS, verify=CERTIFI, stream=True)
    if result.status_code != 200:
        logging.error(f"Failed to get stream link with status code {result.status_code}")
        return False
    logging.warning(f"Stream link received successfully in {result.elapsed.total_seconds()}sec")
    video_url = result.json()['video'][0]["source"]
    return video_url


if __name__ == "__main__":
    pass
