import numpy as np
from Cube import Cube, back_cmd, split_cmd
from util import bcolors
from time import sleep

print()
cube = Cube(shuffle=True, shuffle_seed='RLUDUFFBBRFDRDRBRUDRRLLDLULRBULF') # 60번 회전
print(cube)
# FDULBDRULRUURFURLBBBRLFDRFRBDFUF
# DBFLBBRBLBFFRBLBFURFRRFFLBLFDDDR
# BRRLFLBUDRDLULLFLDRBFUBLBFFBRRFF
# LLFRUFBRFDFFRFURLDFDDDBDLUDLFUDL


class Cuber():
    Cross_solutions = [ ### U = cube.U 값을 복사했기 때문에 실제 바뀐 값이랑 연동되지 않음
        (('R',1), ('U',5), [1, 5, 7, 3], ['F','R','B','L'], "R'F R"),
        (('U',7), ('F',1), [1, 5, 7, 3], ['F','R','B','L'], "F2"), 
        (('F',3), ('L',5), [3, 1, 5, 7], ['L','F','R','B'], "L"),
        (('F',5), ('R',3), [5, 7, 3, 1], ['R','B','L','F'], "R'"),
    ]
    F2L_solutions = [
        (('F2L Case 1A') ,('F',2),[('U',8),('R',0)],('U',5),('R',1),("U  R  U' R'")),                   
        (('F2L Case 1B') ,('R',0),[('U',8),('F',2)],('F',1),('U',7),("F  R' F' R")),                    
        (('F2L Case 2')  ,('D',2),[('F',8),('R',6)],('R',3),('F',5),("R2 U2 F  R2 F' U2 R' U  R'")),    
        # (('F2L Case 3')  ,('D',2),[('F',8),('R',6)],('F',5),('R',3),("")),                              
        (('F2L Case 4A') ,('F',8),[('R',6),('D',2)],('F',5),('R',3),("R2 U2 R' U' R  U' R' U2 R'")),    
        (('F2L Case 4B') ,('R',6),[('D',2),('F',8)],('F',5),('R',3),("y' R2 U2 R  U  R' U  R  U2  R")), 
        (('F2L Case 5A') ,('F',8),[('R',6),('D',2)],('R',3),('F',5),("R  U' R  U  B  U' B' R2")), # R U'R'U' -> R U'R'U      
        (('F2L Case 5B') ,('R',6),[('D',2),('F',8)],('R',3),('F',5),("y' R' U  R' U' F' U  F  R2")),    
        (('F2L Case 6')  ,('U',8),[('R',0),('F',2)],('F',5),('R',3),("R2 U  R2 U  R2 U2 R2")),          
        (('F2L Case 7')  ,('U',8),[('R',0),('F',2)],('R',3),('F',5),("R  U' R' F' U2 F")),              
        (('F2L Case 8A') ,('F',2),[('U',8),('R',0)],('F',5),('R',3),("U' R  U' R' U2 -  R  U' R'")),    
        (('F2L Case 8B') ,('R',0),[('U',8),('F',2)],('F',5),('R',3),("d  R' U  R  U2 -  R' U  R")),     
        (('F2L Case 9A') ,('F',2),[('U',8),('R',0)],('R',3),('F',5),("U' R  U  R' -  U  F' U' F")),     
        (('F2L Case 9B') ,('R',0),[('U',8),('F',2)],('R',3),('F',5),("U  F' U' F  -  U' R  U  R'")),    
        (('F2L Case 10A'),('D',2),[('F',8),('R',6)],('F',1),('U',7),("U  R  U' R' -  F  R' F' R")),     
        (('F2L Case 10B'),('D',2),[('F',8),('R',6)],('U',5),('R',1),("U' F' U  F  -  U  R  U' R'")),    
        (('F2L Case 11A'),('F',8),[('R',6),('D',2)],('U',5),('R',1),("R  U' R' -  U  R  U' R'")),       
        (('F2L Case 11B'),('R',6),[('D',2),('F',8)],('F',1),('U',7),("y' R' U  R  -  U' R' U  R")),     
        (('F2L Case 12A'),('F',8),[('R',6),('D',2)],('F',1),('U',7),("y' R' U' R  -  R' U' R")),        
        (('F2L Case 12B'),('R',6),[('D',2),('F',8)],('U',5),('R',1),("R  U  R' U' -  R  U  R'")),       
        (('F2L Case 13A'),('R',2),[('U',2),('B',0)],('F',1),('U',7),("d  -  R' U' R")),                 
        (('F2L Case 13B'),('F',0),[('U',6),('L',2)],('U',5),('R',1),("U' R  U  R'")),                   
        (('F2L Case 14A'),('R',2),[('U',2),('B',0)],('U',7),('F',1),("R  U2 R' U2 -  R  U' R'")),       
        (('F2L Case 14B'),('F',0),[('U',6),('L',2)],('R',1),('U',5),("y' R' U2 R  U2 -  R' U  R")),     
        (('F2L Case 15A'),('U',6),[('L',2),('F',0)],('F',1),('U',7),("U2 R  U  R2 F  R  F' -  R  U' R'")), 
        (('F2L Case 15B'),('U',2),[('B',0),('R',2)],('U',5),('R',1),("U2 R  U' R' U' R  U' R' -  U  R  U' R'")), 
        (('F2L Case 16A'),('U',8),[('R',0),('F',2)],('U',5),('R',1),("R  U2 R' -  U' R  U  R'")),       
        (('F2L Case 16B'),('U',8),[('R',0),('F',2)],('F',1),('U',7),("y' R' U2 R  -  U  R' U' R")),     
        (('F2L Case 17A'),('R',0),[('U',8),('F',2)],('U',7),('F',1),("U  F' U2 F  -  U' R  U  R'")),    
        (('F2L Case 17B'),('F',2),[('U',8),('R',0)],('R',1),('U',5),("U' R  U2 R' -  U  F' U' F")), ### R' -> F'  
        (('F2L Case 18A'),('R',0),[('U',8),('F',2)],('R',1),('U',5),("R  U' R' -  U2 -  F' U' F")),     
        (('F2L Case 18B'),('F',2),[('U',8),('R',0)],('U',7),('F',1),("F' U  F  -  U2 -  R  U  R'")),    
        (('F2L Case 19A'),('R',0),[('U',8),('F',2)],('U',5),('R',1),("U' R  U' R' U  -  R  U  R'")),    
        (('F2L Case 19B'),('F',2),[('U',8),('R',0)],('F',1),('U',7),("d  R' U  R  U' -  R' U' R")), ## R'U R -> R'U'R source에서 오타  
        (('F2L Case 20A'),('U',0),[('L',0),('B',2)],('U',5),('R',1),("R  U  R' -  U  R  U' R'")), # ## F -> L
        (('F2L Case 20B'),('U',0),[('L',0),('B',2)],('F',1),('U',7),("y' R' U' R  -  U' R' U  R")),     
        (('F2L Case 21A'),('U',6),[('L',2),('F',0)],('U',5),('R',1),("R  U2 R' -  U  R  U' R'")),       
        (('F2L Case 21B'),('U',2),[('B',0),('R',2)],('F',1),('U',7),("y' R' U2 R  -  U' R' U  R")),     
        (('F2L Case 22A'),('B',0),[('R',2),('U',2)],('U',7),('F',1),("R  U  R' U  -  R  U  R'")),       
        (('F2L Case 22B'),('L',2),[('F',0),('U',6)],('R',1),('U',5),("R  U  R' U2 F' U' F")),           
        (('F2L Case 23A'),('F',0),[('U',6),('L',2)],('B',1),('U',1),("y' R' U' R  U2 R' U  R")),        
        (('F2L Case 23B'),('R',2),[('U',2),('B',0)],('U',3),('L',1),("R  U  R' U2 R  U' R'")),          
    ]
    OLL_solutions = [
        (('OLL Case 1') ,(0,0,0,0),(('L',0),('R',2),('L',2),('R',0)),("R  U2 R2 F  R  F' U2 -  R' F  R  F'")),
        (('OLL Case 2') ,(0,0,0,0),(('L',0),('B',0),('L',2),('F',2)),("F  -  R  U  R' U' -  S  -  R  U  R' U' -  f'")), ## S -> S' 
        (('OLL Case 3') ,(0,0,0,0),(('L',0),('B',0),('U',6),('R',0)),("F  U  R  U' R' F' -  U' -  F  R  U  R' U' F'")),
        (('OLL Case 4') ,(0,0,0,0),(('U',0),('R',2),('L',2),('F',2)),("F  U  R  U' R' F' -  U  -  F  R  U  R' U' F'")),
        (('OLL Case 5') ,(0,0,0,0),(('U',0),('B',0),('L',2),('U',8)),("R  U  R' U  -  R' F  R  F' -  U2 -  R' F  R  F'")),
        (('OLL Case 6') ,(0,0,0,0),(('U',0),('U',2),('F',0),('F',2)),("r  -  U  R' U  R  U2 -  r2 -  U' R  U' R' U2 r")),
        (('OLL Case 7') ,(0,0,0,0),(('U',0),('U',2),('L',2),('R',0)),("r' -  U2 R  U  R' U  -  r2 -  U2 R' U' R  U' r'")),
        (('OLL Case 8') ,(0,0,0,0),(('U',0),('U',2),('U',6),('U',8)),("M  U  -  R  U  R' U' -  M2 U  R  U' r'")),
        (('OLL Case 9') ,(1,0,0,1),(('L',0),('R',2),('L',2),('R',0)),("R' U2 R2 U  R' U  R  U2 -  B' R' B")),
        (('OLL Case 10'),(0,1,1,0),(('L',0),('R',2),('L',2),('R',0)),("F  -  R  U  R' U' -  R  F' r  U  R' U' r'")),
        (('OLL Case 11'),(0,1,1,0),(('L',0),('B',0),('L',2),('F',2)),("f  -  R  U  R' U' -  R  U  R' U' -  f'")),
        (('OLL Case 12'),(1,0,0,1),(('B',2),('R',2),('F',0),('R',0)),("R' U' R  U' R' U  -  y' R' U  R  B")),
        (('OLL Case 13'),(1,1,0,0),(('B',2),('B',0),('F',0),('F',2)),("r  U2 R' U' -  R  U  R' U' -  R  U' r'")),
        (('OLL Case 14'),(0,1,0,1),(('B',2),('B',0),('F',0),('F',2)),("r' U2 -  R  U  R' U' -  R  U  R' U  r")),
        (('OLL Case 15'),(0,1,0,1),(('B',2),('R',2),('F',0),('R',0)),("R  B' R2 F  R2 B  R2 F' R")),
        (('OLL Case 16'),(1,1,0,0),(('B',2),('R',2),('F',0),('R',0)),("R' F  R2 B' R2 F' R2 B  R'")),
        (('OLL Case 17'),(1,1,0,0),(('L',0),('B',0),('L',2),('F',2)),("F  -  R  U  R' U' -  R  U  R' U' -  F'")),
        (('OLL Case 18'),(1,0,1,0),(('B',2),('R',2),('F',0),('R',0)),("F' -  L' U' L  U  -  L' U' L  U  -  F")),
        (('OLL Case 19'),(1,1,0,0),(('B',2),('R',2),('U',6),('F',2)),("r  U  R' U  R  U2 r'")),
        (('OLL Case 20'),(0,1,0,1),(('U',0),('B',0),('F',0),('R',0)),("r' U' R  U' R' U2 r")),
        (('OLL Case 21'),(1,0,1,0),(('U',0),('B',0),('F',0),('R',0)),("r  R2 U' R  U' R' U2 R  U' M")),
        (('OLL Case 22'),(0,0,1,1),(('B',2),('R',2),('U',6),('F',2)),("r' R2 U  R' U  R  U2 R' U  M'")),
        (('OLL Case 23'),(1,1,0,0),(('L',0),('B',0),('F',0),('U',8)),("R  U  R' U' -  R' F  R2 U  R' U' F'")),
        (('OLL Case 24'),(0,1,0,1),(('B',2),('U',2),('L',2),('F',2)),("R  U  R' U  -  R' F  R  F' -  R  U2 R'")),
        (('OLL Case 25'),(0,0,1,1),(('B',2),('R',2),('L',2),('U',8)),("r' U2 R  U  R' U  r")),
        (('OLL Case 26'),(1,0,1,0),(('L',0),('U',2),('F',0),('R',0)),("r  U2 R' U' R  U' r'")),
        (('OLL Case 27'),(0,1,1,0),(('B',2),('R',2),('U',6),('F',2)),("F  U  R  U2 -  R' U' R  U  R' F'")),
        (('OLL Case 28'),(0,1,1,0),(('L',0),('B',0),('F',0),('U',8)),("R' F  R  U  -  R' F' R  F  -  U' F'")),
        (('OLL Case 29'),(0,1,1,0),(('L',0),('U',2),('F',0),('R',0)),("r  U  r' -  R  U  R' U' -  r  U' r'")),
        (('OLL Case 30'),(0,1,1,0),(('B',2),('R',2),('L',2),('U',8)),("r' U' r  -  R' U' R  U  -  r' U  r")),
        (('OLL Case 31'),(1,1,0,0),(('B',2),('B',0),('U',6),('U',8)),("R  U  R' U  R  U2 R' -  F  R  U  R' U' F'")),
        (('OLL Case 32'),(0,1,0,1),(('U',0),('U',2),('F',0),('F',2)),("R' U' R  U' R' U2 R  -  F  R  U  R' U' F'")),
        (('OLL Case 33'),(1,1,0,0),(('B',2),('U',2),('F',0),('U',8)),("l' U' R  D' R' U2 R' U' R2 D  -  x'")),
        (('OLL Case 34'),(0,1,0,1),(('B',2),('U',2),('F',0),('U',8)),("l  U  R' D  R  U2 R  U  R2 D' -  x")),
        (('OLL Case 35'),(0,0,1,1),(('B',2),('U',2),('F',0),('U',8)),("R  U  -  B' U' R' U  R  B  -  R'")),
        (('OLL Case 36'),(1,0,1,0),(('B',2),('U',2),('F',0),('U',8)),("R' U' -  F  U  R  U' R' F' -  R")),
        (('OLL Case 37'),(1,1,0,0),(('U',0),('R',2),('F',0),('U',8)),("F  R' F' R  -  U  R  U' R'")),
        (('OLL Case 38'),(0,0,1,1),(('L',0),('U',2),('L',2),('U',8)),("f  -  R  U  R' U' -  f'")),
        (('OLL Case 39'),(1,0,1,0),(('L',0),('U',2),('L',2),('U',8)),("F' -  U' L' U  L  -  F")),
        (('OLL Case 40'),(0,0,1,1),(('U',0),('R',2),('F',0),('U',8)),("R  U2 R2 F  R  F' R  U2 R'")),
        (('OLL Case 41'),(0,1,1,0),(('L',0),('U',2),('L',2),('U',8)),("F  -  R  U  R' U' -  F'")),
        (('OLL Case 42'),(0,1,1,0),(('B',2),('U',2),('F',0),('U',8)),("R  U  R' U' -  R' F  R  F'")),
        (('OLL Case 43'),(0,1,1,0),(('L',0),('U',2),('U',6),('F',2)),("R  -  B' R' U' R  U  B  -  U' R'")),
        (('OLL Case 44'),(0,1,1,0),(('U',0),('B',0),('L',2),('U',8)),("R' -  F  R  U  R' U' F' -  U  R")),
        (('OLL Case 45'),(0,1,1,0),(('L',0),('R',2),('U',6),('U',8)),("R  U  R' U' -  B' -  R' F  R  F' -  B")),
        (('OLL Case 46'),(1,0,0,1),(('U',0),('R',2),('U',6),('R',0)),("R' U' -  R' F  R  F' -  U  R")),
        (('OLL Case 47'),(1,1,0,0),(('B',2),('U',2),('U',6),('R',0)),("R  U  R' U  -  R  U' R' U' -  R' F  R  F'")),
        (('OLL Case 48'),(0,1,0,1),(('U',0),('R',2),('F',0),('U',8)),("R' U' R  U' -  R' U  R  U  -  R  B' R' B")),
        (('OLL Case 49'),(1,1,1,1),(('B',2),('B',0),('F',0),('F',2)),("R  U2 R' U' -  R  U  R' U' -  R  U' R'")),
        (('OLL Case 50'),(1,1,1,1),(('L',0),('B',0),('L',2),('F',2)),("R  U2 R2 U' R2 U' R2 U2 R")),
        (('OLL Case 51'),(1,1,1,1),(('B',2),('B',0),('U',6),('U',8)),("R2 D' R  U2 R' D  R  U2 R")),
        (('OLL Case 52'),(1,1,1,1),(('B',2),('U',2),('F',0),('U',8)),("F  R  F' r  U  R' U' r'")),
        (('OLL Case 53'),(1,1,1,1),(('U',0),('R',2),('F',0),('U',8)),("F  R' F' r  U  R  U' r'")),
        (('OLL Case 54'),(1,1,1,1),(('U',0),('B',0),('F',0),('R',0)),("R' U' R  U' R' U2 R")),
        (('OLL Case 55'),(1,1,1,1),(('B',2),('R',2),('U',6),('F',2)),("R  U  R' U  R  U2 R'")),
        (('OLL Case 56'),(1,1,0,0),(('U',0),('U',2),('U',6),('U',8)),("r  U  R' U' M  -  U  R  U' R'")),
        (('OLL Case 57'),(0,1,1,0),(('U',0),('U',2),('U',6),('U',8)),("R  U  R' U' -  M' U  R  U' r'")),
    ]
    PLL_solutions = [
        (('PLL Case 1') ,('FRBL'),('BFRL'),("R2 F2 R' B' R  F2 R' B  R'")),
        (('PLL Case 2') ,('FRBL'),('RBFL'),("R  B' R  F2 R' B  R  F2 R2")),
        (('PLL Case 3') ,('FRBL'),('RFLB'),("F  R' F' r  U  R  U' r' -  F  R  F' r  U  R' U' r'")),
        (('PLL Case 4') ,('FLRB'),('FRBL'),("R' U  R' U' R' U' R' U  R  U  R2")),
        (('PLL Case 5') ,('FBLR'),('FRBL'),("R2 U' R' U' R  U  R  U  R  U' R")),
        (('PLL Case 6') ,('LBRF'),('FRBL'),("R' U' R  U' R  U  -  R  U' R' U  R  U  R2 U' R' U2")),
        (('PLL Case 7') ,('BLFR'),('FRBL'),("M2 U' M2 U2 M2 U' M2")),
        (('PLL Case 8') ,('RFBL'),('FBRL'),("R  U  R' F' -  R  U  R' U' -  R' F  R2 U' R' U'")),
        (('PLL Case 9') ,('FBRL'),('FBRL'),("R' U2 R  U  R' U2 L  U' R  U  L'")),
        (('PLL Case 10'),('RFBL'),('FRLB'),("R' U2 R  U2 R' F  R  U  R' U' R' F' R2 U'")),
        (('PLL Case 11'),('FRLB'),('FBRL'),("R  U  R' -  F' R  U2 R' U2 R' F  -  R  U  R  U2 R' U'")), ### R' -> F'
        (('PLL Case 12'),('FLBR'),('FBRL'),("R  U  R' U' -  R' F  R2 U' R' U' R  U  R' F'")),
        (('PLL Case 13'),('BRFL'),('FBRL'),("R' U' F' -  R  U  R' U' -  R' F  R2 U' R' U' R  U  R' U  R")),
        (('PLL Case 14'),('BRLF'),('LRFB'),("R  U  R' y' R2 u' R  U' R' U  R' u  R2")),
        (('PLL Case 15'),('LFBR'),('RLBF'),("R2 u' R  U' R  U  R' u  R2 y  R  U' R'")),
        (('PLL Case 16'),('LRFB'),('RLBF'),("R' U' R  y  R2 u  R' U  R  U' R  u' R2")),
        (('PLL Case 17'),('FBLR'),('LRFB'),("R2 u  R' U  R' U' R  u' R2 -  F' U  F")),
        (('PLL Case 18'),('FBRL'),('FLBR'),("R' U  R' d' -  R' F' R2 U' R' U  R' -  F  R  F")),
        (('PLL Case 19'),('FRLB'),('FLBR'),("F  R  U' R' U' R  U  R' F' -  R  U  R' U' -  R' F  R  F'")),
        (('PLL Case 20'),('FLBR'),('FLBR'),("L' U  R' U2 L  U' R  -  L' U  R' U2 L  U' R  -  U")),
        (('PLL Case 21'),('FLBR'),('BRFL'),("L  U' R  U2 L' U  R' -  L  U' R  U2 L' U  R' -  U'")),
    ]
    first_look_Oll_solutions = [
        "F R U R' U' S' R U R' U' f'", 
        "F R U R' U' F'", 
        "f R U R' U' f'",
    ]
    second_look_OLL_solutions = [
        (('OLL Case 49'),(('B',2),('B',0),('F',0),('F',2)),("R  U2 R' U' -  R  U  R' U' -  R  U' R'")),
        (('OLL Case 50'),(('L',0),('B',0),('L',2),('F',2)),("R  U2 R2 U' R2 U' R2 U2 R")),
        (('OLL Case 51'),(('B',2),('B',0),('U',6),('U',8)),("R2 D' R  U2 R' D  R  U2 R")),
        (('OLL Case 52'),(('B',2),('U',2),('F',0),('U',8)),("F  R  F' r  U  R' U' r'")),
        (('OLL Case 53'),(('U',0),('R',2),('F',0),('U',8)),("F  R' F' r  U  R  U' r'")),
        (('OLL Case 54'),(('U',0),('B',0),('F',0),('R',0)),("R' U' R  U' R' U2 R")),
        (('OLL Case 55'),(('B',2),('R',2),('U',6),('F',2)),("R  U  R' U  R  U2 R'")),
    ]

    def fit(self):
        del cube.history[:]
        for step_n, step in enumerate([self.Cross, self.F2L, self.OLL, self.PLL]):
            step()
            print(cube)
            print(f'{step_n+1}단계 완료!')
            sleep(0.01)
        print()
        
        all_cmds = []
        all_cmds_files = []
        for cmds in cube.history:
            all_cmds_files.append(' '.join(cmds))
            all_cmds.extend(cmds)
        # print(bcolors.BOLD+f'{bcolors.ENDC} => {bcolors.BOLD}'.join(all_cmds_files)+bcolors.ENDC)
        # for cmds in all_cmds_files:
            # print(f'turn -> {bcolors.BOLD}{cmds}{bcolors.ENDC}')
        for cmds in all_cmds_files:
            print('=>', 
                (bcolors.BOLD if cmds not in ['y','y y','y y y',"y'","y' y'","y' y' y'"] 
                else '') + cmds, bcolors.ENDC, end='')
        print()

        turn_num = 0
        for cmd in all_cmds:
            if cmd in ["-","x","x'","y","y'","z","z'","x2","y2","z2"]: continue
            if '2' in cmd:
                turn_num += 1
            turn_num += 1
        print(f'\n시점 돌리기(xyz)제외 {turn_num}번 회전')


    def check(self, check):
        if check=='Cross':
            if not np.any(cube.D.flatten()[[1,3,5,7]]!=0) and \
                False not in [side[1, 1] == side[2, 1] for side in [cube.L,cube.F,cube.R,cube.B]]:
                return True
            else:
                return False

        elif check=='F2L':
            for side in [cube.L, cube.F, cube.R, cube.B]:
                if np.any(side.flatten()[[3,5,6,8]]!=side[1,1]):
                    return False
            return True

        elif check=='first_look_OLL':
            return True if not np.any(cube.U.flatten()[[1,3,5,7]]!=5) else False

        elif check=='second_look_OLL':
            return True if not np.any(cube.U.flatten()[[0,2,6,8]]!=5) else False

        elif check=='OLL':
            return True if not np.any(cube.U!=5) else False
        
        elif check=='PLL':
            if np.any(cube.D!=cube.D[1,1]) or \
                np.any(cube.L!=cube.L[1,1]) or \
                np.any(cube.F!=cube.F[1,1]) or \
                np.any(cube.R!=cube.R[1,1]) or \
                np.any(cube.B!=cube.B[1,1]) or \
                np.any(cube.U!=cube.U[1,1]):
                return False
            else:
                return True
    
        
    def Cross(self):
        y = "y'" if cube.L[2, 1]==0 or cube.F[0, 1]==0 else 'y'

        while not self.check('Cross'):
            print()
            for _ in range(4):
                if cube.F[2, 1] == 0:
                    cmd = "F'" if cube.F[1, 0]!=0 else "F"
                    cube.turn(cmd)

                moved = True
                while moved:
                    moved = False
                    for (target, target2, D_idxs, D2_sides, cmd_main) in self.Cross_solutions:
                        if cube(*target)==0:
                            cmd_D = ''
                            for bias in range(4):
                                if cube('D', D_idxs[bias])==0:
                                    rotate_n = (cube(*target2)-cube(D2_sides[bias], 7)+bias) % 4 # 고정된 자리 - 움직이는 자리
                                    cmd_D = ("D'"*rotate_n).replace("D'D'D'","D").replace("D'D'","D2")
                                    moved = True
                                    break
                        
                            cube.turn(cmd_D + cmd_main)

                            if not np.any(cube.D.flatten()[[1,3,5,7]]!=0):
                                for D_idx, side in zip([3, 1, 5, 7], ['L','F','R','B']):
                                    if cube('D', D_idx) == 0:
                                        rotate_n = (cube(side, 4)-cube(side, 7)) % 4 # 고정된 자리 - 움직이는 자리
                                        if rotate_n == 0: break
                                        cmd_D = ("D'"*rotate_n).replace("D'D'D'","D").replace("D'D'","D2")
                                        cube.turn(cmd_D)
                                        break

                        if self.check('Cross'): return

                cube.turn(y, verbose=False)


    def F2L(self, verbose=False):
        fail_stack = 0

        while not self.check('F2L'):
            print()
            pull_out_n = 0
            for _ in range(4):
                y_stack = []
                for _ in range(4):
                    solved_current_edge = False
                    for (Case_Name, w_color_coner, FRcolors_coner, Fcolor_edge, Rcolor_edge, solution) in self.F2L_solutions:
                        # if Case_Name=='F2L Case 20B':
                            # print(cube.F[1,1]==cube(*Fcolor_edge),
                            # cube.R[1,1]==cube(*Rcolor_edge),
                            # cube(*w_color_coner)==0,
                            # cube(*FRcolors_coner[0]) in [cube.F[1,1],cube.R[1,1]],
                            # cube(*FRcolors_coner[1]) in [cube.F[1,1],cube.R[1,1]])
                        if cube.F[1,1]==cube(*Fcolor_edge) and \
                            cube.R[1,1]==cube(*Rcolor_edge) and \
                            cube(*w_color_coner)==0 and \
                            cube(*FRcolors_coner[0]) in [cube.F[1,1],cube.R[1,1]] and \
                            cube(*FRcolors_coner[1]) in [cube.F[1,1],cube.R[1,1]]:

                            if verbose: print(cube)
                            cube.turn(solution.split(), Case_Name=Case_Name)
                            if verbose: print(cube)
                            solved_current_edge = True
                            break
                    
                    if self.check('F2L'): return

                    if not solved_current_edge and fail_stack > 0 and pull_out_n < 3 and ( ### 0 in [cube('D',2) +
                        ((0 in [cube('D',2),cube('F',8),cube('R',6)] and (
                        cube('D',2) in [cube.B[1,1],cube.L[1,1]] or \
                        cube('F',8) in [cube.B[1,1],cube.L[1,1]] or \
                        cube('R',6) in [cube.B[1,1],cube.L[1,1]])) or (
                        
                        5 not in [cube('F',5),cube('R',3)] and \
                        (cube('F',5) in [cube.B[1,1],cube.L[1,1]] or \
                        cube('R',3) in [cube.B[1,1],cube.L[1,1]])))):
                        # print((0 in [cube('D',2),cube('F',8),cube('R',6)],(
                        # cube('D',2) in [cube.B[1,1],cube.L[1,1]] or \
                        # cube('F',8) in [cube.B[1,1],cube.L[1,1]] or \
                        # cube('R',6) in [cube.B[1,1],cube.L[1,1]])), (
                        
                        # 5 not in [cube('D',2),cube('F',8),cube('R',6)], \
                        # (cube('F',5) in [cube.B[1,1],cube.L[1,1]] or \
                        # cube('R',3) in [cube.B[1,1],cube.L[1,1]])))

                        if verbose: print(cube)
                        cube.turn(["F'","U'","F","U"])
                        pull_out_n += 1
                        if verbose: print(cube)

                    if "y'" not in solution and 'd' not in solution:
                        cube.turn(["y'"], verbose=False) 
                        y_stack.append("y'")

                cube.turn(['U'])
            
            fail_stack += 1
            if fail_stack == 5: break
        

    def first_look_OLL(self):
        if not self.check('first_look_OLL'):
            print()
            if len(np.where(cube.U.flatten()[[1,3,5,7]]==5)[0])==0:
                cube.turn(self.first_look_Oll_solutions[0].split())
            elif len(np.where(cube.U.flatten()[[1,3,5,7]]==5)[0])==2:
                if cube('U',1)==cube('U',7)==5 or cube('U',3)==cube('U',5)==5:
                    if cube('U',1)==5:
                        cube.turn(['U'])
                    cube.turn(self.first_look_Oll_solutions[1].split())
                else:
                    if cube('U',1)==cube('U',3)==5: # a==b!=c is not a!=c and b!=c
                        cube.turn(['U2'])
                    elif cube('U',1)==cube('U',5)==5:
                        cube.turn(['U'])
                    elif cube('U',3)==cube('U',7)==5:
                        cube.turn(["U'"])
                    cube.turn(self.first_look_Oll_solutions[2].split())


    def second_look_OLL(self):
        
        if not self.check('second_look_OLL'):
            print()
            U_stack = []
            for _ in range(4):
                for (Case_Name, Y_idxs, solution) in self.second_look_OLL_solutions:
                    # if Case_Name in ['OLL Case 55']:
                        # print(cube(*Y_idxs[0])==5, cube(*Y_idxs[1])==5,
                        # cube(*Y_idxs[2])==5, cube(*Y_idxs[3])==5)
                    if cube(*Y_idxs[0])==5 and cube(*Y_idxs[1])==5 and \
                        cube(*Y_idxs[2])==5 and cube(*Y_idxs[3])==5:
                        if len(U_stack) != 0:
                            print('turn ->', ' '.join(U_stack))
                        cube.turn(solution.split(), Case_Name=Case_Name)
                        return

                cube.turn(['U'], verbose=False)
                U_stack.append('U')

 
    def OLL(self):
        if not self.check('OLL'):
            print()
            U_stack = []
            for _ in range(4):
                for (Case_Name, edge_isYs, corner_Y_idxs, solution) in self.OLL_solutions:
                    # if Case_Name == 'OLL Case 4':
                        # print(cube(*corner_Y_idxs[0])==5, cube(*corner_Y_idxs[1])==5, \
                        # cube(*corner_Y_idxs[2])==5, cube(*corner_Y_idxs[3])==5, \
                        # (cube('U',1)==5)==edge_isYs[0], (cube('U',3)==5)==edge_isYs[1], \
                        # (cube('U',5)==5)==edge_isYs[2], (cube('U',7)==5)==edge_isYs[3])
                    if cube(*corner_Y_idxs[0])==5 and cube(*corner_Y_idxs[1])==5 and \
                        cube(*corner_Y_idxs[2])==5 and cube(*corner_Y_idxs[3])==5 and \
                        (cube('U',1)==5)==edge_isYs[0] and (cube('U',3)==5)==edge_isYs[1] and \
                        (cube('U',5)==5)==edge_isYs[2] and (cube('U',7)==5)==edge_isYs[3]:
                        if len(U_stack) != 0:
                            print('turn -> '+bcolors.BOLD+' '.join(U_stack)+bcolors.ENDC)
                        cube.turn(solution.split(), Case_Name=Case_Name)
                        return

                cube.turn(['U'], verbose=False)
                U_stack.append('U')
                        

    def PLL(self):
        if not self.check('PLL'):
            print()
            for _ in range(4):
                y_stack = []
                for _ in range(4):
                    for (Case_Name, edge_color_sides, corner_color_sides, solution) in self.PLL_solutions:
                        # print(Case_Name, cube.F[0,1]==cube(edge_color_sides[0],4),
                            # cube.R[0,1]==cube(edge_color_sides[1],4),
                            # cube.B[0,1]==cube(edge_color_sides[2],4),
                            # cube.L[0,1]==cube(edge_color_sides[3],4),
                            # cube.F[0,0]==cube(corner_color_sides[0],4),
                            # cube.R[0,0]==cube(corner_color_sides[1],4),
                            # cube.B[0,0]==cube(corner_color_sides[2],4),
                            # cube.L[0,0]==cube(corner_color_sides[3],4))
                        if cube.F[0,1]==cube(edge_color_sides[0],4) and \
                            cube.R[0,1]==cube(edge_color_sides[1],4) and \
                            cube.B[0,1]==cube(edge_color_sides[2],4) and \
                            cube.L[0,1]==cube(edge_color_sides[3],4) and \
                            cube.F[0,0]==cube(corner_color_sides[0],4) and \
                            cube.R[0,0]==cube(corner_color_sides[1],4) and \
                            cube.B[0,0]==cube(corner_color_sides[2],4) and \
                            cube.L[0,0]==cube(corner_color_sides[3],4): ### 1 -> 4
                            
                            cube.turn(solution.split(), Case_Name=Case_Name)
                            return
                    
                    cube.turn(['y'], verbose=False)
                    y_stack.append('y')
                
                if self.check('PLL'): return
                cube.turn(['U'])


    def search_error(self, test_num=100):
        cuber.fit()
        for i in range(test_num):
            cube.shuffle()
            cuber.fit()
            if not cuber.check(check='PLL'): 
                print(f'\n{i+1}번째 테스트 중 오류 발견')
                break
            else:
                print(f'\n{i+1}번째 테스트 완료')



