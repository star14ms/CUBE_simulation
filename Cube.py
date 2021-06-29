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
    
    if ("'" in cmd and (cmd_0==side0 or cmd_0==side1) or (
        not "'" in cmd and cmd_0==side2)):
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
    cmds = cmds.replace('"',"'").replace(' ','')
    splited_cmds = []
    cmd_start = None
    for idx, cmd in enumerate(cmds):
        if cmd in ['U','E','D','R','M','L','F','S','B','x','y','z','u','d','r','l','f','b','-']:
            if cmd_start == None:
                cmd_start = idx
            else:
                splited_cmds.append(cmds[cmd_start:idx])
                cmd_start = idx
        elif cmd not in ["'",'2']:
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
    def __init__(self, shuffle=False, shuffle_seed=''):
        self.D = np.full([3, 3], 0, dtype=np.int)
        self.L = np.full([3, 3], 1, dtype=np.int)
        self.F = np.full([3, 3], 2, dtype=np.int)
        self.R = np.full([3, 3], 3, dtype=np.int)
        self.B = np.full([3, 3], 4, dtype=np.int)
        self.U = np.full([3, 3], 5, dtype=np.int)
        self.seed = ''
        self.history = []
        self.pre_not_verbose = False

        # self.U = np.array(
            # [5,2,1,
            #  4,5,1,
            #  0,1,2]).reshape(3,3)
        # self.L = np.array(
            # [2,5,4,
            #  4,4,1,
            #  3,2,4]).reshape(3,3)
        # self.F = np.array(
            # [3,2,0,
            #  0,1,4,
            #  5,3,0]).reshape(3,3)
        # self.R = np.array(
            # [3,4,4,
            #  0,2,3,
            #  1,2,3]).reshape(3,3)
        # self.B = np.array(
            # [0,3,1,
            #  0,3,3,
            #  5,5,5]).reshape(3,3)
        # self.D = np.array(
            # [1,5,2,
            #  0,0,5,
            #  2,1,4]).reshape(3,3)

        if shuffle:
            self.shuffle(shuffle_seed)
    
    
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


    def turn(self, cmds, verbose=True, Case_Name=None, verbose_each_turn=False, add_history=True):
        if '?' in cmds: 
            print('turn ->',
             ' '.join(cmds))
            return
        if type(cmds) == str:
            cmds = split_cmd(cmds.replace('"',"'"))
        
        for cmd in cmds:
            
            cmd_0 = cmd[0].upper()
            
            if cmd_0 in ['D','E','U']:
                target = np.concatenate([rotate(self.R,2), rotate(self.F,2), rotate(self.L,2), rotate(self.B,2)], axis=1)

                target = _turn(target, cmd, sides=['D','E','U'])
                R, F, L, B = np.hsplit(target, [3, 6, 9])
                self.R, self.F, self.L, self.B = rotate(R,2), rotate(F,2), rotate(L,2), rotate(B,2)

                if cmd_0=='U':
                    self.U = rotate(self.U, (-1 if "'" in cmd else 2 if '2' in cmd else 1))
                if cmd_0=='D':
                    self.D = rotate(self.D, (-1 if "'" in cmd else 2 if '2' in cmd else 1))

            if cmd_0 in ['L','M','R']:
                target = np.concatenate([rotate(self.F, 1), rotate(self.U, 1), rotate(self.B, -1), rotate(self.D, 1)], axis=1)
                
                target = _turn(target, cmd, sides=['L','M','R'])
                F, U, B, D = np.hsplit(target, [3, 6, 9])
                self.F, self.U, self.B, self.D = rotate(F, -1), rotate(U, -1), rotate(B, 1), rotate(D, -1)

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
            
        if verbose: 
            if self.pre_not_verbose: 
                print('turn -> '+' '.join(self.history[-1]))
                self.pre_not_verbose = False
            print('turn -> '+(bcolors.WARNING if Case_Name!=None else bcolors.BOLD)+ \
            ' '.join(cmds), f'({Case_Name})' if Case_Name!=None else '', bcolors.ENDC)
        else:
            self.pre_not_verbose = True

        if not add_history: return

        if len(self.history)==0 or cmds not in [["y"],["y'"]] or \
            self.history[-1] not in [["y"],["y y"],["y y y"],["y'"],["y' y'"],["y' y' y'"]]:
            self.history.append(cmds)
        elif cmds==["y"]:
            self.history[-1] = [self.history[-1][0] + " y"]
        elif cmds==["y'"]:
            self.history[-1] = [self.history[-1][0] + " y'"]


    def shuffle(self, cmd='', shuffle_num=32):
        if cmd=='':
            for _ in range(shuffle_num):
                cmd = cmd + random.choice(['U','D','R','L','F','B'])
        self.turn(cmd, verbose=False, add_history=False)
        print('shuffle ->', cmd)
        self.seed = cmd
        self.pre_not_verbose = False


    def __call__(self, side, index):
        if   side == 'D': side = self.D
        elif side == 'L': side = self.L
        elif side == 'F': side = self.F
        elif side == 'R': side = self.R
        elif side == 'B': side = self.B
        elif side == 'U': side = self.U
        else: return None

        return side.flatten()[index]
