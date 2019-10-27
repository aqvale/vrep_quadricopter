import time

from util import vrep
from scene.scene_map import SceneMap

class Quadricopter():
    _serverIp   = None
    _serverPort = None
    _refObj     = None
    _clientID   = None
    target      = None
    vision      = None
    sonar       = None
    vMin        = None

    _objFound   = None
    msg         = ''

    def __init__(self, refObj, _serverIp:str = '127.0.0.1' , _serverPort:int = 19999, vMin:float = 0.1):
        self._serverIp     = _serverIp
        self._serverPort   = _serverPort  
        self._refObj       = refObj
        self.vMin          = vMin
        self._clientID     = self._startServer()
        self.target        = self._createTargetControl()
        self.vision        = self._createVisionSensor()
        self.sonar         = self._createSonarSensor()
    
    def _createTargetControl(self):
        return Quadricopter.TargetControl(self._clientID)

    def _createVisionSensor(self):
        return Quadricopter.VisionSensor(self._clientID)

    def _createSonarSensor(self):
        return Quadricopter.SonarSensor(self._clientID)

    def _startServer(self) -> bool:
        return vrep.simxStart(self._serverIp, self._serverPort, True, True, 2000,5)

    def _finishServer(self):
        vrep.simxFinish(self._clientID)

    def startPosition(self, vStart, sMap: SceneMap):
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
            
    def searchObj(self, sMap: SceneMap):
        v = 0
        y_control = 0
        xEnable = True
        yEnable = False
        boss = False
        while vrep.simxGetConnectionId(self._clientID) != -1:
            x, y, z = self.target.getPosition()
            if x >= (sMap.xMin) and y >= (sMap.yMax):
                break 
            
            if xEnable:
                if (x < sMap.xMin and self.vMin < 0) or (x > sMap.xMax and self.vMin > 0):
                    self.vMin = self.vMin * (-1)
                    xEnable = False
                    yEnable = True
                
                if (x > sMap.xMin+1 and x < sMap.xMax-1 and not boss):
                    boss = True
                else:
                    if (x <= sMap.xMin+1 or x >= sMap.xMax-1 and boss):
                        boss = False
                v = self.vMin*4 if boss else self.vMin
                x = x + v
            if yEnable:
                y = y + 0.1
                y_control = y_control + 1
                if (y_control >= 40):
                    y_control = 0
                    yEnable = False
                    xEnable = True
            self.target.setPosition(x, y, z)
            time.sleep(0.1)

            image = self.vision.getImage()
            if self._refObj in image:
                self._objFound = True
                self.vMin = self.vMin/10
                return
        self._objFound = False
        self.msg = 'Object not found!'

    def land(self, sMap: SceneMap):
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
                if orientation == 0 and direction == 0 and z <= sMap.zMin:
                    self.msg = "Find the object! He is below."
                    return True 
                
                if orientation == 0 or direction == 0:
                    height = -0.01

                if z <= sMap.zMax/2:
                    height = height*10
                    self.vMin = self.vMin/10
                
                if not self.sonar.getStateColision():
                    self.target.setPosition((x+orientation), (y+direction), (z+height))
                else:
                    self.msg = "Find the object! He is below. Dangerous airfield!"
                    return True
                    
                height = 0
                notFound = 0
            else:
                self.target.setPosition((x-self.vMin), y, z)
                notFound += 1
            
            if notFound > 500:
                self.msg = "Lose object"
                self.vMin = self.vMin * 10
                return False
            time.sleep(0.15)

    class VisionSensor():
        id          = None
        _clientID   = None
        resolution  = None
        line        = None
        half        = None


        def __init__(self, clientID):
            self.id = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_blocking)[1]
            self._clientID = clientID
            vrep.simxGetVisionSensorImage(clientID, self.id, 0, vrep.simx_opmode_streaming)
            time.sleep(0.5)

        def getImage(self):
            if not self.resolution:
                error, res, image = vrep.simxGetVisionSensorImage(self._clientID, self.id, 0, vrep.simx_opmode_buffer)
                self.resolution = res[0]
                self.line = self.resolution * 3
                self.half = int(self.line*self.resolution/2)
                return image
            return vrep.simxGetVisionSensorImage(self._clientID, self.id, 0, vrep.simx_opmode_buffer)[2]

        def getPositionObject(self, image, refObj) -> list:
            front = image[self.half:]
            back = image[:self.half]
            control = 0
            orientation = None
            searched = 0
            v = 0.02
            if refObj in front:
                control = 0
                orientation = v
                while True:
                    control += 1
                    valor = front.pop()
                    if refObj == valor:
                        searched += 1
                        if searched >= 3:
                            break
                    else:
                        searched = 0
                    
                    if control == self.line:
                        control = 0
                        searched = 0
                    
                    if len(front) == 0:
                        control = 0
                        searched = 0
                        break
            
            if refObj in back: 
                control = 0
                orientation = -v if not orientation else 0
                while True:
                    control += 1
                    valor = back.pop()
                    if refObj == valor:
                        searched += 1
                        if searched >= 3:
                            break
                    else:
                        searched = 0
                    
                    if control == self.line:
                        control = 0
                        searched = 0
                    
                    if len(back) == 0:
                        control = 0
                        searched = 0
                        break
            
            if control == 0:
                return [-1, -1]
            elif control >= ((self.line/2) -4) and control <= self.line/2:
                return [orientation, 0] 
            elif control <= self.line/2:
                return [orientation, -v]
            else:
                return [orientation, v]   

    class TargetControl():
        id         = None
        _clientID  = None
        
        def __init__(self, clientID):
            self.id = vrep.simxGetObjectHandle(clientID, 'Quadricopter_target', vrep.simx_opmode_blocking)[1]
            self._clientID = clientID
            vrep.simxGetObjectPosition(self._clientID, self.id, -1, vrep.simx_opmode_streaming)
            time.sleep(0.5)

        def getPosition(self):
            return vrep.simxGetObjectPosition(self._clientID, self.id, -1, vrep.simx_opmode_buffer)[1]

        def setPosition(self, x, y, z):
            vrep.simxSetObjectPosition(self._clientID, self.id, -1, [x, y, z], vrep.simx_opmode_oneshot)

    class SonarSensor():
        id         = None
        _clientID  = None

        def __init__(self, clientID):
            self.id = vrep.simxGetObjectHandle(clientID, 'Proximity_sensor', vrep.simx_opmode_blocking)[1]
            self._clientID = clientID
            vrep.simxReadProximitySensor(self._clientID, self.id, vrep.simx_opmode_streaming)
            time.sleep(0.5)

        def getStateColision(self):
            return vrep.simxReadProximitySensor(self._clientID, self.id, vrep.simx_opmode_buffer)[1]