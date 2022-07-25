import cv2 as cv
import mediapipe as mp

class HandDetector():

    def __init__(self,mode=False,MaxHands=1,DetectionConfidence=0.5,TrackConfidence=0.5):
        self.mode= mode
        self.MaxHands = MaxHands
        self.DetectionConfidence =DetectionConfidence
        self.TrackConfidence=TrackConfidence
        self.mp_holistic = mp.solutions.holistic
        self.mp_hands =mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False,min_detection_confidence=0.5,min_tracking_confidence=0.5)
        self.MpDraw = mp.solutions.drawing_utils

    def FindHands(self,img,draw =True):
        imgRGB = cv.cvtColor( img, cv.COLOR_BGR2RGB )
        self.results = self.hands.process( imgRGB )
        # print(results.multi_hand_landmarks)                self.MpDraw.draw_landmarks( img,  landmark, self.mp_hands .HAND_CONNECTIONS )
        # cv.putText( img, str( int( fps ) ), (10, 70), cv.FONT_ITALIC, 3, (225, 50, 225), 2 )
        if self.results.multi_hand_landmarks:
            for id, hand_land_mark in enumerate(self.results.multi_hand_landmarks):
                if draw and id==0:
                    self.MpDraw.draw_landmarks( img,  hand_land_mark, self.mp_hands .HAND_CONNECTIONS )
        return img

    def FindPositions(self,img):
        landmark_list =[]
        if not self.results.multi_hand_landmarks:
            return None

        for  hand_no,landmark in enumerate(self.results.multi_hand_landmarks):
            height, width, channel = img.shape
            #selecting any one hand
            if hand_no ==0:
                for i in range(0,len(landmark.landmark)):
                    pos_x, pos_y = int( landmark.landmark[i].x * width ), int( landmark.landmark[i].y * height )
                    # adding  positions of all dots
                    landmark_list.append( {'x': pos_x,'y': pos_y} )
                # if draw:
                #     cv.circle( img, (posx, posy), 10, (22, 0, 0,), cv.FILLED )
        return landmark_list
    # def GetNoOfHands(self):
    #     return NoOfHands
    # def GetHands(self):
    #     return FoundHands
