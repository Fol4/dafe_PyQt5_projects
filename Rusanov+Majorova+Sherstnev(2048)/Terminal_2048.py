import random


def MakeFlags(size):
    flags_table = []
    for i in range(size):
        flags_table.append([True] * size)
    return flags_table

def DisplayField(field):
    size = len(field)
    for i in range(size):
        for j in range(size):
            if field[i][j] // 10 == 0:
                print(field[i][j], end="    ")
            elif field[i][j] // 100 == 0:
                print(field[i][j], end="   ")
            elif field[i][j] // 1000 == 0:
                print(field[i][j], end="  ")
            else:
                print(field[i][j], end=" ")
        print()


def MoveUp(a):
    size = len(a)
    flags = MakeFlags(size)
    flag = True
    while (flag):
        flag = False
        for i in range(1, size):
            for j in range(size):
                if a[i][j] == a[i - 1][j] and flags[i][j] and flags[i - 1][j] and a[i][j] != 0:
                    a[i - 1][j] = 2 * a[i - 1][j]
                    a[i][j] = 0
                    flags[i][j] = False
                    flags[i - 1][j] = False
                    flag = True
                if a[i - 1][j] == 0 and a[i][j] != 0:
                    a[i - 1][j] = a[i][j]
                    flags[i - 1][j] = flags[i][j]
                    a[i][j] = 0
                    flag = True
    return a

def PossibleUp(a):
    size = len(a)
    flags = MakeFlags(size)
    flag = True
    while (flag):
        flag = False
        for i in range(1, size):
            for j in range(size):
                if a[i][j] == a[i - 1][j] and flags[i][j] and a[i][j] != 0:
                    return True
                if a[i - 1][j] == 0 and a[i][j] != 0:
                    return True
    return False

def MoveLeft(a):
    size = len(a)
    flags = MakeFlags(size)
    flag = True
    while (flag):
        flag = False
        for i in range(size):
            for j in range(1, size):
                if a[i][j] == a[i][j - 1] and flags[i][j] and flags[i][j - 1] and a[i][j] != 0:
                    a[i][j - 1] = 2 * a[i][j - 1]
                    a[i][j] = 0
                    flags[i][j] = False
                    flags[i][j - 1] = False
                    flag = True
                if a[i][j - 1] == 0 and a[i][j] != 0:
                    a[i][j - 1] = a[i][j]
                    a[i][j] = 0
                    flags[i][j - 1] = flags[i][j]
                    flag = True
    return a

def PossibleLeft(a):
    size = len(a)
    flags = MakeFlags(size)
    flag = True
    while (flag):
        flag = False
        for i in range(size):
            for j in range(1, size):
                if a[i][j] == a[i][j - 1] and flags[i][j] and a[i][j] != 0:
                    return True
                if a[i][j - 1] == 0 and a[i][j] != 0:
                    return True
    return False

def MoveDown(a):
    size = len(a)
    flags = MakeFlags(size)
    flag = True
    while (flag):
        flag = False
        for i in range(size - 2, -1, -1):
            for j in range(size):
                if a[i][j] == a[i + 1][j] and flags[i][j] and flags[i + 1][j] and a[i][j] != 0:
                    a[i + 1][j] = 2 * a[i + 1][j]
                    a[i][j] = 0
                    flags[i][j] = False
                    flags[i + 1][j] = False
                    flag = True
                if a[i + 1][j] == 0 and a[i][j] != 0:
                    a[i + 1][j] = a[i][j]
                    flags[i][j] = flags[i + 1][j]
                    a[i][j] = 0
                    flag = True
    return a

def PossibleDown(a):
    size = len(a)
    flags = MakeFlags(size)
    flag = True
    while (flag):
        flag = False
        for i in range(size - 1):
            for j in range(size):
                if a[i][j] == a[i + 1][j] and flags[i][j] and a[i][j] != 0:
                    return True
                if a[i + 1][j] == 0 and a[i][j] != 0:
                    return True
    return False

def MoveRight(a):
    size = len(a)
    flags = MakeFlags(size)
    flag = True
    while (flag):
        flag = False
        for i in range(size):
            for j in range(size - 2, -1, -1):
                if a[i][j] == a[i][j + 1] and flags[i][j] and flags[i][j + 1] and a[i][j] != 0:
                    a[i][j + 1] = 2 * a[i][j + 1]
                    a[i][j] = 0
                    flags[i][j] = False
                    flags[i][j + 1] = False
                    flag = True
                if a[i][j + 1] == 0 and a[i][j] != 0:
                    a[i][j + 1] = a[i][j]
                    flags[i][j] = flags[i][j + 1]
                    a[i][j] = 0
                    flag = True
    return a

def PossibleRight(a):
    size = len(a)
    flags = MakeFlags(size)
    flag = True
    fl1 = False
    while (flag):
        flag = False
        for i in range(size):
            for j in range(size - 1):
                if a[i][j] == a[i][j + 1] and flags[i][j] and a[i][j] != 0:
                    return True
                if a[i][j + 1] == 0 and a[i][j] != 0:
                    return True
    return False

size = 4
a = []
for i in range(size):
    b = [0] * size
    a.append(b)
wasmove = True
while True:
    flags = MakeFlags(size)
    k = []
    for i in range(size):
        for j in range(size):
            if a[i][j] == 0:
                k.append(i * size + j)
    if a[0][0] != 0 and not(PossibleUp(a) or PossibleRight(a) or PossibleDown(a) or PossibleLeft(a)):
        print("\n-=-=-=-=[YOU LOST]=-=-=-=-")
        break
    t = random.randint(0, len(k) - 1)
    if wasmove:
        a[k[t] // size][k[t] % size] = 2
        DisplayField(a)
        wasmove = False
    move = input("use WASD to move\n")
    if move == "w" or move == "W":
        if PossibleUp(a):
            a = MoveUp(a)
            wasmove = True
    if move == "a" or move == "A":
        if PossibleLeft(a):
            a = MoveLeft(a)
            wasmove = True
    if move == "s" or move == "S":
        if PossibleDown(a):
            a = MoveDown(a)
            wasmove = True
    if move == "d" or move == "D":
        if PossibleRight(a):
            a = MoveRight(a)
            wasmove = True

