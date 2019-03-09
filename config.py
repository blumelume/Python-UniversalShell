import os

user = "maxr"
homedir = os.path.dirname(os.path.realpath(__file__))

inpConfig = [ '\n:', #Cursor; Required, Always visible
        user,
        " @ ",
        homedir + ">  "]
