matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]

def saveMatrix(matrix, fisier):
    f = open(fisier, "w")
    f.write(str(len(matrix)))
    f.write(" ")
    f.write(str(len(matrix[0])))
    f.write("\n")
    for linie in matrix:
        for element in linie:
            f.write(str(element))
            f.write(" ")
        f.write("\n")
    f.close()

def loadMatrix(fisier):
    f = open(fisier, "r")
    lines = f.readlines()
    ok = 0
    matrix = []
    for line in lines:
        line = line.strip()
        line = line.split()
        if ok == 0:
            m, n = int(line[0]), int(line[1])
            ok = 1
        else:
            linie_matrice = []
            i = 0
            while i < len(line):
                if line[i] == "//":
                    break
                else:
                    linie_matrice.append(int(line[i]))
                i += 1
            if len(linie_matrice) != 0 and len(linie_matrice) == int(n):
                matrix.append(linie_matrice)
    print (matrix)

print("1. Load matrix")
print("2. Save matrix")
variabila = int(input("Enter an option: "))
if variabila == 1:
    loadMatrix("fisier.in")
elif variabila == 2:
    saveMatrix(matrix, "fisier.out")
else:
    print("Invalid input")

# loadMatrix("fisier.in")
# saveMatrix(matrix, "fisier.out")

