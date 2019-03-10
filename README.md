#Python shell by Maximilian Rudolph

Reference the shell by using pythons import statement.
e.a.: import ~/pythonShell/main

General Information

-> inp ->> an array mimicking the users input. It is the result of the input parsing. The first index of the array
   (inp[0]) is a command object (instance of command). The rest of the arrays indices are the arguments / attributes
   the user entered.



In the file you use the shell in, you need a couple of things in order for the shell to work properly.
First of all, you need a function called load ( def load(): ).
In this function you will load the commands you want to add to the default ones.

->  To load a command into the shells list of commands you append it to that list
    (main.commands.append( <command object> )).
    The '<command object>' needs to be replaced with an instance (object) of the command class.
    (e.a.: c = command( ... ))

    The three dots need to be replaced with the arguments, that a command takes. These are defined by the command class.
    It takes an ID (e.a.: 14574 or just 0) and a label which is the name of the command and
    that also defines what you have to type in order to launch that command.
    The third argument that it takes is an array of attributes. These are objects or instances of the attribute class.
    Here is how you would define an attribute: a = attribute(<label>, <required>)
    Where the <label> is a string and can be replaced with basically everything and the <required> has to be of type boolean.

    If you have done all of that you need to specify three crucial functions for every single command.

      One of these is the validate function. You specify that by referencing the command instance that you just created
      and adding a '.validate' after it. After that you have to specify the actual function that should be called, when these
      arguments of your command need to be validated.
      (e.a.: c.validate = main.MethodType(<function>, c) )
      <function> needs to be replaced with the name of the function you wrote to validate the arguments (To see how to do that,
      see 'Validate function' below).
!!   (If your command doesnt take any arguments, you can replace everything after the '=' with a zero
!!   e.a.: c.validate = 0)

      The second one is the description function.
      Same as for the validate function. Except this one is required for every command. Even if it doesnt take a
      single argument. It gets used when the help command is executed.
!!    You do not need this function if you remove the default help command in the config file  
      (e.a.: c.description = main.MethodType(<function>))
      <function> needs to be replaced with the name of the function you wrote that contains the commands description
      (To see how to do that, see 'Description function' below).

      All of your commands also need a 'Run function'. This specifies what happens when your command gets successfully
      executed. It defines the output it produces.
      (e.a.: c.run = main.MethodType(<function>, c) )
      <function> needs to be replaced with the name of the function you wrote that will generate the commands output
      (To see how to do that, see 'Run function' below).



Validate function

-> !! You do not need this function if your command doesnt take any arguments !!
   This function needs two arguments. (e.a.: def exampleValidate(c, inp): )
   You now need to validate these arguments. The command is already validated at this point. So is the amount of given arguments.
   You really only need to check if you are able to use these arguments and later generate output based on them.
   How you do that is up to you and depends on your command and what you want to do in general.
   Just remember to return 0 if the arguments are valid and return 1 if they are not.


Run function

-> !! This function is required for every command !!
   The run function needs two arguments (e.a.: def exampleRun(c, inp): )
   You then basically do what ever you want to do. Just remember that this is the output so some print statements
   would make a lot of sense.


Description function

-> !! If you have the help command disabled you dont need this function. If you have it enabled it is required for every
   !! command you add.
   This function only needs one argument (e.a.: def exampleDesc(c): )
   This function can be extremely simple. You just need a simple print statement that contains a description of what your
   command does and what it might be used for or something. At least thats its normal usage.
