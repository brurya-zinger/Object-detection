import cv2
import xlsxwriter
import lane
import numpy as np
from time import sleep
from tracker import *

net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
ln = net.getLayerNames()
output_layers_names = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
classes = []
with open('coco.txt', 'r') as f:
    classes = f.read().splitlines()
# Create tracker object
tracker = EuclideanDistTracker()
pathOut = 'roads_v2.mp4'
cap = cv2.VideoCapture('videoThursday0.mp4')


frame_list = []
out = None
fps = 25.0

object_detector = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=100)
counterWrite = 2


offset = 6
detec = []
delay = 60


id =''
ids = []
#Initialize a list
lane.creatList()
# create a excel sheet 
workbook = xlsxwriter.Workbook('result.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Hour')
worksheet.write('B1', 'TrackingId')
worksheet.write('C1', 'LaneId')
worksheet.write('D1', 'Type')

while True:
    _, img = cap.read()
    detections = []

    if hasattr(img, 'shape') == True:
        tempo = float(1 / delay)
        # sleep(tempo)
        height, width, _ = img.shape
        # build the data (blob)  from the input image and then forward to  YOLO object detector,
        #giving us our bounding boxes and the confidences  that it is the correct detection
       
 
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (256, 256),
                                     swapRB=True, crop=False)
        #  the *output* layer names that we need from YOLO
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        net.setInput(blob)
        layerOutputs = net.forward(ln)
        # initialize our lists of detected bounding boxes, confidences, and
        # class IDs
        boxes = []
        confidences = []
        class_ids = []
        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence of
                # the current object detection
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                # filter out weak predictions by ensuring the detected
                # probability is greater than 50%
                if confidence > 0.5:
                    # scale the bounding box coordinates
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, w, h])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)
                    # detections.append([x, y, w, h])

        #Create the lines that were intended to count the vehicles in each direction
        cv2.line(img, (539 ,  657), (151 ,  588), (255, 255, 255), thickness=3)  # white, no 0
        cv2.line(img, (1381 ,  639), (1318  , 806), (100, 0, 255), thickness=3)  #
        cv2.line(img, (1790  , 551), (1762,   649), (0, 255, 255), thickness=3)  # 6,7 =     2
        cv2.line(img, (1275 ,  543), (1286 ,  596), (207, 59, 93), thickness=3)  # no 3
        cv2.line(img, (1002,   969), (533  , 887), (222, 100, 93), thickness=3)  # no  4,5,6      4
        cv2.line(img, (675  , 738), (540  , 720), (207, 59, 93), thickness=3)  # no 12             5
        cv2.line(img, (191  , 495), (41 ,  593), (0, 255, 255), thickness=3)  # yellow no,13        6
        cv2.line(img, (1002 ,  445), (1279 ,   473), (255, 255, 255), thickness=3)  # white no 17        7


        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
# Creating the rectangle of object boundaries,add the class name,id(from the tracker
#To count cars that have not yet been counted and are not tracked
        font = cv2.FONT_HERSHEY_PLAIN
        colors = np.random.uniform(0, 255, size=(len(boxes), 3))
        # ensure at least one detection exists
        if len(indexes) != 0:
            # Object Tracking
            boxes_ids = tracker.update(boxes)
            # loop over the indexes we are keeping
            for i in indexes.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                id = boxes_ids[i]
                # print("ids ",ids)
                label = str(classes[class_ids[i]])

                confidence = str(round(confidences[i], 2))
                color = colors[i]
                # draw a bounding box rectangle and label on the image
                cv2.rectangle(img, (x, y), (x + w, y + h), (0,5,0), 2)
                cv2.putText(img, label + " "+str(id) , (x, y + 20), font, 2, (255, 255, 255), 2)

                # Path calculation
                #get the  central point of the object
                centro = lane.pega_centro(x, y, w, h)
                #detec.append(centro)

                if label == 'car' or label == 'truck' or label == 'bus' or label == 'motorcycle' :


                    if id not in ids:#the ID has not yet been counted
                        #print("in if")
                        #By the center point of the object we  calculated in which direction the object is located
                        laneId = lane.pathCalculation(centro[0],centro[1])
                        print("lane id  ", laneId)
                        if laneId!=-1:
                            ids.append(id)
                            lane.RaiseCounter(laneId)
                            #add the data to the excel sheet 
                            worksheet.write('A'+str(counterWrite), str(lane.timer()))
                            worksheet.write('B' + str(counterWrite), id)
                            worksheet.write('C'+str(counterWrite), laneId)
                            worksheet.write('D'+str(counterWrite), label)
                            counterWrite+=1
                            #For the visuals while running we will create a red circle that will appear during the count
                            cv2.circle(img, centro, 4, (0, 0, 255), 3)
                            

        frame_list.append(img)
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        img = cv2.resize(img, (1920, 1080))
        cv2.imshow('Image', img)

        size = (width, height)
        key = cv2.waitKey(1)
        if key == 27:
            break

    if hasattr(img, 'shape') == False:
        break
out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
for i in range(len(frame_list)):
    # writing to a image array
    out.write(frame_list[i])
cap.release()
out.release()
cv2.destroyAllWindows()
lane.printList()
workbook.close()


