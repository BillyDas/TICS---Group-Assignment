import sensor, time, image, tf

# Helper function for sorting predictions
def sort_preds(pred):
    return pred[1]

def setup():
    # Reset sensor
    sensor.reset()

    # Sensor settings
    sensor.set_framesize(sensor.HQVGA)
    sensor.set_pixformat(sensor.GRAYSCALE)

    # Load Haar Cascade
    global face_cascade = image.HaarCascade("/facemask/face_mask_cascade.cascade", stages=25)

    # Load tensorflow lite model
    global net = "/facemask/trained.tflite"
    global labels = [line.rstrip('\n') for line in open("/facemask/labels.txt")]


    # FPS clock
    global clock = time.clock()

def main():
    while (True):
        clock.tick()

        # Capture snapshot
        img = sensor.snapshot()

        # Find faces
        faces = img.find_features(face_cascade, threshold=0.75, scale_factor=1.25)

        # Loop trhough each face
        for face in faces:
            (x, y, w, h) = face

            # give a bit more vertical space - it seems to cut the face too short
            face = (x, y, w, int(h*1.2))

            center = (int(x + w / 2), int(y + h / 2))

            # tracking of faces can be achieved by calculating the euclidian distance between multiple frames

            img.draw_cross(center)
            img.draw_rectangle((x, y, w, h))

            for obj in tf.classify(net, img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5, roi=face):
                predictions_list = list(zip(labels, obj.output()))

                sorted_list = list(zip(labels, obj.output()))
                # sort our predictions from most confident to least
                sorted_list.sort(reverse=True,key=sort_preds)

                # draw our prediction above the face with a black background
                img.draw_rectangle(x,y-10,w,10,(0,0,0),1,True)
                img.draw_string(x,y-10,sorted_list[0][0])

                print("**********\nPrediction at [x={0},y={1},w={2},h={3}]: {4} - {5}%".format(x, y, w, h, sorted_list[0][0], sorted_list[0][1] * 100))

# uncomment for direct use
# setup()
# main()
