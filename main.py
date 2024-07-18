import mediapipe as md
from cvzone.HandTrackingModule import HandDetector
from cvzone import cornerRect
import cv2 as cv
import numpy as np
cap=cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector=HandDetector(detectionCon=0.8)
# color=(255,0,255)
Centerx,Centery,w,h=100,100,200,200


# class DragObject():
#     def __init__(self,positioncenter,size=(200,200)):
        
#         self.positioncenter=positioncenter
#         self.size=size
        
#     def update(self,hand,finger,colors):
#         self.colors=colors
#         self.hand=hand
#         self.finger=finger
    
#         Centerx,Centery=self.positioncenter
#         w,h=self.size
#         # if the finger top in the rectangle 
#         if Centerx-w//2<Top_Second_Finger[0]<Centerx+w//2 and Centery-h//2<Top_Second_Finger[1]<Centery+h//2:#0 for x 1 for y
#                     colors=(0,255,0)
#                     color=colors
#                     self.positioncenter= hand["lmList"][8][:2]
#         else:
#                 colors=(255,255,255)
#                 color=colors
        
# rect=DragObject([150,150])

# while True:
#     suc,img=cap.read()
#     img=cv.flip(img,1,0)
#     hands,img=detector.findHands(img)#hands heni l landmarks
#     if hands:
        
#         # know i want to check if th top of the second finger and third finger together  touch the rectangel or its with our rectangle
#         hand=hands[0]
#         lmlist=hand["lmList"]
#         if lmlist:
#             distance, _, _ = detector.findDistance((lmlist[8][0], lmlist[8][1]), (lmlist[12][0], lmlist[12][1]), img)
#             if distance<65:
#                 Top_Second_Finger=lmlist[8]
#                 print(distance)
#                 # call the update
#                 rect.update(hand,Top_Second_Finger,color)
            
               
                

    
#     w,h=rect.size
#     Centerx,Centery=rect.positioncenter
#     Centerx,Centery=rect.positioncenter
#     cv.rectangle(img,(Centerx-w//2,Centery-h//2),(Centerx+w//2,Centery+h//2),color,cv.FILLED)
    
#     cv.imshow("image",img)
#     if cv.waitKey(1) & 0xFF == ord('q'
#):   
#         break   
class DragObject():
    def __init__(self, positioncenter, size=(200, 200),color=(0,0,255)):
        self.positioncenter = positioncenter
        self.size = size
        self.color = color # Initialize color as an attribute of the class

    def update(self, hand, finger):
        Centerx, Centery = self.positioncenter
        w, h = self.size
        # Check if the finger top is within the rectangle
        if Centerx - w // 2 < finger[0] < Centerx + w // 2 and \
           Centery - h // 2 < finger[1] < Centery + h // 2:
            self.color = (0, 255, 0)  # Update the color attribute
            self.positioncenter = hand["lmList"][8][:2]
        else:
            self.color = (0, 0, 255)  # Update the color attribute
rectlis=[]
for x in range(5):
    rectlis.append(DragObject([x*250+150, 150]))

while True:
    suc, img = cap.read()
    img = cv.flip(img, 1, 0)
    hands, img = detector.findHands(img)  # Hands with landmarks

    if hands:
        hand = hands[0]
        lmlist = hand["lmList"]
        if lmlist:
            distance, _, _ = detector.findDistance((lmlist[8][0], lmlist[8][1]), (lmlist[12][0], lmlist[12][1]), img)
            if distance < 65:
                Top_Second_Finger = lmlist[8]
                for rect in rectlis:
                    rect.update(hand, Top_Second_Finger)
            else:
                rect.color=(0,0,255)
    # for rect in rectlis:
    #     w, h = rect.size
    #     Centerx, Centery = rect.positioncenter
    #     cv.rectangle(img, (Centerx - w // 2, Centery - h // 2), (Centerx + w // 2, Centery + h // 2), rect.color, cv.FILLED)
    new_img=np.zeros_like(img,np.uint8)
    for rect in rectlis:
        w, h = rect.size
        Centerx, Centery = rect.positioncenter
        cv.rectangle(new_img, (Centerx - w // 2, Centery - h // 2), (Centerx + w // 2, Centery + h // 2), rect.color, cv.FILLED)
    out=img.copy()
    alpha=3
    mask=new_img.astype(bool)
    out[mask]=cv.addWeighted(img,alpha,new_img,1-alpha,0)[mask]
    cv.imshow("image", out)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
