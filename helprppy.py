#!/usr/bin/env python3
#
#
# copyright (C) 2024 Radu BERINDEANU
# distributed under the ISC License www.isc.org/licenses
#
# maintainer raberpy4@outlook.com
#
#=======================
# 
#  Help module
#
#=======================

introtxt = """
    Introduction
    ============
  Reverse Polish Python, or RPPy, is an attempt to use the 
concatenative paradigm applied to classic Python. Generally 
speaking, most programming languages use the application of 
function to arguments, where you define a function with formal 
arguments and use it with concrete values for those arguments. 
In a concatenative language, there are no formal arguments:
instead, all functions, called WORDS, use a single type of data, 
usually a stack, to get their input values, leaving the output 
values also here, for the next functions to get. For example:

  In Python:
def meanval(a,b):      # formal parameters a,b
   return(a+b)/2
	
meanval(10,20)         # assignment of values for a,b
15.0                   # result

  In RPPy:
meanval: + 2 / ; .     # no formal parameters, only operators:
                       # "+" adds the two top stack values, leaving sum
                       # 2 puts its own value on top of stack
                       # "/" divide sum by 2, leave quotient
                       # ";" means return, word's execution terminated
                       # (ignore the dot ".", it means terminating user input)
10 20 .                # putting values on the stack
[10,20]                # RPPy displays the stack: two values, with 20 on top
meanval .              # call the word meanval, arguments are ready to use
[15.0]                 # RPPy displays the stack, result ready for next word
print .                # print needs an argument, which is already here
15.0                   # result printed
[]                     # RPPy displays the stack: empty, as all arguments
                       # are consumed by meanval and print
					
  In fact, more shortly:
10 20 meanval print .
15.0
[]

  Programming in concatenative style means simply composing words 
to define new ones:
mvprint: meanval print ; .
10 20 mvprint .
15.0
[]

  And why Reverse Polish? RPN, or Reverse Polish Notation, is perfectly
suited for the way concatenative programming works: always the operators 
follow their operands, 20 + 30 is 20 30 + in RPN; there is no need for 
parentheses, as (10+20)*5 is 10 20 + 5 * , or if stretching your imagination 
5 10 20 + * (take pencil and paper and work out the stack effect...)
In Python you have strict precedence for operators (PEMDAS - parentheses,
exponentiation, multiplication, division, add, subtract); in RPPy the order  
of operations is entirely at your choice, as expression evaluation is always 
done left to right.

  But what we gain with this concatenative approach? Here's a quick answer:
  
- point-free style programming: no need for named parameters, your whole 
program is nothing but a sequence of literals (values being pushed on the 
stack) and words using them

- concision: the only "glue" between words is whitespace, a line of code 
in RPPy may include several calls to words by mentioning only their name, 
no need for parameter names and assigning values

- factoring: any common sequence of words found in multiple definitions 
can be factored out as a separate definition, which leads to shorter 
programs enhancing readability

- interactivity: at the console, define a word, put some values on the 
stack, test it - WYSIWYE - What You See Is What You Execute! ; the stack 
is always visible, no need to insert "print(xxx)" everywhere as debugging 
aid. Once tested, use it in other definitions; integrate from simple to 
complex until arriving at the final words of your application, a process 
known as "incremental compiling"

- shortest development cycle: Python, in interpret mode, is also highly 
interactive, but even the smallest program needs a separate source code, 
the so-called script, which has to be edited , tested, corrected at source 
level with an editor, re-tested again. On the other hand, RPPy HAS NO SOURCE 
CODE! You create and test interactively your set of words which can be saved 
at any instant as compiled code, reloaded again and continued by adding new 
words, or even redefining old words until finished. No need for a separate 
source editor

- spreadsheet-like data handling: as there is no difference between words 
defining data and words defining functions, saving your set of words means 
saving each time a current snapshot of your program, data included. 
As with spreadsheets, what is saved in the cells at session end will be 
retrieved at next loading; no need to save data in separate files.

  OK, all that's wonderful ;););), but what we loose?
  
- patience: the learning curve is steep, as mostly we are used with infix
notation, not postfix RPN; all has to be done backwards...

- attention: it is more difficult to program in concatenative mode, as you 
have to pay attention not only to the control flow of program's execution, 
but also to the DATA FLOW on the stack. Loosing focus on what's happening 
on the stack is very easy, with consequences Not-To-Be-Named-Here...

  Countermeasure: short definitions, thoroughly tested before advancing to 
the next one; minimise stack shuffling; comment every definition with the 
associated stack effect. More on this in the user manual.

  As prerequisite, knowing at least programming at ground level in Python is 
necessary: RPPy uses basic functions and methods from Python, only accessed 
in concatenative mode. Unfortunately, learning RPPy will not improve your 
skills at Python programming: no indentation, no formal parameters, 
no statements, no expressions, no OOP, and the control flow at program 
execution is totally different. 
But what you could find useful is mastering Python's data types 
and operations on them.

  Compared to Python, in RPPy you dispose only of a fraction (about 250) 
of the vast number of functions & methods available in Python land, but 
even with this reduced set a good deal of data handling is covered.

  And the grand final question: what is RPPy good at?
  - quick & dirty small apps as it’s highly interactive with short 
  development cycle, but difficult to scale up
  - banging your head on the wall (or screen, if you have a prehistoric 
  15" monitor in your basement)

=======================================================================
	Have fun! Because that's the only reason why RPPy was created...
=======================================================================

"""

