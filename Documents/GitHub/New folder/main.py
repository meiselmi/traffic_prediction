import cv2
import numpy as np
import face_recognition
import os
from email.message import EmailMessage
import ssl
import smtplib

path='images'
img=[]
classNames=[]
mylist=os.listdir(path)
print(mylist)
for cl in mylist:
    curImg=cv2.imread(f'{path}/{cl}')
    img.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
encodeListeKnown= findEncodings(img)
print('encoding done')

cap=cv2.VideoCapture(0)

while True:
    success,img= cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    facesCurFrame= face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceloc in zip(encodeCurFrame,facesCurFrame):
        matches=face_recognition.compare_faces(encodeListeKnown,encodeFace)
        faceDis=face_recognition.face_distance(encodeListeKnown,encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)
        if(not faceDis):
            email_sender=''
            email_password=''
            email_receiver=''
            subject='ALERT'
            body="""
            Someone broke into your home!!!!!
            """
            em=EmailMessage()
            em['From']=email_sender
            em['To']=email_receiver
            em['Subject']=subject
            em.set_content(body)
            context=ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(email_sender,email_password)
                email.sendmail(email_sender,email_receiver,em.as_string())


        elif matches[matchIndex]:
            name=classNames[matchIndex].upper()
            print(name)
            y1,x2,y2,x1=faceloc
            #y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)



    cv2.imshow('webcam',img)
    cv2.waitKey(1)




