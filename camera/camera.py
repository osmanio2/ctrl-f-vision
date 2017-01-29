import datetime
import imageio
import os
import sys
import visvis as vv

# which camera?
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
    if (tstep >= 9 and tstep <= 17):
        return "KEY"
    else:
        return "NONE"

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
                    print(img_buffer[0].shape)
                    # we would love to make the gif more compressed...
                    kargs = { 'loop':1, 'quantizer':'nq' }
                    imageio.mimwrite("gifs/%s.gif" % recording_now,
                                     img_buffer, 'GIF-FI', **kargs)
                    # get timestamp
                    print(recording_now + " was last seen at " +
                          str(datetime.datetime.now()) + "\n")
                    recording_now = "NONE"
# done!
cv2.destroyWindow("preview")