usingtxt = """
    1. Using RPPy
    =============
  At program start, RPPy is in execution mode, signalled by the prompt "ex>", 
awaiting user input; as a following convention, all console output is shown
in pairs of fenced markers "~~~" ; comments may appear after the hash "#".
~~~
 Data stack empty       # there's no data yet in the stack
ex>                     # RPPy prompts for user input
~~~
Now try executing some calculations:
~~~
ex> 10 20 30 .          # put three values on the stack, separated by space(s)
 Data stack items: 3    # ALWAYS terminate input  by dot "." followed by Enter
[10, 20, 30]            # the stack has now three values, with the last one on
ex>                     # top of the stack, shown in the rightmost position
~~~
Add the top two numbers:
~~~
ex> + .                 
 Data stack items: 2
[10, 50]                # result is on top of stack, replacing arguments 20,30
ex>
~~~
Now divide top of stack (TOS) by next of stack (NOS), aka 50/10
~~~
ex> / .
 Data stack items: 1
[0.2]                   # ?!? that's not what you expected...
ex>
~~~
How does "/" work?  Ask by using "pdef", which means "print definition":
~~~
ex> '/ pdef .           # prefix a string w/o spaces with single quote "'"
Kernel primitive: / ; XT: k_slash() ; action: ( x y -- x/y ) divide NOS 
by TOS - floating point div
 Data stack items: 1
[0.2]
ex>
~~~
  Ignore for the moment what it says about kernel primitive and XT, and look
at action; the parentheses include always the stack effect of given word:
"( what's on the stack before -- what's on the stack after )", so if you 
have two numbers x and y before executing division, the "/" operator 
works by dividing x by y, aka NOS by TOS, not what we wanted: 50/10
Now comes what is known as the biggest hurdle in learning RPPy:
*stack shuffling* - a set of words to manipulate stack content in order to 
achieve desired order of operands needed by each word at execution
  Let's start again:
~~~
ex> 10 20 30 + .        # add the two top numbers
 Data stack items: 3
[0.2, 10, 50]
ex> swap .              # swap does: ( x y -- y x) 
 Data stack items: 3
[0.2, 50, 10]           # now order of operands is ok for division
ex> / .
 Data stack items: 2
[0.2, 5.0]              # desired result achieved
ex> swap drop .         # but the wrong result "0.2" should be discarded
                        # so use drop ( x -- ) which discards TOS
 Data stack items: 1
[5.0]                   # finally print result if you wish
ex> print .             # print needs an item to display: ( item -- )
5.0
 Data stack empty       # print consumed TOS, stack is now empty
ex>
~~~
 
  Now suppose you want to keep the above inputted words for further use 
(even it doesn't make great sense, only as an example...) ; you create a 
definition by giving a name with colon ":" as suffix :
~~~
ex> mydef: "" ( n1 n2 n3 -- (n2+n3)/n1 )"" # stack effect
co> + swap / print ; # words terminated by a semicolon meaning "return"
co> . # the dot signals end of definition
 Data stack empty
ex>
~~~
  Always put the definition name as the first item in the input line,  
followed (not compulsory, but highly recommended) by the stack effect, 
started and ended by the double double quote '""'. As RPPy has no notion
of source code, this stack effect description is the only documentary 
part which remains attached to a definition. Comments, as in Python, 
could be written by a hash '# ' followed by any text, but they are not
taken into account in the dictionary of stored definitions.

  If the first item inputted is a definition name, RPPy changes to 
compile mode, signalled by "co>" . Now you can input the body of the 
definition, consisting of ALREADY PREDEFINED WORDS and literals, there's
no notion of forward references "use it now, define it later". 
You create a program in RPPy by definining more an more complex words 
based on the previous ones, a process known as "incremental compiling".

  The semicolon ";" is the equivalent of a return in Python, but compiling 
continues until dot "."; think of a sequence of RPPy words as an ordinary 
text sentence, ending always with "." Only after receiving the ending dot 
RPPy changes back to execute mode. So you can spread a definition in a 
number of lines, but, opposed to Python, there's no indentation. The notion
of code block for each indentation level in Python doesn't exist: you simply 
give a name to whatever group of words seems appropiate.
  OK, after all that , let's see if our definition works:
~~~
ex> 15 75 25 mydef .
6.666666666666667
 Data stack empty
ex>
~~~
  Wonderful, but what if we forget an argument?
~~~
ex> 15 75 mydef .
"swap" aborted:  Data Stack Underflow
 Index:  6
 In definition: "mydef" at index: 4
 Return stack items:1
1 return from: mydef
 Data stack empty
ex>
~~~
  Not very encouraging...let's see what happened: 
  - Data Stack Underflow: you tried to use more arguments than present
  on the stack
  - Index: all RPPy words are encoded in a list called "Execution List", 
  which can be displayed giving starting index followed by "pexlst" ,
  "print execution list". As mydef is coded starting at index 4 and the 
  error-emitting word, swap, is at index 6, you do:
~~~
ex> 4 pexlst .
    4 mydef:            # start of mydef
    5 +                 # each word comprising mydef is coded as an 
    6 swap              # entry in the execution list
    7 /
    8 print
    9 ;                 # end of mydef
   10 lit  15           # what follows after is all what you inputted
   11 lit  75           # to execute mydef
   12 lit  25           # the input "15 75 25 mydef" is coded as three
   13 call mydef        # literals followed by a call to mydef
   14 lit  15           # next, you give only two literals as arguments
   15 lit  75
   16 call mydef        # with only 2 arguments, mydef executed "+" , 
   17 lit  4            # which leaved 90 on the stack, now "swap" tried
   18 pexlst            # to swap 90 with a non-existing value: aborted
 Data stack items: 2
[90, None]
ex>
~~~
  What if we call mydef with a string instead a number?
~~~
ex> 15 75 " abc" mydef .
"+" aborted: unsupported operand type(s) for +: 'int' and 'str'
 Aborted at Execution List Index:  5
 In definition: "mydef" at index: 4
  TOS:  <class 'str'> abc
  NOS:  <class 'int'> 74
 Return stack items:1
1 return from: mydef
 Data stack items: 5
[90, None, 15, 75, 'abc']
~~~
  This time it's the sum of 75 and the string abc which caused the abort, 
as an integer cannot be added to a string; in this case, RPPy displayed
TOS and NOS, showing the type of operands ("str"-string, "int"-integer)

  An abort is the equivalent of Python's error messages, but instead of 
ending the script with a traceback, in RPPy you simply continue working,
testing definitions until ok, without the need to edit/reinterpret source
code. 

  Anytime you can save your set of definitions and reload them later for 
further completion. See "Editing, saving and loading definitions".

  Finally, if you want to see later your definition, use "pdef" ;
if a string is spacefree, instead of "(space) mydef" you can use the 
single quote as prefix, WITHOUT space : 'mydef (see "Basic Datatypes - 
Strings" from help)
~~~
ex> 'mydef pdef .  
  mydef       at index:  4 "" ( n1 n2 n3 -- (n2+n3)/n1 ) ""
  mydef: + swap / print ;

  No duplicate (older definitions) present
 Data stack items: 5
[90, None, 15, 74, 'abc']
ex>
~~~

  If you want to see the dictionary of all built-in words, the so-called 
kernel primitives, enter:
~~~
ex> pkernall .             # pkern stands for "print kernel definitions"
  ###1       ===Data Stack words===
  dup      ( n -- n n ) duplicate TOS
  2dup     ( x y -- x y x y ) duplicate NOS and TOS
  drop     ( n -- ) drop TOS
  2drop    ( x y -- ) drop TOS and NOS
  swap     ( x y -- y x ) exchange TOS with NOS
  over     ( x y -- x y x ) copy NOS over TOS
  ...
  ...
~~~
                        # press Enter to continue displaying, any other key stops
~~~
  ###3       ===Math words===
  +        ( x y -- x+y ) add TOS to NOS
  -        ( x y -- x-y ) subtract TOS from NOS
  *        ( x y -- x*y ) multiply TOS by NOS
  /        ( x y -- x/y ) divide NOS by TOS - floating point div
  //       ( x y -- x//y ) divide NOS by TOS - floored (integer) div
  %        ( x y -- rem ) remainder of x/y division
  divmod   ( x y -- quot rem ) quotient & remainder of x/y division
  **       ( x y -- x**y ) NOS at power of TOS
  ++       ( n -- n+1 ) increment TOS by 1
  --       ( n -- n-1 ) decrement TOS by 1
  ...
  ...
~~~
  If you want to see a single group of words per category, use "pkern".
  
  The notation used for the stack effect is as follows:
  - n, x, y, z : 
    - concerning stack manipulation: any type of data
    - concerning math, assignment, bitwise ops : numbers
  - str : strings
  - seq : sequence, as strings, lists, etc.
  - idx : index of a word in the execution list (function pointer)
  - item : one element in a sequence
  - ZF : Zero Flag, positioned by comparisons
  - I, J, K : index registers used to acces/slice sequences and in 
    counted loops

  Clear the data stack with "cleards" , there's no need to accumulate 
  a bunch of already used data here; preserve only what you need for 
  further testing:
~~~
ex> cleards . # clears the data stack
 Data stack empty
ex>
~~~
  And the famous Hello World! program?
~~~
ex> hello: "" ( -- ) ""  # no data before/after executing "hello"
co> " Hello World!" print ; .
 Data stack empty
ex> hello .
Hello World!
 Data stack empty
ex>
~~~
  As a beginner, one of the most frequent errors is forgetting to put a space 
after a string-starting double quote:
~~~
ex> "Hello World!" print .
Compile error: unterminated string literal (detected at line 1) (<string>, line 1) in expression: "Hello
 Undefined: ""Hello"
ex>
~~~
  The double quote is a word, so it needs a space after; in this example, 
the first word extracted at input is "Hello, which is not defined.

  Display all your definitions with "pdefall":
~~~
ex> pdefall .
  mydef       at index:  4 "" ( n1 n2 n3 -- (n2+n3)/n1 ) ""
  hello       at index:  10 "" ( -- )  ""

 High Level Dictionary Definitions:  2
 Data stack empty
ex>
~~~

  Now it's time to nail down some basic concepts:
  
  1. a word is ANY sequence of characters separated by whitespace ( space,
  tabulation or newline) , there are no "identifiers" as in Python, which 
  must start with a letter or underscore and contain only letters, 
  underscore or the digits 0..9
  Valid words are 2dup, sum+ , s[i:j], even n! or $#.k00->/ if that means 
  anything to you...
  
  2. every word has an ACTION associated to it, even if at a first glance 
  it doesn't seem so: ok, swap interchages TOS with NOS, but what does 10 
  or 30 do? Those are LITERALS, whose action is always the same: pushing 
  themselves on the stack. Numbers, strings, lists, dictionaries, etc. all 
  are literals
  
  3. knowing the action of a given word, to ensure correct execution of 
  said action means preparing the stack in advance BEFORE invoking the 
  word - remember this as the basic rule of concatenative programming!
  
  4. the evaluation rule for a concatenative language is very simple: 
  scan input left to right, push literals on the stack, call words.
  Each word is either a "primitive", coded in Python, or a "high level" 
  composed of primitives and other pre-defined high level words. 
  There are neither expressions nor statements in RPPy: only a stream 
  of literals and words

  To summarise the basic rules of RPPy:
  ====================================
  
  1. test a sequence of words in execute mode, always looking at the
  data stack:
  - work step by step, input only what's needed for the following
  word; don't chain more new words on a single input line until all except 
  the last one are already tested
  - remember to look at the stack effect of the kernel primitives until 
  you master them by heart; mostly all run time errors are generated by 
  the wrong order/number/type of arguments on the stack
  
  2. any sequence of literals and words can be memorised as a definition:
  - always start with the definition's name suffixed with ":"
  - the definition name cannot start with:
    - single quote "'": the prefix for strings without spaces included
    - asterisk "*": the prefix for word's index in the execution list
  - the definition name must be the first item in the input line
  - attach a stack effect description "" ( stack before -- stack after)""
  as it'll be the only way to remember what that word does (don't forget 
  the space after the double double quote...)
  - exit with dot "." from compile mode
  NB. in execution mode, but only here, you can terminate input with TWO 
  consecutive Enter keys; in compile mode the dot is compulsory
  
  3. a definition can be redefined with the same name, but attention:
   - new words created from here onwards using the redefined word will,
   as expected, use the new variant
   - older words including this definition will preserve her OLD BEHAVIOR,
   there's no automatic replacing of the old ones with the new one; see
   "Editing, saving and loading definitions"
   - as a matter of fact, redefine at will your definition until it's 
   thoroughly tested; only then use it in other definitions. There's no 
   problem if later on you wish to modify this definition, but at the cost
   of manually replacing the old variant   
   
   4. save your work often, by using Ctrl-S or save, as there may be situations
   when RPPy crashes unexpectedly (hopefully not too often…) or simply exits with a 
   Python traceback because of a (not yet) catched error in a kernel primitive; 
   unfortunately at this instant all definitions created in the current session are lost;
   see "Editing, saving and loading definitions"
   
   5. corollary:
   - keep definitions short, a couple of lines maximum, operating on a few values once;
     each time you feel that it gets too complicated, break the definition in more
     subwords factoring as much as possible
   - each definition should do only one thing
   - try to give meaningful names to definitions; as there’s no source code in RPPy,
     a good choice of names helps further maintenance
   - minimise stack shuffling, the stack output of one word should match the stack
     input of the next word concerning order of items
   - comment the stack effect, as it’s the only comment which remains attached to
     the definition; you can even add other meaningful information here (only it has
     to be done on a single input line)

   NB. read first "Data stack management" and "Error handling" 
   until you gain some experience with RPPy.
   
        Have fun !
        
=== End of chapter 1 ===
"""
datamanagtxt = """
    2. Data stack management
    ==========================
  The biggest difficulty in learning RPPy is the proper use of the data
stack. As every word uses it to get arguments and to leave results here 
for the next word, it's crucial to have:
a) correct number of arguments:
  - too many: stack overflow as unwanted data accumulates in time
  - too few: stack underflow or wrong input arguments picked
b) correct type of arguments:
  - execution errors if, as example, an integer is given as filename
  or a string is added to a number
c) correct order of arguments:
  - difficult to debug, as, contrary to a) and b), there may be no 
  execution error but instead an erroneous data output
  By the way, all words use positional arguments, there are no keyword
  arguments as in Python.
  
  In order to achieve all this, a number of stack management (or stack 
"shuffling") words are defined in RPPy; list them with "pkern" option 1:
  dup      ( n -- n n ) duplicate TOS
  2dup     ( x y -- x y x y ) duplicate NOS and TOS
  drop     ( n -- ) drop TOS
  2drop    ( x y -- ) drop TOS and NOS
  swap     ( x y -- y x ) exchange TOS with NOS
  over     ( x y -- x y x ) copy NOS over TOS
  nip      ( x y -- y ) drop NOS
  tuck     ( x y -- y x y ) insert TOS before NOS
  rot      ( x y z -- y z x ) rotate rightwise top three items
  -rot     ( x y z -- z x y ) rotate leftwise top three items
  pick     ( xn xn-1 xn-2 ... x0 n -- xn xn-1 xn-2 ... x0 xn ) replace 
           TOS with a copy of the n-th item
  cleards  ( ... -- ) empty data stack
  Here TOS means Top Of Stack and NOS is Next Of Stack.
  
  Usually you'll be using dup/drop to get desired number of arguments and 
swap/over/rot to get desired order, but that's only a very simplistic 
rule of thumb...
  See some examples by using RPPy as a calculator:
~~~
ex> # calculate 7*3**2-2*3 given 7 3 2 on the stack
ex> 7 3 2 .             # initial values
 Data stack items: 3
[7, 3, 2]
ex> over .
 Data stack items: 4
[7, 3, 2, 3]
ex> * .
 Data stack items: 3
[7, 3, 6]
ex> swap .
 Data stack items: 3
[7, 6, 3]
ex> dup .
 Data stack items: 4
[7, 6, 3, 3]
ex> * .
 Data stack items: 3
[7, 6, 9]
ex> rot .
 Data stack items: 3
[6, 9, 7]
ex> * .
 Data stack items: 2
[6, 63]
ex> swap .
 Data stack items: 2
[63, 6]
ex> - .
 Data stack items: 1
[57]                    # final result
ex> drop .              # discard it
 Data stack empty
ex>
~~~
  Of course you could have done it in a single input line after 1 year 
of experience :)
~~~
ex> 7 3 2 over * swap dup * rot * swap - .
 Data stack items: 1
[57]
ex>
~~~
~~~
ex> # calculate the sum of squares 10**2 + 20**2 + 30**2
ex> 10 20 30 .          # initial values
 Data stack items: 3
[10, 20, 30]
ex> dup .
 Data stack items: 4
[10, 20, 30, 30]
ex> * .
 Data stack items: 3
[10, 20, 900]
ex> swap .
 Data stack items: 3
[10, 900, 20]
ex> dup .
 Data stack items: 4
[10, 900, 20, 20]
ex> * .
 Data stack items: 3
[10, 900, 400]
ex> + .
 Data stack items: 2
[10, 1300]
ex> swap .
 Data stack items: 2
[1300, 10]
ex> dup .
 Data stack items: 3
[1300, 10, 10]
ex> * .
 Data stack items: 2
[1300, 100]
ex> + .
 Data stack items: 1
[1400]                  # result
ex>
~~~

  A good help if it gets too complicated is the user
stack to save intermediary data: define a word 2swap
~~~
ex> 2swap: "" ( a b c d -- c d a b)""
co> rot    #  ( a b c d -- a c d b )
co> uspush #  ( a c d b -- a c d )
co> rot    #  ( a c d -- c d a )
co> uspop  #  ( c d a -- c d a b )
co> ; .
 Data stack empty
ex> 11 22 33 44 .
 Data stack items: 4
[11, 22, 33, 44]
ex> 2swap .
 Data stack items: 4
[33, 44, 11, 22]
ex> '2swap pdef .
  2swap       at index:  2 "" ( a b c d -- c d a b) ""
  2swap: rot uspush rot uspop ;

  No duplicate (older definitions) present
 Data stack items: 4
[33, 44, 11, 22]
ex>
~~~

  Now, with the help of 2swap define 2over:
~~~
ex> 2over: "" ( a b c d -- a b c d a b )""
co> uspush uspush # ( a b c d -- a b )
co> 2dup # ( a b -- a b a b )
co> uspop uspop # ( a b a b -- a b a b c d )
co> 2swap # ( a b a b c d -- a b c d a b )
co> ; .
ex> cleards .
 Data stack empty
ex> 1 2 3 4 .
 Data stack items: 4
[1, 2, 3, 4]
ex> 2over .
 Data stack items: 6
[1, 2, 3, 4, 1, 2]
ex>
~~~

  And, if you feel in good mood, define 3dup and 4dup:
~~~
ex> 3dup: "" ( a b c -- a b c a b c )""
co> dup # ( a b c -- a b c c )
co> 2over # ( a b c c -- a b c c a b )
co> rot   # ( a b c c a b -- a b c a b c )
co> ; .
 Data stack empty
ex> 1 2 3 .
 Data stack items: 3
[1, 2, 3]
ex> 3dup .
 Data stack items: 6
[1, 2, 3, 1, 2, 3]
ex> 4dup: "" ( a b c d -- a b c d a b c d )""
co> 2over #  ( a b c d -- a b c d a b )
co> 2over #  ( a b c d a b -- a b c d a b c d )
co> ; .
ex> 1 2 3 4 .
 Data stack items: 4
[1, 2, 3, 4]
ex> 4dup .
 Data stack items: 8
[1, 2, 3, 4, 1, 2, 3, 4]
ex>
~~~


  Beware that 2dup is not the equivalent of dup dup:
~~~
ex> 99 88 2dup .
 Data stack items: 4
[99, 88, 99, 88]
ex> cleards .
 Data stack empty
ex> 99 88 dup dup .
 Data stack items: 4
[99, 88, 88, 88]
ex>
~~~

  A word about "pick": even if it's part of RPPy, use it sparely: do 
not treat the data stack as an array (internally it's a list, but whatever) 
where you can pick at will at any depth; a stack does it's job by pushing 
and popping data, not by indexing. By the way, "0 pick" is dup and "1 pick" is 
over ...
~~~
ex> 11 22 33 .
 Data stack items: 3
[11, 22, 33]
ex> 0 pick .
 Data stack items: 4
[11, 22, 33, 33]
ex> drop .
 Data stack items: 3
[11, 22, 33]
ex> 1 pick .
 Data stack items: 4
[11, 22, 33, 22]
ex>
~~~

  A good way to minimise stack shuffling is combining a group of short
definitions instead of a single large one; also think of arranging the 
output of a word so as the next word in chain isn't forced to rearrange 
it's received input to work correctly.
	
=== End of chapter 2 ===

"""

