import json
file=open('../json/lines of stop.json', mode="r")
lines_of_stop = json.load(file, encoding='utf-8')


ends_turns= {1: (4873436913, 1364747314, 4873436913), #1
             2: (4873436915, 5403604506, 5398020251), #2
             3: (4873436913, 1364747314, 4873436913), #3
             4: (5401229911, 1364747314, 5401229910), #4
             5: (5398378854, 1364747314, -1), #5 # this line end had to be eliminated as it would cause conflicts
             6: (5395534183, 1364747314, 5395534182), #6
             8: (5410260321, 5398378854, 5410260321), #8
             10:(5410259987, 5398378854, 5410259986), #10
             11:(1699701236, -1, -1), #11 #this line end had to be eliminated as it would cause conflicts
             12:(5410259987, 5405326919, 5410259986), #12
             13:(5407623407, 4852088188, 1799461738)} #13
            # Start     ,  Turn     ,   End
            
line_ends= list(map (lambda x:(x[2]),ends_turns.values()))

for stop in line_ends:
    print(lines_of_stop[str(stop)]['lines'])