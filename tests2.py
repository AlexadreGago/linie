ends_turns=[(4873436913, 1364747314, 4873436913), #1
            (4873436915, 5403604506, 5398020251), #2
            (4873436913, 1364747314, 4873436913), #3
            (5401229911, 1364747314, 5401229910), #4
            (5398378854, 1364747314, 5398378854), #5
            (5395534183, 1364747314, 5395534182), #6
            (5410260321, 5398378854, 5410260321), #8
            (5410259987, 5398378854, 5410259986), #10
            (1699701236, 0000000000, 4852045631), #11
            (5410259987, 5405326919, 5410259986), #12
            (5407623407, 4852088188, 1799461738)] #13
            # Start     ,  Turn     ,   End
            
line_ends= list(map (lambda x:(x[2]),ends_turns))


print(line_ends)