constvartxt = """
    3. Constants, variables, assignment operations
    ==============================================
  There are no constants in RPPy ( Python has a few ones: True, False, None, 
NotImplemented ...) but defining them is easy:
~~~
ex> PI: 3.14159 ; .
 Data stack empty
ex> PI .
 Data stack items: 1
[3.14159]
ex>
~~~
  Concerning True, False and None: all values which are not zero are True.
True, False and None are reflected in RPPy with the predefined ZeroFlag ZF, 
set to 1 for True and to 0 for False & None; see "Control Flow".
  
  There are no variables in RPPy (?!?); ok, there are no EXPLICIT variables, 
any definition whose FIRST ITEM is a literal is a variable; let's see an 
example:
In Python:
~~~
>>> a = 10
>>> b = 20
>>> c = a + b
>>> c
30
>>>
~~~
And now in RPPy:
~~~
ex> a: 10 ;
co> b: 20 ;
co> c: a b + ; .
 Data stack empty
ex> c .
 Data stack items: 1
[30]
ex>
~~~
  Assigning a new value to a variable:
~~~
ex> 15 *a = .           # assign 15 to index of variable a
 Data stack items: 1    # always prefix with "*" variable's name
[30]                    # to obtain the pointer to that variable
ex> 25 *b = .           # idem, assign 25 to b
 Data stack items: 1
[30]
ex> c .                 # executing c shows the new value 40
 Data stack items: 2
[30, 40]
ex>
~~~
  The asterisk "*" works by leaving on the stack the index, or pointer
if you prefer, where the variable is defined in the execution list. 
Now, the equal "=" sign , meaning assigning as in Python, tests if the
next word in the definition is a literal; if ok, the new value is stored
in the definition, so next time it's executed the new value is pushed 
on the stack. Forgetting to prefix a variable aborts the assignment, 
with all sort of strange output depending on what "=" finds at the 
false index position in the execution list...
  By the way, as there is no (not yet) notion of namespace in RPPy, all
variables are, being nothing more than a definition, global, like all 
definitions are.
  There's much less need to work with variables in RPPy compared to 
Python; pass arguments for words on the stack, not in variables.

  If you want to avoid using variables as locals in words, RPPy offers 
an auxiliary data stack, the user stack, accessed by:
  uspush   ( n -- ) data stack | ( -- n ) user stack ; push TOS to user stack
  uspop    ( -- n ) data stack | ( n -- ) user stack ; pop TOS of user stack
                                          & push to data stack
  clearus  ( ... -- ) empty user stack
  pus      ( -- ) print user stack
~~~
ex> 88 99 .
 Data stack items: 2
[88, 99]
ex> uspush .
 Data stack items: 1
[88]
ex> uspush .
 Data stack empty
ex> pus .
 User stack items: 2
[99, 88]
 Data stack empty
ex> uspop pus .
 User stack items: 1
[99]
 Data stack items: 1
[88]
ex> uspop pus .
 User stack empty
 Data stack items: 2
[88, 99]
~~~

  Following assignment operations are available in RPPy (see "pkern"):
  ###7       ===Assignment words===
  =        ( n idx -- ) store n to var[idx]: variable with index idx
  +=       ( n idx -- ) var[idx] += n
  -=       ( n idx -- ) var[idx] -= n
  *=       ( n idx -- ) var[idx] *= n
  /=       ( n idx -- ) var[idx] /= n
  //=      ( n idx -- ) var[idx] //= n
  %=       ( n idx -- ) var[idx] %= n
  **=      ( n idx -- ) var[idx] **= n
  Always push the desired value on the stack, followed by the indexed variable
~~~
ex> a b .
 Data stack items: 2
[15, 25]                # old values of a,b
ex> 3 *a /=    2 *b *= . # divide a by 3, multiply b by 2
 Data stack items: 2
[15, 25]
ex> a b .
 Data stack items: 4
[15, 25, 5.0, 50]       # new values of a,b
ex>
~~~
=== End of chapter 3 ===
"""

numberstxt = """
    4. Basic Datatypes - Numbers
    ============================
  - integers 
  - floating point
  - complex
~~~
ex> 22 33 +
ex>
 Data stack items: 1
[55]
ex> type .              # use "type" to get type of data
 Data stack items: 1
[<class 'int'>]         # "int" for integer type
ex> 44 11 / .
 Data stack items: 2
[<class 'int'>, 4.0]    # division leaves always a floating point number
ex> type .
 Data stack items: 2
[<class 'int'>, <class 'float'>] # "float" type
ex> 20 6 // .           # floored division, leaves integer part
 Data stack items: 3
[<class 'int'>, <class 'float'>, 3]
ex> (2+6j) (3+4j) + .   # complex numbers
 Data stack items: 4
[<class 'int'>, <class 'float'>, 3, (5+10j)]
ex> type .
 Data stack items: 4
[<class 'int'>, <class 'float'>, 3, <class 'complex'>]
ex>
~~~
  Look with "pkern" to see the available math operations:
    ###3       ===Math words===
  +        ( x y -- x+y ) add TOS to NOS
  -        ( x y -- x-y ) subtract TOS from NOS
  *        ( x y -- x*y ) multiply TOS by NOS
  /        ( x y -- x/y ) divide NOS by TOS - floating point div
  //       ( x y -- x//y ) divide NOS by TOS - floored (integer) div
  %        ( x y -- rem ) remainder of x/y division
  divmod   ( x y -- quot rem ) quotient & remainder of x/y division
  **       ( x y -- x**y ) NOS at power of TOS
  ++       ( n -- n+1 ) increment TOS by 1
  --       ( n -- n-1 ) decrement TOS by 1
  neg      ( n -- neg(n) ) negate n
  abs      ( x -- abs(x) ) absolute value of x
  round    ( n i -- round(n))  n rounded to i digits
  ...
  ...
  
  Converting to different number types is available with:
  int     ( str/n -- n ) convert str or number n to integer n
  float   ( str/int -- n ) convert string or integer to floating point number
  complex ( str -- n ) convert str to complex number n
  str     ( n -- str ) return a string interpretation of n
  See also "Miscellaneous words" for other types of number conversions.
~~~
ex>  3.14 int .
 Data stack items: 1
[3]
ex> 99 float .
 Data stack items: 2
[3, 99.0]
ex> 3.14159 str .
 Data stack items: 3
[3, 99.0, '3.14159']
ex> " 123" int .
 Data stack items: 4
[3, 99.0, '3.14159', 123]
ex> " 123" float .
 Data stack items: 5
[3, 99.0, '3.14159', 123, 123.0]
ex> " 11+22j" complex .
 Data stack items: 6
[3, 99.0, '3.14159', 123, 123.0, (11+22j)]
ex>
~~~
  
=== End of chapter 4 ===
"""

stringstxt  = """
    5. Basic Datatypes - Strings
    =============================

  Strings can be defined in RPPy as follows:
  - if the string doesn't have any space included, PREFIX it with single quote
~~~
ex> 'Hello,World! .
 Data stack items: 1
['Hello,World!']
ex>
~~~
  - if the string has spaces included, use the WORD double quote " as start of
  string: the space after " , as you already know, is the word's separator and 
  is obviously not part of the string. The first next double quote encountered 
  ends the string: that means that you cannot include double quotes as part of
  the string, only single quotes
~~~
ex> " Hello World!   " .
 Data stack items: 2
['Hello,World', 'Hello World!   ']
ex> "     Hello World!" .
 Data stack items: 3
['Hello,World', 'Hello World!   ', '    Hello World!']
ex> " Hello 'World!'" .
 Data stack items: 4
['Hello,World', 'Hello World!   ', '    Hello World!', "Hello 'World!'"]
ex>
~~~
  - if the string includes a mix of single and double quotes,use the word "-> "
  as starting the string, and the marker (not word!) "<-" as end of string
~~~
ex> cleards .
 Data stack empty
ex> -> all sort of quotes: "doubles 'singles' mixed"   <- .
 Data stack items: 1
['all sort of quotes: "doubles \'singles\' mixed"   ']
ex> print .
all sort of quotes: "doubles 'singles' mixed"
 Data stack empty
ex>
~~~
  NB. the backslash "\" is used to quote a quote (escape it) at displaying 
  the stack;  print interprets the quoted quote correctly
  
  - if the string starts with the word "" double double quote, and ends with 
  the "" marker, it is a docstring attached to the current definition. Using 
  it outside a definition ignores all the rest of the input line
~~~
ex> spam: " that's the spam definition" print
co> " nothing to do"
co> "" (spam before -- spam after)"" ; .
 Data stack empty
ex> spam .
that's the spam definition
 Data stack items: 1
['nothing to do']
ex> 'spam pdef .
  spam        at index:  2 "" (spam before -- spam after) ""
  spam: " that's the spam definition" print " nothing to do" ;

  No duplicate (older definitions) present
 Data stack items: 1
['nothing to do']
ex>
~~~

  - if a multiline string is needed, start it with the word \""" triple double
  quote and end it with the triple quote marker \""" in the last line. All 
  input data after the end marker \""" is lost, put always the end marker on a 
  separate input line
~~~
ex> cleards .
 Data stack empty
ex> \""" Multiline string
""> line 1              # apart "ex>" and "co>" , this is the only case when
""> line 2              # at input the prompt '"">' is displayed, until ending 
""> line 3              # the multiline string
""> end \""" 111 222 .   # 111 222 and the dot are ignored!
Compile warning: all data after closing triple-quote in current line is ignored!
ex> .                   # so, to end input, press "." 
 Data stack items: 1
['Multiline string \\nline 1\\nline 2\\nline 3\\nend ']
ex> print .             # the "\\n" is the escape character for newline
Multiline string        # print interprets correctly "\\n"
line 1
line 2
line 3
end
 Data stack empty
ex>
~~~

  Strings, being a sequence of characters, can be indexed using the built-in 
  "index registers" I, J, K. An index register is like a variable, but shorter
  at use:
~~~
ex> 0 i= .          # no need for an "*" prefixing i; no need for separate "="
 Data stack empty
ex> i .             # like a variable, i leaves it's value on the stack
 Data stack items: 1
[0]
ex>
~~~
  The first item in a sequence has index 0:
~~~
ex> " Hello!" .
 Data stack items: 1
['Hello!']
ex> s[i] .              # extract character at index i by "s[i]"
 Data stack items: 2    # which stands for "sequence item at i"
['Hello!', 'H']         # "H" is at index 0
ex> swap .              # put the string "Hello" at TOS
 Data stack items: 2    # as needed by s[i]
['H', 'Hello!']
ex> 4 i= s[i] .         # extract the fifth character at index 4
 Data stack items: 3
['H', 'Hello!', 'o']
ex>
~~~
  The last item in a sequence has index -1, before last -2, a.s.o.:
~~~
ex> swap .
 Data stack items: 3
['H', 'o', 'Hello!']
ex> -1 i= s[i] .        # extract "!"
 Data stack items: 4
['H', 'o', 'Hello!', '!']
ex> swap .
 Data stack items: 4
['H', 'o', '!', 'Hello!']
ex> -5 i= s[i] .        # extract "e"
 Data stack items: 5
['H', 'o', '!', 'Hello!', 'e']
ex>
~~~
  Extracting a substring, called slicing, uses two indexes I and J where 
  I = start index, J = end index ( the end index is always excluded):
~~~
ex> swap .
 Data stack items: 5
['H', 'o', '!', 'e', 'Hello!']
ex> 2 i= 4 j= s[i:j] .  # extract from 2 (included) to 4 (excluded)
 Data stack items: 6
['H', 'o', '!', 'e', 'Hello!', 'll']
ex>
~~~
  For practical reasons, you can use s[i:] to extract from i to the end, 
  and s[:j] to extract from start to j :
~~~
ex> swap .
 Data stack items: 6
['H', 'o', '!', 'e', 'll', 'Hello!']
ex> 3 i= s[i:] .        # extract from 3 until end
 Data stack items: 7
['H', 'o', '!', 'e', 'll', 'Hello!', 'lo!']
ex> swap .
 Data stack items: 7
['H', 'o', '!', 'e', 'll', 'lo!', 'Hello!']
ex> 5 j= s[:j] .        # extract from start until 5 (excluded)
 Data stack items: 8
['H', 'o', '!', 'e', 'll', 'lo!', 'Hello!', 'Hello']
ex> swap .
 Data stack items: 8
['H', 'o', '!', 'e', 'll', 'lo!', 'Hello', 'Hello!']
ex> -3 j= s[:j] .       # extract from start until -3 (excluded)
 Data stack items: 9
['H', 'o', '!', 'e', 'll', 'lo!', 'Hello', 'Hello!', 'Hel']
ex>
~~~
  Using an index out of range aborts s[i] :
~~~
ex> swap .
 Data stack items: 9
['H', 'o', '!', 'e', 'll', 'lo!', 'Hello', 'Hel', 'Hello!']
ex> 999 i= s[i] .
"s[i]" aborted: string index out of range
 Aborted at Execution List Index:  56
 Aborted in execution string or in definition with multiple returns
  TOS:  <class 'str'> Hello!
  NOS:  <class 'str'> Hel
 Data stack items: 9
['H', 'o', '!', 'e', 'll', 'lo!', 'Hello', 'Hel', 'Hello!']
ex>
~~~
  However in slicing, an out of range index doesn't leave an error:
~~~
ex> s[i:] .             # remember, i is 999
 Data stack items: 10
['H', 'o', '!', 'e', 'll', 'lo!', 'Hello', 'Hel', 'Hello!', '']
ex>                     # as there's nothing from 999 onwards, the result
                        # is the empty string '' ...
~~~

  Strings are immutable in RPPy as in Python, you cannot insert a string in
  another; create a new one by slicing and adding substrings:
~~~
ex> cleards
ex>
 Data stack empty
ex> " Hello!" .
 Data stack items: 1
['Hello!']
ex> 5 j= s[:j] .        # extract first part 
 Data stack items: 2
['Hello!', 'Hello']
ex> " , World!" + .     # add second part
 Data stack items: 2
['Hello!', 'Hello, World!']
ex> print .
Hello, World!
 Data stack items: 1
['Hello!']
ex>
~~~

  A last word about empty strings: you cannot create an empty string 
  using " " or "  " ; the first is aborted and the second is a string
  with lenght 1 containing a space. Use "emptystr" instead
~~~
ex> " " .
Compile error: " without closing marker "
ex> "  " .
 Data stack items: 2
['Hello!', ' ']
ex> emptystr .
 Data stack items: 3
['Hello!', ' ', '']
ex>
~~~

  There are many words concerning string manipulations; see "pkern"
  
=== End of chapter 5 ===
"""

