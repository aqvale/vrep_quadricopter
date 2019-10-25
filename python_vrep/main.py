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
        print("Nao encontrado - ", direct)
        return [0.000001, 0.00001]
    elif control >= 23 and control <= 24:
        print("Meio - ", direct)
        return [direct, 0] 
    elif control <= 24:
        print("Direita - ", direct)
        return [direct, -0.02]
    else:
        print("Esquerda - ", direct)
        return [direct, 0.02]   

if __name__ == "__main__":
    #definicoes iniciais
    serverIP = '127.0.0.1'
    serverPort = 19999
    clientID = vrep.simxStart(serverIP,serverPort,True,True,2000,5)

     x_limit = {-8.5, 8.5}
    y_limit = {-9, 9} 
    z_limit = {0, 3}
    
    #Start x = -8.5 y = -9 z = 4   
    START = true
    v_start = 0.02
    x = -8.5
    y = -9
    z = 3
    
    #Search
    SEARCH = false
    vx_search = 0.1
    x_enable = true
    boss = false

    vy_search = 0.04
    y_enable = false
    y_control = 0

    VISION = False
    height = 0

    if clientID != 1:
        print ('Servidor conectado!')

        erro, vSensor = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_blocking)
        erro, target = vrep.simxGetObjectHandle(clientID, 'Quadricopter_target', vrep.simx_opmode_blocking)
        erro, pos = vrep.simxGetObjectPosition(clientID, target, -1, vrep.simx_opmode_streaming)
        image = vrep.simxGetVisionSensorImage(clientID, vSensor, 0, vrep.simx_opmode_streaming)
        obj_ref = 23
        time.sleep(1)
        while vrep.simxGetConnectionId(clientID) != -1:
            erro, pos = vrep.simxGetObjectPosition(clientID, target, -1, vrep.simx_opmode_buffer)
            
            if (SEARCH):
                pos = sim.getObjectPosition(targetObj,-1)
                x = pos[1]
                y = pos[2]
                z = pos[3]
                if (x_enable):
                    if (x < x_limit[1] and vx_search < 0):
                        vx_search = vx_search * (-1)
                        x_enable = false
                        y_enable = true
                    if (x > x_limit[2] and vx_search > 0):
                        vx_search = vx_search * (-1)
                        x_enable = false
                        y_enable = true
                    
                    if (x > -6 and x < 6 and not boss):
                        boss = true
                        vx_search = vx_search * 2.5
                    else
                        if (x <= -6 or x >= 6 and boss):
                            boss = false
                            vx_search = vx_search > 0 and 0.1 or -0.1 
                    x = x + vx_search
                if (y_enable):
                    y = y + vy_search
                    y_control = y_control + 1
                    print(y_control)
                    if (y_control >= 50):
                        y_control = 0
                        y_enable = false
                        x_enable = true
                sim.setObjectPosition(targetObj, -1, {x, y, z})

            if (START):
                pos = sim.getObjectPosition(targetObj,-1)
                if (pos[1] > x_limit[1]):
                    sim.setObjectPosition(targetObj, -1, {pos[1]-v_start, pos[2], pos[3]})
                pos = sim.getObjectPosition(targetObj,-1)
                if (pos[2] > y_limit[1]):
                    sim.setObjectPosition(targetObj, -1, {pos[1], pos[2]-v_start, pos[3]})
                pos = sim.getObjectPosition(targetObj,-1)
                if (pos[3] < z_limit[2]):
                    sim.setObjectPosition(targetObj, -1, {pos[1], pos[2], pos[3]+v_start})
                pos = sim.getObjectPosition(targetObj,-1)
                if (pos[1] <= x_limit[1] and pos[2] <= y_limit[1] and pos[3] >= z_limit[2]):
                    START = false
                    SEARCH = true
                
            error, resolution, image = vrep.simxGetVisionSensorImage(clientID, vSensor, 0, vrep.simx_opmode_buffer)
            if VISION:
                orientation, direction = func(image, obj_ref)
                if orientation == 0 and direction == 0:
                    print("Centro do Objeto")
                    print(image)
                    break 
                if orientation == 0 or direction == 0:
                    height = -0.1
                vrep.simxSetObjectPosition(clientID, target, -1, [pos[0]+orientation, pos[1]+direction, pos[2]+height], vrep.simx_opmode_oneshot)
                height = 0
                time.sleep(0.1)
            
            if START and obj_ref in image:
                START = False
                SEARCH = False
                VISION = True
                vrep.simxSetObjectPosition(clientID, target, -1, [pos[0]-0.5, pos[1], pos[2]], vrep.simx_opmode_oneshot)
            
            if (SEARCH and x >= 8 and y >= 8):
                SEARCH = false
                break

            time.sleep(0.05)    

            
        vrep.simxFinish(clientID) # fechando conexao com o servidor
        print ('Conexao fechada!')
    else:
        print ('Problemas para conectar o servidor!')     