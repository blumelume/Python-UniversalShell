# Custom Python Shell by Maximilian Rudolph


### General Information
-> inp => an array mimicking the users input. It is the result of the input parsing. The first index of the array
   (`inp[0]`) is a command object (instance of command class). The rest of the arrays indices are the arguments / attributes
   the user entered.

### Initial setup
-> In the file you use the shell in, you need a couple of things in order for everything to work properly.
   First of all you need to import the shell like you would import a library.
   Simply write 'Import' at the top of your file and then the path to the main file (e.a.: `Import ~/Desktop/pythonShell/main`).
   If you want to add commands, you need a function to load them. See more on that in the 'loading new commands' section.
   To start the shell you need to call the `main.mainLoad()` function.

### Config file
-> In the config file you can configure the behaviour of the shell.
   First you can customize the input prompt. The first index of the given list is the cursor. The rest is up to you.
   You also have option to enable and disable the four default commands that the shell comes with. Replace the zeros with
   ones and the corresponding command has been disabled.
   The last option is for setting the maximum length of the command history. That is of course only relevant if the 'h'
   default command is enabled. Set it to any number you want or 'n' to set it to infinite.

### Errors and error codes
-> Errors can occur in a lot of different situations. The message telling the user what they did wrong depends on the
   error code. The error function and its arguments looks like this: `error( <error code/errID>, <command object> )`
   There is a total of 4 default error codes.

   > 0 => Invalid input
   1 => Invalid amount of arguments
   2 => Invalid argument(s)
   3 => Too many arguments
   4 => Command history is empty

### Loading new commands
->  To load a new command into the shells list of commands you append it to that list
    Before you can do that however, you need to complete the setup of a new command. You can read about how to do that below.

   First you need to create a attribute object.
    ``(e.a.: `a = attribute( ... )`)``
    The three dots need to be replaced with the arguments, that an attribute takes. See 'Attribute object' section.

   After that the command need to be defined.
    ``(a.a.: `c = command( ... )`)``
    The three dots need to be replaced with the arguments, that a command takes.
    For more on that look at the 'command object' section.

   If you have done that you need to specify four crucial functions for every single command.
    These functions are unique to every command.

   1. Validate function ``(e.a.: `c.validate = MethodType( <function>, c )`)``
       This function is only needed if the command takes any arguments.
       For more see 'Validate function'.

    2. Description function ``(e.a.: `c.description = MethodType( <function>, c )`)``
       For more see 'Description function'.

    3. Run function ``(e.a.: `c.description = MethodType( <function>, c )`)``
       For more see 'Run function'.

    4. Usage function ``(e.a.: `c.usage = MethodType( <function>, c )`)``
       This function is only needed if the command takes any arguments.
       For more see 'Usage function'

   If the functions are written, they have to be linked to the command they belong to.
    - `<command object>.validate = main.MethodType( <function you have written>, <command object> )`
    - `<command object>.description = main.MethodType( <function you have written>, <command object> )`
    - `<command object>.run = main.MethodType( <function you have written>, <command object> )`
    - `<command object>.usage = main.MethodType( <function you have written>, <command object> )`

   e.a.: `c.validate = main.MethodType( commandxValidate, c )`
    In the example above, 'c' is a command object and 'commandxValidate' is a the actual, unique function for validating
    the entered arguments.

   If your command doesnt take any arguments, you would set
   `<command object.validate` and
    `<command object>.usage` equal to 0.
    e.a.: `c.validate = 0`
          `c.usage = 0`

   If you have done all of that, you can finally append this command object to the global list of commands.
    - `main.commands.append(<command object>)`
    e.a.: `main.commands.append(c)`

   Now you have loaded a new command into the shells 'brain'.
    However if you dont want the command not to load when the shell is reloaded, you need to put all of this into a function.
    That function can be called whatever you. I called it 'load'. Just for simplicity.
    e.a.: `def load():
            ...`

   When you then call the 'mainload' function, you just pass this function in as an argument.
    e.a.: `main.mainload( load )`

### Validate function
-> !! You do not need this function if your command doesnt take any arguments !!
   This function should validate the arguments you command takes.
   It needs to take two arguments.
   1. An instance of the command class (command object).
   2. The 'inp' array. Look under 'General information' for more info.

   The command that has been entered is already validated at this point. So is the amount of given arguments.
   You really only need to check if you are able to use these arguments and later generate output based on them.
   How you do that is up to you and depends on your command and what you want to do in general.
   Just remember to return 0 if the arguments are valid and return a different error code if they are not.

### Description function
-> !! If you have the help command disabled you dont need this function. !!
   !! If you have it enabled it is required for every command you add. !!
   This function is used to display an explanation of a give command. It is associated with the default 'help' command.

   This function only needs one argument.
   1. An instance of the command class.

   This function can be extremely simple. You just need a simple print statement that contains a description of what your
   command does and what it might be used for or something. At least thats its normal usage.

### Run function
-> !! This function is required for every command !!
   This specifies what happens when your command gets successfully executed. It defines the output your command produces.

   The run function needs two arguments
   1. An instance of the command class (command object).
   2. The 'inp' array. Look under 'General information' for more info.

   You then basically do what ever you want to do. Just remember that this is the output so some print statements
   to tell the user what you are doing would make a lot of sense.

### Command object
-> Command objects are instances of the command class.
   This how the definition for the command class looks.

     class command:
         def __init__(self, label, att):
             self.label = label
             self.att = att

   As you can see a command has two parameters.
   1. label, the commands name. It is of type string anf defines what the user has to type to run the command.
   2. att, an array of attribute objects (See 'Attribute object' for more info)


### Attribute object
-> Attribute objects are instances of the attribute class.
   This is the definition of the attribute class:

	   class attribute:
	       def __init__(self, req):
	           self.req = req

   An attribute object has only a single parameter.
   1. req stands for required and is of type boolean.
       It defines whether this argument is needed in order for the command to run or not.
