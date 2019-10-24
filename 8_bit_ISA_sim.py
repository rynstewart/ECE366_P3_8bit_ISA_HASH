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
    while(good_in == False):
        file_Name = input("Please type file name, enter for default, or q to quit:")
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
        f.write('------------------------------ \n')
        if(not(':' in line)):
            f.write('MIPS Instruction: ' + line + '\n')
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0
        

        if(line[0:4] == "halt"):
            PC += 4
            break
        #implement actual sim here



        lineCount += 1

    print("REGISTERS:")
    print("-----------")
    for x in range(len(regval)):
        if(x == 5):
            print("lo: ", hex(regval[x]))
        elif(x == 6):
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
