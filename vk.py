import cv2 as cv
import mediapipe as mp
#import handtrackingmodule as htm
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

cap = cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
finaltext = ''
keys = [['Q','W','E','R','T','Y','U','I','O','P','[',']'],
['A','S','D','F','G','H','J','K','L',':',';','?'],
['Z','X','C','V','B','N','M',',','.','/','\\','#']]
buttonList = []

detector = HandDetector()
keyboard = Controller()

def drawAll(img,buttonList):
    for button in buttonList:
        x,y = button.pos
        w,h = button.size
        cv.rectangle(img,(x,y),(x+w,y+h),(255,0,255),cv.FILLED)
        cv.putText(img,button.text,(x+18,y+60),cv.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
    return img


class Button():
    def __init__(self,pos,text,size=[80,80]):
        self.pos = pos
        self.size = size
        self.text = text

for i in range(len(keys)):
    for j,key in enumerate(keys[i]):
        buttonList.append(Button([100*j+50,100*i+50],key))

while True:
    success, img = cap.read()
    hands,img = detector.findHands(cv.flip(img,1),draw=False)
    #img = cv.flip(img,1)
    img = drawAll(img,buttonList)
    if hands:
        for hand in hands:
            lmList = hand['lmList']
            for id,lm in enumerate(lmList):
                cx,cy = lm[:2]
                cv.circle(img,(cx,cy),6,(255,0,255), cv.FILLED)

            for connection in detector.mpHands.HAND_CONNECTIONS:
                x1, y1 = lmList[connection[0]][:2]
                x2, y2 = lmList[connection[1]][:2]
                cv.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            #bbox = hand['bbox']

            if lmList:
                for button in buttonList:
                    x,y = button.pos
                    w,h = button.size
                    if x< lmList[8][0] <x+w and y<lmList[8][1]<y+h:
                        cv.rectangle(img,(x,y),(x+w,y+h),(175,0,175),cv.FILLED)
                        cv.putText(img,button.text,(x+18,y+60),cv.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                        # Check if at least 13 landmarks exist (since index 12 is used)
                        if len(lmList) >= 13:
                            result = detector.findDistance(lmList[8][:2], lmList[12][:2])
    
                        if isinstance(result, tuple) and len(result) == 3:
                            l, _, _ = result
                            print(l)
                        
                        if l<50:
                            keyboard.press(button.text)
                            cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),cv.FILLED)
                            cv.putText(img,button.text,(x+18,y+60),cv.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                            finaltext+= button.text
                            sleep(0.2)
                        

    cv.rectangle(img,(50,350),(1000,450),(175,0,175),cv.FILLED)
    cv.putText(img,finaltext,(60,425),cv.FONT_HERSHEY_PLAIN,4,(255,255,255),4)


                        
    cv.imshow("Image", img)
    cv.waitKey(1)        
