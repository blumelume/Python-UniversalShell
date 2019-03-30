import config
import sys
from importlib import reload
from tkinter import *
from types import MethodType

class command:
    def __init__(self, label, att):
        self.label = label
        self.att = att

class attribute:
    def __init__(self, req):
        self.req = req

def send():
    print(entryTxt.get())

    w.config(state = NORMAL)
    w.insert(END, "\n" + entryTxt.get())
    w.config(state = DISABLED)
    w.see(INSERT)

def addCommand(cLabel, valFunc = 0, runFunc = 0, usageFunc = 0, descFunc = 0, aBool = "Null"):
    # if (valFunc == 0 or runFunc == 0 or usageFunc == 0 or descFunc == 0):
    #     error(-1)

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
        count = 0
        for i in commands:
            if (inp[1] != i.label):
                count += 1
                if (count == len(commands)): return 1 #Command invalid
    return 0

def hValidate(c, inp):

    if (len(cmdHistory) < 1):
        return 4

    if (len(inp) == 2):
        try:
            inp[1] = int(inp[1])
        except ValueError:
            return 2

        if (inp[1] > len(cmdHistory) or inp[1] < 1):
            return 2

    return 0

def restartRun(c, inp):
    scw()
    scw("Restarting shell")
    scw()
    scw("-------------------------------------------------------")
    return "restart"

def exitRun(c, inp):
    scw("Goodbye")
    scw()
    sys.exit()

def helpRun(c, inp):
    scw("Type 'help' <command> for commands description.")
    scw()
    if (len(inp) > 1):
        count = 0
        for i in commands:
            if (inp[1] == i.label):
                i.description()
                break
    else:
        for i in range(0, len(commands)):
            scw(str(i + 1) + ". " + commands[i].label, end = "")

            if (len(commands[i].att) >= 1):
                scw(" -  ", end = "")
                commands[i].usage()
            else:
                print()

def hRun(c, inp):
    if (len(inp) == 2):
        temp = len(cmdHistory) - inp[1]
    else:
        temp = len(cmdHistory) - 2

    scw(">> " + cmdHistory[temp])
    i = input("? ")

    if (i.lower() == ""):
        main(cmdHistory[temp])

    elif (i.lower() != "n"):
        error(2, inp[0])

def helpUsage(c):
    scw("help (<command>)")

def hUsage(c):
    scw("h (<1-max number>)")

def restartDesc(c):
    scw("This command restarts this 'shell'. That means it clears the command-history and reloads all of the commands as well as the config file.")

def exitDesc(c):
    scw("By typing 'exit', the shells main loop will end and the python script will terminate.")

def helpDesc(c):
    scw("I`m assuming you know what help does, since you just used it. Well it shows you all of the commands you can enter here :)")
    scw("If you type 'help' <command> it will show you the commands description.")
    scw("If you just type 'help' it will show all of the commands with their usage.")

def hDesc(c):
    scw("This command lets you use a command you have recently typed already. It gives you acces to the command history.")
    scw("You can also type 'h' <number from 1-number of entered commands or maximum length>. This number increases he further back in he history you get.")
    scw("For the latest command you would type 'h' or 'h 1'. For the secodn latest 'h 2' and so on...")
    scw("You will get a question mark. You either type enter to execute the command like shown above or type 'n' to abort the process.")
    scw()
    scw("You can set the historys maxium length in the config.py file.")

def loadDefaultCmd(defcmdConfig):

    if (defcmdConfig[0] == 0):
        addCommand("restart", 0, restartRun, 0, restartDesc)
    if (defcmdConfig[1] == 0):
        addCommand("exit", 0, exitRun, 0, exitDesc)
    if (defcmdConfig[2] == 0):
        addCommand("help", helpValidate, helpRun, helpUsage, helpDesc, False)
    if (defcmdConfig[3] == 0):
        addCommand("h", hValidate, hRun, hUsage, hDesc, False)


