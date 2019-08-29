milasm
======

Macros for CLR IL assembly. This is just a proof of concept but it works, you can try to build the code, write your own macros, write your own CLR applications.

Let's start with an example:

// hello.il

    <<console_input_output.min>>
    <<branching.min>>
    <<instructions.min>>
    
    .assembly extern mscorlib {}
    
    .assembly hello
    {
        .ver 1:0:1:0
    }
    
    .module hello.exe
    
    .method static void main() cil managed
    {
            .maxstack 2
            .entrypoint
        
            .locals init (int32 a, int32 b)

            ((write: "Input positive x: "))
            ((read line))
            ((parse it as int32))
            ((store it as local a))
            ((check if ((local a)) > ((int32 0)) ))
            ((if so {{
                        ((write: "It is positive!\n")) 
                        ((load int32 2))
                        ((store it as local b))
                         
                        ((write: "x * 2 = "))
    
                        ((load local a))
                        ((load local b))
                        ((multiply them))

                        ((write int32))      
                        ((write line: ""))      
                }}else{{
                        ((write: "It isn't positive.\n"))
                }} 
            ))
            ((read line))           
            ((return))
    }

This is a valid ILAsm code with milasm macroses. Not a mock-up, but a buildable thing. 

It reads a number from the console, checks if it's positive, and if it is, returns the double of this number. What's important, you can read this yourself from the code even if you don't know the least of CLR assembly. This is meant to be low-level but readable.

Macros are defined in free-form syntax using double square brackets, like this:

    [[write $type -> call void [mscorlib]System.Console::Write ($type) ]]

The macro expansion works like this: the part before the `->` is a pattern, the part after the arrow is the substitution. `$type` is a macro argument. All the words starting from `$` are macro arguments. When a pattern occurs in the code, it's being replaced recursively until no recursive patterns left.

    ldstr "Hello!"
    ((write string))
    
Becomes:

    ldstr "Hello!"
    call void [mscorlib]System.Console::Write (string)
    
Of course, you can multiline macros like this:

    [[write: $text -> 
	    ldstr $text 
	    call void [mscorlib]System.Console::Write (string) 
    ]]

And you can make recursive macros:

    [[write: $text -> 
        ldstr $text 
        ((write string))
    ]]

And then replace some repeating code pattern with a single line:

    ((write: "Hello!"))
    
When you want to write a macro with the block of other macros or some ILAsm code as a macros variable, use double curly brackets: `{{ }}`. Kind of a cheap take on first-order macros if you wish.

Note that apart from the parenthesis, the syntax of these macroses is non restricted. Macroexpansion uses primitive prolog style pattern-matching with atoms being always separated by space, so you can use almost any symbols in your macro definition. Just remember that all identifiers starting with `$` are supposed to be macro variables. 

And there is one special macro variable: `$#`. It is a macro expansion instance ID. it is intended for branching, so you can make labels like `HERE_$#:` expanding like `HERE_$5:` or `HERE_$16:` or `HERE_$192:` anew every time the macro expansion is happening.

Another feature is files inclusion dedicated for macros only. You can write your macros definitions in the same file your code is, but you can store them elsewhere and then include them with double corner braces like this:

    <<console_input_output.min>>
 
I didn't want to mess with all CLR infrastructure, so this is not the usual C-style inline. it deliberately works with *macros definitions only* ignoring all the other text: code or comments. I'd recomend keeping extension for these files `min` (for macros include) to avoid confusion mixing them with the code files but this is not an inherent restriction.

**TL&DR**

This is a readable Assembly made of prolog-like pattern matching macros.
