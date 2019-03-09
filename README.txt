Reference the shell by using pythons import statement.
e.a.: import ~/pythonShell/main

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
      (e.a.: c.validate = MethodType(<function>, c) )
      <function> needs to be replaced with the name of the function you wrote to validate the arguments (To see how to do that,
      see 'Validate function' below).
!!   (If your command doesn`t take any arguments, you can replace everything after the '=' with a zero
!!   e.a.: c.validate = 0)

      The second one is the description function.
      Same as for the validate function. Except this one is required for every command. Even if it doesn`t take a
      single argument.
      (e.a.: c.description = MethodType(<function>))
      <function> needs to be replaced with the name of the function you wrote that contains the commands description
      (To see how to do that, see 'Description function' below).



Validate function

-> !! You do not need this function if your command doesn`t take any arguments !!
  This function can take two arguments. (e.a.: def exampleValidate(c, inp): )
  The input being an array of the parsed user input. The first index (inp[0]) is the command, the rest of the array
  are the entered arguments.
  You now need to validate these arguments. The command is already validated at this point. So is the amount of given arguments.
  You really only need to check if you are able to use these arguments and later generate output based on them.
  How you do that is up to you and depends on your command and what you want to do in general.
  Just remember to return 0 if the arguments are valid and return 1 if they are not.
