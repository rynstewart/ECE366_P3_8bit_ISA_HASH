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

#setting ip registers
def regNameInit(regName): 
    i = 0
    while (i <= 4):
        regName.append(str(i))
        i = i + 1
    regName.append('lo')
    regName.append('hi')

#created list to read non empty and un commented lines
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
    # starting with 259 spots in MEM
    MEM = [0] * 259
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

    #op code declarations
    initlo = "00"
    inithi = "10"  # has to be checked before ld and st(last ones)
    xor = "0010"
    sinc2b = "0011"
    addu = "0110"
    and1 = "1000"
    srl = "1010"
    Fold = "1101"
    sub = "1111"
    Hash_branch = "1110"
    LA = "0000"
    pat_Count = "0101"

    #bit of UI
    while (good_in == False):

        file_Name = input("Please type file name, enter for default, or q to quit:\n")

        if (file_Name == "q"):
            print("Bye!")
            return
        if (file_Name == ""):
            file_Name = "FA_mc.txt"
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
        
        
        #starting to print to output.txt
        f.write('------------------------------ \n')
        if (not (':' in line)):
            f.write('MIPS Instruction: ' + line + '\n')


        if(line[0:4] == srl):
            DIC += 1
            # XXXXSSTT
            #always to $3
            PC += 4
            RT = regval[int(line[6:8], 2)]

            regval[3] = regval[int(line[4:6],2)] >> RT

            f.write('Operation: $' + str(int(line[6:8],2)) + ' = ' + str(regval[int(line[6:8],2)]) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('DIC is now at '+str(DIC))
        
        #this branch does pattern count by using 4 different
        #if statements, it was implemented in hardware using Muxes
        elif(line[0:4] == pat_Count):
            DIC += 1
            PC += 4
            pattern = regval[int(line[6:8],2)]
            if(pattern == 0):
                MEM[0] += 1
                y = 0

            elif(pattern == 1):
                MEM[1] += 1
                y = 1

            elif(pattern == 2):
                MEM[2] += 1
                y = 2

            elif(pattern == 3):
                MEM[3] += 1
                y = 3
            
            
            f.write('Operation: MEM[+'+str(y)+'] = ' + str(regval[int(line[6:8],2)]) + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('DIC is now at '+str(DIC))


        elif (line[0:4] == sinc2b):
            DIC += 1
            PC += 4
            X = regval[int(line[6:8],2)]
            MEM[mem_addr] = X
            mem_addr += 1
            f.write('Operation: MEM[$' + str(mem_addr-1) + '] = ' + str(regval[int(line[6:8],2)]) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('DIC is now at '+str(DIC))
        
        #This instuction will load the unaddressable register A into an addressable register
        elif(line[0:4] == LA):
            DIC += 1
            PC += 4
            regval[int(line[6:8],2)] = regval[A]
            f.write('Operation: $' + str(int(line[6:8],2)) + ' = ' + str(regval[int(line[6:8],2)]) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('DIC is now at '+str(DIC))

        # addu not really implemented, but in theory in should be, 
        # however we wrote the input so it doesn't cause any issues
        # at the moment
        elif(line[0:4] == addu):
            DIC += 1
            PC += 4
            regval[int(line[4:6],2)] += regval[int(line[6:8],2)]
            
            f.write('Operation: $' + str(int(line[4:6],2)) + ' = ' + str(regval[int(line[4:6],2)]) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('DIC is now at '+str(DIC))

        #this instruction is mainly used for setting equal to 0
        elif(line[0:4] == sub):
            DIC += 1
            PC += 4
            regval[int(line[4:6],2)] -= regval[int(line[6:8],2)]
            
            f.write('Operation: $' + str(int(line[4:6],2)) + ' = ' + str(regval[int(line[4:6],2)]) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('DIC is now at '+str(DIC))

        #andi
        elif(line[0:4] == and1):
            DIC += 1
            PC += 4
            regval[int(line[4:6],2)] = regval[int(line[4:6],2)] & regval[int(line[6:8],2)]
            f.write('Operation: $' + str(int(line[4:6],2)) + ' = ' + str(regval[int(line[4:6],2)]) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('DIC is now at '+str(DIC))

        # xor
        elif (line[0:4] == xor):
            DIC += 1
            PC += 4
            regval[0] = regval[int(line[4:6],2)] ^ regval[int(line[6:8],2)]
            f.write('Operation: $0 = ' + str(regval[0]) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('DIC is now at '+ str(DIC))

        #Fold
        elif (line[0:4] == Fold):
            #Always comes out from C = $0
            DIC += 1
            PC += 4
            result = regval[int(line[4:6],2)] * regval[int(line[6:8],2)]
            regval[LO] = result & 0b11111111
            regval[HI] = result >> 8
            regval[int(line[6:8],2)] = regval[HI] ^ regval[LO]
            f.write('Operation: $' + str(0) + ' = ' + str(regval[0]) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('DIC is now at '+str(DIC))
        
        
        # Specific branch function to be used with hash only
        # it loops back to the first line of the code and 
        # increments contents of register A till it's 255
        elif (line[0:4] == Hash_branch):
            DIC += 1
            if(regval[A] != 255):
                PC = 0
                lineCount = 0
                regval[A] += 1
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Branch Taken. No Registers have changed. \n')
                f.write('DIC is now at '+str(DIC))
                continue
            f.write('Branch not taken, no Registers have changed. \n')
            f.write('DIC is now at '+str(DIC))
            PC += 4

        #initli: lower 4 bit intialization (only usable with $1)
        elif (line[0:2] == initlo):
            DIC += 1
            PC += 4
            reg = int(line[2:4], 2)
            imm = int(line[4:8], 2)
            regval[reg] += imm
            f.write('Operation: $' + str(reg) + ' lower 4 bits = ' + str(imm) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('DIC is now at '+str(DIC))

        #initui: upper 4 bit intialization (only usable with $1)
        elif (line[0:2] == inithi):
            DIC += 1
            PC += 4
            reg = int(line[2:4], 2)
            imm = int(line[4:8], 2)
            regval[reg] += imm << 4
            f.write('Operation: $' + str(reg) + ' upper 4 bits = ' + str(imm) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + str(reg) + ' = ' + str(imm) + '\n')
            f.write('DIC is now at '+str(DIC))

        lineCount += 1


    f.write("\nREGISTERS:\n")
    f.write("-----------\n")

    for x in range(len(regval)):
        if (x == LO):
            f.write("LO: " + str(hex(regval[x]))+'\n')
        elif (x == HI):
            f.write("HI: " + str(hex(regval[x]))+'\n')
        elif (x == A):
            f.write("A: " + str(hex(regval[x]))+'\n')
        else:
            f.write("$"+ str(x) + ": " + str(hex(regval[x]))+'\n')
    f.write("PC: " + str(hex(PC))+'\n')
    f.write("DIC: " + str(hex(DIC))+'\n')

    f.write("\n")
    f.write("USED MEMORY VALUES:\n")
    f.write("---------------------------------------------------------------------\n")
    for x in range(4, len(MEM), 1):
        f.write("At " + str(x) + "\tA = " + str(x-3) +"\tC = "+ str(MEM[x]) + "  ")
        if (x - 3) % 4 == 0:
            f.write("\n")

    f.write("\n")
    
    f.write("\nMODES OF 2 BIT BINARY RESULTS (in decimal)\n")
    f.write("----------------------------------------")
    for x in range (0,4,1):
        f.write("\nMem["+str(x)+"] = ")
        f.write(str(MEM[x]))

    f.write("\n")

    f.close()


main()
