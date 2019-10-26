from util import vrep
import time

class ScenaMap():
    xMin = None
    xMax = None
    yMin = None
    yMax = None
    zMin = None
    zMax = None

    def __init__(self, xMin, xMax, yMin, yMax, zMin, zMax):
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
        self.zMin = zMin
        self.zMax = zMax

class Quadricopter():
    _serverIp   = None
    _serverPort = None
    _refObj     = None
    _clientID   = None
    target      = None
    vision      = None
    vMin        = None

    _objFound   = False
    msg         = ''

    def __init__(self, _serverIp, _serverPort, refObj, vMin:float = 0.1):
        self._serverIp     = _serverIp
        self._serverPort   = _serverPort  
        self._refObj       = refObj
        self.vMin          = vMin
        self._clientID     = self._startServer()
        self.target        = self._createTargetControl()
        self.vision        = self._createVisionSensor()
    
    def _createTargetControl(self):
        return Quadricopter.TargetControl(self._clientID)

    def _createVisionSensor(self):
        return Quadricopter.VisionSensor(self._clientID)

    def _startServer(self) -> bool:
        return vrep.simxStart(self._serverIp, self._serverPort, True, True, 2000,5)

    def _finishServer(self):
        vrep.simxFinish(self._clientID)

    def startPosition(self, vStart, sMap: ScenaMap):
        pos = self.target.getPosition()
        x = sMap.xMin
        y = sMap.yMin
        z = sMap.zMax
        while not (pos[0] <= x and pos[1] <= y and pos[2] >= z):
            if pos[2] < z:
                xNew = pos[0]
                yNew = pos[1]
                zNew = pos[2] + vStart
            else:
                xNew = pos[0] - vStart if pos[0] > x else pos[0]
                yNew = pos[1] - vStart if pos[1] > y else pos[1]
                zNew = pos[2]
            
            self.target.setPosition(xNew, yNew, zNew)
            time.sleep(0.05)
            
            image = self.vision.getImage()
            if self._refObj in image:
                self._objFound = True
                break
            
            pos = self.target.getPosition()
            
    def searchObj(self, sMap: ScenaMap):
        v = 0
        xEnable = True
        yEnable = False
        boss = False
        while vrep.simxGetConnectionId(self._clientID) != -1:
            x, y, z = self.target.getPosition()
            if x >= (sMap.xMax -1) and y >= (sMap.yMax - 1):
                break 
            
            if xEnable:
                if (x < sMap.xMin and self.vMin < 0):
                    self.vMin = self.vMin * (-1)
                    xEnable = False
                    yEnable = True
                
                if (x > sMap.xMax and self.vMin > 0):
                    self.vMin = self.vMin * (-1)
                    xEnable = False
                    yEnable = True
                
                if (x > -7 and x < 7 and not boss):
                    boss = True
                    v = self.vMin * 3
                else:
                    if (x <= -7 or x >= 7 and boss):
                        boss = False
                        v = self.vMin if self.vMin > 0 else -self.vMin 
                x = x + v
            
            if yEnable:
                y = y + abs(self.vMin)
                y_control = y_control + 1
                if (y_control >= 45):
                    y_control = 0
                    yEnable = False
                    xEnable = True
            self.target.setPosition(x, y, z)
            time.sleep(0.1)

            image = self.vision.getImage()
            if self._refObj in image:
                self._objFound = True
                return True
        return False
    
    def land(self, sMap: ScenaMap):
        height = 0
        notFound = 0
        while True:
            x, y, z = self.target.getPosition()
            if z <= sMap.zMin:
                self.msg = "Find the object! He is below."
                return True
            
            image = self.vision.getImage()
            orientation, direction = self.vision.getPositionObject(image, self._refObj)
            if orientation != -1 and direction != -1:
                if orientation == 0 and direction == 0:
                    self.msg = "Find the object! Object center, he is below"
                    return True 
                
                if orientation == 0 or direction == 0:
                    height = -0.1
                
                self.target.setPosition((x+orientation), (y+direction), (z+height))
                height = 0
                notFound = 0
            else:
                self.target.setPosition((x-self.vMin), y, z)
                notFound += 1
            
            if notFound > 20:
                self.msg = "Lose object"
                return False
            time.sleep(0.15)

    class VisionSensor():
        vSensor     = None
        resolution  = None
        _clientID   = None

        def __init__(self, clientID):
            self.vSensor = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_blocking)[1]
            self._clientID = clientID

        def getImage(self):
            error, self.resolution, image = vrep.simxGetVisionSensorImage(self._clientID, self.vSensor, 0, vrep.simx_opmode_buffer)
            return image

        def getPositionObject(self, image, refObj) -> list:
            line = self.resolution * 3
            front = image[line*self.resolution/2:]
            back = image[:line*self.resolution/2]
            
            control = 0
            direction = None
            searched = 0
            v = 0.02
            if refObj in front:
                control = 0
                direction = v
                while True:
                    control += 1
                    valor = front.pop()
                    if refObj == valor:
                        searched += 1
                        if searched >= 3:
                            break
                    else:
                        searched = 0
                    
                    if control == line:
                        control = 0
                        searched = 0
                    
                    if len(front) == 0:
                        control = 0
                        searched = 0
                        break
            
            if refObj in back: 
                control = 0
                direction = -v if not direction else 0
                while True:
                    control += 1
                    valor = back.pop()
                    if refObj == valor:
                        searched += 1
                        if searched >= 3:
                            break
                    else:
                        searched = 0
                    
                    if control == line:
                        control = 0
                        searched = 0
                    
                    if len(back) == 0:
                        control = 0
                        searched = 0
                        break
            
            if control == 0:
                return [-1, -1]
            elif control >= ((line/2) -1) and control <= line/2:
                return [direction, 0] 
            elif control <= line/2:
                return [direction, -v]
            else:
                return [direction, v]   

    class TargetControl():
        targetObj  = None
        _clientID  = None
        
        def __init__(self, clientID):
            self.targetObj = vrep.simxGetObjectHandle(clientID, 'Quadricopter_target', vrep.simx_opmode_blocking)[1]
            self._clientID = clientID

        def getPosition(self):
            return vrep.simxGetObjectPosition(self._clientID, self.targetObj, -1, vrep.simx_opmode_buffer)[1]

        def setPosition(self, x, y, z):
            vrep.simxSetObjectPosition(self._clientID, self.targetObj, -1, [x, y, z], vrep.simx_opmode_oneshot)