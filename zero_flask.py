# !pip install face_recognition

"""ライブラリーのインポート"""

# coding: utf-8
import face_recognition
import cv2
import time
import json
import urllib.parse
import urllib.request
import base64

from flask import Flask,jsonify, request
from flask_cors import CORS

import fingerPrint as fp

app = Flask( __name__ )
CORS(app)

@app.route('/',methods=['post'])
def photo_request():
   
  video_capture = cv2.VideoCapture(0)
  cnt = 5
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
      cnt -= 1

      if (cnt < 0):
        cv2.imwrite("data/tmp.jpg", frame)
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
  f = open("data/tmp.jpg", "rb")
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

@app.route('/fingerprint',methods=['post'])
def finger_print():
  fingerPrint = fp.FingerPrint('/dev/ttyS0', 57600, 1.0, 27)
  listfinger = b''

  #print("1:登録　2:認証")
  selectNum = request.json["fingerFlag"]
  if int(selectNum) == 1:
    fingerPrint.enroll()
    fingerPrint.regModel()
    listfinger = fingerPrint.upImage1()
    b64_finger = base64.b64encode(listfinger).decode('utf-8')
    return jsonify(b64_finger)

  elif int(selectNum) == 2:
    idname = request.json["userId"]
    listfinger = base64.b64decode(request.json["fingerPass"].encode())
    fingerPrint.loginFinger()
    fingerPrint.downLoadImage2(listfinger)
    result = fingerPrint.match()
    if result == 1:
      return jsonify("true")
    elif result == 2:
      return jsonify("false")
    elif result == 100:
      print("認証失敗。もう一度お願い")
    else:
      return jsonify("false")
       
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