cuber = Cuber()
back_stack = 0

while True:
    cmds = input('돌리기: ')
    if len(cmds) == 0: continue
    if cmds == 'break': break
    
    if cmds in ['init','초기화','ㅑㅜㅑㅅ','chrlghk']:
        cube.init()
    elif cmds in ['shuffle','섞기','노ㅕㄹ릳','tjRrl','shuf']:
        cube.shuffle()
    elif cmds in ['seed','시드']:
        print('shuffle ->', cube.seed)
    elif cmds in ['fit', '맞춰', '럇', 'akwcnj']:
        cuber.fit()
    elif cmds in ['find error', '오류찾기']:
        cuber.search_error()
    elif cmds in ['back','뒤로','ㅠㅁ차','enlfh']:
        if not back_stack+1 <= len(cube.history):
            continue
        back_stack += 1
        backcmd = back_cmd(cube.history[-back_stack])
        print('back ->', ' '.join(backcmd))
        cube.turn(backcmd, False)
    elif cmds in ['redo','앞으로','ㄱㄷ애','dkvdmfh']:
        if not 0 <= back_stack-1 < len(cube.history):
            continue
        redocmd = cube.history[-back_stack]
        print('redo ->', ' '.join(redocmd))
        cube.turn(redocmd, False)
        back_stack -= 1
    else:
        cmds_splited = split_cmd(cmds)
        cube.turn(cmds_splited)
        if back_stack > 0:
            cube.history = cube.history[:-back_stack]
        back_stack = 0

    print(cube)

