import cv2
import numpy as np
import time
import glob

video_capture = cv2.VideoCapture(0)
facecascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

facedict = {}
emotions = ["angry", "happy", "sad", "neutral"]

def crop_face(clahe_image, face):
    for (x, y, w, h) in face:
        faceslice = clahe_image[y:y+h, x:x+w]
        faceslice = cv2.resize(faceslice, (350, 350))
    facedict["face%s" %(len(facedict)+1)] = faceslice
    return faceslice

def update_model(emotions):
    for i in range(0, len(emotions)):
        save_face(emotions[i])
        facedict.clear()
    print("collected images, looking good!")

def save_face(emotion):
    print("\n\nplease look " + emotion.upper() + " when the timer expires and keep the expression stable until instructed otherwise.")
    for i in range(0,5):
        print(5-i)
        time.sleep(1)
    
    while True:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        clahe_image = clahe.apply(gray)
        face = facecascade.detectMultiScale(clahe_image, scaleFactor=1.1, minNeighbors=15, minSize=(10,10),flags=cv2.CASCADE_SCALE_IMAGE)
        for (x, y, w, h) in face: 
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2) 
        cv2.imshow("webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if len(face) == 1: 
            if len(facedict.keys()) < 11:
                faceslice = crop_face(clahe_image, face)
        else:
            print("no/multiple faces detected, passing over frame")
   
        if len(facedict.keys()) == 10:
            print("Image captured!")
            for x in facedict.keys(): 
                cv2.imwrite("class_dataset\\%s\\%s.jpg" %(emotion, len(glob.glob("class_dataset\\%s\\*" %emotion))),facedict[x])
            

update_model(emotions)