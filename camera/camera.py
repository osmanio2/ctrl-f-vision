import datetime
from retrainingexample import *
import imageio
import numpy as np
import copy
import os
import sys
import _thread
import visvis as vv

# which camera?
imageio.plugins.ffmpeg.download()
reader = imageio.get_reader("<video%d>" % int(sys.argv[1]))
t = vv.imshow(reader.get_next_data(), clim=(0, 255))

# hardcoded stuff (pick sensible values)
sample_rate = 50
frames_before = 10
frames_after = 5
max_buffer_len = 50

max_images = 4
current_images = 0
label = "without"

# what is currently recorded?
img_buffer = []
recording_now = "without"
sess = create_graph()

# manage recording 'logic'
idx = 0
post_frames = 0

# download gif stuff
imageio.plugins.freeimage.download()

# actually put recognition stuff
def item_seen(frame):
    global sess, max_images, current_images, label
    # DIRTY!!
    imageio.imwrite('picture_out.jpg', frame)
    image = run_inference_on_image('picture_out.jpg', sess)
	
    if image != "without" and image == label:
        current_images += 1
    else:
        current_images = 0
        label = image
	
    if current_images > max_images:
        print("This is the label yaaaaaaaaaaaaaa {}".format(image))
        current_images = max_images
        return image
    else: 
        print("No Still Nothing useful although I am seeing {}".format(image))
        return "without"
        
	
	
    
    # maybe resize?
    #(w, h, c) = frame.shape
    #scipy.misc.imresize(np.asarray(frame), min(200.0 / w, 200.0 / h))
    #return run_inference_on_image(np.asarray(frame))

# method to write the gif
def gifwrite(name, img_buf):
    print("Thread spawned"*7)
    kargs = { 'quantizer':'nq' }
    imageio.mimwrite(name + ".gif", img_buf, 'GIF-FI', **kargs)
	# write additional data inside json
    fp = open("../records/%s.json" % name, 'w')
    fp.write("{\n")
    fp.write("    \"id\": 123,");
    fp.write("    \"gifUrl\": \"%s.gif\", \n" % name);
    fp.write("    \"timestamp\": \"%s\", \n" %
                             str(datetime.datetime.now()))
    fp.write("    \"tags\": [\"andrej\",\"hack\"]");
    fp.write("}\n")
    fp.close()

# main loop
for im in reader:
    # get current frame
    vv.processEvents()
    t.SetData(im)
    # not interested in all of them
    idx = (idx + 1) % sample_rate
    if (idx == 0):
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
                    post_frames = 0
                    temp_buf = copy.deepcopy(img_buffer)
                    try:
                        _thread.start_new_thread(gifwrite, ("../records/%s" % recording_now, temp_buf))
                    except:
                        print("Could not spawn gif creation thread")
                    
                    recording_now = "without"
# done!