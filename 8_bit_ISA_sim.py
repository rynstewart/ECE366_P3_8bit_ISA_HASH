def saveJumpLabel(asm,labelIndex, labelName, labelAddr):
    lineCount = 0
    for line in asm:
        line = line.replace(" ","")
        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(lineCount) # append the label's index\
            labelAddr.append(lineCount*4)
            #asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

def regNameInit(regName):
    i = 0
    while(i<=4):
        regName.append(str(i))
        i = i + 1
    regName.append('lo')
    regName.append('hi')


def main():
    #starting with 100 spots in MEM
    MEM = [0]*256
    labelIndex = []
    labelName = []
    labelAddr = []
    regName = []
    PC = 0
    regNameInit(regName)
    regval = [0]*6 #0-4, lo and hi
    LO = 5
    HI = 6
    good_in = False

    addiu = "1000"
    xor = "1001"
    initli = "00"
    initui = "01" #has to be checked before ld and st
    ld = "0100"
    st = "0101"
    add = "0110"
    bezR0 = "1011"
    jmp = "1100"

    while(good_in == False):
      
        file_Name = input("Please type file name, enter for default, or q to quit:\n")

        if(file_Name == "q"):
           print("Bye!")
           return
        if(file_Name == ""):
            file_Name = "test.asm"
        try:
            f = open(file_Name)
            f.close()
            good_in = True
        except FileNotFoundError:
            print('File does not exist')
    
    f = open("mc.txt","w+")
    h = open(file_Name,"r")

    asm = h.readlines()
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm,labelIndex,labelName, labelAddr) # Save all jump's destinations

    #for lineCount in len(asm):
    lineCount = 0
    while(lineCount < len(asm)):

        line = asm[lineCount]
        
        if(line[0]=='#'):
            lineCount += 1
            continue

        f.write('------------------------------ \n')
        if(not(':' in line)):
            f.write('MIPS Instruction: ' + line + '\n')
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0
        #breakpoint()
        if(line[0:2] == initli):
            PC +=4
            regval[int(line[1:2],2)]= int(line[3:6],2)
            f.write('Operation: $' + str(int(line[1:2],2)) + ' = ' + str(int(line[3:6],2)) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
        
        #addiu
        elif(line[0:4] == addiu):
            line = line.replace("addi", "").split(",")
            PC += 4
            regval[int(line[0])] = regval[int(line[1])] + int(line[2])
            f.write('Operation: MEM[$' + line[1] + '] = ' + line[0] + '; ' + '\n')

        #xor
        elif (line[0:4] == xor):
            line = line.replace("xor", "").split(",")
            PC += 4
            regval[int(line[0])] = regval[int(line[1])] ^ regval[int(line[2])]

        elif(line[0:2] == ld):
            line= line.replace(ld,"")
            line = line.replace("(","")
            line = line.replace(")","")
            line= line.split(",")
            PC +=4

            regval[int(line[0])]= MEM[regval[int(line[1])]]
            f.write('Operation: $' + line[0] + ' = ' + 'MEM[$' + line[1] + ']; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

        elif(line[0:2] == "st"):
            line= line.replace("st","")
            line = line.replace("(","")
            line = line.replace(")","")
            line= line.split(",")
            print(line)
            PC +=4
            X= regval[int(line[0])]
            MEM[regval[int(line[1])]] = X
            f.write('Operation: MEM[$' + line[1] + '] = ' + line[0] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            #ask about regs that changed

        elif(line[0:5] == "bezR0"): # Beq
            line = line.replace("bezR0","")
            line = line.split(",")
            try:
                imm = int(line[0],16)
            except:
                f.write("ERROR: Invalid Instruction")
                break
            if(regval[0]==0):
                PC = PC + (4*imm)
                lineCount = lineCount + imm
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('No Registers have changed. \n')
                continue
            f.write('No Registers have changed. \n')
            PC += 4


        elif(line[0:3] == "jmp"): # jmp
            line = line.replace("jmp","")
            line = line.split(",")
            try:
                imm = int(line[0],16)
            except:
                f.write("ERROR: Invalid Instruction")
                break
            PC = PC + (4*imm)
            lineCount = lineCount + imm
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('No Registers have changed. \n')
            continue

        lineCount += 1

    print("REGISTERS:")
    print("-----------")
    for x in range(len(regval)):
        if(x == 4):
            print("lo: ", hex(regval[x]))
        elif(x == 5):
            print("hi: ", hex(regval[x]))
        else:
            print("$", x,": ", hex(regval[x]))
    print("PC: ", hex(PC))

    print("\n")
    print("Used Memory values:\n")
    print("            ", end="")
    for x in range(0,8,1):
        print("0x"+ format((x*4),"08x"), end=" ")
    print("\n")
    print("--------------------------------------------------------------------------------------------------",end="")
    count = 0
    print("\n")
    for x in range(0x0000,0x0100,4):
        if((x-0x3)%0x20==0):
            print("0x"+format(x-0x3,"08x") + '|', end=" ")
        print("0x", end="")
        for y in range(0,4,1):
            print(format(MEM[x-y], "02x"), end="")
        print(" ", end = "")
        count += 1
        if(count == 8):
            count = 0
            print("\n")

    f.close()

if __name__ == "__main__":
    main()
