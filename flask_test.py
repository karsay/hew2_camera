from flask import Flask,jsonify
from flask_cors import CORS

import os
import face_recognition
import cv2
import numpy as np
import glob
"""顔情報の初期化"""

face_locations = []
face_encodings = []

"""登録画像の読み込み"""

app = Flask( __name__ )
CORS(app)

@app.route('/') 
def index():
    video_capture = cv2.VideoCapture(0)
    while True:
        # ビデオの単一フレームを取得
        _, frame = video_capture.read()

        # 結果をビデオに表示
        cv2.imshow('Video', frame)

        # ESCキーで終了
        if cv2.waitKey(1) == 27:
            break
        
    # ウェブカメラへの操作を開放
    video_capture.release()
    cv2.destroyAllWindows()    


    
def return_user(name):
    
    return jsonify({
    "user":"karsay",
    "pass":"0001"
    })
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
