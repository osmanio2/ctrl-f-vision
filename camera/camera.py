import cv2
import datetime
import sys

# which camera?
camera_id = int(sys.argv[1])

# setting up
cv2.namedWindow("preview")
vc = cv2.VideoCapture(camera_id)

# hardcoded stuff (pick sensible values)
sample_rate = 5
frames_before = 5
frames_after = 5
max_buffer_len = 50

# what is currently recorded?
img_buffer = []
recording_now = "NONE"

# manage recording 'logic'
idx = 0
post_frames = 0

# TODO: actually put recognition stuff
def item_seen(frame):
    if (idx >= sample_rate * 9 and idx <= sample_rate * 17):
        return "KEY"
    else:
        return "NONE"

# is camera working
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

# main loop
while rval:
    # get current frame
    cv2.imshow("preview", frame)
    (rval, frame) = vc.read()
    key = cv2.waitKey(20)
    idx = (idx + 1) % sample_rate
    # not interested in all of them
    if (idx == 0):
        img_buffer.append(frame)
        seen_stuff = item_seen(frame)
        # keep buffer limit
        while (len(img_buffer) > max_buffer_len):
            del img_buffer[0]
        if (seen_stuff != "NONE"):
            # we only now see something of interest
            recording_now = seen_stuff
            print("I can see the " + recording_now + "\n")
        else:
            if (recording_now == "NONE"):
                # nothing is being observed
                while (len(img_buffer) > frames_before):
                    del img_buffer[0]
            else:
                # I no longer see what I am recording
                # record for a little longer
                post_frames = post_frames + 1
                if (post_frames == frames_after):
                    # save images
                    curridx = 0
                    for f in img_buffer:
                        print("img/%s_%d.jpg" % (recording_now, curridx))
                        cv2.imwrite("img/%s_%d.jpg" % (recording_now, curridx),
                                    f)
                        curridx = curridx + 1
                    # get timestamp
                    print(recording_now + " was last seen at " +
                          str(datetime.datetime.now()) + "\n")
                    recording_now = "NONE"
# done!
cv2.destroyWindow("preview")
