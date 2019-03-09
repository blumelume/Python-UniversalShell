import config
from importlib import reload

class command:
    def __init__(self, Id, label, att):
        self.Id = Id
        self.label = label
        self.att = att


class attribute:
    def __init__(self, label, req):
        self.label = label
        self.req = req

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
