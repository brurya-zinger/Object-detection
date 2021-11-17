from datetime import datetime
def timer():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    return(current_time)

list = []
class LaneRange:
    def __init__(self, x1, x2,y1,y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.x=range(x1,x2)
        self.y=range(y1,y2)
        self.counter=0

    def addtocount(self):
        self.counter+1

def RaiseCounter(laneId):
   list[laneId].counter=list[laneId].counter+1
   # print(list[laneId].counter,laneId)



def creatList():
    # A list of directions in which each member contains the range of the his  direction
    list.append(LaneRange(151,539,588,657))
    list.append(LaneRange(1318, 1381, 639, 806))  
    list.append(LaneRange(1762, 1790, 551, 649))  

    list.append(LaneRange(1275,1286, 543,596 )) 

    list.append(LaneRange(533,1002, 887, 969))  
   
    list.append(LaneRange(540,675, 720, 738))  
    list.append(LaneRange(41, 191, 495, 593)) 
   
    list.append(LaneRange(1002, 1279, 445, 473)) 

    return ""


#center of the object
def pega_centro(x, y, w, h):
    cx = (x + x + w) // 2
    cy = (y + y + h) // 2
    # x1 = int(w / 2)
    # y1 = int(h / 2)
    #
    # cx = x + x1
    # cy = y + y1
    return cx, cy
# Path calculation
def pathCalculation(cx,cy):
    print("befor for",cx, cy)
    for obj in list:
         if cx in obj.x:
             if  cy in obj.y:
                print(list.index(obj))
                return list.index(obj)
    return -1
def printList():
    for obj in list:
        print(list.index(obj),obj.counter, sep =' ')
