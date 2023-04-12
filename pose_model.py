import cv2
import mediapipe as mp
import time
import math

class poseDetector():
    def __init__(self, mode=False,
               model_complexity=1,
               smooth_landmarks=True,
               enable_segmentation=False,
               smooth_segmentation=True,
               min_detection_confidence=0.7,
               min_tracking_confidence=0.7):
          
        self.mode=mode
        self.model_complexity= model_complexity
        self.smooth_landmarks=smooth_landmarks
        self.enable_segmentation=enable_segmentation
        self.smooth_segmentation=smooth_segmentation
        self.min_detection_confidence=min_detection_confidence
        self.min_tracking_confidence= min_tracking_confidence
        self.mpDraw=mp.solutions.drawing_utils
        self.mpPose=mp.solutions.pose
        self.pose=self.mpPose.Pose(self.mode,self.model_complexity,
                                   self.smooth_landmarks,self.enable_segmentation,
                                   self.smooth_segmentation,
                                   self.min_detection_confidence,
                                   self.min_tracking_confidence,)
        self.drawing_spec=self.mpDraw.DrawingSpec(color=(0,255,0))




    def findPose(self,frame,draw=True):
        frame_rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.results=self.pose.process(frame_rgb)
        if self.results.pose_landmarks:
            pose_found=True
            if draw:
                self.mpDraw.draw_landmarks(frame,self.results.pose_landmarks, 
                                           self.mpPose.POSE_CONNECTIONS,connection_drawing_spec=self.drawing_spec)
        else:
            pose_found=False
        return frame, pose_found
        
    def getPosition(self,frame,draw=True):
        self.lmlist=[]
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c=frame.shape
                cx,cy=int(lm.x*w), int(lm.y*h)
                self.lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(frame,(cx,cy),7,(255,0,255),4)
        return self.lmlist

    def findAngle(self,frame, p1, p2, p3, draw=True):



        x1,y1=self.lmlist[p1][1:]
        x2,y2=self.lmlist[p2][1:]
        x3,y3=self.lmlist[p3][1:]

        #------------------------------------
        angle=int(math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2)))
        #print(angle)
        if angle<0:
            angle+=360


        #------------------------------------
        if draw:
            cv2.line(frame,(x1,y1),(x2,y2),(255,255,255),3)
            cv2.line(frame,(x2,y2),(x3,y3),(255,255,255),3)

            cv2.circle(frame,(x1,y1),10,(0,0,255),cv2.FILLED)
            cv2.circle(frame,(x1,y1),15,(0,0,255),2)

            cv2.circle(frame,(x2,y2),10,(0,0,255),cv2.FILLED)
            cv2.circle(frame,(x2,y2),15,(0,0,255),2)

            cv2.circle(frame,(x3,y3),10,(0,0,255),cv2.FILLED)
            cv2.circle(frame,(x3,y3),15,(0,0,255),2)
            cv2.putText(frame,str(angle),(x2-50,y2+50),cv2.FONT_HERSHEY_PLAIN,
                        2,(0,0,255),2)
        return angle




    

def main():
    cam=cv2.VideoCapture(1)
    c_time=0
    p_time=0
    detector=poseDetector()
    while True:
        _,frame=cam.read()
        frame=detector.findPose(frame)
        lmlist=detector.getPosition(frame)
        print(lmlist)



        c_time=time.time()
        fps=1/(c_time-p_time)
        p_time=c_time
        cv2.putText(frame,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,
                    3,(255,0,255),3)
        cv2.imshow("Camera",frame)
        
        if cv2.waitKey(1)==ord("q"):
            break




if __name__=="__main__":
    main()