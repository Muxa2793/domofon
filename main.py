import requests
import logging
import numpy as np
import cv2
from settings import HEADERS, OPEN_URL, VIDEO_URL


def open_door():
    result = requests.post(f'{OPEN_URL}', headers=HEADERS, json={"door": "left_door", "id": "7361"}, verify=False)
    if result.status_code != 200:
        logging.error(f"Failed to open the door with status code {result.status_code}")
        print('nope')
        return False
    logging.warning(f"Door opened successfully in {result.elapsed.total_seconds()}sec")
    print('yep')
    return True


def get_video():
    result = requests.get(VIDEO_URL, headers=HEADERS, verify=False, stream=True)
    if result.status_code != 200:
        logging.error(f"Failed to get stream link with status code {result.status_code}")
        return False
    logging.warning(f"Stream link received successfully in {result.elapsed.total_seconds()}sec")
    video_url = result.json()['video'][0]["source"]
    cap = cv2.VideoCapture(video_url)
    while(True):
        ret, frame = cap.read()
        cv2.imshow('Stream IP camera opencv', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    get_video()
