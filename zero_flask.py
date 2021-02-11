# !pip install face_recognition

"""ライブラリーのインポート"""

# -*- coding: utf-8 -*-
import face_recognition
import cv2
import time
import json
import urllib.parse
import urllib.request

from flask import Flask,jsonify, request
from flask_cors import CORS

app = Flask( __name__ )
CORS(app)

@app.route('/',methods=['post'])
def photo_request():
   
  video_capture = cv2.VideoCapture(0)
  user_id = request.json["userId"]

  cnt = 3
  # 処理フラグ初期化
  process_this_frame = True

  while True:
    # ビデオの単一フレームを取得
    _, frame = video_capture.read()

    # 　フレーム毎に処理をスキップ
    if process_this_frame:
      # 画像を縦1/4　横1/4に圧縮
      small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

      # ビデオの現在のフレーム内のすべての顔に対してその位置情報を検索
      face_locations = face_recognition.face_locations(small_frame)

    # 　処理フラグの切り替え
    process_this_frame = not process_this_frame

    # 位置情報の表示
    if face_locations:
      time.sleep(1)
      cv2.putText(frame, str(cnt), (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 5, (0,255,0), 5, cv2.LINE_AA)
      cnt -= 1

      if (cnt < 0):
        cv2.imwrite("data/{}.jpg".format(user_id), frame)
        break

    # 結果をビデオに表示
    cv2.imshow('Video', frame)

    # ESCキーで終了
    if cv2.waitKey(1) == 27:
      break

  # ウェブカメラへの操作を開放
  video_capture.release()
  cv2.destroyAllWindows()

  # 画像を保存
  f = open("data/face.jpg", "rb")
  reqbody = f.read()
  f.close()

  # リクエストフラグで登録、認証分岐
  url = "http://192.168.0.14:5000/{}".format(request.json["reqFlag"])

  req = urllib.request.Request(
    url,
    reqbody,
    method="POST",
    headers={"Content-Type": "application/octet-stream"},
  )

  with urllib.request.urlopen(req) as res:
    return jsonify(json.loads(res.read()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

