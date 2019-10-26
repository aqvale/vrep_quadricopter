from drone.quadricopter import Quadricopter, ScenaMap

if __name__ == "__main__":
    serverIP = '127.0.0.1'
    serverPort = 19999
    sMap = ScenaMap(-9, 9, -9, 9, 0.5, 3)
    quadricopter = Quadricopter(serverIP, serverPort, 23)
    quadricopter.startPosition(0.08, sMap)  
    while not isinstance(quadricopter._objFound, bool):
        quadricopter.searchObj(sMap)

    if quadricopter._objFound:
        if quadricopter.land(sMap):
            print(quadricopter.msg)
        else:
            print(quadricopter.msg)
    else:
        print("Objeto não encontrado!")