liststxt = """
    6. Basic Datatypes - Lists
    =============================
  
  Lists are composed of comma-separated values (items) enclosed by square
brackets; usually the items are of same type, but they can be mixed of 
all sort: numbers, strings, other lists, etc.

  Creating lists in RPPy can be done as follows:
  - if no space follows the separating commas, and no spaces in string items,
write it simply as is:
~~~
ex> [1,2,"abc",5.99,"efg"] .
 Data stack items: 1
[[1, 2, 'abc', 5.99, 'efg']] # beware that list items are displayed with a space
ex>                          # after comma, even if inputted without spaces
~~~
  - if anywhere there's at least one space present, create a string with all 
items, WITHOUT the enclosing square brackets and use the word "list":
~~~
ex> " 1, 2, 'a b c', 5.99, 'e f g'" list .
 Data stack items: 2
[[1, 2, 'abc', 5.99, 'efg'], [1, 2, 'a b c', 5.99, 'e f g']]
ex>
~~~
  Use single quotes inside the defining string, otherwise the first double quote 
encountered ends abruptly your string; use "-> " and "<-" if you want to mix 
single with double quotes (see "Basic Datatypes - Strings")

  - if you want to create a list from a series of items ALREADY on the stack, 
push the starting marker "[]" followed by any items wanted and use "listcre":
~~~
ex> '[] 11 22 'abc " e f g h" 33 44 listcre .
 Data stack items: 3
[[1, 2, 'abc', 5.99, 'efg'], [1, 2, 'a b c', 5.99, 'e f g'], 
[11, 22, 'abc', 'e f g h', 33, 44]]
ex>
~~~
  Forgetting to push the starting marker "[]" forces listcre to add all data 
stack content to your list:
~~~
ex> cleards .
 Data stack empty
ex> 111 222 'abcdefgh " xx yy" 333 listcre .
 Data stack items: 1
[[111, 222, 'abcdefgh', 'xx yy', 333]]
ex>
~~~
  - the content of a given list can be pushed as separate items on the stack 
using the word "listexp":
~~~
ex> 111 222 'abcdefgh " xx yy" 333 listcre .
 Data stack items: 1
[[111, 222, 'abcdefgh', 'xx yy', 333]]
ex> listexp .
 Data stack items: 5
[111, 222, 'abcdefgh', 'xx yy', 333]
ex>
~~~
  Beware that listexp doesn't push a starting marker on the stack...
  
  Lists, being sequences, can be indexed and sliced, like strings, see 
"Basic Datatypes - Strings" for details on indexing & slicing
~~~
ex> cleards
ex>
 Data stack empty
ex> " 11, 22, 'abc', 33, 'xyz'" list .
 Data stack items: 1
[[11, 22, 'abc', 33, 'xyz']]
ex> 1 i= s[i] .         # extract item 1
 Data stack items: 2
[[11, 22, 'abc', 33, 'xyz'], 22]
ex> swap .
 Data stack items: 2
[22, [11, 22, 'abc', 33, 'xyz']]
ex> 4 j= s[i:j] .       # extract slice from 1 (included) to 4 (excluded)
 Data stack items: 3    # the slice is also a list of 3 elements
[22, [11, 22, 'abc', 33, 'xyz'], [22, 'abc', 33]]
ex>
~~~
  
  Lists, contrary to strings, are mutable: you can insert and delete items:
~~~
ex> 2 i= del[i] .       # delete item at index 2 aka 33 from [22,'abc',33]
 Data stack items: 3
[22, [11, 22, 'abc', 33, 'xyz'], [22, 'abc']]
ex> 1 99 insert .       # insert at index 1 the value 99
 Data stack items: 3
[22, [11, 22, 'abc', 33, 'xyz'], [22, 99, 'abc']]
ex> 3 swap insert .     # insert [22,99,'abc'] at index 3
 Data stack items: 2    # now it's a list with a list included
[22, [11, 22, 'abc', [22, 99, 'abc'], 33, 'xyz']]
ex> 3 i= 2 j= s[i][j] . # get third item from the sublist at index 3 in list
 Data stack items: 3
[22, [11, 22, 'abc', [22, 99, 'abc'], 33, 'xyz'], 'abc']
ex>
~~~

  Use the word "len" to get the lenght of a list (or string, dictionary, etc.):
~~~
ex> drop .              # discard 'abc'
 Data stack items: 2
[22, [11, 22, 'abc', [22, 99, 'abc'], 33, 'xyz']]
ex> len .               # the lenght is 6, as the sublist counts as a single
 Data stack items: 2    # element, not three
[22, 6]
ex>
~~~
  See "pkern" for the words concerning list manipulation
  
=== End of chapter 6 === 
"""

dictiotxt = """
    7. Basic Datatypes - Dictionaries
    =================================
  
  Dictionaries are composed of a set of key:value pairs enclosed in curly 
braces "{}" ; accessing a value is done by these keys, not by index as 
in strings or lists.

  Creating a dictionary in RPPy can be done as follows:
  - if no space follows the separating commas, and no spaces in string items,
write it simply as is:
~~~
ex> {'jessie':22,'nora':30,'johanna':33} .
 Data stack items: 1
[{'jessie': 22, 'nora': 30, 'johanna': 33}]
ex>
~~~

  - if anywhere there's at least one space present, create a string with all 
items, WITHOUT the enclosing curly braces and use the word "dict":
~~~
ex> " 10:'value ten', 20:'value twenty', 'list':[1, 2, 3]" dict .
 Data stack items: 2
[{'jessie': 22, 'nora': 30, 'johanna': 33}, {10: 'value ten', 20: 'value twenty', 'list': [1, 2, 3]}]
ex>
~~~

  - finally, you can create a dictionary by using two lists of equal lenght: 
the first is a list of keys, the second a list of associated values to these
keys; use the word "dictcre":
~~~
ex> [1,2,3] ['abcd','efgh','ijkl'] dictcre .
 Data stack items: 1
[{1: 'abcd', 2: 'efgh', 3: 'ijkl'}]
ex>
~~~
  - the reverse of "dictcre" is "dictexp", which expands a dictionary to the 
two lists: key list and value list

  - to get a value attached to a key, use "get" :
~~~
ex> dup 2 get .         # duplicate TOS, as get removes it
 Data stack items: 2    # use key "2" to extract "efgh"
[{1: 'abcd', 2: 'efgh', 3: 'ijkl'}, 'efgh']
ex>
~~~

  - to return and remove a value with associated key, use "popkey"; 
to add a new key:value pair use "setdefault"
~~~
ex> drop dup 3 popkey .
 Data stack items: 3
[{1: 'abcd', 2: 'efgh'}, {1: 'abcd', 2: 'efgh'}, 'ijkl']
ex> drop 'one_hundred 100 setdefault .
 Data stack items: 2
[{1: 'abcd', 2: 'efgh', 'one_hundred': 100}, {1: 'abcd', 2: 'efgh', 'one_hundred': 100}]
ex>
~~~
  Important to remember: dup, even it appears to duplicate TOS, for objects 
like dictionaries, lists, etc. RPPy duplicates only a reference to the same
object; as a consequence, modifying the dictionary on top modifies also the 
same dictionary (in fact it's a single object) on next of stack. Use "copy" 
instead of "dup" if you want preserving the initial data:
~~~
ex> drop .
 Data stack items: 1    # leave the original dictionary
[{1: 'abcd', 2: 'efgh', 'one_hundred': 100}]
ex> copy .
 Data stack items: 2    # create a copy, not a duplicate with "dup"
[{1: 'abcd', 2: 'efgh', 'one_hundred': 100}, {1: 'abcd', 2: 'efgh', 'one_hundred': 100}]
ex> 'two_hundred 200 setdefault .
 Data stack items: 2    # this time the original data remains unmodified
[{1: 'abcd', 2: 'efgh', 'one_hundred': 100}, {1: 'abcd', 2: 'efgh', 'one_hundred': 100, 'two_hundred': 200}]
ex>
~~~

  - finally, to add a entire sequence to a dictionary, use "update":
~~~
ex> agedict: {'jessie':22,'nora':30,'johanna':33} ; .
 Data stack empty
ex> agedict print .
{'jessie': 22, 'nora': 30, 'johanna': 33}
 Data stack empty
ex> agedict " 'hermann':40, 'mike':45, 'josh':50" dict update .
 Data stack items: 1
[{'jessie': 22, 'nora': 30, 'johanna': 33, 'hermann': 40, 'mike': 45, 'josh': 50}]
ex>
~~~
  
=== End of chapter 7 ===
"""

