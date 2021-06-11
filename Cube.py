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


def split_cmd(cmds):
    cmds = cmds.replace('"',"'")
    splited_cmds = []
    cmd_start = None
    for idx, cmd in enumerate(cmds):
        if cmd in ['U','E','D','R','M','L','F','S','B','x','y','z','u','d','r','l','f','b']:
            if cmd_start == None:
                cmd_start = idx
            else:
                splited_cmds.append(cmds[cmd_start:idx])
                cmd_start = idx
        elif cmd not in [' ',"'",'2']:
            return [cmd, '?']

    splited_cmds.append(cmds[cmd_start:])

    return splited_cmds


def back_cmd(cmds):
    back_cmds = []
    
    for cmd in reversed(cmds):
        if "'" in cmd:
            new_cmd = cmd.replace("'","")
        elif "2" not in cmd:
            new_cmd = cmd + "'"
        else:
            new_cmd = cmd
        
        back_cmds.append(new_cmd)
    
    return back_cmds



class Cube():
    def __init__(self, shuffle=False):
        self.D = np.full([3, 3], 0, dtype=np.int)
        self.L = np.full([3, 3], 1, dtype=np.int)
        self.F = np.full([3, 3], 2, dtype=np.int)
        self.R = np.full([3, 3], 3, dtype=np.int)
        self.B = np.full([3, 3], 4, dtype=np.int)
        self.U = np.full([3, 3], 5, dtype=np.int)

        if shuffle:
            self.shuffle()
    
    
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


    def turn(self, cmds, verbose=True, verbose_each_turn=False):
        if '?' in cmds: 
            print('turn ->', ' '.join(cmds))
            return
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
 
            if verbose_each_turn: 
                print(cmd)
                print(self)
            
        if verbose: print('turn ->', ' '.join(cmds))


    def shuffle(self, shuffle_num=32):
        cmd = ''
        for _ in range(shuffle_num):
            cmd = cmd + random.choice(['U','D','R','L','F','B'])
        self.turn(cmd, False)


    def find(self, side, index):
        if side == 'D': side = self.D
        elif side == 'L': side = self.L
        elif side == 'F': side = self.F
        elif side == 'R': side = self.R
        elif side == 'B': side = self.B
        elif side == 'U': side = self.U
        else: return None

        return side.flatten()[index]



class Cuber():
    def fit(self, cube):
        self.level_1(cube)
        

    def check_level_1(self, cube):
        if not np.any(cube.D.flatten()[[1, 3, 5, 7]]!=0) and \
            False not in [side[1, 1] == side[2, 1] for side in [cube.L,cube.F,cube.R,cube.B]]:
            print('1단계 완료!')
            return True
        else:
            return False

    def level_1(self, cube):
        y = "y'" if cube.L[2, 1]==0 or cube.F[0, 1]==0 else 'y'
        
        plus_formula_info = [ ### U = cube.U 값을 복사했기 때문에 실제 바뀐 값이랑 연동되지 않음
            (('R',1), ('U',5), [1, 5, 7, 3], ['F','R','B','L'], "R'FR"),
            (('U',7), ('F',1), [1, 5, 7, 3], ['F','R','B','L'], "F2"), 
            (('F',3), ('L',5), [3, 1, 5, 7], ['L','F','R','B'], "L"),
            (('F',5), ('R',3), [5, 7, 3, 1], ['R','B','L','F'], "R'"),
        ]

        fit_w = 1 if np.any(cube.D.flatten()[[1, 3, 5, 7]]==0) else 0
        while not self.check_level_1(cube):
            for _ in range(4):
                if cube.F[2, 1] == 0:
                    cmd = "F'" if cube.F[1, 0]!=0 else "F"
                    cube.turn(cmd)
                    history.append([cmd])

                for (target, target2, D_idxs, D2_sides, cmd_main) in plus_formula_info:
                    if cube.find(*target)==0:
                        cmd_D = ''
                        for bias in range(4):
                            if cube.find('D', D_idxs[bias])==0:
                                rotate_n = (cube.find(*target2)-cube.find(D2_sides[bias], 7)+bias) % 4 # 고정된 자리 - 움직이는 자리
                                cmd_D = ("D'"*rotate_n).replace("D'D'D'","D").replace("D'D'","D2")
                                break
                    
                        cube.turn(cmd_D + cmd_main)
                        history.append(_split_cmd(cmd_D + cmd_main))
                        fit_w += 1
                    if fit_w == 4: break
                    
                if fit_w == 4: break
                cube.turn(y)
                history.append([y])
                
            if not np.any(cube.D.flatten()[[1, 3, 5, 7]]!=0):
                for D_idx, side in zip([3, 1, 5, 7], ['L','F','R','B']):
                    if cube.find('D', D_idx) == 0:
                        rotate_n = (cube.find(side, 4)-cube.find(side, 7)) % 4 # 고정된 자리 - 움직이는 자리
                        if rotate_n == 0: break
                        cmd_D = ("D'"*rotate_n).replace("D'D'D'","D").replace("D'D'","D2")
                        cube.turn(cmd_D)
                        history.append([cmd_D])
                        break



