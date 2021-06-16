import cv2
import time
import numpy as np
import os
from main import get_video_url, open_door


def get_video():
    video_url = get_video_url()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('couch/trainer.yml')
    faceCascade = cv2.CascadeClassifier('/Users/dreadnote/Projects/domofon/env/lib/python3.8/site-packages/cv2/data/'
                                        'haarcascade_frontalface_alt2.xml')
    font = cv2.FONT_HERSHEY_SIMPLEX

    # iniciate id counter
    id = 0

    # names related to ids: example ==> Mikhail: id=1,  etc
    names = ['None', 'Mikhail', 'Adelina']

    cap = cv2.VideoCapture(video_url)
    cap.set(3, 640)  # set Width
    cap.set(4, 480)  # set Height

    # Define min window size to be recognized as a face
    minW = 0.1*cap.get(3)
    minH = 0.1*cap.get(4)

    while(True):
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
                                            gray,
                                            scaleFactor=1.2,
                                            minNeighbors=5,
                                            minSize=(int(minW), int(minH)))
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            if (confidence < 100):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
            elif (40 < confidence < 100):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
                open_door()
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            cv2.putText(img, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x+5, y+h-5), font, 1, (255, 255, 0), 1)

        cv2.imshow('video', img)
        # time.sleep(0.3)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return True


if __name__ == "__main__":
    get_video()
