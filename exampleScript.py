import main
import sys

#Mask for a new command with one attribute / argument
def newCommA(aBool, cLabel, valFunc, runFunc, usageFunc, descFunc):
    if (aBool != 0):
        a = main.attribute(aBool)
        c = main.command(cLabel, [a])
        c.validate = main.MethodType(valFunc, c)
        c.usage = main.MethodType(usageFunc, c)
    else:
        c = main.command(cLabel, [ ])

    c.description = main.MethodType(descFunc, c)
    c.run = main.MethodType(runFunc, c)
    main.commands.append(c)

#Command specific functions

def turnValidate(c, inpArray):
    directions = [ "left", "right", "forward", "backward",
                    "north", "south", "east", "west"]
    count = 0
    for i in directions:
        if (inpArray[1].lower() != i):
            count += 1
            if (count == len(directions)):  return 2
        else: return 0

def chValidate(c, inp):
    return 0

def turnRun(c, inp):
    print("You turned towards the", inp[1] + ".")

def chRun(c, inp):
    print("You changed the name of", inp[1], "to", inp[2] + "." )

def turnUsage(c):
    print("turn + 'left' / 'right' / 'backward' / 'forward' / ")
    print("       'North' / 'South' / 'East' / 'West'")

def chUsage(c):
    print("ch + 'Name of a first file' 'Name of a second file'")

def turnDesc(c):
    print("This command makes you turn around. Could be useful for a text-based RPG maybe?")
def chDesc(c):
    print("'Ch' changes the name of a imaginary file. I doesn`t really do anything to be honest. It might at sometime though.")

#Loading the commands etc
#Only when shell is starting up and on restart
def load():
    # Slowly appending commands :)
    newCommA(True, "turn", turnValidate, turnRun, turnUsage, turnDesc)

    a = main.attribute(True)
    a2 = main.attribute(True)
    c = main.command("ch", [a, a2])
    c.validate = main.MethodType(chValidate, c)
    c.usage = main.MethodType(chUsage, c)
    c.run = main.MethodType(chRun, c)
    c.description = main.MethodType(chDesc, c)
    main.commands.append(c)

    print("commands loaded")
    print(main.commands[0])

main.mainLoad(load)