def mainLoad(ld = 0):
    global load
    global commands
    global cmdHistory
    global printString

    global mw
    global entryTxt
    global labelTxt
    global w

    cmdHistory = []
    commands = []

    load = ld
    if (load != 0): load()

    reload(config)
    loadDefaultCmd(config.defcmdConfig)

    printString = ''
    for i in range(1, len(config.inpConfig)):
        printString += (config.inpConfig[i])
    printString += config.inpConfig[0]

    # Tkinter init
    windowWidth = 600
    windowHeight = 200
    textFieldHeight = 50

    mainBG = '#fff3e6'

    mw = Tk()
    mw.configure(background = '#fff3e6')
    mw.minsize(width = windowWidth, height = windowHeight)
    mw.maxsize(width = windowWidth, height = windowHeight)
    mw.grid_columnconfigure( [0, 1, 2, 3 ], minsize = 150)
    mw.grid_rowconfigure([0, 1, 2, 3 ], minsize = 50)
    mw.pack_propagate(0)

    labelFrame = Frame(mw, width = 580, height = 140)
    labelFrame.configure(background = '#ffe6e6')
    labelFrame.grid(row = 0, column = 0, columnspan = 1, rowspan = 3, padx = (10, 0), pady = (10, 0), sticky = 'NW')
    labelFrame.pack_propagate(0)

    textFrame = Frame(mw, width = 430, height = 30)
    textFrame.configure(background = mainBG)#'#ccffcc')
    textFrame.grid(row = 3, column = 0, columnspan = 2, rowspan = 3, padx = (10, 0), pady = (10, 0), sticky = "NW")
    textFrame.pack_propagate(0)

    w = Text(labelFrame)
    scrollbar = Scrollbar(labelFrame, command = w.yview)
    w.config(yscrollcommand = scrollbar.set)

    scrollbar.pack(side = "right", fill = BOTH)
    w.pack(side = "left")

    entryTxt = StringVar()
    e = Entry(textFrame, textvariable = entryTxt, width = 52)
    e.grid(sticky = "NW")

    b = Button(mw, text = "send", width = 10, command = send)
    b.grid(row = 3, column = 0, sticky = "E")


    print()
    print("done")
    
    mw.mainloop()
    main()

def main(hCmd = "Null"):
    global cmdHistory

    #Mainloop
    a = True
    while(a):
        #Keep command history at right length
        if (config.cmdHistoryLen != "n" and len(cmdHistory) > config.cmdHistoryLen):
            del cmdHistory[0]

        curr = getInp(hCmd) #input gathering
        hCmd = "Null"

        splitArray = split(curr) #input parse

        inp = val(splitArray) #input validation

        out(inp) #generate output

        mw.mainloop()

def error(errID, inp = 0):
    # There are no switch statements in python! WHY?!?!?

    if (errID > 0):
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
        elif (errID == 5):
            print("Value error. Unable to convert to integer.")
        elif (errID == 6):
            print("Value error. Unable to convert to string.")

        main()

    else:
        print("CodingError: ", end = " ")
        if (errID == -1):
            print("You didnt define")
        elif (errID == -2):
            print("")

        sys.exit()



def getInp(hCmd):
    global printString

    print()
    if (hCmd == "Null"):
        #curr = input(printString + " ")
        curr = entryTxt.get()
        print()
    else:
        curr = hCmd

    return curr

def split(curr):
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

    #Validating number of attributes
    if (len(inp[0].att) >= 1): #Command takes arguments / attributes
        count = 0
        for i in range(0, len(inp[0].att)):
            if (inp[0].att[i].req == True):
                count += 1

        if(len(inp) - 1 < count or len(inp) - 1 > len(inp[0].att)):
            error(1, inp[0]) #Invalid amount of attributes

    elif (len(inp) > 1):
        error(3, inp[0])

    #Validate Attributes
    if (len(inp[0].att) >= 1):
        temp = inp[0].validate(inp)
        if (temp != 0):
            error(temp, inp[0])

    return inp

def scw(str):
    w.insert(END, "\n" + str)

def out(inp):
    a = inp[0].run(inp)

    temp = inp[0].label
    for i in range(1, len(inp)):
        temp += " " + str(inp[i])
    cmdHistory.append(temp)

    if (a == "restart"):
        mainLoad(load)

mainLoad()
