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



def main():
    pass



if __name__=="__main__":
    main()