tupsettxt = """
    8. Basic Datatypes - Tuples, Sets
    =================================
  
  A tuple is similar to a list, but enclosed in parentheses; it may contain 
data of different types, but contrary to lists, tuples are, like strings, 
immutable.

  Creating a tuple in RPPy can be done as follows:
  - if no space follows the separating commas, and no spaces in string items,
write it simply as is:
~~~
ex> (1,2,'abc','efg') .
 Data stack items: 1
[(1, 2, 'abc', 'efg')]
ex>
~~~

  - if anywhere there's at least one space present, create a string with all 
items, WITHOUT the enclosing parentheses and use the word "tuple":
~~~
ex> " 1, 2, 3, 'Hello World!', 99" tuple .
 Data stack items: 2
[(1, 2, 'abc', 'efg'), (1, 2, 3, 'Hello World!', 99)]
ex>
~~~

  - finally you can create a tuple by giving as input a list of values 
and using "tupcre"; expand a tuple to a list of values by "tupexp":
~~~
ex> [111,222,'abcd'] tupcre .
 Data stack items: 3
[(1, 2, 'abc', 'efg'), (1, 2, 3, 'Hello World!', 99), (111, 222, 'abcd')]
ex> tupexp .
 Data stack items: 3
[(1, 2, 'abc', 'efg'), (1, 2, 3, 'Hello World!', 99), [111, 222, 'abcd']]
ex>
~~~

  - as with lists, get an item by using "s[i]"; you can also apply slicing, 
see "Basic Datatypes - Strings"
~~~
ex> drop 3 i= s[i] .    # drop the list leaved by tupexp
 Data stack items: 3    # get item at index 3
[(1, 2, 'abc', 'efg'), (1, 2, 3, 'Hello World!', 99), 'Hello World!']
ex>
~~~

  - tuples being immutable, you cannot delete or insert an item:
~~~
ex> drop .
 Data stack items: 2
[(1, 2, 'abc', 'efg'), (1, 2, 3, 'Hello World!', 99)]
ex> del[i] .            # try to delete item at index 3 in I
"del[i]" aborted: 'tuple' object doesn't support item deletion
 Aborted at Execution List Index:  25
 Aborted in execution string or in definition with multiple returns
  TOS:  <class 'tuple'> (1, 2, 3, 'Hello World!', 99)
  NOS:  <class 'tuple'> (1, 2, 'abc', 'efg')
 Data stack items: 2
[(1, 2, 'abc', 'efg'), (1, 2, 3, 'Hello World!', 99)]
ex> 4 " Bye!" insert .  # try to insert an item at index 4
"insert" aborted: 'tuple' object has no attribute 'insert'
 Aborted at Execution List Index:  28
 Aborted in execution string or in definition with multiple returns
  TOS:  <class 'str'> Bye!
  NOS:  <class 'int'> 4
 Data stack items: 4
[(1, 2, 'abc', 'efg'), (1, 2, 3, 'Hello World!', 99), 4, 'Bye!']
ex>
~~~

  A set is an unordered collection of items enclosed in curly braces, 
without any duplicated elements, used for membership testing and operations 
like union, intersection, difference.

  Creating a set in RPPy is done, as with tuples, by using "set" for a string
with items or simply by enclosing items in curly braces if no spaces present:
~~~
ex> " 'apple', 'banana', 'pear', 'apple', 'apple', 'banana'" set .
 Data stack items: 1
[{'apple', 'banana', 'pear'}]  # all duplicates removed
ex> {1,2,3,1,1,3,4,5,5} .
 Data stack items: 2
[{'apple', 'banana', 'pear'}, {1, 2, 3, 4, 5}]
ex>
~~~
  Also, use "setcre" to create a set from a list, and "setexp" to expand
the set to a list, as with tuples above.

  A string itself can be decomposed to it's characters by using "setstr":
~~~
ex> " abcd efgh ijkl ab" setstr .
 Data stack items: 3
[{'apple', 'banana', 'pear'}, {1, 2, 3, 4, 5}, {' ', 'c', 'l', 'd', 'j', 
'b', 'g', 'f', 'e', 'i', 'h', 'a', 'k'}]
ex> 'abracadabra setstr .
 Data stack items: 4
[{'apple', 'banana', 'pear'}, {1, 2, 3, 4, 5}, {' ', 'c', 'l', 'd', 'j', 
'b', 'g', 'f', 'e', 'i', 'h', 'a', 'k'}, {'c', 'r', 'd', 'b', 'a'}]
ex>
~~~

  Difference of two sets:
~~~
ex> cleards
ex>
 Data stack empty
ex> 'abcd setstr 'cdef setstr .
 Data stack items: 2
[{'d', 'b', 'c', 'a'}, {'d', 'c', 'f', 'e'}]
ex> difference .
 Data stack items: 1
[{'b', 'a'}]
ex>
~~~

  Symmetric difference:
~~~
ex> drop .
 Data stack empty
ex> 'abcd setstr 'cdef setstr .
 Data stack items: 2
[{'d', 'b', 'c', 'a'}, {'d', 'c', 'f', 'e'}]
ex> sdifference .
 Data stack items: 1
[{'b', 'f', 'e', 'a'}]
ex>
~~~
  
=== End of chapter 8 ===
"""
controltxt = """
 
    9. Control Flow
    ===============
 
  9.1 Conditions
  --------------
  As in Python, control flow is based on decisions and decisions are 
based on comparisons; the first set is identically to Python:
  <        ( x y -- x y ) ZF = 1 if x<y
  >        ( x y -- x y ) ZF = 1 if x>y
  <=       ( x y -- x y ) ZF = 1 if x<=y
  >=       ( x y -- x y ) ZF = 1 if x>=y
  ==       ( x y -- x y ) ZF = 1 if x==y
  !=       ( x y -- x y ) ZF = 1 if x!=y
  
  But, opposed to Python, there are no True/False boolean values; instead 
in RPPy you have the ZeroFlag register, ZF, which is set to 1 or 0 and 
tested by branching words at program execution.

  The second set is RPPy-specific:
  <0       ( n -- n ) ZF = 1 if n < 0
  >0       ( n -- n ) ZF = 1 if n > 0
  =0       ( n -- n ) ZF = 1 if n == 0
  !=0      ( n -- n ) ZF = 1 if n != 0
  <0>      ( idx1 idx2 idx3 n -- ) if n<0 execute word with idx1; if n=0 execute idx2; else idx3
  <=>      ( idx1 idx2 idx3 x y -- ) if x<y execute word with idx1; if x=y execute idx2, else idx3
  zf=      ( n -- ) pop TOS to ZF
  zf       ( -- ZF ) push ZF

  The ZF register can be accessed in the same manner as the index registers; 
you can store any value to be used by the branching words, always knowing 
that any non-zero value is equivalent to ZF == 1

  9.2 Branching
  -------------
  
  The most common branching word is "if" with the following syntax:
  "condition IF true part THEN false part", opposed to Python where you have:
  IF condition:
    true part
  ELSE:        # the ELSE is optional
    false part
~~~
>>> a=10
>>> if a %2 == 0 :
...   print('Even number')
... else:
...   print('Odd number')
...
Even number
>>>
~~~

  In RPPy there's no ELIF or ELSE:
~~~
ex> evenodd: 2 % =0 if " Even number" print ; then " Odd number" print ; .
 Data stack empty
ex> 10 evenodd .
Even number
 Data stack items: 1
[0]
ex> 11 evenodd .
Odd number
 Data stack items: 2
[0, 1]
ex>
~~~

  There's also the opposite test, "ifz", which executes the conditional 
  part if ZF = 0, and the non-equality test "ifneq" which executes the 
  conditional part if TOS is not equal to NOS. See "pcomp" which shows 
  RPPy's compiling words.
~~~
ex> pcomp .
             ===Compiler words===
  #        ( -- ) comment, skip rest of line
  .        ( -- ) mark end of compile phase, start execution phase
  ""       ( -- ) mark start of docstring to embed in definition
  \"""      ( -- ) mark start of multiline string
  "        ( -- ) mark start of string with blanks and without double quotes
  ->       ( -- ) mark start of string with blanks/quotes of all sort
  ;        ( -- ) compile return or compile jump (if tail call optimisation)
  if       ( -- ) compile if: continue execution if ZF == 1, else branch to "then"
  ifz      ( -- ) compile ifz: same as if, but for ZF == 0
  ifneq    ( x y -- x y ) compile ifneq: continue execution if x!=y, else branch to "then"
  then     ( -- ) compile then: branch there if condition not satisfied

 Compiler Definitions:  11
 Data stack empty
ex>
~~~

  Another branching word is "choose" with the following syntax:
  " index_of_word_for_true_branch  index_of_word_for_false_branch CHOOSE "
  Let's redefine our "evenodd":
~~~
ex> even: " Even number" print ;
co> odd: " Odd number" print ;
co> evenodd1: 2 % =0 *even *odd choose ; .
 Data stack empty
ex> 10 evenodd1 .
Even number
 Data stack items: 1
[0]
ex> 13 evenodd1 .
Odd number
 Data stack items: 2
[0, 1]
ex>
~~~

  Finally, there are two triple-branching words "<0>" and "<=>" which 
test for <0, =0, >0 and x<y, x=y, x>y respectively:
~~~
ex> less-0: " Negative number" print ;
co> equal-0: " Zero" print ;
co> greater-0: " Positive number" print ;
co> arglist: *less-0 *equal-0 *greater-0 ;
co> 3test: <0> ; .
 Data stack empty
ex> arglist -22 3test .
Negative number
 Data stack empty
ex> arglist 0 3test .
Zero
 Data stack empty
ex> arglist 99 3test .
Positive number
 Data stack empty
ex>
~~~
  As a matter of convenience, put the indexes in a separate word to 
avoid stack shuffling, as working with three or more stack items 
becomes quickly cumbersome and error prone (not that with two items 
it's error free...)

  9.3 Looping
  -----------
  
  A while loop executes as long as the while condition is true; in 
  Python you have:
~~~
>>> a=10
>>> while a != 0 :
...   print(a)
...   a -= 1
...
10
9
8
7
6
5
4
3
2
1
>>>
~~~
 
  In RPPy you have:
~~~
ex> while-true-loop: !=0 if dup print -- while-true-loop ; then " while ended" print ; .
 Data stack empty
ex> 10 while-true-loop .
10
9
8
7
6
5
4
3
2
1
while ended
 Data stack items: 1
[0]
ex>
~~~
~~~
ex> while-false-loop: =0 if " while ended" print ; then dup print -- while-false-loop ; .
 Data stack items: 1
[0]
ex> 10 while-false-loop .
10
9
8
7
6
5
4
3
2
1
while ended
 Data stack items: 2
[0, 0]
ex>
~~~
  In RPPy a call to a word followed by return ";" is converted to a 
single jump to that word; the return itself is not compiled. See 
user manual for "tail call optimisation".
  
  A counted loop uses in Python the range function:
~~~
>>> for a in range(1,11):
...   print(a)
...
1
2
3
4
5
6
7
8
9
10
~~~

  In RPPy the counted loop uses an index register I, J, K, where the
count is assigned; the body of the loop must be a separate word, repeatedly 
executed by "iloop", "jloop" or "kloop":
~~~
ex> iprint: i print i-- ;
co> counted-loop: i= *iprint iloop ; .
 Data stack empty
ex> 10 counted-loop .
10
9
8
7
6
5
4
3
2
1
 Data stack empty
ex>
~~~
  Beware that the word defining the body must be prefixed with "*", 
to obtain it's index, as needed by i-j-k-loop.  

  9.4 Switching
  -------------
 
  There are no predefined switch primitives in RPPy, but by using a 
list of indexed words you can define either a case-like numerical
switch or a key-driven one:
~~~
ex> sw0: " case 0" print ;
co> sw1: " case 1" print ;
co> sw2: " case 2" print ;
co> sw-list: *sw0 *sw1 *sw2 ; .
ex> number-switch: "" ( switchlist n -- ) switch to n-th word in switchlist""
co> 2dup # ( switchlist n switchlist n)
co> swap # ( switchlist n n switchlist )
co> len -- # ( switchlist n n listlenght-1 )
co> > if " switch number out of list range" print ;
co> then 2drop # ( switchlist n)
co> i= s[i] # ( switchlist n-th_item_in_switchlist )
co> execidx drop # ( ) execute word at n-th position in switchlist
co> ; .
ex> sw-list 2 number-switch .
case 2
 Data stack empty
ex> sw-list 0 number-switch .
case 0
 Data stack empty
ex> sw-list 3 number-switch .
switch number out of list range
 Data stack items: 4    # at n > listlenght no stack clearing is done,
[[12, 16, 20], 3, 3, 2] # in order to identify faulty arguments
ex>                     # by the way, this definition has a big problem
~~~                     # even if input is ok (see drop after execidx...)

  Use a similar way for a key-driven switch; create a dictionary from two 
lists: the key list and the associated indexed word list; execute the word 
found at key:index pair:
~~~
ex> keylist: ['first','second','third'] ; .
ex> keydict: keylist sw-list dictcre ; .
ex> keydict .
 Data stack items: 1     # see the indexes associated to keys
[{'first': 12, 'second': 16, 'third': 20}]
ex> key-switch: "" ( keydict key -- ) switch to key:word association""
co> in ifz " key not found" print ; # test if key present in dictionary
co> then get execidx # get the index associated to key and execute word
co> ; .
ex> cleards
ex>
 Data stack empty
ex> keydict 'second key-switch .
case 1
 Data stack empty
ex> keydict 'first key-switch .
case 0
 Data stack empty
ex> keydict 'last key-switch .
key not found
 Data stack items: 2
[{'first': 12, 'second': 16, 'third': 20}, 'last']
ex>
~~~

...NB. what's the problem with "drop" in number-switch above:
   - if the called word leaves a result on the stack, drop drops it
   - if we don't put a drop after execidx, the switchlist rests on 
   the stack; decide then what to discard depending on execution flow
  
=== End of chapter 9 ===

"""

