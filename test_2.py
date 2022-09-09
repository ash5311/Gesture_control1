from keras.models import load_model
from proj_file import HandDetector
from collections import deque
import cv2
import socket
import math
import time
import numpy as np

writ_mode = False
fin_left = []
fin_right = []
wcam = 1280
hcam = 1080
detector = HandDetector(detectionCon=0.6, maxHands=2)
model = load_model('best_model.h5')
letters = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l',
           12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w',
           23: 'x', 24: 'y', 25: 'z', 26: ''}

blackboard = np.zeros((hcam, wcam, 3), dtype=np.uint8)
alphabet = np.zeros((200, 200, 3), dtype=np.uint8)
right = dict()
points = deque(maxlen=512)
capture = 0
cap = cv2.VideoCapture(capture)
cap.set(3, hcam)
cap.set(4, wcam)

led_state1 = False
led_state2 = False
hold = 0
fold = 0
old_l = 0
new_l = 0
new_t = 0
old_t = 0
on = 0
tim = 0
host = "192.168.231.99"
port = 80
radius = 0
ct = []
lst = []
room = "HALL"
led_no = 1
menu = False
options = False
suboptions = False
modes = False
opt_old_time = time.time()
opt_new_time = 0
cursor = [0, 0]

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((host, port))


prediction = 26
centerPoint1 = 0
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    # hands, img = detector.findHands(img)
    new_t = time.time()
    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmarks points
        bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
        centerPoint1 = hand1["center"]  # center of the hand cx,cy
        handType1 = hand1["type"]  # Hand Type Left or Right
        left = dict()
        right = dict()
        centerPoint2 = 0

        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmarks points
            bbox2 = hand2["bbox"]  # Bounding Box info x,y,w,h
            centerPoint2 = hand2["center"]  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type Left or Right

            if handType2.upper() == "LEFT":
                fin_left = detector.fingersUp1(hand2)
                left = hands[1]
            else:
                right = hands[1]
                fin_right = detector.fingersUp1(hand2)

        if handType1.upper() == "LEFT":
            left = hands[0]
            fin_left = detector.fingersUp1(hand1)

        else:
            right = hands[0]
            fin_right = detector.fingersUp1(hand1)

        #########################################################################################

        if fin_left == [1, 1, 1, 0, 1]:                 # FOR TURNING ON
            on = 1
            old_t = time.time()

        ###################################################################
        if left and on == 1:                                                      # for intensity
            if right and fin_right == [1, 1, 1, 0, 0] and writ_mode == False:

                lst = right["lmList"]
                lrt = left["lmList"]

                cx1, cy1 = centerPoint1
                cx2, cy2 = centerPoint2
                length = math.hypot(cx2 - cx1, cy2 - cy1)
                cv2.circle(img, (cx1, cy1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (cx2, cy2), 15, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (cx1, cy1), (cx2, cy2), (255, 0, 0), 2)
                new_l = length
                dif = new_l - old_l
                old_l = length
                # print(dif)
                factor = (int(length))
                new_f = factor
                if factor < 150:
                    perc = 0
                elif factor > 700:
                    perc = 100
                else:
                    perc = ((factor - 150) / 550) * 100

                cv2.putText(img, str(perc), (300, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
                if dif > 10:
                    print("increasing: ", factor)

                    #s.sendall(bytes(str(abs(factor)), 'utf-8'))
                    #s.sendall("exit".encode())#data being sent to arduino code
                if dif < -10:
                    print("decreasing", factor)
                    #s.sendall(bytes(str(abs(factor)), 'utf-8'))
                    #s.sendall("exit".encode())#data being sent to arduino code

                old_t = time.time()

        ###############################################################################################################

        if on == 1:

            if right and writ_mode == False:                              # for turning on stuff
                lst = right["lmList"]
                x1, y1, z1 = lst[8][0], lst[8][1], lst[8][2]
                x2, y2 = lst[5][0], lst[5][1]
                p1 = (x1, y1)
                p2 = (x2, y2)

                l, i = detector.findDistance(p1, p2)
                fin_ri = detector.fingersUp1(right)
                #print(z1)
                if fin_ri == [0, 1, 1, 0, 0]:
                    hold = time.time()
                if fin_ri == [0, 0, 0, 0, 0]:
                    fold = time.time()
                    tim = hold - fold




                if -0.1 <= tim < 0 and hold != 0 and fold != 0:
                    # print("clicked")
                    fold = 0

                    if abs(z1) > 40 and room == "HALL":
                        led_no = 1
                    if abs(z1) < 40 and room == "HALL":
                        led_no = 2


                    if led_state1:
                        print("led off ", room, "  ", led_no)


                        #s.sendall(bytes(str(2), 'utf-8'))
                        #s.sendall("exit".encode())
                        led_state1 = False
                    else:

                        #s.sendall(bytes(str(1), 'utf-8'))
                        #s.sendall("exit".encode())
                        print("led on ", room, "  ", led_no)
                        # print(l)
                        led_state1 = True

                old_t = time.time()

        ############################################################################################
        if on == 1:                                                             # for menu options
            if right:
                old_t = time.time()
            if fin_right == [1, 1, 1, 0, 1] and writ_mode == False:

                opt_new_time = time.time()

                if int(abs(opt_old_time-opt_new_time)) >= 2:
                    if menu:
                        menu = False
                        opt_old_time = time.time()

                    else:
                        menu = True
                        opt_old_time = time.time()

            if fin_left == [1, 1, 1, 0, 1] and fin_right == [1, 1, 1, 0, 1]:
                writ_mode = False

            if menu:
                cv2.putText(img, "Menu", (650, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
                # writ_mode = False

            if fin_right == [0, 1, 0, 0, 0] and writ_mode == False:
                if right:
                    lst = right["lmList"]
                x1, y1 = lst[8][0], lst[8][1]
                cv2.circle(img, (x1, y1), 3, (125, 344, 278), 7)
                cursor.clear()
                cursor.append(x1)
                cursor.append(y1)
                # print(cursor)

            if (640 <= cursor[0] <= 660 and 40 <= cursor[1] <= 60) and menu:
                menu = False
                modes = True

            if modes:
                cv2.putText(img, "1) Rooms", (200, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
                cv2.putText(img, "2) Write Mode", (450, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

                if 90 <= cursor[1] <= 110:
                    if 190 <= cursor[0] <= 210:
                        options = True
                        modes = False
                    if 440 <= cursor[0] <= 460:
                        modes = False
                        writ_mode = True

            if options:
                cv2.putText(img, "Rooms", (650, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
                cv2.putText(img, "1) Bedroom", (100, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
                cv2.putText(img, "2) Restroom", (350, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
                cv2.putText(img, "3) HALL", (600, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

                if 140 <= cursor[1] <= 160:
                    if 90 <= cursor[0] <= 110:
                        print("Room : Bedroom")
                        room = "Bedroom"
                        options = False
                        suboptions = True
                    if 340 <= cursor[0] <= 360:
                        print("Room : Restroom")
                        room = "Restroom"
                        options = False
                        suboptions = True
                    if 590 <= cursor[0] <= 610:
                        print("Room : Hall")
                        options = False
                        suboptions = True
                        room = "Hall"

            if suboptions:
                cv2.putText(img, "Led 1", (200, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
                cv2.putText(img, "Led 2", (450, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

                if 90 <= cursor[1] <= 110:
                    if 190 <= cursor[0] <= 210:
                        menu = True
                        suboptions = False
                        led_no = 1
                        print("led: 1")

                    if 440 <= cursor[0] <= 460:
                        menu = True
                        suboptions = False
                        led_no = 2
                        print("led: 2")

############################################################################

        ############################################################
            # if (fin_left) == [0, 0, 1, 1, 1]:
            #   writ_mode = False
            # if (fin_right) == [0, 0, 1, 1, 1]:
            #   writ_mode = True
            if writ_mode and right:
                # img = cv2.flip(img, 1)
                cv2.putText(img, "Write Mode", (450, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
                on = 1
                # print(cent)
                if fin_right == [0, 1, 0, 0, 0]:

                    lst = right["lmList"]
                    x1, y1 = lst[8][0], lst[8][1]
                    cent = (x1, y1)
                    # cv2.circle(img, (x1, y1), 3, (125, 344, 278), 7)
                    points.appendleft(cent)

                elif len(points) != 0:
                    blackboard_gray = cv2.cvtColor(blackboard, cv2.COLOR_BGR2GRAY)
                    blur = cv2.medianBlur(blackboard_gray, 15)
                    blur = cv2.GaussianBlur(blur, (5, 5), 0)
                    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                    # if writ_mode:
                    #   cv2.imshow("Thresh", thresh)

                    blackboard_cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

                    if len(blackboard_cnts) >= 1:
                        cnt = sorted(blackboard_cnts, key=cv2.contourArea, reverse=True)[0]

                        if cv2.contourArea(cnt) > 1000:
                            x, y, w, h = cv2.boundingRect(cnt)
                            alphabet = blackboard_gray[y - 10:y + h + 10, x - 10:x + w + 10]
                            try:
                                img1 = cv2.resize(alphabet, (28, 28))
                            except cv2.error as e:
                                continue

                            img1 = np.array(img1)
                            img1 = img1.astype('float32') / 255

                            prediction = model.predict(img1.reshape(1, 28, 28))[0]
                            #print(prediction)
                            prediction = np.argmax(prediction)

                    # Empty the point deque and also blackboard
                    points = deque(maxlen=512)
                    blackboard = np.zeros((hcam, wcam, 3), dtype=np.uint8)

            old_t = time.time()
        ################################################################################

        for i in range(1, len(points)):
            if points[i - 1] is None or points[i] is None:
                continue
            cv2.line(img, points[i - 1], points[i], (255, 0, 0), 10)
            cv2.line(blackboard, points[i - 1], points[i], (255, 255, 255), 8)


        if on == 1:
            if right and fin_right == [1, 1, 1, 0, 0]:
                pass
        if fin_left == [1, 1, 0, 0, 1]:
            on = 0

    #########################################
                                                                    # display
    if on == 0:
        cv2.putText(img, "OFF", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 5)
    count = int(abs(new_t - old_t))

    if on == 1 and count < 7:
        cv2.putText(img, "ON", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 5)

    if count >= 7 and count < 10 and on == 1 and writ_mode == False:
        cv2.putText(img, "Turning OFF", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 5)

    if count >= 10 and on == 1 and writ_mode == False:
        on = 0

    if on == 1 and writ_mode:
        cv2.putText(img, "Alphabet Read: " + str(letters[int(prediction)]), (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (255, 0, 0), 2)

    if on == 1 and writ_mode == False:
        cv2.putText(img, room, (100, 500), cv2.FONT_HERSHEY_COMPLEX, 2, (1, 138, 242), 4)
        cv2.putText(img, str(led_no), (900, 500), cv2.FONT_HERSHEY_COMPLEX, 2, (1, 138, 242), 4)





    cv2.imshow("Gesture recognition", img)




    '''

    if (writ_mode):
        if str(letters[int(prediction)]) == "r":
            s.sendall(bytes(str(abs(4)), 'utf-8'))
            s.sendall("exit".encode())#data being sent to arduino code
        if str(letters[int(prediction)]) == "g":
            s.sendall(bytes(str(abs(5)), 'utf-8'))
            s.sendall("exit".encode())#data being sent to arduino code
        if str(letters[int(prediction)]) == "b":
            s.sendall(bytes(str(abs(3)), 'utf-8'))
            s.sendall("exit".encode())#data being sent to arduino code
        if str(letters[int(prediction)]) == "p":
            s.sendall(bytes(str(abs(6)), 'utf-8'))
            s.sendall("exit".encode())  # data being sent to arduino code
        if str(letters[int(prediction)]) == "o":
            s.sendall(bytes(str(abs(7)), 'utf-8'))
            s.sendall("exit".encode())  # data being sent to arduino code
        if str(letters[int(prediction)]) == "w":
            s.sendall(bytes(str(abs(8)), 'utf-8'))
            s.sendall("exit".encode())  # data being sent to arduino code

    '''


######################################








    if cv2.waitKey(1) == 27:  # if I press enter
        break
cap.release()
cv2.destroyAllWindows()