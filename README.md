milasm
======

Macros system for CLR IL assembly. This is just an early prototype still in progress, but it can do certain things or at least show the way I see them done.

Macros are defined in an arbitrary syntax using double square brackets, like this:

    [[write $type -> call void [mscorlib]System.Console::Write ($type) ]]

It takes the pattern on the left side of an arrow and then replaces it being called with double round brackets it a code so:

    ldstr "Hello!"
    ((write string))
    
Becomes:

    ldstr "Hello!"
    call void [mscorlib]System.Console::Write (string)
    
Of course you can multiline macroses like this:

    [[write: $text -> 
	    ldstr $text 
	    call void [mscorlib]System.Console::Write (string) 
    ]]

And then replace some repeating code pattern with a single line:

    ((write: "Hello!"))
    
Note, that syntax of these macroses are completely arbitrary. Macroexpansion uses primitive pattern-matching prolog style with atoms being always separated by space, so you can use almost any symbols in a macro definition. Just remember that all identifiers starting with `$` are suppose to be macro variables. 

There is one special macro variable: `$#`. It is a number of macro expansion instance. it is intended for branching, so you can make labels like `HERE_$#:` expanding like `HERE_$5:` or `HERE_$16:` or `HERE_$192:` new every time the macro expansion is happening.

Another feature is macro definition files inclusion. You can write your macros definition in the same file the code is, or you can include them with double corner braces like this:

    <<console_input_output.mil>>
 
I didn't want to mess with all CLR infrastructure, so this is not the usual C-style inline. it deliberately works with macros definitions only ignoring all the other text. I recomend to keep extension for these files `min` to avoid confusion mixing them with usual `il` or macrosed `mil` files.
