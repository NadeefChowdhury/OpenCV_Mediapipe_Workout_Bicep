import cv2
import mediapipe as mp
import time
import math
import numpy as np

mpPose= mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
pTime=0
cap = cv2.VideoCapture('Video.mp4')

cx11,cy11 = 0,0
cx13,cy13 = 0,0
cx15,cy15 = 0,0

count=0
direction=0

while True:
    success, img = cap.read()
    cv2.namedWindow("Video", cv2.WINDOW_NORMAL) 
  
    # Using resizeWindow() 
    cv2.resizeWindow("Video", 800, 600) 
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results =  pose.process(imgRGB)
    if results.pose_landmarks:
        for ID, lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = img.shape
            cx,cy= int(lm.x*w), int(lm.y*h)
            #print(ID, cx, cy)
            
            
            
            if ID == 0:
                cv2.circle(img,(cx,cy),20,(0,0,255),cv2.FILLED)
            
            
            
            if ID == 11:
                cv2.circle(img,(cx,cy),20,(0,0,255),cv2.FILLED)
                cx11,cy11 = cx,cy
            
            
            if ID == 13:
                cv2.circle(img,(cx,cy),20,(0,0,255),cv2.FILLED)
                cx13,cy13 = cx,cy
            
           
            if ID == 15:
                cv2.circle(img,(cx,cy),20,(0,0,255),cv2.FILLED)
                cx15,cy15 = cx,cy
        
       
        angle = 180 + math.degrees(math.atan2(cy11 - cy13, cx11 - cx13) - math.atan2(cy13 - cy15, cx13 - cx15))
        per = np.interp(angle, (50,149), (0,100))
        #print(angle, per)
        #cv2.putText(img,"Angle is: "+str(int(angle)),(10, 100), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,255), 3 )        
        mpDraw.draw_landmarks(img,results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        if per == 0:
            if direction == 0:
                count += 0.5
                direction=1
        if per == 100:
            if direction == 1:
                count += 0.5
                direction=0
        print(count)
             
        cv2.rectangle(img, (0,0), (900,200), (0,255,0), cv2.FILLED)
        cv2.putText(img,"Number of reps: "+str(int(count)),(10, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0), 3 )   
    
    cv2.namedWindow("Video", cv2.WINDOW_NORMAL) 
    cTime = time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    #cv2.putText(img,str(int(fps)),(10, 150), cv2.FONT_HERSHEY_PLAIN, 10, (0,0,255), 3 )        
    cv2.imshow("Video", img)
    if cv2.waitKey(20) & 0xFF==ord('d'):
        break

cv2.destroyAllWindows()