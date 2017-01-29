import cv2
import datetime
import numpy as np
from retrainingexample import *
cv2.namedWindow("preview")
vc = cv2.VideoCapture(1)

sample_rate = 5
frames_before = 5
frames_after = 5
max_buffer_len = 50
img_buffer = []
recording_now = "NONE"


# Creates graph from saved GraphDef.
create_graph()

idx = 0
post_frames = 0

def item_seen(frame):
    return run_inference_on_image(np.asarray(frame))

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    idx = idx + 1
    if (idx % sample_rate == 0):
        img_buffer.append(frame)
        seen_stuff = item_seen(frame)
        while (len(img_buffer) > max_buffer_len):
            del img_buffer[0]
        if (seen_stuff != "NONE"):
            recording_now = seen_stuff
            print ( "Found the damn " + recording_now + "\n")
        else:
            if (recording_now == "NONE"):
                while (len(img_buffer) > frames_before):
                    del img_buffer[0]
            else:
                post_frames = post_frames + 1
                if (post_frames == frames_after):
                    curridx = 0
                    for f in img_buffer:
                        cv2.imwrite("gotit%d.jpg"%curridx, f);
                        curridx = curridx + 1
                    print ( recording_now + " was last seen at " + str(datetime.datetime.now()) + "\n")
                    recording_now = "NONE"
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")
