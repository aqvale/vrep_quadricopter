from drone.quadricopter import Quadricopter, SceneMap

if __name__ == "__main__":
    serverIp = '127.0.0.1'
    serverPort = 19999
    sMap = SceneMap(-10, 10, -9, 9, 0.5, 3)
    quadricopter = Quadricopter(serverIp, serverPort, 23)
    if quadricopter._clientID != -1:
        print("Serve Connect!")
        quadricopter.startPosition(0.08, sMap)
        while not isinstance(quadricopter._objFound, bool):
            quadricopter.searchObj(sMap)
        if quadricopter._objFound:
            if quadricopter.land(sMap):
                print(quadricopter.msg)
            else:
                print(quadricopter.msg)
        else:
            print(quadricopter.msg)
    else:
        print("Serve offline!")