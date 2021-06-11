from Cube import Cube, Cuber, split_cmd, back_cmd

cube = Cube(shuffle=True)
print(cube)

history = []
back_stack = 0

while True:
    cmds = input('돌리기: ')
    cmds_splited = split_cmd(cmds)
    
    if cmds in ['init','초기화','ㅑㅜㅑㅅ','chrlghk']:
        cube.init()
    elif cmds in ['shuffle','섞기','노ㅕㄹ릳','tjRrl','shuf']:
        cube.shuffle()
    elif cmds in ['fit', '맞춰', '럇', 'akwcnj']:
        Cuber().fit(cube)
    elif cmds in ['back','뒤로','ㅠㅁ차','enlfh']:
        if not back_stack+1 <= len(history):
            continue
        back_stack += 1
        backcmd = back_cmd(history[-back_stack])
        print('back ->', ' '.join(backcmd))
        cube.turn(backcmd, False)
    elif cmds in ['redo','앞으로','ㄱㄷ애','dkvdmfh']:
        if not 0 <= back_stack-1 < len(history):
            continue
        redocmd = history[-back_stack]
        print('redo ->', ' '.join(redocmd))
        cube.turn(redocmd, False)
        back_stack -= 1
    else:
        cube.turn(cmds_splited)
        if back_stack > 0:
            history = history[:-back_stack]
        history.append(cmds_splited)
        back_stack = 0

    print(cube)