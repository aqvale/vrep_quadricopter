from drone.quadricopter import Quadricopter
from scene.scene_map import SceneMap


if __name__ == "__main__":
    sMap = SceneMap(-10.5, 10, -9, 10, 0.5, 3)
    quadricopter = Quadricopter(23)
    if quadricopter._clientID != -1:
        print("Serve Connect!")
        quadricopter.startPosition(0.1, sMap)
        while not isinstance(quadricopter._objFound, bool):
            quadricopter.searchObj(sMap)
        while quadricopter._objFound:
            if quadricopter.land(sMap):
                print(quadricopter.msg)
                break
            else:
                quadricopter.searchObj(sMap)
                print(quadricopter.msg)
        else:
            print(quadricopter.msg)
    else:
        print("Serve offline!")