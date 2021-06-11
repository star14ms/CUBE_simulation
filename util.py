import sys
class bcolors:
    
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\u001b[38;5;208m'

    c = [HEADER, OKBLUE, OKCYAN, OKGREEN, WARNING, FAIL, ENDC, BOLD, UNDERLINE, ORANGE]

    def test():
        for color in bcolors.c:
            print(color + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)

    def set_original():
        return bcolors.ENDC

    def set_by_cube_id(x):
        if x == 0 or x not in [1, 2, 3, 4, 5]:
            return bcolors.ENDC
        elif x == 1:
            return bcolors.ORANGE
        elif x == 2:
            return bcolors.OKBLUE
        elif x == 3:
            return bcolors.FAIL
        elif x == 4:
            return bcolors.OKGREEN
        elif x == 5:
            return bcolors.WARNING

    def tile_by_cube_id(x):
        if x == 0 or x not in [1, 2, 3, 4, 5]:
            return '⬜'
        elif x == 1:
            return '🟧'
        elif x == 2:
            return '🟦'
        elif x == 3:
            return '🟥'
        elif x == 4:
            return '🟩'
        elif x == 5:
            return '🟨'

    

    def ANSI_codes():
        for i in range(0, 16):
            for j in range(0, 16):
                code = str(i * 16 + j)
                sys.stdout.write(u"\u001b[38;5;" + code + "m" + code.ljust(4))
            print(u"\u001b[0m")


import numpy as np
def rotate_2dim_array(arr, d, add_0dim=False): # 2차원 배열을 90도 단위로 회전해 반환한다. 
    # 이때 원 배열은 유지되며, 새로운 배열이 탄생한다. 
    # 이는 회전이 360도 단위일 때도 해당한다. 
    # 2차원 배열은 행과 열의 수가 같은 정방형 배열이어야 한다.
    # arr: 회전하고자 하는 2차원 배열. 입력이 정방형 행렬이라고 가정한다. 
    # d: 90도씩의 회전 단위. -1: -90도, 1: 90도, 2: 180도, ...

    size = len(arr)
    ret = np.zeros([size, size], dtype=int)

    N = size - 1
    if d % 4 not in (1, 2, 3, 4, 5, 6, 7): 
        for r in range(size): 
            for c in range(size): 
                ret[r][c] = arr[r][c] 
    elif d % 4 == 1:
        for r in range(size): 
            for c in range(size): 
                ret[c][N-r] = arr[r][c] 
    elif d % 4 == 2: 
        for r in range(size): 
            for c in range(size): 
                ret[N-r][N-c] = arr[r][c] 
    elif d % 4 == 3: 
        for r in range(size): 
            for c in range(size): 
                ret[N-c][r] = arr[r][c] 

    # elif d % 8 == 4:
    #     for r in range(size): 
    #         for c in range(size): 
    #             ret[r][N-c] = arr[r][c]
    # elif d % 8 == 5: # arr.T
    #     for r in range(size): 
    #         for c in range(size): 
    #             ret[N-c][N-r] = arr[r][c]
    # elif d % 8 == 6:
    #     for r in range(size): 
    #         for c in range(size): 
    #             ret[N-r][c] = arr[r][c]
    # elif d % 8 == 7:
    #     for r in range(size): 
    #         for c in range(size): 
    #             ret[c][r] = arr[r][c]

    if not add_0dim:
        return ret
    else:
        return ret.reshape(1, size, size)
