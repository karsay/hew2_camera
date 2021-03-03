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

from camera import Camera
from flask import Flask,jsonify, request,Response, render_template
from flask_cors import CORS

import fingerPrint as fp

app = Flask( __name__ )
CORS(app)

shutter = False
streamFlag = False
frame = "https://jmva.or.jp/wp-content/uploads/2018/07/noimage.png"

@app.route('/',methods=['post'])
def photo_request():
  global shutter
  global frame
  global streamFlag
  
  if streamFlag == True:
    # ウェブカメラへの操作を開放
    video_capture = cv2.VideoCapture(0)
    frame = None
    video_capture.release()
    cv2.destroyAllWindows()
    
  streamFlag = True

  video_capture = cv2.VideoCapture(0)
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
    for (top, right, bottom, left) in face_locations:

      # 圧縮した画像の座標を復元
      top *= 4
      right *= 4
      bottom *= 4
      left *= 4

      # 顔領域に枠を描画
      cv2.rectangle(frame, (left - 50, top - 50), (right + 50, bottom + 50), (0, 255, 0), 2)
    
    # 位置情報の表示
    #if face_locations:
    #  time.sleep(1)
    #  cnt -= 1

    #  if (cnt < 0):
    #    cv2.imwrite("data/tmp.jpg", frame)
    #    break
    
    if face_locations:
      if shutter == True:
        cv2.imwrite("data/tmp.jpg", frame)
        break
    shutter = False
    # 結果をビデオに表示
    #cv2.imshow('Video', frame)

    # ESCキーで終了
    if cv2.waitKey(1) == 27:
      break

  # ウェブカメラへの操作を開放
  video_capture.release()
  cv2.destroyAllWindows()
  streamFlag = False

  # 画像を保存
  f = open("data/tmp.jpg", "rb")
  reqbody = f.read()
  f.close()

  # リクエストフラグで登録、認証分岐
  url = "http://192.168.43.6:5000/{}".format(request.json["reqFlag"])

  req = urllib.request.Request(
    url,
    reqbody,
    method="POST",
    headers={"Content-Type": "application/octet-stream"},
  )

  with urllib.request.urlopen(req) as res:
    return jsonify(json.loads(res.read()))

@app.route('/shutter', methods=['post'])
def shutter_on():
  global shutter
  shutter = True
  return jsonify(True)

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
    b64_finger = base64.b64encode(listfinger).decode('utf-8', 'replace')
    strdata = json.dumps(b64_finger)
    bindata = strdata.encode()
    print(len(bindata))
    if(len(bindata) < 3090):
      return jsonify("error")
    return jsonify(bindata)

  elif int(selectNum) == 2:
    idname = request.json["userId"]
    strrx = request.json["fingerPass"].encode()
    dictrx = json.loads(strrx)
    listfinger = base64.b64decode(dictrx.encode())
    fingerPrint.loginFinger()
    fingerPrint.downLoadImage2(listfinger)
    result = fingerPrint.match()
    if result == 1:
      return jsonify("true")
    elif result == 2:
      return jsonify("false")
    elif result == 100:
      return jsonify("false")
    else:
      return jsonify("false")


def gen():
    global frame
    frame = cv2.imread('./images/Video.png', 0)
    while True:
        frame = cv2.resize(frame, dsize=(935,680))
        ret, v_frame = cv2.imencode('.jpg', frame)

        if v_frame is not None:
            yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + v_frame.tobytes() + b"\r\n")
        else:
            print("frame is none")
            
#def video_feed():
#   return Response(gen(Camera()),
#          mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/video_feed")
def video_feed():
    return Response(gen(),
            mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/stream")
def stream():
    return render_template("stream.html")
       
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