inputprinttxt = """
    10. Input and printing
    =====================
  
  The word "input" reads a line from standard input, converts it 
to a string (stripping a trailing newline), and pushes the string 
to the data stack:
  input ( -- str ) read a line from input and convert data to a string
~~~
ex> input .
Hello World!
 Data stack items: 1
['Hello World!']
ex>
~~~~
  Do not attempt to input numbers and then use math on them directly,
as the stack contains strings, not numbers:
~~~
ex> input .
50
 Data stack items: 2
['Hello World!', '50']
ex> input .
10
 Data stack items: 3
['Hello World!', '50', '10']
ex> + .                 # the "+" adds two strings here, not numbers
 Data stack items: 2    # convert them with "int, float" if math wanted
['Hello World!', '5010']
ex>
~~~
 
  If you want a prompt before input, use "inputprompt":
  inputprompt ( strprompt -- str ) write strprompt to standard output,
  then read a line
~~~
ex> " Enter your name here: " inputprompt .
Enter your name here: Max Weber
 Data stack items: 1
['Max Weber']
ex>
~~~

  You have already used some indispensable printing words like 
"pkern", "pdef", etc. , but let's present all RPPy specific printing 
words:
  - pds: print data stack; useful if you switch the automatic stack 
  printing off in order to unclutter console output
  - pdson/pdsoff: switch on/off the data stack printing; at RPPy start, 
  the switch is on
  NB. if the data stack contains more than 10 items, only the top 10 
  will be displayed; use "cleards" to empty accumulated unnecessary data
~~~
ex> cleards .
 Data stack empty
ex> 11 22 33 .
 Data stack items: 3
[11, 22, 33]
ex> pdsoff .
ex> 44 55 .
ex> + .
ex> pds .
 Data stack items: 4
[11, 22, 33, 99]
ex> drop .
ex> swap + .
ex> pdson .
 Data stack items: 2
[11, 55]
ex>
~~~

  - pus (nothing related to the medical term...): print user stack; 
  as seen in "Constants, variables ..." the user stack holds temporary 
  data, avoiding the need of locals in words.
  Use "uspush" and "uspop" to transfer/retrieve data; "clearus" clears 
  the user stack similarly to "cleards"  
~~~
ex> cleards .
 Data stack empty
ex> 88 99 .
 Data stack items: 2
[88, 99]
ex> uspush .
 Data stack items: 1
[88]
ex> uspush .
 Data stack empty
ex> pus .
 User stack items: 2
[99, 88]
 Data stack empty
ex> uspop pus .
 User stack items: 1
[99]
 Data stack items: 1
[88]
ex> uspop pus .
 User stack empty
 Data stack items: 2
[88, 99]
ex>
~~~
  - prs: print return stack; see the chain of words called
  NB1. the return stack can't be modified by the user, only visualized
  NB2. at abort, the return stack is always displayed, then emptied
~~~
ex> prs .
 Return stack items:0
 Data stack empty
ex> xx: " xx executed" print prs ;
co> yy: " yy executed" print xx ;
co> zz: " zz executed" print yy ;
co> aa: zz yy xx ; .
 Data stack empty
ex> aa .
zz executed
yy executed
xx executed
 Return stack items:2
2 return from: zz
1 return from: aa
yy executed
xx executed
 Return stack items:2
2 return from: yy
1 return from: aa
xx executed
 Return stack items:1
1 return from: aa
 Data stack empty
ex> prs .
 Return stack items:0
 Data stack empty
ex>
~~~

  - plist: print list as enumerated items
~~~
ex> ['one','two','three'] .
 Data stack items: 1
[['one', 'two', 'three']]
ex> plist .
   0 one
   1 two
   2 three
 Data stack empty
ex>
~~~

  - pexlst: print Execution List starting at given index; useful if 
  execution aborted by various reasons, to see the execution stream
  where it happened
~~~
ex> " some work before declaring a definition" .
 Data stack items: 1
['some work before declaring a definition']
ex> print .
some work before declaring a definition
 Data stack empty
ex> 22 33 * 3 / .
 Data stack items: 1
[242.0]
ex> dup 5 // .
 Data stack items: 2
[242.0, 48.0]
ex> 1 pexlst .
    1 ;                 # starting at index 2 you see the execution history
    2 lit  some work before declaring a definition
    3 print
    4 lit  22
    5 lit  33
    6 *
    7 lit  3
    8 /
    9 dup
   10 lit  5
   11 //
   12 lit  1            # the last thing done is calling pexlst
   13 pexlst
 Data stack items: 2
[242.0, 48.0]
ex>
~~~
  Now suppose we start defining some words:
~~~
ex> xx: " empty def" ;
co> yy: " call xx" xx ;
co> zz: yy print print ; .
 Data stack items: 2
[242.0, 48.0]
ex> cleards 888 999 .
 Data stack items: 2
[888, 999]
ex> 1 pexlst .
    1 ;                 # all the previous history is gone
    2 xx:               # new definitions are stored always after the last
    3 lit  empty def    # one always here, ending with";" or jump
    4 ;                 # that way no execution stream remains stored, as 
    5 yy:               # it is the VOLATILE part; only the last exec-stream 
    6 lit  call xx      # rests after the last def declared, to be also erased
    7 jump xx           # if starting the next definition (see after index 13)
    8 zz:
    9 call yy
   10 print
   11 print
   12 ;
   13 cleards
   14 lit  888
   15 lit  999
   16 lit  1
   17 pexlst
 Data stack items: 2
[888, 999]
ex> aa: " will be stored at index 13 after zz" print ; .
 Data stack items: 2
[888, 999]
ex> 8 pexlst .
    8 zz:
    9 call yy
   10 print
   11 print
   12 ;
   13 aa:
   14 lit  will be stored at index 13 after zz
   15 print
   16 ;
   17 lit  8
   18 pexlst
 Data stack items: 2
[888, 999]
ex>
~~~

  - print: print item from the stack, item may be a number, string,
  list, dictionary, etc. ( item -- )
  Contrary to Python, only one item can be printed at a time; 
  also the output is only stdout, there's no printing to file (yet...)
~~~
ex> " string print" print .
string print
 Data stack empty
ex> 3.14 print .
3.14
 Data stack empty
ex> {'one':1,'two':2} print .
{'one': 1, 'two': 2}
 Data stack empty
ex> ('aaa',111,'bbb',222) print .
('aaa', 111, 'bbb', 222)
 Data stack empty
ex>
~~~
  Each item is printed on a new line; use "printend" with desired separator
if printing on the same line ( item endstr -- ):
~~~
ex> " line 1" print " line 2" print " line 3" print .
line 1
line 2
line 3
 Data stack empty
ex> " line 1" " , " printend " line 2" " , " printend " line 3" print .
line 1, line 2, line 3
 Data stack empty
ex>
~~~
  Use "printnl" to print a single newline
~~~
ex> " line 1" print printnl " line 2" print printnl .
line 1

line 2

 Data stack empty
ex>
~~~
  If you want to print multiple items, use a list:
~~~
ex> p-item: pop " , " printend ;
co> multi-print: dup len i= *p-item iloop ; .
 Data stack empty
ex> [1,'abc','efg',2] multi-print .
2, efg, abc, 1,  Data stack items: 1
[[]]                    # as pop starts from the last item, the 
ex> drop .              # output is last-to-first, so use "reverse"
 Data stack empty
ex> [1,'abc','efg',2] reverse multi-print drop .
1, abc, efg, 2,  Data stack empty
ex>
~~~

  Finally, use "printf" for formatted output; push the format string 
followed by the item to print : ( formatstr item -- ). See user manual 
for all sort of format strings.
NB. There are no f-strings in RPPy
~~~
ex> formdec: " {:d}" ;
co> formcomma: " {:,d}" ;
co> formcentered: " {:^15,d}" ;
co> formpadded: " {:*^15,d}" ;
co> formfloat: " {:*^15.2f}" ;
co> formhex: " {:*>15X}" ; .
 Data stack empty
ex> formdec 9999 printf .
9999
 Data stack empty
ex> formcomma 9999 printf .
9,999
 Data stack empty
ex> formcentered 9999 printf .
     9,999
 Data stack empty
ex> formpadded 9999 printf .
*****9,999*****
 Data stack empty
ex> formfloat 9999 printf .
****9999.00****
 Data stack empty
ex> formhex 65535 printf .
***********FFFF
 Data stack empty
ex>
~~~
  
=== End of chapter 10 ===
 
"""

filetxt = """
    11. File I/O
    ============

  Working with files involves three steps: 
  - open file 
  - read/write from/to file
  - close file
  
  To open a file, push two strings: filename and mode of file use:
( filename filemode -- filehandle ) 
  If only the filename is given, the current file directory is taken
into account; you can also specify a relative or absolute filepath as
C:/main/Python/filename.ext in Windows; do not use backslash as folder 
separator as usually in Windows, as RPPy uses only forward slash here.
  The file mode has following values:
  'r open for reading 
  'w open for writing, truncating the file first
  'x open for exclusive creation, failing if the file already exists
  'a open for writing, appending to the end of file if it exists
  'b binary mode
  't text mode
  '+ open for updating (reading and writing)

~~~
ex> 'testfile.txt 'w open .
 Data stack items: 1
[<_io.TextIOWrapper name='testfile.txt' mode='w' encoding='cp1252'>]
ex>
~~~
  What you get is a file object, called filehandle in RPPy, used in all
consequent operations on this file. 
  Now define a text and write it to testfile.txt:
~~~
ex> filetext: \"""
""> line 1
""> line 2
""> line 3
""> eot
""> \"""
Compile warning: all data after closing triple-quote in current 
line is ignored!
co> ; .
Empty line, nothing to execute
 Data stack items: 1
[<_io.TextIOWrapper name='testfile.txt' mode='w' encoding='cp1252'>]
ex> dup uspush .        # save filehandle to user stack, as it'll 
                        # be needed at close
 Data stack items: 1
[<_io.TextIOWrapper name='testfile.txt' mode='w' encoding='cp1252'>]
ex> filetext .
 Data stack items: 2
[<_io.TextIOWrapper name='testfile.txt' mode='w' encoding='cp1252'>, ' \\nline 1\\nline 2\\nline 3\\neot\\n']
ex> write .             # write needs the filehandle followed by the textstring
                        # to write
 Data stack items: 1
[27]                    # after a succesfull write op, the number of written 
                        # chars is pushed
ex> uspop .             # beware that \\n counts as a single char: newline
 Data stack items: 2
[27, <_io.TextIOWrapper name='testfile.txt' mode='w' encoding='cp1252'>]

ex> close .             # always close file after writing ops, otherwise 
                        # the operating system's buffering algo doesn't 
                        # guarantee instant write; only when exiting RPPy
 Data stack items: 1    # pending writes are executed and all open remainded 
                        # files are automatically closed
[27]                    
ex> drop .
 Data stack empty
ex>
~~~

  Now read the file back and display it:
~~~
ex> 'C:/main/python/testfile.txt 'r open .  # try with absolute path
 Data stack items: 1
[<_io.TextIOWrapper name='C:/main/python/testfile.txt' mode='r' encoding='cp1252'>]
ex> dup uspush .        # save filehandle as needed further by close
 Data stack items: 1
[<_io.TextIOWrapper name='C:/main/python/testfile.txt' mode='r' encoding='cp1252'>]
ex> read .
 Data stack items: 1
[' \\nline 1\\nline 2\\nline 3\\neot\\n']
ex> print .

line 1
line 2
line 3
eot

 Data stack empty
ex> uspop close .
 Data stack empty
ex>
~~~
  NB1. Unfortunately RPPy has no Python-like contextual coding using
  "with", which assures automated file close at end of operations; this
  forces you to manually close files as shown above.
    
  NB2. Open works in RPPy with following keyword arguments frozen:
  buffering=-1, encoding=None, errors=None, newline=None, closefd=True,
  opener=None ; only filename and filemode are taken into account.
  Also modes "r" and "t" which are default on Python, must be specified
  
  NB3. All examples are validated for Windows, working with paths is a 
  little different in Linux and MacOS
  
=== End of chapter 11 ===

"""

