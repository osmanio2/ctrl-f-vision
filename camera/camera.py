import datetime
from retrainingexample import *
import imageio
import numpy as np
import os
import sys
import visvis as vv	

# which camera?
imageio.plugins.ffmpeg.download()
reader = imageio.get_reader("<video%d>" % int(sys.argv[1]))
t = vv.imshow(reader.get_next_data(), clim=(0, 255))



# hardcoded stuff (pick sensible values)
sample_rate = 50
frames_before = 5
frames_after = 5
max_buffer_len = 50

# what is currently recorded?
img_buffer = []
recording_now = "NONE"

# manage recording 'logic'
idx = 0
post_frames = 0
tstep = 0 # only for testing

# download gif stuff
imageio.plugins.freeimage.download()

# TODO: actually put recognition stuff
def item_seen(frame):
	# Creates graph from saved GraphDef.
	create_graph()
    return run_inference_on_image(np.asarray(frame))

# main loop
for im in reader:
    # get current frame
    vv.processEvents()
    t.SetData(im)
    # not interested in all of them
    idx = (idx + 1) % sample_rate
    if (idx == 0):
        tstep = tstep + 1
        img_buffer.append(im)
        seen_stuff = item_seen(im)
        # keep buffer limit
        while (len(img_buffer) > max_buffer_len):
            del img_buffer[0]
        if (seen_stuff != "without"):
            # we only now see something of interest
            recording_now = seen_stuff
        else:
            if (recording_now == "without"):
                # nothing is being observed
                while (len(img_buffer) > frames_before):
                    del img_buffer[0]
            else:
                # I no longer see what I am recording
                # record for a little longer
                post_frames = post_frames + 1
                if (post_frames == frames_after):
                    # we would love to make the gif more compressed...
                    kargs = { 'loop':1, 'quantizer':'nq' }
                    imageio.mimwrite("records/%s.gif" % recording_now,
                                     img_buffer, 'GIF-FI', **kargs)
                    # write additional data inside json
                    fp = open("records/%s.json" % recording_now, 'w')
                    fp.write("{\n")
                    fp.write("    \"id\": \"%s\", \n" % recording_now);
                    fp.write("    \"time\": \"%s\" \n" %
                             str(datetime.datetime.now()))
                    fp.write("}\n")
                    fp.close()
                    recording_now = "NONE"
# done!
cv2.destroyWindow("preview")
