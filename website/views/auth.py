from flask import Blueprint, render_template
import cv2
import face_recognition
import numpy as np
import os
from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
from PIL import Image
import base64
import io

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return render_template("common/login.html")


@auth.route("/logout")
def logout():
    return "<h1>Logout<h1/>"


@auth.route("/register")
def register():
    return "<h1>Register<h1/>"

@auth.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@auth.route('/video')
def index():
    return render_template('common/video.html')

def gen_frames():  # Generator function for video streaming
    camera = cv2.VideoCapture(0)  # Access webcam
    while True:
        success, frame = camera.read() 
        if not success:
            break

        ret, buffer = cv2.imencode('.jpg', frame)  
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@auth.route('/process_encoding', methods=["POST"])
def process_encodings():
    data = request.get_json()
    
    nparr = np.frombuffer(base64.b64decode(data['imageData']), np.uint8)

    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    known_faces_encoding = load_known_encodings()
    result = {}
    for face_encoding in face_encodings:
        #known_image = face_recognition.load_image_file(imagePath)
        #encoding = face_recognition.face_encodings(known_image)[0]

        matches = face_recognition.compare_faces(known_faces_encoding, face_encoding)
      
        if True in matches:
            result = {'match' : True in matches}
            break
   
        

    return jsonify(result) 

def load_known_encodings():
    face_encodings = [];

    folder_path = os.getcwd()+'/storedImages/'
    print("OS: " + os.getcwd())

    for filename in os.listdir(folder_path):
        supported_extensions = ('.jpg', '.jpeg', '.png')  # Add more if needed
        for filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, filename)

            try:
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)[0]
                #print(image)
                face_encodings.append(encodings);
            except (IOError, SyntaxError) as e:
                print(f"Invalid image: {image_path}")       

    return face_encodings     