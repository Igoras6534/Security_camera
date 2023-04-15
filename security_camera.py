import cv2
import pose_model as pm
import datetime
import time
from mail_sender import EmailSender



cam=cv2.VideoCapture(1)
frame_size=(int(cam.get(3)),int(cam.get(4)))

c_time=0
p_time=0
detector=pm.poseDetector()
email_sender=EmailSender()




used_paths=[]
detection=False
detection_stopped_time=None
timer_started=False
seconds=7
fourcc=cv2.VideoWriter_fourcc(*"mp4v")


while True:
    _,frame=cam.read()
    frame=cv2.flip(frame,1)
    frame,pose_found=detector.findPose(frame,False)
    if pose_found==True:
        if detection == True:
            timer_started=False
        else:
            detection=True
            path=datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out=cv2.VideoWriter(f"videos/{path}.mp4",fourcc,20,frame_size)#Make a folder for videos in order to keep everything clean 
            print("Started recording")
            email_sender.send_email("your@mail.com")# A person you want to send the notification
    elif pose_found == False:
        if timer_started:
            if time.time()-detection_stopped_time>=seconds:
                detection=False
                timer_started=False
                out.release()
                if path not in used_paths:
                    email_sender.send_video("your@mail.com",path)
                    used_paths.append(path)
        else:
            timer_started=True
            detection_stopped_time=time.time()
    if detection == True:
        out.write(frame)




    c_time=time.time()
    fps=int(1/(c_time-p_time))
    p_time=c_time

    cv2.putText(frame,f"FPS:{fps}",(30,70),cv2.FONT_HERSHEY_PLAIN
                ,2,(255,0,0),2)
    cv2.imshow("Cam",frame)
        
    if cv2.waitKey(1)==ord("q"):
        break

out.release()
cam.release()
cv2.destroyAllWindows()

