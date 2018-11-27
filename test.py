from boards import *

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