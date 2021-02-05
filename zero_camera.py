# !pip install face_recognition

"""ライブラリーのインポート"""

# -*- coding: utf-8 -*-
import face_recognition
import cv2
import time
import json
import urllib.parse
import urllib.request

"""登録画像の読み込み"""
video_capture = cv2.VideoCapture(0)

def main():
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
      # top = face_locations[0][0] * 4
      # right = face_locations[0][1] * 4
      # bottom = face_locations[0][2] * 4
      # left = face_locations[0][3] * 4
      # # 顔領域に枠を描画
      # face = frame[top - 200:bottom + 50, left - 100:right + 100]
      # if(face.all):
      cv2.putText(frame, str(cnt), (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 5, (0,255,0), 5, cv2.LINE_AA)
      cnt -= 1

      if (cnt < 0):
        cv2.imwrite("data/face.jpg", frame)
        break

    # 結果をビデオに表示
    cv2.imshow('Video', frame)

    # ESCキーで終了
    if cv2.waitKey(1) == 27:
      break

  # read image data
  f = open("data/face.jpg", "rb")
  reqbody = f.read()
  f.close()

  # create request with urllib
  url = "http://localhost:5000/authentication"
  req = urllib.request.Request(
    url,
    reqbody,
    method="POST",
    headers={"Content-Type": "application/octet-stream"},
  )

  # send the request and print response
  with urllib.request.urlopen(req) as res:
    print(json.loads(res.read()))

main()

# ウェブカメラへの操作を開放
video_capture.release()
cv2.destroyAllWindows()
