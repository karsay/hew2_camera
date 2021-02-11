from flask import Flask,jsonify, request
from flask_cors import CORS

import os
import face_recognition
import cv2
import numpy as np
import glob

import config
user_info = config.user_info
threshold = config.threshold

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

@app.route('/')
def index():
  return "hello"

@app.route('/rename', methods=["POST"])
def rename():
  path1 = 'images/tmp.jpg'
  path2 = 'images/{}.jpg'.format(request.json["userId"])
  os.rename(path1, path2)
  return "true"

@app.route('/registration', methods=["POST"])
def registration():
  # 画像名変更
  path1 = 'images/tmp.jpg'
  path2 = 'images/{}.jpg'.format(request.json["userId"])
  os.rename(path1, path2)

  # 受信画像のエンコード
  _bytes = np.frombuffer(request.data, np.uint8)
  img = cv2.imdecode(_bytes, flags=cv2.IMREAD_COLOR)
  cv2.imwrite("images/tmp.jpg", img)

  file = open('config.py', 'w')
  file.write("user_info['{}'] = '{}'".format(request.json["userId"], request.json["fingerPass"]))
  file.close()
  return "true"

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

  for face_encoding in face_encodings:
    # 顔が登録済みの顔と一致するか確認
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, threshold)
    # カメラ画像と最も近い登録画像を見つける
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
      name = known_face_names[best_match_index]
    else:
      name = "error"

  return jsonify(name)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
