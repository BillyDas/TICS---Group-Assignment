# Untitled - By: pi - Thu. Oct. 15 2020

import pyb, sensor, image, time, os, tf, math


# Settings
person_threshold = 0.7

#--------------SETUP---------------------
global person
#Onboard LED (1:red, 2:green, 3:blue, 4:IR)
led = pyb.LED(1)
led.off

#CAM Setup
cam_RezX = 1280 # In Pixles
cam_Rezy = 720 # In Pixels
angle_width = 52 #In degrees
angle_height = 23 # In Degrees
camera_separation = 0.22 # In Meters

imgfilenameLeft = "SocialDistancingImg/LeftPos.jpg"
imgfilenameRight = "SocialDistancingImg/RightPos.jpg"
FullDetection = 0

#begin with left movement (left 1)
left = 1
right = 0

#Array setup
personLeft = []
personRight = []
Distance = []

#MATH SETUP
PLX = 0
x_origin = None
y_origin = None
x_adjacent = None
y_adjacent = None


#-------PIN NUMBERS----------
left_Stopper = pyb.Pin("P6", pyb.Pin.IN)
Right_Stopper = pyb.Pin("P5", pyb.Pin.IN)



sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)


clock = time.clock()


#Camera Snap (Take Picture)
def capturepic(left_cam_true):
    print("[INFO] ----------------------- IMAGE CAPTURE ----------------------------")
    for x in range(0, 2):
        # Capture frame-by-frame

        if left_cam_true:
            sensor.snapshot().save(imgfilenameLeft)
            print("[INFO] - Captured Left Pic")
        else:
            sensor.snapshot().save(imgfilenameRight)
            print("[INFO] - Captured Right Pic")

def readinput():
    global LSwitchIsOn
    global RSwitchIsOn
    LSwitchIsOn = left_Stopper.value()
    RSwitchIsOn = Right_Stopper.value()

def process_photo():
    print("[INFO] ----------------------- IMAGE PROCESS ----------------------------")

    #--------------------YET TO BUILD AND IMPLEMENT-----------------------
    #Loads Left Image
    img = image.Image(imgfilenameLeft, copy_to_fb = True)
    #DETECT PERSON
    #ADD PERSON CORDS TO PERSONLEFT

    img = image.Image(imgfilenameRight, copy_to_fb = True)
    #DETECT PERSON
    #ADD PERSON CORDS TO PERSONRIGHT


def math_time(personLeft, personRight):
    print("[INFO] ----------------------- MATHS ----------------------------")
    #Calculates Angles of the left and right camera (full angles add up to 180)
    B1 = (180-angle_width)/2
    B2 = (180-angle_width)/2
    #grabs the+ X aix pixel cordinate.
    #if len(personLeft) == len(personRight):
    if len(personLeft) == len(personRight):
        for i in range(len(personLeft)):
            PLX = str(personLeft[i]).split(", ")[0].strip("()")
            PRX = str(personRight[i]).split(", ")[0].strip("()")
            PRX = int(PRX)
            PLX = int(PLX)

            #Gets the distance of the X cordinates from the 0,0 position (top left)
            AP1 = angle_width / PLX
            AP2 = angle_width / PRX

            P1 = cam_RezX - PLX
            P2 = PRX - 1

            O1 = P1 * AP1
            O2 = P2 * AP2

            Theta = P1 * (angle_width / cam_RezX) + B1
            Phi = P2 * (angle_width / cam_RezX) + B2

            Car_angle = 180 - (Phi - Theta)

            Distance.append((camera_separation * math.sin(math.radians(Phi) * math.sin(math.radians(Theta))))/math.sin(math.radians(180 - (Theta + Phi))))



while(True):
    clock.tick()

    #print("[INFO] ---------------------------- Program Start -----------------------------")

    #if FullDetection == 2:

        ##PERSON DETECTION AI SYSTEM
        #process_photo()
        #math_time(personLeft,personRight)

        #for p in Distance:
            #print("[INFO] - Person Detected (In Meters): " + str(p))

        #global l
        #for l in range(0, (len(Distance)-1)):
            #l2 = l + 1

            ##Checks if person A is further than 1.5m from Person B
            #DistanceClose = Distance[l2] - 1.5
            #DistanceFar = Distance[l2] + 1.5


            #if Distance[l] > DistanceClose or Distance[l] < DistanceFar:
                #print("[INFO] - Person #" + str(l) + " and Person #" + str(l2) + " are to close!")

        #personLeft.clear()
        #Distance.clear()
        #personRight.clear()
        #FullDetection = 0
        #print("[INFO] -----------------------------PROGRAM COMPLETED-----------------------")

    #elif left == 1:
        #while left == 1:
            ##------Left Stopper-----
            #readinput()
            #if LSwitchIsOn == 1:
                #left_cam_true = True
                ##capturepic(left_cam_true)

                #print("[INFO] - LEFT STOPPER CLICKED")
                #time.sleep(.10)
                #left = 0
                #right = 1
                #FullDetection = FullDetection + 1

            #elif LSwitchIsOn == 0:
                #print("[INFO] - LEFT STOPPER NOT CLICKED")
                #time.sleep(.10)

    #elif right == 1:
        #while right == 1:
            ##------Right Stopper--------
            #readinput()
            #if RSwitchIsOn == 1:

                #left_cam_true == False
                ##capturepic(left_cam_true)

                #print("[INFO] - RIGHT STOPPER CLICKED")
                #time.sleep(.10)
                #left = 1
                #right = 0
                #FullDetection = FullDetection + 1
            #elif RSwitchIsOn == 0:
                #print("[INFO] - RIGHT STOPPER NOT CLICKED")
                #time.sleep(.10)


#--------------------------------
#|                              |
#|      This Is For Testing     |
#|                              |
#--------------------------------

    print("[INFO] ---------------------------- Program Start -----------------------------")


    #PERSON DETECTION AI SYSTEM

    personLeft.append("(410, 667)")
    personLeft.append("(979, 658)")
    personRight.append("(328, 625)")
    personRight.append("(898, 610)")

    math_time(personLeft,personRight)

    print(Distance)
    for p in Distance:
        print("[INFO] - Person Detected (In Meters): " + str(p))

    global l
    for l in range(0, (len(Distance)-1)):
        l2 = l + 1

        #Checks if person A is further than 1.5m from Person B
        DistanceClose = Distance[l2] - 1.5
        DistanceFar = Distance[l2] + 1.5


        if Distance[l] > DistanceClose or Distance[l] < DistanceFar:
            print("[INFO] - Person #" + str(l) + " and Person #" + str(l2) + " are to close!")

    personLeft.clear()
    Distance.clear()
    personRight.clear()
    FullDetection = 0
    print("[INFO] -----------------------------PROGRAM COMPLETED-----------------------")

    capturepic(left_cam_true = True)
    capturepic(left_cam_true = False)




    print(clock.fps(), "fps")
