
from audioop import reverse

from flask_login import ID_ATTRIBUTE


def checkDirection(paragem,line,stops_array):
    print("linha:",line)
    linha = bus_list[bus_id][0]
    print(ends_turns[linha][0])
    direction = 2 # not detected
    for paragem_temp in reversed(stops_array):
        if paragem_temp == ends_turns[linha][0]:
            print("esta na IDa ")
            direction = 0
        if paragem_temp == ends_turns[linha][1]:
            print("esta na vinda")
            direction = 1
        if paragem_temp == ends_turns[linha][2]:
            direction = 0 # sus
            print("mudou de linha")
            
    return direction
    
    
#DATA
paragem=123456789
bus_list={}
bus_list[50]=[1,2]
bus_list[51]=[1]
bus_id=51
stops_array=[98765432,12345678,1364747314,98769547]

ends_turns= {1: (4873436913, 1364747314, 4873436913), #1
             2: (4873436915, 5403604506, 5398020251), #2
             3: (4873436913, 1364747314, 4873436913), #3
             4: (5401229911, 1364747314, 5401229910), #4
             5: (5398378854, 1364747314, 5398378854), #5
             6: (5395534183, 1364747314, 5395534182), #6
             8: (5410260321, 5398378854, 5410260321), #8
             10:(5410259987, 5398378854, 5410259986), #10
             11:(1699701236, 0000000000, 4852045631), #11
             12:(5410259987, 5405326919, 5410259986), #12
             13:(5407623407, 4852088188, 1799461738)} #13
            # Start     ,  Turn     ,   End
            
            
checkDirection(paragem,bus_list[bus_id],stops_array)


