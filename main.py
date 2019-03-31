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



def mainLoad(ld):
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

    b = Button(mw, text = "send", width = 10, command = main)
    b.grid(row = 3, column = 0, sticky = "E")

    load = ld
    print(load)
    load()

    reload(config)
    # loadDefaultCmd(config.defcmdConfig)

    printString = ''
    for i in range(1, len(config.inpConfig)):
        printString += (config.inpConfig[i])
    printString += config.inpConfig[0]



    print()
    scw("done")
    mw.mainloop()

# def loadDefaultCmd(defcmdConfig):
#
#     if (defcmdConfig[0] == 0):
#         addCommand("restart", 0, restartRun, 0, restartDesc)
#     if (defcmdConfig[1] == 0):
#         addCommand("exit", 0, exitRun, 0, exitDesc)
#     if (defcmdConfig[2] == 0):
#         addCommand("help", helpValidate, helpRun, helpUsage, helpDesc, False)
#     if (defcmdConfig[3] == 0):
#         addCommand("h", hValidate, hRun, hUsage, hDesc, False)


def main(hCmd = "Null"):
    global cmdHistory

    #Keep command history at right length
    if (config.cmdHistoryLen != "n" and len(cmdHistory) > config.cmdHistoryLen):
            del cmdHistory[0]

    curr = getInp(hCmd) #input gathering
    hCmd = "Null"

    splitArray = split(curr) #input parse

    inp = val(splitArray) #input validation

    out(inp) #generate output

def error(errID, inp = 0):
    # There are no switch statements in python! WHY?!?!?

    if (errID >= 0):
        scw("Error: ", end = " ")
        if (errID == 0):
            scw("This input is invalid.")
        elif (errID == 1):
            scw("Invalid amount of arguments. Usage:")
            inp.usage()
        elif (errID == 2):
            scw("Invalid arguments. Usage:")
            inp.usage()
        elif (errID == 3):
            scw("Too many arguments. No arguments needed.")
        elif (errID == 4):
            scw("Command history is empty.")
        elif (errID == 5):
            scw("Value error. Unable to convert to integer.")
        elif (errID == 6):
            scw("Value error. Unable to convert to string.")

        mw.mainloop()

    else:
        scw("CodingError: ", end = " ")
        if (errID == -1):
            scw("You didnt define")
        elif (errID == -2):
            scw("")

        sys.exit()



def getInp(hCmd):
    global printString

    print()
    if (hCmd == "Null"):
        #curr = input(printString + " ")
        curr = entryTxt.get()
        print("curr:", curr)
    else:
        curr = hCmd

    if (curr != ''):
        scw()
        scw(printString + " " + curr)
        return curr
    else:
        mw.mainloop()

def split(curr):
    splitArray = curr.split(' ')

    for i in splitArray:
        i.strip()
        if (i == ''):
            splitArray.remove(i)

    return splitArray

def val(inp):
    print("val")
    print(inp)

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

def scw(temp = "", end = 0):
    global w
    print("scw")
    if (end == 0):
        temp = str(temp) + '\n'

    w.config(state = NORMAL)
    w.insert(END, temp)
    w.config(state = DISABLED)
    w.see(INSERT)
    print("written")

def out(inp):
    print("out")
    a = inp[0].run(inp)

    temp = inp[0].label
    for i in range(1, len(inp)):
        temp += " " + str(inp[i])
    cmdHistory.append(temp)

    if (a == "restart"):
        mainLoad(load)
