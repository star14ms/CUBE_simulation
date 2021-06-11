import numpy as np
from util import bcolors, rotate_2dim_array as rotate
import random

np.set_printoptions(linewidth=np.inf, formatter={
    'all':lambda x: (bcolors.set_by_cube_id(x) + str(x) + bcolors.set_original())})

def _turn(target, cmd, sides):
    cmd_0 = cmd.lower()[0]
    side0, side1, side2 = sides[0].lower(), sides[1].lower(), sides[2].lower()
    lower_cmd = True if cmd[0] in ['u','d','r','l','f','b'] else False
    
    height = 0 if cmd_0==side0 else 1 if cmd_0==side1 else 2
    
    if ("'" in cmd and (cmd_0==side0 or (not cmd_0==side1 and not cmd_0==side2))) or (
        not "'" in cmd and (not cmd_0==side0 and (cmd_0==side1 or cmd_0==side2))
    ):
        move = -6 if '2' in cmd else -3
    else:
        move = 6 if '2' in cmd else 3
    
    part1, part2 = target[height][move:], target[height][:move]
    target[height] = np.r_[part1, part2]
    
    if lower_cmd: 
        part3, part4 = target[1][move:], target[1][:move]
        target[1] = np.r_[part3, part4]
    
    return target


def _split_cmd(cmds):
    splited_cmds = []
    cmd_start = None
    for idx, cmd in enumerate(cmds):
        if cmd in ['U','E','D','R','M','L','F','S','B','x','y','z','u','d','r','l','f','b']:
            if cmd_start == None:
                cmd_start = idx
            else:
                splited_cmds.append(cmds[cmd_start:idx])
                cmd_start = idx
        elif cmd != ' ':
            return [cmd, '?']

    splited_cmds.append(cmds[cmd_start:])

    return splited_cmds


def back_cmd(cmds):
    back_cmds = []
    splited_cmds = _split_cmd(cmds)
    
    for cmd in reversed(splited_cmds):
        if "'" in cmd:
            new_cmd = cmd.replace("'","")
        elif "2" not in cmd:
            new_cmd = cmd + "'"
        else:
            new_cmd = cmd
        
        back_cmds.append(new_cmd)
    
    return back_cmds


