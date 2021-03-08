from flask import Flask, jsonify, request, Response
from flask_cors import CORS

import os
import face_recognition
import cv2
import numpy as np
import glob

import requests
import base64
import hashlib


import time

import config
user_info = config.user_info
threshold = config.threshold

import images

import random

"""顔情報の初期化"""

face_locations = []
face_encodings = []

"""登録画像の読み込み"""

image_paths = glob.glob('images/*')
image_paths.sort()
known_face_encodings = []
known_face_names = []
checked_face = []

app = Flask(__name__)
CORS(app)

app.register_blueprint(images.app)

@app.route('/')
def index():
  return "hello"

@app.route('/create_icon', methods=["POST"])
def create_icon():
  data = open('tests/00.jpg', 'rb')

  styles = ['https://video-images.vice.com/_uncategorized/1554346499928-02.jpeg',
            'https://casie.jp/media/wp-content/uploads/2020/09/Van_Gogh_Self-Portrait_with_Straw_Hat_1887-Detroit.jpg',
            'https://auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0105/users/ff8558e1fe2b4810b6f62ca52a22e93fb5949a71/i-img900x1200-1590300556xwpbcw11877.jpg',
            'https://www.artbank.co.jp/stockillust/vol8_image/visualgenerallaboratory/1-S-CHD107.jpg',
            'https://images-na.ssl-images-amazon.com/images/I/619cmE%2B4EUL._AC_.jpg',
            'https://pbs.twimg.com/profile_images/1065419302256275456/y1oe1dOQ.jpg'
            ]

  r = requests.post(
    "https://api.deepai.org/api/CNNMRF",
    data={
      'content': base64.b64encode(data.read()),
      'style': random.choice(styles),
    },
    headers={'api-key': 'ca6dafe3-27ec-4ed0-9c87-b11380bb396c'}
  )

  response = requests.get(r.json()['output_url'])
  image = response.content

  file_name = "icons/" + hashlib.md5(image).hexdigest() + ".jpg"

  with open(file_name, "wb") as aaa:
    aaa.write(image)

@app.route('/authenticationregistration', methods=["POST"])
def authentication_registration():
  path1 = 'images/tmp.jpg'
  path2 = 'images/{}.jpg'.format(request.json["userId"])
  os.rename(path1, path2)

  file = open('config.py', 'a')
  file.write("user_info['{}'] = '{}'\r\n".format(request.json["userId"], request.json["fingerPass"]))
  file.close()
  return "true"

@app.route('/registration', methods=["POST"])
def registration():
  # 受信画像のエンコード
  _bytes = np.frombuffer(request.data, np.uint8)
  img = cv2.imdecode(_bytes, flags=cv2.IMREAD_COLOR)
  cv2.imwrite("images/tmp.jpg", img)
  return "true"

@app.route('/hello-world')
def hello_world():
    comments = [
        'Hello',
        'Flask',
        'Stream',
        'Server!',
    ]
    def generate():
        cnt = 0
        for comment in comments:
            yield '<li>' + comment + '</li>'
            time.sleep(0.5)  # 動作をわかりやすくするために追加
            cnt += 1
            if cnt == 3:
                yield '<li>' + 'finish!!' + '</li>'
                break
        return Response(generate())

@app.route('/authentication', methods=["POST"])
def authentication():
  for image_path in image_paths:
    im_name = os.path.basename(image_path).split('.')[0]  # os.path.basename ファイル名の取得
    image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(face_encoding)
    known_face_names.append(im_name)

  _bytes = np.frombuffer(request.data, np.uint8)
  # decode the bytes to image directly
  img = cv2.imdecode(_bytes, flags=cv2.IMREAD_COLOR)
  # ビデオの現在のフレーム内のすべての顔に対してその位置情報を検索
  face_locations = face_recognition.face_locations(img)
  # 顔の位置情報からエンコードを生成
  face_encodings = face_recognition.face_encodings(img, face_locations)

  name = ""
  password = ""

  for face_encoding in face_encodings:
    # 顔が登録済みの顔と一致するか確認
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, threshold)
    # カメラ画像と最も近い登録画像を見つける
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
      name = known_face_names[best_match_index]
      password = user_info[name]
    else:
      name = "error"
      password = ""

  return jsonify(name, password)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=False)
