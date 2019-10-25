def func(v):
    front = v[384:]
    back = v[:384]
    control = 0
    ref = 0.090196080505848
    direct = ''
    if ref in front:
        direct = 'Front'
        while True:
            control += 1
            valor = front.pop()
            if ref == valor:
                break
            if control == 48:
                control = 0
            if len(front) == 0:
                control = 0
                break
    if ref in back:
        direct = 'Back'
        while True:
            control += 1
            valor = back.pop()
            if ref == valor:
                import pdb; pdb.set_trace()
                break
            if control == 48:
                control = 0
            if len(back) == 0:
                control = 0
                break
    if control == 0:
        print("Nao encontrado - ", direct)
    elif control >= 23 and control <= 24:
        print("Meio - ", direct)
    elif control <= 24:
        print("Direita - ", direct)
    else:
        print("Esquerda - ", direct)