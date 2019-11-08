#Start
import os.path
import numpy as np
import cv2
import json
from flask import Flask,request,Response
import uuid
from flask import Flask

#function detect image
def faceDetect(img):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #convert to grey img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #detect face return face
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    #read size face
    for (x, y, w, h) in faces:
       #draw rectange
       result = cv2.rectangle(img, (x, y), (x + w, y + h), (200, 0, 0), 2)
    #save file image
    path_file=('static/%s.jpg'%uuid.uuid4().hex)
    cv2.imwrite(path_file,result)
    path_file= 'http://127.0.0.1:5000/' + path_file
    return json.dumps(path_file) #return image file name

app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return "Home page"
#API
@app.route('/api/')
def api():
    return 'Hello, this is page API'

#route http post to this method
@app.route('/api/upload',methods=['POST'])
def upload():
    #retrive img from client
    img = cv2.imdecode(np.fromstring(request.files['image'].read(),np.uint8),cv2.IMREAD_UNCHANGED)
    #process img
    result = faceDetect(img)
    #reponse

    return Response(response=result,status=200,mimetype="application/json") #return json string
if __name__ == '__main__':
    app.run()

