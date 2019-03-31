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
    main.scw("You turned towards the", inp[1] + ".")

def chRun(c, inp):
    main.scw("You changed the name of " + inp[1] + " to " + inp[2] + "." )

def turnUsage(c):
    main.scw("turn + 'left' / 'right' / 'backward' / 'forward' / ")
    main.scw("       'North' / 'South' / 'East' / 'West'")

def chUsage(c):
    main.scw("ch + 'Name of a first file' 'Name of a second file'")

def turnDesc(c):
    main.scw("This command makes you turn around. Could be useful for a text-based RPG maybe?")
def chDesc(c):
    main.scw("'Ch' changes the name of a imaginary file. I doesn`t really do anything to be honest. It might at sometime though.")

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
    main.scw()
    main.scw("Restarting shell")
    main.scw()
    main.scw("-------------------------------------------------------")
    return "restart"

def exitRun(c, inp):
    main.scw("Goodbye")
    main.scw()
    sys.exit()

def helpRun(c, inp):
    main.scw("yee")
    main.scw("Type 'help' <command> for commands description.")
    main.scw()
    if (len(inp) > 1):
        count = 0
        for i in commands:
            if (inp[1] == i.label):
                i.description()
                break
    else:
        for i in range(0, len(commands)):
            main.scw(str(i + 1) + ". " + commands[i].label, end = "")

            if (len(commands[i].att) >= 1):
                main.scw(" -  ", end = "")
                commands[i].usage()
            else:
                main.scw()

def hRun(c, inp):
    if (len(inp) == 2):
        temp = len(cmdHistory) - inp[1]
    else:
        temp = len(cmdHistory) - 2

    main.scw(">> " + cmdHistory[temp])
    i = input("? ")

    if (i.lower() == ""):
        main(cmdHistory[temp])

    elif (i.lower() != "n"):
        error(2, inp[0])

def helpUsage(c):
    main.scw("help (<command>)")

def hUsage(c):
    main.scw("h (<1-max number>)")

def restartDesc(c):
    main.scw("This command restarts this 'shell'. That means it clears the command-history and reloads all of the commands as well as the config file.")

def exitDesc(c):
    main.scw("By typing 'exit', the shells main loop will end and the python script will terminate.")

def helpDesc(c):
    main.scw("I`m assuming you know what help does, since you just used it. Well it shows you all of the commands you can enter here :)")
    main.scw("If you type 'help' <command> it will show you the commands description.")
    main.scw("If you just type 'help' it will show all of the commands with their usage.")

def hDesc(c):
    main.scw("This command lets you use a command you have recently typed already. It gives you acces to the command history.")
    main.scw("You can also type 'h' <number from 1-number of entered commands or maximum length>. This number increases he further back in he history you get.")
    main.scw("For the latest command you would type 'h' or 'h 1'. For the secodn latest 'h 2' and so on...")
    main.scw("You will get a question mark. You either type enter to execute the command like shown above or type 'n' to abort the process.")
    main.scw()
    main.scw("You can set the historys maxium length in the config.py file.")

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

    main.scw("commands loaded")
    main.scw(main.commands[0])

main.mainLoad(load)