jsontxt = """
    12. JSON words
    ==============

  JSON (JavaScript Object Notation) is a lightweight data interchange format 
inspired by JavaScript object literal syntax. Converting between JSON and 
Python objects is done as follows:
  Python        JSON
  ------------------
  dict          object
  list          array
  tuple         array
  str           string
  int,float     number
  True          true
  False         false
  None          null
  
  Convert a Python object to JSON string with "jsdumps" 
  and from JSON back to Python with "jsloads" :
  
~~~
ex> {'Name':'Jeff','age':31} .
 Data stack items: 1
[{'Name': 'Jeff', 'age': 31}]
ex> jsdumps .           # convert a dictionary to JSON
 Data stack items: 1
['{"Name": "Jeff", "age": 31}'] # JSON uses always double quotes
ex> jsloads .           # convert back from JSON
 Data stack items: 1
[{'Name': 'Jeff', 'age': 31}]
ex>
~~~
  Beware that if a key in key:value pair is a number, it 
is converted to a string in JSON, so at reconversion back to
Python dictionary the key remains a string, not number as in the
original dictionary:
~~~
ex> {111:'key1',222:'key2'} update .
 Data stack items: 1
[{'Name': 'Jeff', 'age': 31, 111: 'key1', 222: 'key2'}]
ex> jsdumps .
 Data stack items: 1
['{"Name": "Jeff", "age": 31, "111": "key1", "222": "key2"}']
ex> jsloads .           # the keys 111 and 222 are strings now
 Data stack items: 1
[{'Name': 'Jeff', 'age': 31, '111': 'key1', '222': 'key2'}]
ex>
~~~

  Similar to jsdumps and jsloads there are:
  jsdump ( filename pyobj -- ) write Python object as JSON object
                               to filename
  jsload ( filename -- pyobj ) load JSON object as Python object
                               from filename

~~~
ex> cleards
ex>
 Data stack empty
ex> 'testjs.jss {'Monday':1,'Tuesday':2} jsdump .
 Data stack empty
ex> 'testjs.jss jsload .
 Data stack items: 1
[{'Monday': 1, 'Tuesday': 2}]
ex>
~~~

  All following parameters, except filename and object/string 
are frozen in RPPy:
  jsload/jsloads:
(cls=None, object_hook=None, parse_float=None, parse_int=None, 
parse_constant=None, object_pairs_hook=None)
  jsdump/jsdumps:
(skipkeys=False, ensure_ascii=True, check_circular=True, 
allow_nan=True, cls=None, indent=None, separators=None, 
default=None, sort_keys=False)
  
=== End of chapter 12 ===

"""
misctxt = """
    13. Miscellaneous words
    =======================

   - abort ( str -- ) print abort message str, switch to REPL
   Useful to abort execution if a certain condition is not 
   satisfied:
~~~
ex> testneg:  <0 if " negative value not allowed" abort
co> then " value ok" print drop ; .
 Data stack empty
ex> 33 testneg .
value ok
 Data stack empty
ex> -33 testneg .
User Abort
"abort" aborted: negative value not allowed
 Aborted at Execution List Index:  6
 In definition: "testneg" at index: 2
  TOS:  <class 'int'> -33
 Return stack items:1
1 return from: testneg
 Data stack items: 1
[-33]
ex>
~~~

  - all ( seq -- ) ZF=1 if all elements in seq are true or seq is empty
~~~
ex> testall: all if " all elements are true or empty sequence" print ;
co> then " at least one element is false" print ; .
 Data stack empty
ex> [1,2,3,4] testall .
all elements are true or empty sequence
 Data stack empty
ex> emptystr testall .
all elements are true or empty sequence
 Data stack empty
ex> [] testall .
all elements are true or empty sequence
 Data stack empty
ex> [1,2,0,4] testall .
at least one element is false
 Data stack empty
ex>
~~~

  - any ( seq -- ) ZF=1 if any element in seq is true; ZF=0 if seq is empty
~~~
ex> testany: any if " at least one element is true" print ;
co> then " sequence is empty" print ; .
 Data stack empty
ex> [1,0,3,0] testany .
at least one element is true
 Data stack empty
ex> [] testany .
sequence is empty
 Data stack empty
ex>
~~~

  - bin ( n -- strbin ) convert integer n to binary string
~~~
ex> 255 bin print .
0b11111111
 Data stack empty
ex>
~~~

  - chr ( n -- strchr ) convert integer n to string representing associated glyph
~~~
ex> 65 chr print .
A
 Data stack empty
ex> 17 chr print .
◄
 Data stack empty
ex> 17 chr .
 Data stack items: 1
['\x11']
ex>
~~~

  - complex ( str -- n ) convert str to complex number n
~~~
ex> '11+22j complex .
 Data stack items: 1
[(11+22j)]
ex> '33 complex .
 Data stack items: 2
[(11+22j), (33+0j)]
ex> '44j complex .
 Data stack items: 3
[(11+22j), (33+0j), 44j]
ex>
~~~

  - choose ( idx1 idx2 -- ) if ZF=1 execute word with idx1, else idx2
  See "Control Flow"
  
  - enumerate ( seq -- list ) list of tuples (count,value) iterating over seq
~~~
ex> 'abcd enumerate .
 Data stack items: 1
[[(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd')]]
ex>
~~~
~~~
ex> {'Fred':32,'Anna':24,'Gregory':40} enumerate .
 Data stack items: 1
[[(0, 'Fred'), (1, 'Anna'), (2, 'Gregory')]]
ex>
~~~

  - eval ( str -- item ) TOS = eval(str) 
~~~
ex> " (10 + 20) * 3 / 2" eval .
 Data stack items: 1
[45.0]
ex> (10+20)*3/2 .       # if no spaces, the same expression, without
 Data stack items: 2    # string and eval, is evaluated as above, but
[45.0, 45.0]            # here you must use INFIX notation, with regard
ex> 10 20 + 3 * 2 / .   # to Python's precedence rules
 Data stack items: 3    # ... and now in postfix 
[45.0, 45.0, 45.0]
ex> 2 3 10 20 + * swap / .
 Data stack items: 4
[45.0, 45.0, 45.0, 45.0]
ex>
~~~
  NB. RPPy uses Python's eval as input in the Read-Eval-Print-Loop, par 
  consequence any valid Python expression containing only number/string values
  can be evaluated, using infix notation and known precedence rules. But using
  variables, as in Python, doesn't work, a=10; b=20; eval("a+b") is a valid 
  Python expression and a rejected RPPy one:
~~~
ex> a: 10 ;
co> b: 20 ; .
 Data stack empty
ex> " a+b" eval .
"eval" aborted: name 'a' is not defined
 Aborted at Execution List Index:  48
 Aborted in execution string or in definition with multiple returns
  TOS:  <class 'str'> a+b
 Data stack items: 1
['a+b']
ex>
~~~
  The variable "a" is defined as a word, not as a Python variable, 
  so it is not visible to the eval function. But you can define 
  Python variables, see "exec"
  
  - exec ( str -- ... ) exec(str), stack depends of what exec does
~~~
ex> pyvar: \"""
""> a=10
""> b=20
""> c=eval("a+b")
""> print("Executed as Python statements")
""> print("c=",c)
""> \"""
Compile warning: all data after closing triple-quote in current line is ignored!
co> ; .
 Data stack empty
ex> pyvar exec .
Executed as Python statements
c= 30
 Data stack empty
ex>
~~~
  Exec is a useful word if you want to extend the capabilities of RPPy;
  see more on this in "Extending RPPy".
  
  - execidx ( idx -- ) execute word with index idx
~~~
ex> exidx: " exidx executed with index: " "  " printend print ;
co> testidx: *exidx dup execidx ; .
 Data stack empty
ex> testidx .
exidx executed with index:  53
 Data stack empty
ex> 'exidx pdef .
  exidx       at index:  53 ""  ""
  exidx: " exidx executed with index: " "  " printend print ;

  No duplicate (older definitions) present
 Data stack empty
ex>
~~~

  - float ( str/int -- n ) convert string or integer to floating point number
~~~
ex> " 3.151596 " float .
 Data stack items: 1
[3.151596]
ex> 99 float .
 Data stack items: 2
[3.151596, 99.0]
ex>
~~~

  - format ( formstr n  -- str ) convert value n to str according to formstr
~~~
ex> '{:*^10.3f} 99 format .
 Data stack items: 1
['**99.000**']
ex>
~~~
  See more format string examples in "Input and printing" for "printf"
  
  - help ( -- ) print help chapters
  
  - hex ( n -- strhex ) convert integer n to hexadecimal string
~~~
ex> 65535 hex .
 Data stack items: 1
['0xffff']
ex>
~~~

  - input ( -- str ) read a line from input and convert data to a string
  See "Input and printing"
  
  - inputprompt ( strprompt -- str ) write strprompt to standard output,
  then read a line
  See "Input and printing"
  
  - int ( str/n -- n ) convert str or number n to integer n
~~~
ex> 3.14 int .
 Data stack items: 1
[3]
ex> " 99" int .
 Data stack items: 2
[3, 99]
ex>
~~~

  - intbase ( str base -- n ) convert str to integer n according to base
~~~
ex> '999 10 intbase .
 Data stack items: 1
[999]
ex> 'ffff 16 intbase .
 Data stack items: 2
[999, 65535]
ex> '1100 2 intbase .
 Data stack items: 3
[999, 65535, 12]
ex> 'abcd 36 intbase .
 Data stack items: 4
[999, 65535, 12, 481261]
ex>
~~~

  - intro ( -- ) print introduction to RPPy
  
  - license ( -- ) print RPPy license
  
  - oct ( n -- stroct ) convert integer n to octal string
~~~
ex> 63 oct .
 Data stack items: 1
['0o77']
ex> 64 oct .
 Data stack items: 2
['0o77', '0o100']
ex>
~~~

  - ord ( strchr -- n ) convert string representing one character to integer n
~~~
ex> 'A ord .
 Data stack items: 1
[65]
ex> 'a ord .
 Data stack items: 2
[65, 97]
ex> "  " ord .
 Data stack items: 3
[65, 97, 32]
ex>
~~~

  - quit ( ... -- ... ) end execution of RPPy
  Works similarly to Ctrl-Q, asking for definitions to save, to prevent 
  accidentally loosing what has been defined in a work session.
  
  - str ( item -- str ) return a string interpretation of item
~~~
ex> 99.998 str .
 Data stack items: 1
['99.998']
ex> [1,'abcd',2] str .
 Data stack items: 2
['99.998', "[1, 'abcd', 2]"]
ex>
~~~

 - type ( item -- itemtype ) TOS = type of item
~~~
ex> {} type .
 Data stack items: 1
[<class 'dict'>]
ex> (11+22j) type .
 Data stack items: 2
[<class 'dict'>, <class 'complex'>]
ex> (1,2,3) type .
 Data stack items: 3
[<class 'dict'>, <class 'complex'>, <class 'tuple'>]
ex> {1,2,3} type .
 Data stack items: 4
[<class 'dict'>, <class 'complex'>, <class 'tuple'>, <class 'set'>]
ex> [1,2,3] type .
 Data stack items: 5
[<class 'dict'>, <class 'complex'>, <class 'tuple'>, <class 'set'>, <class 'list'>]
ex>
~~~
  
=== End of chapter 13 ===
"""
editloadsavetxt = """
    14. Editing, saving and loading definitions
    ===========================================
  
  There are two types of words in RPPy:
- kernel primitives written in Python
- high level words written as a combination of kernel 
primitives and other already defined high level words.
  The kernel primitives are the equivalent of Python's 
built-in functions/methods; adding/modifying them can be 
done only by changing the RPPy script at source level.
  Each time RPPy is launched, only the kernel primitives
are available for use; the user has to create his own 
definitions, saving them for further reuse/completion.

  Saving definitions is done by:
  - save ( filename -- ) save RPPy user generated words to filename
  The filename must be without extension, as RPPy
adds ".rpp" as extension; you can use absolute or relative path 
with filename, otherwise if only the name is given the file is created
in the current directory.
  - Ctrl-S or s. ( -- ) save RPPy user generated words to file "tempsave.rpp"
  The file "tempsave.rpp" is always created in the current directory;
also Ctrl-S has to be pressed only at start of line input. Use "s." as an 
alternative where Ctrl-S poses problems.

  Loading definitions is done by:
  - load ( filename -- ) load RPPy user generated words from filename
  As with "save", the filename must be without extension, as 
only files of type .rpp are recognized.
  Loading always overwrites all existing definitions, if any, there's no
concept of overlays in RPPy. You start at beginning with an empty dictionary,
then create a first set of definitions; save them, and from now on, at each
working session load them first and continue adding other definitions until
finishing the application.
  A very important issue about variables (which are also definitions): at 
save, always their LAST VALUE is written on file, from this point of view 
RPPy works like a spreadsheet: what you have in the cells at saving will be 
retrieved at next loading. Problems could arise if, as example, a variable 
is used to initialise a loop index and incremented afterwards; it'll be saved
with the last count and not the starting one, so at next reloading the loop 
goes awry...
~~~
ex> pdefall .

 High Level Dictionary Definitions:  0
 Data stack empty
ex> w1: " first def" print ;
co> w2: " second def" print ;
co> w3: " third def" print ; .
 Data stack empty
ex> 'c:/main/python/test-save-load save . # do not use "\\" even on Windows path
Saved: 3 definitions to c:/main/python/test-save-load.rpp
 Data stack empty
ex> w4: 444 ;
co> w5: 555 ; .
 Data stack empty
ex> pdefall .
  w1          at index:  2 ""  ""
  w2          at index:  6 ""  ""
  w3          at index:  10 ""  ""
  w4          at index:  14 ""  ""
  w5          at index:  17 ""  ""

 High Level Dictionary Definitions:  5
 Data stack empty
ex> ^Q
Saved only 3 definitions from a total of 5
Quit anyway? (y/n):n
 Data stack empty
ex> ^S
Saved: 5 definitions to tempsave.rpp
 Data stack empty
~~~

  - deldef ( defname -- ) delete definition defname
~~~
ex> 'w1 deldef 'w2 deldef .
"w1" at index 2 deleted
"w2" at index 6 deleted
 Data stack empty
ex> pdefall .
  w3          at index:  10 ""  ""
  w4          at index:  14 ""  ""
  w5          at index:  17 ""  ""

 High Level Dictionary Definitions:  3
 Data stack empty
ex> 'c:/main/python/test-save-load load .
! Warning: all current definitions will be lost - proceed? (y/n): y
  Definitions loaded:
    0 w1
    1 w2
    2 w3
 Data stack empty
ex> pdefall .
  w1          at index:  2 ""  ""
  w2          at index:  6 ""  ""
  w3          at index:  10 ""  ""

 High Level Dictionary Definitions:  3
 Data stack empty
ex> 'tempsave load .
! Warning: all current definitions will be lost - proceed? (y/n): y
  Definitions loaded:
    0 w1
    1 w2
    2 w3
    3 w4
    4 w5
 Data stack empty
ex> pdefall .
  w1          at index:  2 ""  ""
  w2          at index:  6 ""  ""
  w3          at index:  10 ""  ""
  w4          at index:  14 ""  ""
  w5          at index:  17 ""  ""

 High Level Dictionary Definitions:  5
 Data stack empty
ex> ^Q
RPPy ended; last saved: 5 definitions
~~~

  Editing a definition is done by:
  - edit ( defname -- ) edit definition defname
~~~
ex> w1: " Hello!" print ;
co> w2: w1 " How are you?" print ;
co> w3: w1 " Glad to see you" print ; .
 Data stack empty
ex> w2 .
Hello!
How are you?
 Data stack empty
ex> w3 .
Hello!
Glad to see you
 Data stack empty
ex> 'w1 edit .
  Warning: works only in Windows Command Prompt !
   Type Ctrl-M, cursor changes shape
   Use arrow keys to move cursor at beginning of displayed definition
   Hold Shift pressed, move right arrow to select entire definition
   Type Ctrl-Insert to copy selected text to clipboard, cursor moves back to input line
   Type Ctrl-V to paste clipboard to input line
   Edit input line , terminate as usually with "." plus Enter
  w1          at index:  2 ""  ""
  w1: " Hello!" print ;

  No duplicate (older definitions) present
 Data stack empty
ex> w1: " Hello dear user!" print ; .  # new variant of w1
Empty line, nothing to execute
 Data stack empty
ex> w4: w1 " Good bye!" print ; .      # w4 uses the new w1 variant
 Data stack empty                      # because w4 is defined after new w1
ex> w4 .
Hello dear user!
Good bye!
 Data stack empty
ex> w2 .                # w2 and similarly w3 retain the old variant of w1
Hello!                  # if all occurencies of w1 should be replaced, use
How are you?            # repdef
 Data stack empty
~~~

  - repdef ( defname -- ) replace old definitions of defname with the last one defined
~~~
ex> 'w1 repdef .
  Replacing 1 older definitions
  Replaced in 2 definitions
 Data stack empty
ex> w2 .                # now all words use the last variant of w1
Hello dear user!
How are you?
 Data stack empty
ex> w3 .
Hello dear user!
Glad to see you
 Data stack empty
ex> w4 .
Hello dear user!
Good bye!
 Data stack empty
ex>
~~~

  - refdef ( defname -- list ) list of all definitions including a reference to defname
~~~
ex> 'w1 refdef .
 Data stack items: 1
[['w2', 'w3', 'w4']]
ex>
~~~
  
=== End of chapter 14 ===
 
"""

