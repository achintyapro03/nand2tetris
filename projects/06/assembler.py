# checks whether the conversion was successful or not
success = True

# convert a number from decimal to int using bin function
# a string of length is returned using bit extension
def decToBinary(num, u):
    a = str(bin(num))[2:]
    l = len(a)
    for _ in range(u - l):
        a = '0' + a
    return a

# stores the lines in the .asm file
lines = []

a = int(input("Enter choice to convert .asm file to .hack\n1-Add\t2-Max\t3-Pong\t4-Rect : "))

files = ["add/Add", "max/Max", "pong/Pong", "rect/Rect"]


with open((files[a-1]+".asm"), "r") as file:

    # lines are read
    lines = file.read().splitlines()
    new = []

    # comments are filtered out and while spaces are removed
    for i in range(len(lines)):
        if lines[i] != '':
            x = lines[i].replace(' ', '')
            idx = x.find('//')
            if idx == -1:
                new.append(x)
            elif idx != -1 and x[:idx] != '':
                new.append(x[:idx])

    lines = new

# links stores the assembly code without symbols
# all symbols are replaced with integer values
links = []

# lables stores the line numbers of the lables
labels = {}

# stores the key value pairs of the predefined variables in hack
symTab = {"R0": '0', "R1": '1', "R2": '2', "R3": '3', "R4": '4', "R5": '5', "R6": '6', "R7": '7', "R8": '8', "R9": '9',
          "R10": '10', "R11": '11', "R12": '12', "R13": '13', "R14": '14', "R15": '15',
          "SCREEN": '16384',
          "KBD": '24576',
          "SP": '0',
          "LCL": '1',
          "ARG": '2',
          "THIS": '3',
          "THAT": '4',
          "LOOP": '4',
          "STOP": '18',
          "i": '16',
          "sum": '17'
          }


# codes for destination part of the instruction
dest = {'null': '000', 'M': '001', 'D': '010', 'MD': '011', 'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}

# codes for computation part of the instruction
comp = {'0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100', 'A': '0110000',
        'M': '1110000', '!D': '0001101', '!A': '0110001', '!M': '1110001', '-D': '0001111',
        '-A': '0110011', '-M': '1110011', 'D+1': '0011111', 'A+1': '0110111', 'M+1': '1110111',
        'D-1': '0001110', 'A-1': '0110010', 'M-1': '1110010', 'D+A': '0000010', 'D+M': '1000010',
        'D-A': '0010011', 'D-M': '1010011', 'A-D': '0000111', 'M-D': '1000111', 'D&A': '0000000',
        'D&M': '1000000', 'D|A': '0010101', 'D|M': '1010101'}

# codes for jump part of the instruction
jump = {'null': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

# varIdx starts from 16, if new variable is added the carIdx is updated
varIdx = 16

# stores the assembly code without lables
new = []
rem = 0

# jump line of the labels are calculated and stored in lables
for i in range(len(lines)):
    if lines[i][0] == "(":
        tag = lines[i][1:lines[i].find(')')]
        if tag not in labels:
            labels[tag] = str(i - rem)
            rem += 1
        else:
            success = False
            print('Error!!')
            break
    else:
        new.append(lines[i])

# symbols are replaced by their integer values and stored oin links
for i in new:

    # if instruction is A type
    if i[0] == '@':
        x = i[1:]
        try:
            # if the A type instruction has a number
            num = int(x)
            links.append('@' + x)
        except:

            # if the A type instruction has a label

            # the string is searched in labels and symTab
            # the corresponding integer is used
            if x in symTab and x in labels:
                links.append('@' + labels[x])
            elif x in symTab:
                links.append('@' + symTab[x])
                if x == 'i':
                    varIdx += 1

            elif x in labels:
                links.append('@' + labels[x])
            else:
                symTab[x] = str(varIdx)
                varIdx += 1
                links.append('@' + symTab[x])

    # if the instruction is C type
    else:
        links.append(i)

# stores the binary form of all the instructions
binInst = []

for i in links:
    # if the instruction is A type
    if i[0] == '@':
        x = "0" + str(decToBinary(int(i[1:]), 15))
        binInst.append(x)

    # if instruction has = then it is an arithmatic instruction
    elif '=' in i:
        # the string before = gives the destination
        # the string after gives the computation part
        idx = i.find('=')
        d = i[:idx]
        c = i[idx + 1:]

        # now using the dest and the comp dictionaries the codes for the destination and the comp part is obtained
        if c in comp:
            bC = comp[c]
        elif c[::-1] in comp:
            bC = comp[c[::-1]]

        # if they are not present then the line is invalid according to Hack ISA
        else:
            success = False
            print("Invalid operator")
            print("Error!!!")
            print(i)
            break

        # Final string is obtained by concatenating the foloowing in order
        # "111" as it is a C type instruction bits and bits 14 and 13 are always 1
        # bC the 76 bit compuatation part

        s = "111" + bC + dest[d] + "000"
        binInst.append(s)

    # if ; is present then the instruction is jump type
    # the part before ; gives the compuytation part
    # the part after ; gives the jump condition
    elif ';' in i:
        idx = i.find(';')
        c = i[:idx]
        j = i[idx + 1:]

        s = "111" + comp[c] + "000" + jump[j]

        # final binarystring is calculated
        binInst.append(s)
    
    else:
        print("Invalid statement")
        print("Error!!!")
        print(i)
        success = False
        break

# if the conversion is successful, the binary code is written into a file
if(success):
    with open((files[a-1]+".hack"), "w") as f:
        for i in binInst:
            f.write(i)
            f.write('\n')

    print(f"\n{files[a-1]}.asm has been converted into {files[a-1]}.hack format.\nPlease check the respective sub folder\n")
else:
    print("Conversion failed\nI Give Up!!")
