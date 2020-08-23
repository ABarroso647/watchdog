import cv2
import os
import time
import random
from google.cloud import storage
from flask import Flask, jsonify
from flask import request


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    try:
        fileloc = os.path.dirname(os.path.abspath(__file__)) + "/key.json"
        print(os.path.dirname(os.path.abspath(__file__)))
        storage_client = storage.Client.from_service_account_json(fileloc)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        #blob.delete()
        print(
            "Blob {} downloaded to {}.".format(
                source_blob_name, destination_file_name
            )
        )
        return True
    except:
        return False

def point_system (value):
    activity_map = ['Safe driving',
                    'Texting - right',
                    'Talking on the phone - right',
                    'Texting - left',
                    'Talking on the phone - left',
                    'Operating the radio',
                    'Drinking',
                    'Reaching behind',
                    'Hair and makeup',
                    'Talking to passenger']
    classification = 0
    for i in range(len(activity_map)):
        if i == value:
            classification = i
    if classification > 0 and classification <= 4:
        return 20
    if (classification > 4 and classification <= 7) or classification == 9:
        return 100
    if classification == 8:
        return 70
    else:
        return 200


def sequence(data):
    folderpath = os.path.dirname(os.path.abspath(__file__))
    new_path = folderpath + data.decode("utf-8")
    bucket_name = "watchdog_image_bucket-123"
    if download_blob(bucket_name, data, new_path):
        cap = cv2.VideoCapture(new_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        framecount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        score = 0
        i = 0
        inc = 0
        if(framecount< fps*5):
            score = -1
        while i <= (framecount - fps *5) and cap.isOpened():
            success, image = cap.read()
            if success and (int(i % (2 * fps)) == 0):
                imgpath = folderpath + "/images/frame.jpg"
                image = cv2.resize(image, (640, 480))
                cv2.imwrite(imgpath, image)
                time.sleep(0.25)  # call the ml here and ge tits response
                random_bool = random.getrandbits(9)
                score += point_system(random_bool)
                os.remove(imgpath)
                inc += 1
            i += 1
        score /= inc
        score = int(score%100)
        return str(score)
    return "-1"

app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
    data = request.data
    print(type(data))
    score = sequence(data)
    return score


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
