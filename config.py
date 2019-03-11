import os

user = "maxr"
homedir = os.path.dirname(os.path.realpath(__file__))

inpConfig = [
              '\n:', #Cursor; Required, Always visible
              user,
              " @ ",
              homedir + ">  "
            ]

defcmdConfig = [
                0, # Default command 'restart'. Replace 0 with 1 to disable.
                0, # Deafult command 'exit'. Replace 0 with 1 to disable.
                0, # Deafult command 'help'. Replace 0 with 1 to disable
                0  # Deafult command 'h'. Replace 0 with 1 to disable
               ]

cmdHistoryLen = 5 # Defines maximum length of the command hostory. Set to 'n' for infinite.