extendtxt = """
    15. Extending RPPy
    ==================

  Using "exec" you can extend the functionalities of RPPy:  
  - exec ( str -- ... ) exec(str), stack depends of what exec does
  
  If for example you want to calculate the square root of a number,
you can define a word which imports the math module:
~~~
ex> sqbase: \"""         # define a multiline string including all
""> import math         # desired Python statements to be executed
""> if tos() < 0 :
"">     print('Negative number')
""> else:
"">     dpush(math.sqrt(dpop()))
""> \"""
Compile warning: all data after closing triple-quote in current line is ignored!
co> ; .
 Data stack empty
ex> sqrt: "" ( n -- sqrt(n))""
co> sqbase exec ; .
 Data stack empty
ex> 144 sqrt .
 Data stack items: 1
[12.0]
ex> -144 sqrt .
Negative number
 Data stack items: 2
[12.0, -144]
ex>
~~~
  But you need to know a little bit of RPPy internals to interface it
with Python:
  - use "dpush( xxx )" to push data on the data stack
  - use "dpop()" to pop data from the data stack
  - use "tos()" and "nos()" if you want to test values on TOS & NOS
  without discarding them
  - use pkern to get the names of kernel primitives associated functions,
  the so-called eXecutionTokens "XT", for stack manipulation or other
  functions: 
    - k_dup() to duplicate TOS
    - k_swap() to exchange TOS with NOS
	...
  
~~~
ex> getcwd: \"""         # define a word to get the current working directory
""> import os
""> print(os.getcwd())
""> \"""
Compile warning: all data after closing triple-quote in current line is ignored!
co> ; .
ex> cwd: getcwd exec ; .
 Data stack empty
ex> cwd .
c:\\main\\Python
 Data stack empty
ex>
~~~

  An useful word to list the content of a given directory:
~~~
ex> getdir: \"""
""> import os
""> dpush(os.listdir(path=tos()))
""> \"""
Compile warning: all data after closing triple-quote in current line is ignored!
co> ; .
 Data stack empty
ex> dir: getdir exec plist ; .
 Data stack empty
ex> 'c:/main/Python/advancedrpn dir .
   0 calculator.py
   1 main1.py
   2 pycalc.py
   3 settings.json
   4 __init1__.py
   5 __main__.py
   6 __pycache__
 Data stack items: 1
['c:/main/Python/advancedrpn']
ex>
~~~
  It's up to you to add testing of valid input...otherwise you 
risk to be aborted by Python with a traceback and loose all your
work (if you were not smart enough to save it before experimenting...):
~~~
ex> 'c:/main/Python/zzzzzzz dir .
Traceback (most recent call last):
  File "c:\\main\\Python\\rppy.py", line 4318, in <module>
    NEXT()
  File "c:\\main\\Python\\rppy.py", line 430, in NEXT
    exec(ExecList[IP][CFA])
  File "<string>", line 1, in <module>
  File "c:\\main\\Python\\rppy.py", line 4043, in k_exec
    exec(dpop())
  File "<string>", line 3, in <module>
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'c:/main/Python/zzzzzzz'
~~~
  And all your data is lost ...
  To avoid such mishap, use the well known pair try-except:
~~~
ex> getdir: \"""
""> import os
""> try:
"">     dpush(os.listdir(path=tos()))
""> except(AttributeError,TypeError,OSError) as e:
"">     abort(str(e))
""> \"""
Compile warning: all data after closing triple-quote in current line is ignored!
co> ; .
 Data stack empty
ex> dir: getdir exec plist ; .
 Data stack empty
ex> 'c:/main/Python/zzzzzzz dir .
"exec" aborted: [WinError 3] The system cannot find the path specified: 'c:/main/Python/zzzzzzz'
 Aborted at Execution List Index:  7
 In definition: "dir" at index: 5
  TOS:  <class 'str'> c:/main/Python/zzzzzzz
 Return stack items:1
1 return from: dir
 Data stack items: 1
['c:/main/Python/zzzzzzz']
ex>
~~~
  Now the error is catched inside RPPy, continue working in all tranquility...
  
  And a last example, to print today's date:
~~~
ex> getdate: \"""
""> import datetime as dt
""> dpush(dt.date.today())
""> \"""
Compile warning: all data after closing triple-quote in current line is ignored!
co> ; .
 Data stack empty
ex> date: getdate exec print ; .
 Data stack empty
ex> date .
2024-11-17
 Data stack empty
ex>
~~~
=== End of chapter 15 ===

"""

errortxt = """
    16. Error handling
    ==================
	
  Generally speaking, there are three kinds of errors encountered:
  
- compile errors:
  - unknown word
  - definition doesn't start at input line beginning
  - unmatched pairs if-then
  - absence of closing markers for strings
  - wrong syntax in expressions (strings without blanks as input to evaluate
    by RPPy or "eval")
  What's important to know: compiling is done all time around, not only at 
  defining a new word; RPPy ALWAYS generates compiled code, which, if not 
  used in a definition, is discarded after execution. So don't be surprised 
  if it says "compile error xxx" even if the input prompt is "ex> "
  
- runtime errors:
  - mostly these are of two kind: 
    - missing arguments 
	- wrong argument type
	
- semantic errors:
  - no error is signalled, but the output is not what was expected.
  Hard to debug, try avoiding them by thoroughly testing every new 
  definition before it's included in the next ones. Include a data 
  stack printing "pds" at word start and before return, where you
  guess it may be a problem; later on you can remove it by redefining
  that word. But generally, as said multiple times before, define 
  short words, less than 2 or 3 lines long. It's much easier to make 
  them work as expected, compared to a maze of imbricated comparisons,
  loops and branches in a n-lines huge definition.
  
  Now, specific for RPPy as opposed to Python, an error doesn't abruptly
end your program with a traceback; instead you continue to write corrected
data/words from where on the error was detected, no matter if inside or 
outside a definition. Let's see concrete examples:
~~~
ex> 20 45 swap - 33 xx 44 * .
Compile error: name 'xx' is not defined in expression: xx
 Undefined: "xx"
ex>                     # all part before xx is executed
 Data stack items: 2    # 20 45 swap - is 25 , then 33 pushed
[25, 33]                # but all part after xx is not executed
ex>
~~~
  Continue from where the error appeared:
~~~
ex> + 44 * .
 Data stack items: 1
[2552]
ex>
~~~
~~~
ex> 22 33 add 99 print .
"add" aborted: First argument for "add" must be a set
 Aborted at Execution List Index:  33
 Aborted in execution string or in definition with multiple returns
  TOS:  <class 'int'> 33
  NOS:  <class 'int'> 22
 Data stack items: 2
[22, 33]
ex>
~~~
  Same as before: 22 and 33 pushed on the stack, but 99 print ignored,
therefore get correct arguments for add, then do the rest.
  As a rule of thumb, get assured that the stack contains valid data
before continuing input after error point.

  Correcting errors inside definitions obeys the same rule; you simply
continue with the corrected part:
~~~
ex> baddef: 11 22 swax 33 + ; .
Compile error: name 'swax' is not defined in expression: swax
 Undefined: "swax"
co> swap 33 + ; .       # RPPy remains in compile mode, so you can
 Data stack empty       # continue with corrected data
ex> 'baddef pdef .
  baddef      at index:  2 ""  ""
  baddef: 11 22 swap 33 + ; # corrected def 

  No duplicate (older definitions) present
 Data stack empty
ex>
~~~
  NB. There's no need to start again from the beginning with the 
  definition, continue it as said before.
  
  A runtime error example:
~~~
ex> zdiv: 0 / ; .
 Data stack empty
ex> aa: 99 zdiv ; .
 Data stack empty
ex> aa .
"/" aborted: division by zero
 Aborted at Execution List Index:  16
 In definition: "zdiv" at index: 14
  TOS:  <class 'int'> 0
  NOS:  <class 'int'> 99
 Return stack items:1
1 return from: aa
 Data stack items: 2
[99, 0]
ex> 14 pexlst .         # see where the error appears
   14 zdiv:
   15 lit  0            # wrong data in zdiv
   16 /
   17 ;
   18 aa:
   19 lit  99
   20 jump zdiv
   21 call aa
   22 lit  14
   23 pexlst
 Data stack items: 2
[99, 0]
ex>
~~~
  Here execution of your words stops and control is returned to the 
  Read-Eval-Print-Loop of RPPy; unfortunately there's no traceback,
  only the faulty word appears in the abort message.

=== End of chapter 16 ===

"""

lsttxt = [usingtxt,datamanagtxt,constvartxt,numberstxt,stringstxt,\
liststxt,dictiotxt,tupsettxt,controltxt,inputprinttxt,filetxt,\
jsontxt,misctxt,editloadsavetxt,extendtxt,errortxt]

def phelp(txt):
    listtxt = txt.splitlines(keepends=False)
    for i in range(len(listtxt)):
        print(listtxt[i])
        if i%20 == 0 and i != 0 :
            s=input('More>-------------------v')
            if len(s) != 0 :
                return
        i += 1
    return
    
def k_intro():
    phelp(introtxt)
    return
    
def k_help():
    
    print("  1 - Using RPPy")
    print("  2 - Data stack management")
    print("  3 - Constants, variables, assignment operations")
    print("  4 - Basic Datatypes - Numbers")
    print("  5 - Basic Datatypes - Strings")
    print("  6 - Basic Datatypes - Lists")
    print("  7 - Basic Datatypes - Dictionaries")
    print("  8 - Basic Datatypes - Tuples, Sets")
    print("  9 - Control flow")
    print(" 10 - Input and printing")
    print(" 11 - File I/O")
    print(" 12 - JSON words")
    print(" 13 - Miscellaneous words")
    print(" 14 - Editing, saving and loading definitions")
    print(" 15 - Extending RPPy")
    print(" 16 - Error handling")
    s=input(" Enter your choice: ")
    if len(s) == 0 :
        return
    elif not s.isdigit() or int(s) not in range(1,len(lsttxt)+1) :
        print("Value out of range or not a number")
        return
    else:
        phelp(lsttxt[int(s)-1])
    return
    
#====
# EOP
#====