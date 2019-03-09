import main

import sys
from types import MethodType

#Mask for a new command with one attribute / argument
def newCommA(aLabel, aBool, cID, cLabel, valFunc, runFunc, usageFunc, descFunc):
    if (aLabel != "Null"):
        a = main.attribute(aLabel, aBool)
        c = main.command(cID, cLabel, [a])
        c.validate = MethodType(valFunc, c)
        c.usage = MethodType(usageFunc, c)
    else:
        c = main.command(cID, cLabel, [ ])

    c.description = MethodType(descFunc, c)
    c.run = MethodType(runFunc, c)
    main.commands.append(c)

#Command specific functions

def turnValidate(c, inpArray):
    directions = [ "left", "right", "forward", "backward",
                    "north", "south", "east", "west"]
    count = 0
    for i in directions:
        if (inpArray[1].lower() != i):
            count += 1
            if (count == len(directions)):  return 1
        else: return 0

def chValidate(c, inp):
    return 0

def helpValidate(c, inp):
    if (len(inp) > 1):
        #Command validation
        count = 0
        for i in commands:
            if (inp[1] != i.label):
                count += 1
                if (count == len(commands)): return 1 #Command invalid
    return 0

def turnRun(c, inp):
    print("You turned towards the", inp[1] + ".")

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

def chRun(c, inp):
    print("You changed the name of", inp[1], "to", inp[2] + "." )

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

def turnUsage(c):
    print("turn + 'left' / 'right' / 'backward' / 'forward' / ")
    print("       'North' / 'South' / 'East' / 'West'")

def chUsage(c):
    print("ch + 'Name of a first file' 'Name of a second file'")

def helpUsage(c):
    print("help + opt:'command'")

def turnDesc(c):
    print("This command makes you turn around. Could be useful for a text-based RPG maybe?")
def restartDesc(c):
    print("This command restarts this 'shell'. That means it clears the command-history and reloads all of the commands.")
def exitDesc(c):
    print("By typing 'exit', the shells main loop will end and the python script will terminate.")
def chDesc(c):
    print("'Ch' changes the name of a imaginary file. I doesn`t really do anything to be honest. It might at sometime though.")
def helpDesc(c):
    print("I`m assuming you know what help does, since you just used it. Well it shows you all of the commands you can enter here :)")

#Loading the commands etc
#Only when shell is starting up and on restart
def load():
    # Slowly appending commands :)
    newCommA("direction", True, 0, "turn", turnValidate, turnRun, turnUsage, turnDesc)
    newCommA("Null", 0, 1, "restart", 0, restartRun, 0, restartDesc)
    newCommA("Null", 0, 2, "exit", 0, exitRun, 0, exitDesc)

    a = main.attribute("nameOne", True)
    a2 = main.attribute("nameTwo", True)
    c = main.command(3, "ch", [a, a2])
    c.validate = MethodType(chValidate, c)
    c.usage = MethodType(chUsage, c)
    c.run = MethodType(chRun, c)
    c.description = MethodType(chDesc, c)
    main.commands.append(c)

    newCommA("command", False, 4, "help", helpValidate, helpRun, helpUsage, helpDesc)

    print("commands loaded")
    print(main.commands[0])

main.mainLoad(load)
