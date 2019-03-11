import config
import sys
from importlib import reload
from types import MethodType

class command:
    def __init__(self, label, att):
        self.label = label
        self.att = att


class attribute:
    def __init__(self, req):
        self.req = req

def newCommA(aBool, cLabel, valFunc, runFunc, usageFunc, descFunc):
    if (aBool != "Null"):
        a = attribute(aBool)
        print(a)
        print([a])
        c = command(cLabel, [a])
        print(c.att)
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

def hValidate(c, inp):
    # for i in cmdHistory:
    #     if (i == ):
    #         cmdHistory.remove(i)

    if (len(cmdHistory) < 1):
        return 4

    if (len(inp) == 2):
        try:
            inp[1] = int(inp[1])
        except:
            return 2

        if (inp[1] > len(cmdHistory) or inp[1] < 1):
            return 2

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

def hRun(c, inp):
    if (len(inp) == 2):
        temp = len(cmdHistory) - inp[1]
    else:
        temp = len(cmdHistory) - 2
    print(">> " + cmdHistory[temp])

    i = input("? ")
    if (i.lower() == ""):
        main(cmdHistory[temp])

    elif (i.lower() != "n"):
        error(2, inp[0])

def helpUsage(c):
    print("help + opt:'command'")

def hUsage(c):
    print("h + opt.: <1-5>")

def restartDesc(c):
    print("This command restarts this 'shell'. That means it clears the command-history and reloads all of the commands.")

def exitDesc(c):
    print("By typing 'exit', the shells main loop will end and the python script will terminate.")

def helpDesc(c):
    print("I`m assuming you know what help does, since you just used it. Well it shows you all of the commands you can enter here :)")

def hDesc(c):
    print("This command lets you use a command you have recently typed already. It gives you acces to the command history.")
    print("You can set its maxium length in the config.py file.")

def loadDefaultCmd(defcmdConfig):

    if (defcmdConfig[0] == 0):
        newCommA("Null", "restart", 0, restartRun, 0, restartDesc)
    if (defcmdConfig[1] == 0):
        newCommA("Null", "exit", 0, exitRun, 0, exitDesc)
    if (defcmdConfig[2] == 0):
        newCommA(False, "help", helpValidate, helpRun, helpUsage, helpDesc)
    if (defcmdConfig[3] == 0):
        newCommA(False, "h", hValidate, hRun, hUsage, hDesc)


def mainLoad(ld):
    global load
    global commands
    global cmdHistory
    global CURSOR

    cmdHistory = []
    commands = []

    load = ld
    load()

    reload(config)
    CURSOR = config.inpConfig[0]
    print("done")

    loadDefaultCmd(config.defcmdConfig)

    main()

def main(hCmd = "Null"):
    global cmdHistory

    #Mainloop
    a = True
    while(a):
        if (config.cmdHistoryLen != "n"):
            if (len(cmdHistory) > config.cmdHistoryLen):
                cmdHistory = []

        #input gathering
        curr = getInp(hCmd)
        hCmd = "Null"
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
    elif (errID == 4):
        print("Command history is empty.")

    main()


def getInp(hCmd):

    printString = ''
    for i in range(1, len(config.inpConfig)):
        printString += (config.inpConfig[i])
    printString += CURSOR

    print()
    if (hCmd == "Null"):
        curr = input(printString + " ")
        print()
    else:
        curr = hCmd
        
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
        temp = inp[0].validate(inp)
        if (temp != 0):
            error(temp, inp[0])

    return inp

def out(inp):
    a = inp[0].run(inp)

    temp = inp[0].label
    for i in range(1, len(inp)):
        temp += " " + str(inp[i])
    cmdHistory.append(temp)

    if (a == "restart"):
        mainLoad(load)
