from dis import dis
from turtle import pos, position
import cv2 as cv
import time
import HandDetectionModule
import math
import  pyautogui
pyautogui.FAILSAFE= False
#Initializing the model
HandDetector = HandDetectionModule.HandDetector(mode=False,MaxHands=1,DetectionConfidence=0.05,TrackConfidence=0.5)

# Camera Setting
cap = cv.VideoCapture(0)
CamWidth ,CamHeight =pyautogui.size().width,pyautogui.size().height
cap.set(3,CamWidth)
cap.set(4,CamHeight)

# fps Variables
CurrentTime =0
PreviousTime = 0
fps = 0

# global variables
current_cursor_pos = {'x':0,'y':0}
prev_cursor_pos = {'x':0,'y':0}

current_thumb_pos={'x':0,'y':0}
current_index_pos={'x':0,'y':0}

ThumbIndex = 4
IndexFingerIndex=8
print(pyautogui.size())
# Threshold Distances
PalmDistance_min = 100 # Distance Between Middle and Palm point
MovementThreshold = 2.5 # Recognize movement Threshold

def GetDistance (Point1,Point2):
   return math.dist(Point1,Point2)

def midpoint(x1, y1, x2, y2) -> int:
    return {'x':(x1 + x2)//2,'y': (y1 + y2)//2}

def makeMovement():
    threshold_dist = math.dist([current_cursor_pos['x'],current_cursor_pos['y']],[prev_cursor_pos['x'],prev_cursor_pos['y']])
    dist =  math.dist([current_thumb_pos['x'],current_thumb_pos['y']],[current_index_pos['x'],current_index_pos['y']])
    x_diff = (current_cursor_pos['x']-prev_cursor_pos['x']) * 5
    y_diff = (current_cursor_pos['y']-prev_cursor_pos['y'])* 4
    if(x_diff > 120 or y_diff > 120):return
    if(dist<15):
        pyautogui.click()
    if(threshold_dist<= MovementThreshold):return;
    pyautogui.moveTo(
        pyautogui.position().x+ x_diff,
        pyautogui.position().y +y_diff,
        0.1,
        pyautogui.easeInQuad)

def main():
    global PreviousTime
    global current_cursor_pos
    global prev_cursor_pos
    global current_thumb_pos
    global current_index_pos
    while cap.isOpened():
        success, image = cap.read()
        image = cv.flip(image,1)
        CurrentTime = time.time()
        if(CurrentTime-PreviousTime)!=0:
            fps = 1 / (CurrentTime - PreviousTime)
        PreviousTime = CurrentTime
        cv.putText( image, str( "FPS: " + str( int( fps ) ) ), (10, 70), cv.FONT_HERSHEY_PLAIN, 2, (225, 50, 225), 2 )
        HandDetector.FindHands( image, True )
        positions = (HandDetector.FindPositions(image))

        if positions:
            thumb= positions[ThumbIndex]
            index = positions[IndexFingerIndex]
            mid_point = midpoint(thumb.get('x'),thumb.get('y'),index.get('x'),index.get('y'))
            prev_cursor_pos = current_cursor_pos
            current_cursor_pos = mid_point
            current_thumb_pos={'x':positions[ThumbIndex]['x'],'y':positions[ThumbIndex]['y']}
            current_index_pos={'x':positions[IndexFingerIndex]['x'],'y':positions[IndexFingerIndex]['y']}
            cv.circle(img=image,center=(mid_point['x'],mid_point['y']),radius=5,color= (225, 50, 225),thickness=-1)
            cv.circle(img=image,center=(current_thumb_pos['x'],current_thumb_pos['y']),radius=5,color= (225, 50, 225),thickness=-1)
            cv.circle(img=image,center=(current_index_pos['x'],current_index_pos['y']),radius=5,color= (225, 50, 225),thickness=-1)
            makeMovement()
        cv.imshow( "Video Viewer", image )
        if cv.waitKey( 5 ) & 0xFF == 27:
            break

if __name__ == '__main__':
    main()