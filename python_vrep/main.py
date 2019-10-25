import vrep
import time

def func(v, ref):
    front = v[384:]
    back = v[:384]
    control = 0
    direct = None
    searched = 0
    if ref in front:
        control = 0
        direct = 0.02
        while True:
            control += 1
            valor = front.pop()
            if ref == valor:
                searched += 1
                if searched >= 3:
                    break
            else:
                searched = 0
            if control == 48:
                control = 0
                searched = 0
            if len(front) == 0:
                control = 0
                searched = 0
                break
    if ref in back: 
        control = 0
        direct = -0.02 if not direct else 0
        while True:
            control += 1
            valor = back.pop()
            if ref == valor:
                searched += 1
                if searched >= 3:
                    break
            else:
                searched = 0
            if control == 48:
                control = 0
                searched = 0
            if len(back) == 0:
                control = 0
                searched = 0
                break
    if control == 0:
        #print("Nao encontrado - ", direct)
        return [-1, -1]
    elif control >= 23 and control <= 24:
        #print("Meio - ", direct)
        return [direct, 0] 
    elif control <= 24:
        #print("Direita - ", direct)
        return [direct, -0.02]
    else:
        #print("Esquerda - ", direct)
        return [direct, 0.02]   

if __name__ == "__main__":
    #definicoes iniciais
    serverIP = '127.0.0.1'
    serverPort = 19999
    clientID = vrep.simxStart(serverIP,serverPort,True,True,2000,5)

    x_limit = [-8.5, 8.5]
    y_limit = [-9, 9] 
    z_limit = [0, 3]
    
    #Start x = -8.5 y = -9 z = 4   
    START = True
    v_start = 0.08
    x = -8.5
    y = -9
    z = 3
    
    #Search
    SEARCH = False
    v_min = 0.1
    vx_search = v_min
    x_enable = True
    boss = False

    vy_search = 0.1
    y_enable = False
    y_control = 0

    VISION = False
    height = 0
    msg = ''
    if clientID != 1:
        print ('Servidor conectado!')

        erro, vSensor = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_blocking)
        erro, targetObj = vrep.simxGetObjectHandle(clientID, 'Quadricopter_target', vrep.simx_opmode_blocking)
        erro, pos = vrep.simxGetObjectPosition(clientID, targetObj, -1, vrep.simx_opmode_streaming)
        image = vrep.simxGetVisionSensorImage(clientID, vSensor, 0, vrep.simx_opmode_streaming)
        obj_ref = 23
        time.sleep(1)
        while vrep.simxGetConnectionId(clientID) != -1:
            
            if (SEARCH):
                erro, pos = vrep.simxGetObjectPosition(clientID, targetObj, -1, vrep.simx_opmode_buffer)
                x = pos[0]
                y = pos[1]
                z = pos[2]
                if (x_enable):
                    if (x < x_limit[0] and vx_search < 0):
                        vx_search = vx_search * (-1)
                        x_enable = False
                        y_enable = True
                    if (x > x_limit[1] and vx_search > 0):
                        vx_search = vx_search * (-1)
                        x_enable = False
                        y_enable = True
                    
                    if (x > -7 and x < 7 and not boss):
                        boss = True
                        vx_search = vx_search * 3
                    else:
                        if (x <= -7 or x >= 7 and boss):
                            boss = False
                            vx_search = vx_search > 0 and v_min or -v_min 
                    x = x + vx_search
                if (y_enable):
                    y = y + vy_search
                    y_control = y_control + 1
                    if (y_control >= 45):
                        y_control = 0
                        y_enable = False
                        x_enable = True
                vrep.simxSetObjectPosition(clientID, targetObj, -1, [x, y, z], vrep.simx_opmode_oneshot)
                time.sleep(0.05)

            if (START):
                erro, pos = vrep.simxGetObjectPosition(clientID, targetObj, -1, vrep.simx_opmode_buffer)
                if pos[2] < z_limit[1]:
                    x = pos[0]
                    y = pos[1]
                    z = pos[2]+v_start
                else:
                    x = pos[0]-v_start if pos[0] > x_limit[0] else pos[0]
                    y = pos[1]-v_start if pos[1] > y_limit[0] else pos[1]
                    z = pos[2]
                vrep.simxSetObjectPosition(clientID, targetObj, -1, [x, y, z], vrep.simx_opmode_oneshot)
                if (pos[0] <= x_limit[0] and pos[1] <= y_limit[0] and pos[2] >= z_limit[1]):
                    START = False
                    SEARCH = True
                
            error, resolution, image = vrep.simxGetVisionSensorImage(clientID, vSensor, 0, vrep.simx_opmode_buffer)
            if VISION:
                erro, pos = vrep.simxGetObjectPosition(clientID, targetObj, -1, vrep.simx_opmode_buffer)
                if pos[2] <= 0.5:
                    msg = "Achou o objeto"
                    break
                orientation, direction = func(image, obj_ref)
                if orientation != -1 and direction != -1:
                    if orientation == 0 and direction == 0:
                        print("Centro do Objeto")
                        break 
                    if orientation == 0 or direction == 0:
                        height = -0.1
                    vrep.simxSetObjectPosition(clientID, targetObj, -1, [pos[0]+orientation, pos[1]+direction, pos[2]+height], vrep.simx_opmode_oneshot)
                    height = 0
                    time.sleep(0.1)
                else:
                    print(pos[0]+vx_search)
                    vrep.simxSetObjectPosition(clientID, targetObj, -1, [pos[0]+vx_search, pos[1], pos[2]], vrep.simx_opmode_oneshot)
            
            if obj_ref in image:
                START = False
                SEARCH = False
                VISION = True
                vrep.simxSetObjectPosition(clientID, targetObj, -1, [pos[0], pos[1], pos[2]], vrep.simx_opmode_oneshot)
                vx_search = -0.01 if vx_search > 0 else 0.01
            
            if (SEARCH and x >= 8 and y >= 8):
                SEARCH = False
                break

            time.sleep(0.05)    

            
        vrep.simxFinish(clientID) # fechando conexao com o servidor
        print (msg)
    else:
        print ('Problemas para conectar o servidor!')     