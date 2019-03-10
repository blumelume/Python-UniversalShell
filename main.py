import config
import sys
from importlib import reload
from types import MethodType

class command:
    def __init__(self, label, att):
        self.label = label
        self.att = att


class attribute:
    def __init__(self, label, req):
        self.label = label
        self.req = req

def newCommA(aLabel, aBool, cLabel, valFunc, runFunc, usageFunc, descFunc):
    if (aLabel != "Null"):
        a = attribute(aLabel, aBool)
        c = command(cLabel, [a])
        c.validate = MethodType(valFunc, c)
        c.usage = MethodType(usageFunc, c)
    else:
        c = command(cLabel, [ ])

    c.description = MethodType(descFunc, c)
    c.run = MethodType(runFunc, c)
    commands.append(c)

def helpValidate(c, inp):
    if (len(inp) > 1):
        #Command validation
        count = 0
        for i in commands:
            if (inp[1] != i.label):
                count += 1
                if (count == len(commands)): return 1 #Command invalid
    return 0

def restartRun(c, inp):
    print()
    print("Restarting shell")
    print()
    print("-------------------------------------------------------")
    return "restart"

def exitRun(c, inp):
    print("Goodbye")
    print()
    sys.exit()

def helpRun(c, inp):
    if (len(inp) > 1):
        #Command validation
        count = 0
        for i in commands:
            #print(inp[1])
            #print(i.label)
            if (inp[1] == i.label):
                i.description()
                break
    else:
        for i in range(0, len(commands)):
            print(str(i + 1) + ". " + commands[i].label, end = "")

            if (len(commands[i].att) >= 1):
                print(" -  ", end = "")
                commands[i].usage()
            else:
                print()

def helpUsage(c):
    print("help + opt:'command'")

def restartDesc(c):
    print("This command restarts this 'shell'. That means it clears the command-history and reloads all of the commands.")

def exitDesc(c):
    print("By typing 'exit', the shells main loop will end and the python script will terminate.")

def helpDesc(c):
    print("I`m assuming you know what help does, since you just used it. Well it shows you all of the commands you can enter here :)")

def loadDefaultCmd(defcmdConfig):

    if (defcmdConfig[0] == 0):
        newCommA("Null", 0, "restart", 0, restartRun, 0, restartDesc)
    if (defcmdConfig[1] == 0):
        newCommA("Null", 0, "exit", 0, exitRun, 0, exitDesc)
    if (defcmdConfig[2] == 0):
        newCommA("command", False, "help", helpValidate, helpRun, helpUsage, helpDesc)


def mainLoad(ld):
    global load
    global commands
    global cmdHistory
    global attributes
    global CURSOR

    cmdHistory = []
    commands = []
    attributes = []

    load = ld
    load()

    reload(config)
    CURSOR = config.inpConfig[0]
    print("done")

    loadDefaultCmd(config.defcmdConfig)

    main()

def main():

    #Mainloop
    a = True
    while(a):
        #input gathering
        curr = getInp()
        #input parse
        splitArray = split(curr)
        #input validation
        inp = val(splitArray)
        #generate output
        out(inp)

def error(errID, inp):
    print("Error: ", end = " ")

    if (errID == 0):
        print("This input is invalid.")
    elif (errID == 1):
        print("Invalid amount of arguments. Usage:")
        inp.usage()
    elif (errID == 2):
        print("Invalid arguments. Usage:")
        inp.usage()
    elif (errID == 3):
        print("Too many arguments. No arguments needed.")

    main()


def getInp():
    printString = ''
    for i in range(1, len(config.inpConfig)):
        printString += (config.inpConfig[i])
    printString += CURSOR

    print()
    curr = input(printString + " ")
    print()
    return curr

def split(curr):
    splitArray = []
    splitArray = curr.split(' ')

    for i in splitArray:
        i.strip()
        if (i == ''):
            splitArray.remove(i)

    return splitArray

def val(inp):
    #print(inp)

    #Command validation
    count = 0
    for i in commands:
        if (inp[0] != i.label):
            count += 1
            if (count == len(commands)): error(0, inp[0]) #Command invalid
        else:   #Command is valid
            inp[0] = i
            break

    #print(len(inp) - 1)
    #print(len(inp[0].att))

    #Validating number of attributes
    if (len(inp[0].att) >= 1):
        count = 0
        for i in range(0, len(inp[0].att)):
            if (inp[0].att[i].req == True):
                count += 1

        if( len(inp) - 1 < count or len(inp) - 1 > len(inp[0].att)):
            error(1, inp[0]) #Invalid amount of attributes

    elif (len(inp) > 1):
        error(3, inp[0])

    #Validate Attributes
    if (len(inp[0].att) >= 1):
        if (inp[0].validate(inp) == 1):
            error(2, inp[0])

    return inp

def out(inp):
    cmdHistory.append(inp)
    a = inp[0].run(inp)
    if (a == "restart"):
        mainLoad(load)
