from engine import *

while True:
    mode = input('Choose:   Flip   or   Ultimate\n').lower()
    if mode in ('flip', 'ultimate'):
        break

if mode == 'flip':

    B = FlipMode()

    ctr = 0
    flipping = False

    while True:
        if ctr % 2 == 0:
            val = 'x'
        else:
            val = 'o'
        print('\n' + val.upper() + "'s TURN", end='')
        if flipping:
            print('  (flip)')
        else:
            print('  (place)')
        B.string()

        #try:
        inp = input()

        if inp == 'exit':
            break

        inp = inp.split()

        x, y = int(inp[0]), int(inp[1])

        if flipping:
            if inp[2] not in B.can_flip(x, y):
                continue
            
            f = B.flip(x, y, inp[2])
            print(f)
            if f is not False:
                flipping = False

                if f is not True:
                    print('\n\n' + f.upper() + ' WINS!!!')
                    B.string()
                    break
        else:
            if inp[2] == '1':
                val = val.upper()
            elif inp[2] != '0':
                continue

            if B.get(x, y) != ' ':
                continue

            s = B.set(val, x, y)
            
            if s is not None:
                if s == '-':
                    print('\n\n--DRAW--')
                else:
                    print('\n\n' + s.upper() + ' WINS!!!')
                B.string()
                break

            ctr += 1
            flipping = True
        #except:
         #   print('\nINVALID')
          #  continue

else:

    B = UltimateMode()

    locked = False
    ctr = 0

    while True:
        if ctr % 2 == 0:
            value = 'x'
        else:
            value = 'o'

        print(value.upper() + "'s Turn")
        B.string()

        try:
            inp = input()
            if inp == 'exit':
                break

            inp = inp.split()
            if locked:
                ix, iy = int(inp[0]), int(inp[1])
            else:
                x, y, ix, iy = int(inp[0]), int(inp[1]), int(inp[2]), int(inp[3])

            if B.matrix[x][y][ix][iy] == ' ':

                B.set(value, x, y, ix, iy)

                check = B.check(x, y, ix, iy)
                if check is not False:
                    B.set(check[0], x, y)

                    check = B.check(x, y)
                    if check is not False:
                        print('\n')
                        if check[0] == '-':
                            print('DRAW')
                        elif check[0] == 'x':
                            print('X WINS!')
                        else:
                            print('O WINS!')
                        B.string()
                        break

                if B.big[ix][iy] == ' ':
                    locked = True
                    x, y = ix, iy
                else:
                    locked = False

                ctr += 1
        except:
            print('\nINVALID INPUT')
