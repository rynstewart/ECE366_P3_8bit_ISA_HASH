def saveJumpLabel(asm, labelIndex, labelName, labelAddr):
    lineCount = 0
    for line in asm:
        line = line.replace(" ", "")
        if (line.count(":")):
            labelName.append(line[0:line.index(":")])  # append the label name
            labelIndex.append(lineCount)  # append the label's index\
            labelAddr.append(lineCount * 4)
            # asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')


def regNameInit(regName):
    i = 0
    while (i <= 4):
        regName.append(str(i))
        i = i + 1
    regName.append('lo')
    regName.append('hi')

def splitText(text):
    return text.split("\n")

def readIn(s):
    text = ""
    with open(s, "r") as f:
        for line in f:
            if (line != "\n" and line[0]!='#'):
                text += line

    return text


def main():
    # starting with 100 spots in MEM
    MEM = [0] * 300
    regName = []
    PC = 0
    DIC = 0
    regNameInit(regName)
    regval = [0] * 7  # 0-3, A, lo and hi
    LO = 4
    HI = 5
    A = 6
    regval[A] = 1
    good_in = False
    mem_addr = 0x0004


    #TODO: update op code to same bits
    initlo = "00"
    inithi = "10"  # has to be checked after ld and st(last ones)
    xor = "0010"
    sinc2b = "0011"
    addu = "0110"
    addiu = "0111"
    and1 = "1000"
    srl = "1010"
    Fold = "1101"
    sub = "1111"
    Hash_branch = "1110"
    LA = "0000"
    pat_Count = "0101"

    while (good_in == False):

        file_Name = input("Please type file name, enter for default, or q to quit:\n")

        if (file_Name == "q"):
            print("Bye!")
            return
        if (file_Name == ""):
            file_Name = "test.asm"
        try:
            f = open(file_Name)
            f.close()
            good_in = True
        except FileNotFoundError:
            print('File does not exist')

    f = open("output.txt", "w+")

    text = readIn(file_Name)
    t = splitText(text)

    lineCount = 0
    while (lineCount < len(t)):

        line = t[lineCount]

        f.write('------------------------------ \n')
        if (not (':' in line)):
            f.write('MIPS Instruction: ' + line + '\n')


        if(line[0:4] == srl):
            DIC += 1
            # XXXXSSTT
            #always to $3
            PC += 4
            RT = regval[int(line[6:8], 2)]

            regval[3] = regval[int(line[4:6])] >> RT
        
        elif(line[0:4] == pat_Count):
            DIC += 1
            PC += 4
            pattern = regval[int(line[6:8],2)]
            if(pattern == 0):
                MEM[0] += 1

            if(pattern == 1):
                MEM[1] += 1

            if(pattern == 2):
                MEM[2] += 1

            if(pattern == 3):
                MEM[3] += 1


        elif (line[0:4] == sinc2b):
            DIC += 1
            PC += 4
            X = regval[int(line[4:6])]
            MEM[mem_addr] = X
            mem_addr += 1
            f.write('Operation: MEM[$' + line[7:8] + '] = ' + line[5:6] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
        
        elif(line[0:4] == LA):
            DIC += 1
            PC += 4
            regval[int(line[6:8],2)] = regval[A]
            f.write('Operation: $' + str(int(line[6:8])) + ' = ' + str(regval[int(line[6:8])]) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('DIC is now at '+str(DIC))

        elif(line[0:4] == addu):
            DIC += 1
            PC += 4
            #if(regval[A]==2):
             #   breakpoint()
            regval[int(line[4:6],2)] += regval[int(line[6:8],2)]
            
            f.write('Operation: $' + str(int(line[5:6])) + ' = ' + str(regval[int(line[5:6])]) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('DIC is now at '+str(DIC))

        elif(line[0:4] == sub):
            DIC += 1
            PC += 4
            regval[int(line[4:6],2)] -= regval[int(line[6:8],2)]
            
            f.write('Operation: $' + str(int(line[5:6])) + ' = ' + str(regval[int(line[5:6])]) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('DIC is now at '+str(DIC))

        #andi
        elif(line[0:4] == and1):
            DIC += 1
            PC += 4
            regval[int(line[4:6],2)] = regval[int(line[4:6],2)] & regval[int(line[6:8],2)]
            f.write('Operation: MEM[$' + line[5:6] + '] = ' + line[7:8] + '; ' + '\n')

        # xor
        elif (line[0:4] == xor):
            DIC += 1
            PC += 4
            regval[0] = regval[int(line[4:6],2)] ^ regval[int(line[6:8],2)]


        elif (line[0:4] == Fold):
            #Always comes out from C = $0
            DIC += 1
            PC += 4
            result = regval[int(line[4:6],2)] * regval[int(line[6:8],2)]
            tempL = result & 0b11111111
            tempH = result >> 8
            regval[int(line[6:8],2)] = tempH ^ tempL
            f.write('Operation: $' + str(0) + ' = ' + str(regval[0]) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('DIC is now at '+str(DIC))

        #initli: lower 4
        elif (line[0:2] == initlo):
            DIC += 1
            PC += 4
            reg = int(line[2:4], 2)
            imm = int(line[4:8], 2)
            regval[reg] += imm
            f.write('Operation: $' + str(reg) + ' = ' + str(imm) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + str(reg) + ' = ' + str(imm) + '\n')

        #initui: upper 4
        elif (line[0:2] == inithi):
            DIC += 1
            PC += 4
            reg = int(line[2:4], 2)
            imm = int(line[4:8], 2)
            regval[reg] += imm << 4
            f.write('Operation: $' + str(reg) + ' = ' + str(imm) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + str(reg) + ' = ' + str(imm) + '\n')

        elif (line[0:4] == Hash_branch):
            DIC += 1
            if(regval[A] != 255):
                PC = 0
                lineCount = 0
                regval[A] += 1
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('No Registers have changed. \n')
                continue
            f.write('Branch not taken, no Registers have changed. \n')
            PC += 4

        lineCount += 1


    print("REGISTERS:")
    print("-----------")

    for x in range(len(regval)):
        if (x == LO):
            print("LO: ", hex(regval[x]))
        elif (x == HI):
            print("HI: ", hex(regval[x]))
        elif (x == A):
            print("A: ", hex(regval[x]))
        else:
            print("$", x, ": ", hex(regval[x]))
    print("PC: ", hex(PC))
    print("DIC: ", hex(DIC))

    print("\n")
    print("Used Memory values:\n")
    print("            ", end="")
    #for x in range(0, 4, 1):
     #   print("0b" + format((x * 2), "02b"), end=" ")
    print("\n")
    print("---------------------------------------------------------------------", end="")
    count = 0
    print("\n")
    for x in range(4, 1017, 1):
        x = x*4
        print("0b", end="")
        for y in range(3, -1, -1):
           # z = (y + x)*4
            print(format(MEM[y + x], "02b"), end="")
        print(" ", end="")
        count += 1
        if (count == 4):
            count = 0
            print("\n")
        x = x/4
    
    print("MODES OF 2 BIT BINARY RESULTS (in hex)\n")
    print("----------------------------------------")
    for x in range (0,4,1):
        print("\nMem["+str(x)+"] = ", end="")
        print(format(MEM[x], "02x"))
       
        '''
        if ((x - 0x3) % 0x20 == 0):
            print("0x" + format(x - 0x3, "08x") + '|', end=" ")
        print("0x", end="")
        for y in range(0, 4, 1):
            print(format(MEM[x - y], "02x"), end="")
        print(" ", end="")
        count += 1
        if (count == 8):
            count = 0
            print("\n")
        '''

    f.close()


main()