class Cube():
    def __init__(self):
        self.D = np.full([3, 3], 0, dtype=np.int)
        self.L = np.full([3, 3], 1, dtype=np.int)
        self.F = np.full([3, 3], 2, dtype=np.int)
        self.R = np.full([3, 3], 3, dtype=np.int)
        self.B = np.full([3, 3], 4, dtype=np.int)
        self.U = np.full([3, 3], 5, dtype=np.int)
        self.side = {'D':self.D, 'L':self.L, 'F':self.F, 'R':self.R, 'B':self.B, 'U':self.U}
    
    
    def init(self):
        self.__init__()


    def __str__(self, tile=True, help_line=False):
        if tile:
            text = ''
            mid_sides = np.concatenate([self.L, self.F, self.R, self.B], axis=1)
            
            for i in range(3):
                text += '  '*(2-i)+'↙'+'  '*i+' ' if help_line else '      '
                for j in range(3):
                    text = text + bcolors.tile_by_cube_id(self.U[i][j])
                text += ' '+'  '*i+'↘'+'\n'  if help_line else '\n'
            for i in range(3):
                for j in range(12):
                    text = text + bcolors.tile_by_cube_id(mid_sides[i][j])
                text += '\n'
            for i in range(3):
                text += '  '*i+'↖'+'  '*(2-i)+' ' if help_line else '      '
                for j in range(3):
                    text = text + bcolors.tile_by_cube_id(self.D[i][j])
                text += ' '+'  '*(2-i)+'↗'+'\n'  if help_line else '\n'
            
            return text
        else: 
            return '\n' + \
            '       ' + str(self.U[0]) + '\n' + '       ' + str(self.U[1]) + '\n' + '       ' + str(self.U[2]) + '\n' + \
            str(np.concatenate([self.L, self.F, self.R, self.B], axis=1)) + '\n' + \
            '       ' + str(self.D[0]) + '\n' + '       ' + str(self.D[1]) + '\n' + '       ' + str(self.D[2])


    def turn(self, cmds, print_each_turn=False):
        if '?' in cmds: return
        if type(cmds) == str:
            cmds = _split_cmd(cmds.replace('"',"'"))

        for cmd in cmds:
            
            cmd_0 = cmd[0].upper()
            
            if cmd_0 in ['U','E','D']:
                target = np.concatenate([self.L, self.F, self.R, self.B], axis=1)

                target = _turn(target, cmd, sides=['U','E','D'])
                self.L, self.F, self.R, self.B = np.hsplit(target, [3, 6, 9])

                if cmd_0=='U':
                    self.U = rotate(self.U, (-1 if "'" in cmd else 2 if '2' in cmd else 1))
                if cmd_0=='D':
                    self.D = rotate(self.D, (-1 if "'" in cmd else 2 if '2' in cmd else 1))

            if cmd_0 in ['R','M','L']:
                target = np.concatenate([rotate(self.B, 1), rotate(self.U, -1), rotate(self.F, -1), rotate(self.D, -1)], axis=1)
                
                target = _turn(target, cmd, sides=['R','M','L'])
                B, U, F, D = np.hsplit(target, [3, 6, 9])
                self.B, self.U, self.F, self.D = rotate(B, -1), rotate(U, 1), rotate(F, 1), rotate(D, 1)

                if cmd_0=='L':
                    self.L = rotate(self.L, (-1 if "'" in cmd else 2 if '2' in cmd else 1))
                if cmd_0=='R':
                    self.R = rotate(self.R, (-1 if "'" in cmd else 2 if '2' in cmd else 1))

            if cmd_0 in ['F','S','B']:
                target = np.concatenate([rotate(self.R, 1), rotate(self.U, 2), rotate(self.L, -1), self.D], axis=1)
                
                target = _turn(target, cmd, sides=['F','S','B'])
                R, U, L, D = np.hsplit(target, [3, 6, 9])
                self.R, self.U, self.L, self.D = rotate(R, -1), rotate(U, 2), rotate(L, 1), D

                if cmd_0=='F':
                    self.F = rotate(self.F, (-1 if "'" in cmd else 2 if '2' in cmd else 1))
                if cmd_0=='B':
                    self.B = rotate(self.B, (-1 if "'" in cmd else 2 if '2' in cmd else 1))

            if cmd_0 in ['X','Y','Z']:
                if cmd_0=='X':
                    (self.D, self.L, self.F, self.R, self.B, self.U) = \
                        (self.F, rotate(self.L, 1), self.U, rotate(self.R, -1), rotate(self.D, 2), rotate(self.B, 2)) \
                    if "'" in cmd else \
                        (rotate(self.B, 2), rotate(self.L, -1), self.D, rotate(self.R, 1), rotate(self.U, 2), self.F)
                
                elif cmd_0=='Y':
                    (self.D, self.L, self.F, self.R, self.B, self.U) = \
                        (rotate(self.D, 1), self.B, self.L, self.F, self.R, rotate(self.U, -1)) \
                    if "'" in cmd else \
                        (rotate(self.D, -1), self.F, self.R, self.B, self.L, rotate(self.U, 1))
                
                elif cmd_0=='Z':
                    (self.D, self.L, self.F, self.R, self.B, self.U) = \
                        (rotate(self.L, -1), rotate(self.U, -1), rotate(self.F, -1), rotate(self.D, -1), rotate(self.B, 1), rotate(self.R, -1)) \
                    if "'" in cmd else \
                        (rotate(self.R, 1), rotate(self.D, 1), rotate(self.F, 1), rotate(self.U, 1), rotate(self.B, -1), rotate(self.L, 1))
 
            if print_each_turn: 
                print(self)
                print(cmd)
            

    def shuffle(self):
        cmd = ''
        for _ in range(16):
            cmd = cmd + random.choice(['U','D','R','L','F','B'])
        cube.turn(cmd)

cube = Cube()
# cube.shuffle()
print(cube)

class Cuber():
    def level_1(self):
        global cube
        if not np.any(cube.D.flatten()[[1, 3, 5, 7]]!=0) and \
            False not in [side[1, 1] == side[2, 1] for side in [cube.L, cube.F, cube.R, cube.B]]:
            print('1단계 완료!')
            return 
        else:
            print(cube.D.flatten()[[1, 3, 5, 7]]!=0)
        

history = []
back_stack = 0

while True:
    looking_history = False
    cmds = input('돌리기: ')
    
    if cmds in ['init','초기화','ㅑㅜㅑㅅ','chrlghk']:
        cube.init()
    elif cmds in ['shuffle','섞기','shuffle','tjRrl']:
        cube.shuffle()
    elif cmds in ['맞춰']:
        Cuber().level_1()
    elif cmds in ['back','뒤로','ㅠㅁ차','enlfh']:
        if not back_stack+1 <= len(history):
            continue
        back_stack += 1
        looking_history = True
        backcmd = back_cmd(history[-back_stack])
        print('back ->', ' '.join(backcmd))
        cube.turn(backcmd)
    elif cmds in ['redo','앞으로','ㄱㄷ애','dkvdmfh']:
        if not 0 <= back_stack-1 < len(history):
            continue
        looking_history = True
        redocmd = history[-back_stack]
        print('redo ->', ' '.join(redocmd))
        cube.turn(redocmd)
        back_stack -= 1
    else:
        print('turn ->', ' '.join(_split_cmd(cmds)))
        cube.turn(cmds)
    
    if not looking_history:
        if back_stack > 0:
            history = history[:-back_stack]
        history.append(cmds.replace('"',"'"))
        back_stack = 0

    print(cube)