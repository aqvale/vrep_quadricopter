from util import vrep

class ScenaMap():
    x_min = None
    x_max = None
    y_min = None
    y_max = None
    z_min = None
    z_max = None

    def __init__(self, x_min, x_max, y_min, y_max, z_min, z_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max

class Quadricopter():
    _server_ip    = None
    _server_port  = None
    _client_id    = None
    scena_map     = None

    def __init__(self, _server_ip, _server_port, x_min, x_max, y_min, y_max, z_min, z_max):
        self._server_ip = _server_ip
        self._server_port = _server_port
        self.scena_map = ScenaMap(x_min, x_max, y_min, y_max, z_min, z_max)

    def _start_server(self) -> bool:
        self._client_id = vrep.simxStart(self.server_ip, self.server_port, True, True, 2000,5)
        return True if self._client_id != 1 else False

    def _finish_server(self):
        vrep.simxFinish(self._client_id)

    def _start_position(self)

    def get_position_object(image, res, obj_value) -> list:
        line = res * 3
        front = v[line*res/2:]
        back = v[:line*res/2]
        
        control = 0
        direction = None
        searched = 0
        if ref in front:
            control = 0
            direction = 0.02
            while True:
                control += 1
                valor = front.pop()
                if ref == valor:
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
        if ref in back: 
            control = 0
            direction = -0.02 if not direction else 0
            while True:
                control += 1
                valor = back.pop()
                if ref == valor:
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
            #print("Nao encontrado - ", direction)
            return [-1, -1]
        elif control >= ((line/2) -1) and control <= line/2:
            #print("Meio - ", direction)
            return [direction, 0] 
        elif control <= line/2:
            #print("Direita - ", direction)
            return [direction, -0.02]
        else:
            #print("Esquerda - ", direction)
            return [direction, 0.02]   