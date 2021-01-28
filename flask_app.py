from flask import Flask,jsonify
from flask_cors import CORS

import os
import face_recognition
import cv2
import numpy as np
import glob

import config
emp_info = config.emp_info
threshold = config.threshold
mode = config.mode

"""顔情報の初期化"""

face_locations = []
face_encodings = []

"""登録画像の読み込み"""

image_paths = glob.glob('images/*')
image_paths.sort()
known_face_encodings = []
known_face_names = []
checked_face = []

for image_path in image_paths:
    # im_name = image_path.split(delimiter)[-1].split('.')[0]
    im_name = os.path.basename(image_path).split('.')[0]    # os.path.basename ファイル名の取得
    image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(face_encoding)
    known_face_names.append(im_name)

app = Flask( __name__ )
CORS(app)

@app.route('/') 
def index():
    video_capture = cv2.VideoCapture(0)
    #処理フラグ初期化
    process_this_frame = True
    while True:
        # ビデオの単一フレームを取得
        _, frame = video_capture.read()
        #　フレーム毎に処理をスキップ
        if process_this_frame:
            #画像を縦1/4　横1/4に圧縮
            small_frame = cv2.resize(frame, (0, 0),fx=0.25, fy=0.25)
            
            # ビデオの現在のフレーム内のすべての顔に対してその位置情報を検索
            face_locations = face_recognition.face_locations(small_frame)
            # 顔の位置情報からエンコードを生成
            face_encodings = face_recognition.face_encodings(small_frame, face_locations)
            
            for face_encoding in face_encodings:
                # 顔が登録済みの顔と一致するか確認
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, threshold)
                name = "Unknown"
                # カメラ画像と最も近い登録画像を見つける
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

        #　処理フラグの切り替え
        process_this_frame = not process_this_frame

        # 位置情報の表示
        for (top, right, bottom, left) in face_locations:
            # 圧縮した画像の座標を復元
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            # 顔領域に枠を描画
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # 枠の下に名前を表示
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
            # 本人確認
            if mode == 1 and name != "Unknown":
                # ウェブカメラへの操作を開放
                video_capture.release()
                cv2.destroyAllWindows()
                return jsonify({
                    "user":name,
                    "pass":emp_info[name]
                    })

        # 結果をビデオに表示
        cv2.imshow('Video', frame)

        # ESCキーで終了
        if cv2.waitKey(1) == 27:
            break

    # ウェブカメラへの操作を開放
    video_capture.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

