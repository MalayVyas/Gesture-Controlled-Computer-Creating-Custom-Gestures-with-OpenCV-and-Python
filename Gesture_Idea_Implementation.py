import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import sys

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
detector = htm.handDetector(detectionCon=0.5, trackCon=0.5)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

while True:
    success, img = cap.read()
    img = detector.findHands(img=img, draw=True)
    lmList = detector.findPosition(img)
    # print(lmList)
    if len(lmList) != 0:
        ##################################################################################
        # Tip points and its Calculations
        ##################################################################################
        x1, y1 = lmList[8][1], lmList[8][2]  # Index_Finger_Tip
        x2, y2 = lmList[12][1], lmList[12][2]  # Middle_Finger_Tip
        x3, y3 = lmList[16][1], lmList[16][2]  # Ring_Finger_Tip
        x4, y4 = lmList[20][1], lmList[20][2]  # Pinky_Finger_Tip
        x5, y5 = lmList[1][1], lmList[1][2]  # Thumb_CMC
        cx_12, cy_12 = (x1 + x2) // 2, (y1 + y2) // 2
        cx_23, cy_23 = (x2 + x3) // 2, (y2 + y3) // 2
        cx_34, cy_34 = (x3 + x4) // 2, (y3 + y4) // 2
        point_1 = [x1, y1]
        point_2 = [x2, y2]
        point_3 = [x3, y3]
        point_4 = [x4, y4]
        point_5 = [x5, y5]
        if cx_12 < 0:
            cx_12 = 0
        if cy_12 < 0:
            cy_12 = 0
        height = math.sqrt(cy_12)
        width = math.sqrt(cx_12)
        length12 = math.sqrt(((point_1[0] - point_2[0]) ** 2) + ((point_1[1] - point_2[1]) ** 2))
        length23 = math.sqrt(((point_2[0] - point_3[0]) ** 2) + ((point_2[1] - point_3[1]) ** 2))
        length34 = math.sqrt(((point_3[0] - point_4[0]) ** 2) + ((point_3[1] - point_4[1]) ** 2))
        length15 = math.sqrt(((point_1[0] - point_5[0]) ** 2) + ((point_1[1] - point_5[1]) ** 2))

        ##################################################################################
        # Logical Unit of the Project
        ##################################################################################
        if length12 < 20 and length23 < 20 and length34 < 20 and length15 < 30:
            sys.exit()
        #################################################################################

        if length12 < 20 and length15 > 30:
            cv2.circle(img, (cx_12, cy_12), 10, (255, 0, 100), cv2.FILLED)
            vol = np.interp(height, [10, 20], [maxVol, minVol])
            brightness = np.interp(width, [10, 20], [0, 100])
            volume.SetMasterVolumeLevel(vol, None)
            sbc.set_brightness(brightness)
        ##################################################################################

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f"FPS: {int(fps)}", (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break