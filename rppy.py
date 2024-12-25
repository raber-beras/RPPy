#!/usr/bin/env python3
#
# copyright (C) 2024 Radu BERINDEANU
# distributed under the ISC License www.isc.org/licenses
#
# maintainer raberpy4@outlook.com
#
#
veryy = 24      # version year
vermm = 11      # version month
#
#============================
# import area
import json
import helprppy as h
#
#============================
#   Description of the RPPy VM (Virtual Machine) & associated dictionaries
#============================
#
#   Stacks: data, return & user 
#
dstack = [] # Data Stack: holds any objects ( int, float, string, list, dictionary, tuple, set ) used
#           by the words as they execute: getting input args from the stack and leaving output values
#           for the next word to get
#           Direct accessible by user
#
rstack = [0] # Return Stack: holds continuations (return pointers) for word calls
#           Not user accessible
#
ustack = [] # User Stack: self explanatory; holds any objects; helps avoiding locals in words
#
#============================
#
#   Registers
#
#============================
#
TOS = 0         # holds top of stack ; scratch use
NOS = 0         # holds next of stack ; scratch use

ZF = 0          # zero flag register, set by comparisons ; 1 == True , 0 == False or None
I = 0           # index register I - all index regs are used in counted loops and slices
J = 0           # index register J
K = 0           # index register K
#
#============================
#
#   Kernel words (primitives) dictionary
#       - pairs of key:value , where:
#           - key = name of RPPY word
#           - value = name of associated executable python code function & stack effect
#
KernDef = {
# Data Stack words
            '###1':         ['k_pass()','  ===Data Stack words==='],
            'dup':          ['k_dup()','( n -- n n ) duplicate TOS'],
            '2dup':         ['k_ddup()','( x y -- x y x y ) duplicate NOS and TOS'],
            'drop':         ['k_drop()','( n -- ) drop TOS'],
            '2drop':        ['k_ddrop()','( x y -- ) drop TOS and NOS'],
            'swap':         ['k_swap()','( x y -- y x ) exchange TOS with NOS'],
            'over':         ['k_over()','( x y -- x y x ) copy NOS over TOS'],
            'nip':          ['k_nip()','( x y -- y ) drop NOS'],
            'tuck':         ['k_tuck()','( x y -- y x y ) insert TOS before NOS'],
            'rot':          ['k_rot()','( x y z -- y z x ) rotate rightwise top three items'],
            '-rot':         ['k_rotl()','( x y z -- z x y ) rotate leftwise top three items'],
            'pick':         ['k_pick()','( xn xn-1 xn-2 ... x0 n -- xn xn-1 xn-2 ... x0 xn ) replace TOS with a copy of the n-th item'],
            'cleards':      ['k_clrdstk()','( ... -- ) empty data stack'],
# User Stack words
            '###2':         ['k_pass()','  ===User Stack words==='],
            'uspush':       ['k_uspush()','( n -- ) data stack | ( -- n ) user stack ; push TOS to user stack'],
            'uspop':        ['k_uspop()','( -- n ) data stack | ( n -- ) user stack ; pop TOS of user stack & push to data stack'],
            'clearus':      ['k_clrustk()','( ... -- ) empty user stack'],
# Math words
            '###3':         ['k_pass()','  ===Math words==='],
            '+':            ['k_plus()','( x y -- x+y ) add TOS to NOS'],
            '-':            ['k_minus()','( x y -- x-y ) subtract TOS from NOS'],
            '*':            ['k_star()','( x y -- x*y ) multiply TOS by NOS'],
            '/':            ['k_slash()','( x y -- x/y ) divide NOS by TOS - floating point div'],
            '//':           ['k_dblslash()','( x y -- x//y ) divide NOS by TOS - floored (integer) div'],
            '%':            ['k_rem()','( x y -- rem ) remainder of x/y division'],
            'divmod':       ['k_divmod()','( x y -- quot rem ) quotient & remainder of x/y division'],
            '**':           ['k_dblstar()','( x y -- x**y ) NOS at power of TOS'],
            '++':           ['k_plusone()','( n -- n+1 ) increment TOS by 1'],
            '--':           ['k_minusone()','( n -- n-1 ) decrement TOS by 1'],
            'neg':          ['k_negate()','( n -- neg(n) ) negate n'],
            'abs':          ['k_abs()','( x -- abs(x) ) absolute value of x'],
            'round':        ['k_round()','( n i -- round(n))  n rounded to i digits'],
            'min':          ['k_min()','( seq -- min(seq) ) minimum of values in sequence seq'],
            'max':          ['k_max()','( seq -- max(seq) ) maximum of values in sequence seq'],
            'sum':          ['k_sum()','( seq -- sum(seq) ) sum of  items in sequence seq'],
            'val+':         ['k_sumval()','( n1 n2 ... ni i -- sum(ni) ) sum of top i values, i >= 1'],
            'val*':         ['k_mulval()','( n1 n2 ... ni i -- product(ni) ) product of top i values, i >= 1'],
            'str+':         ['k_sumstr()','( str1 str2 ... stri i -- str ) concatenate top i strings, i >= 1'],
            'lst+':         ['k_sumlst()','( list1 list2 ... listi i -- list ) concatenate top i lists, i >=1'],
# Comparison words
            '###4':         ['k_pass()','  ===Comparison words==='],
            '<':            ['k_le()','( x y -- x y ) ZF = 1 if x<y'],
            '>':            ['k_gt()','( x y -- x y ) ZF = 1 if x>y'],
            '<=':           ['k_leeq()','( x y -- x y ) ZF = 1 if x<=y'],
            '>=':           ['k_gteq()','( x y -- x y ) ZF = 1 if x>=y'],
            '==':           ['k_eq()','( x y -- x y ) ZF = 1 if x==y'],
            '!=':           ['k_neq()','( x y -- x y ) ZF = 1 if x!=y'],
            '<0':           ['k_zle()','( n -- n ) ZF = 1 if n < 0'],
            '>0':           ['k_zgt()','( n -- n ) ZF = 1 if n > 0'],
            '=0':           ['k_zeq()','( n -- n ) ZF = 1 if n == 0'],
            '!=0':          ['k_zneq()','( n -- n ) ZF = 1 if n != 0'],
            '<0>':          ['k_lesszeq()','( idx1 idx2 idx3 n -- ) if n<0 execute word with idx1; if n=0 execute idx2; else idx3'],
            '<=>':          ['k_lesseqgt()','( idx1 idx2 idx3 x y -- ) if x<y execute word with idx1; if x=y execute idx2, else idx3'],
            'zf=':          ['k_setZF()','( n -- ) pop TOS to ZF'],
            'zf':           ['k_ZF()','( -- ZF ) push ZF'],
            'in':           ['k_in()','( seq item -- seq item ) ZF = 1 if item found in sequence'],
            'notin':        ['k_notin()','( seq item -- seq item ) ZF = 1 if item not found in sequence'],
            'is':           ['k_is()','(item1 item2 -- item1 item2 ) ZF = 1 if item1 and item2 are the same object'],
            'isnot':        ['k_isnot()','(item1 item2 -- item1 item2 ) ZF = 1 if item1 and item2 are not the same object'],
# Logical words
            '###5':         ['k_pass()','  ===Logical words==='],
            'and':          ['k_and()','( x y -- x y ) ZF = 1 if both x and y are True'],
            'or':           ['k_or()','( x y -- x y ) ZF = 1 if either x or y or both are True'],
            'xor':          ['k_xor()','( x y -- x y ) ZF = 1 if either (x is True and y is False) or (x is False and y is True)'],
            'not':          ['k_not()','( n -- n ) ZF = 1 if n is False or None'],
            '-not':         ['k_notnot()','( n -- n ) ZF = 1 if n is True'],
# Bitwise words
            '###6':         ['k_pass()','  ===Bitwise words==='],
            '&':            ['k_bitand()','( x y -- x&y ) bitwise and'],
            '|':            ['k_bitor()','( x y -- x|y ) bitwise or'],
            '^':            ['k_bitxor()','( x y -- x^y ) bitwise exclusive or'],
            '~':            ['k_bitcompl()','( n -- ~n ) one\'s complement'],
            '<<':           ['k_lshift()','( n i -- n ) shift left n by i bits'],
            '>>':           ['k_rshift()','( n i -- n ) shift right n by i bits'],
# Assignment words
            '###7':         ['k_pass()','  ===Assignment words==='],
            '=':            ['k_store()','( n idx -- ) store n to var[idx]: variable with index idx'],
            '+=':           ['k_plusstore()','( n idx -- ) var[idx] += n'],
            '-=':           ['k_minusstore()','( n idx -- ) var[idx] -= n'],
            '*=':           ['k_starstore()','( n idx -- ) var[idx] *= n'],
            '/=':           ['k_slashstore()','( n idx -- ) var[idx] /= n'],
            '//=':          ['k_dblslashstore()','( n idx -- ) var[idx] //= n'],
            '%=':           ['k_remstore()','( n idx -- ) var[idx] %= n'],
            '**=':          ['k_dblstarstore()','( n idx -- ) var[idx] **= n'],
# Index register words
            '###8':         ['k_pass()','  ===Index Register words==='],
            'i=':           ['k_setI()','( n -- ) pop TOS to I'],
            'i':            ['k_I()','( -- I ) push I'],
            'i++':          ['k_incI()','( -- ) I += 1'],
            'i--':          ['k_decI()','( -- ) I -= 1'],
            'j=':           ['k_setJ()','( n -- ) pop TOS to J'],
            'j':            ['k_J()','( -- J ) push J'],
            'j++':          ['k_incJ()','( -- ) J += 1'],
            'j--':          ['k_decJ()','( -- ) J -= 1'],
            'k=':           ['k_setK()','( n -- ) pop TOS to K'],
            'k':            ['k_K()','( -- K ) push K'],
            'k++':          ['k_incK()','( -- ) K += 1'],
            'k--':          ['k_decK()','( -- ) K -= 1'],
            'iloop':        ['k_Iloop()','( idx -- ) execute word with index idx I times'],
            'jloop':        ['k_Jloop()','( idx -- ) execute word with index idx J times'],
            'kloop':        ['k_Kloop()','( idx -- ) execute word with index idx K times'],
# Printer words
            '###9':         ['k_pass()','  ===Printer words==='],
            'pds':          ['k_pds()','( -- ) print data stack'],
            'pdson':        ['k_pdson()','( -- ) switch data stack print to ON'],
            'pdsoff':       ['k_pdsoff()','( -- ) switch data stack print to OFF'],
            'pus':          ['k_pus()','( -- ) print user stack'],
            'prs':          ['k_prs()','( -- ) print return stack'],
            'pdefall':      ['k_pdefall()','( -- ) print all definitions dictionary'],
            'pdef':         ['k_pddef()','( defname -- ) print a definition'],
            'pkernall':     ['k_pkerndefall()','( -- ) print all kernel primitives dictionary'],
            'pkern':        ['k_pkerndef()','( -- ) print kernel primitives per category'],
            'pexlst':       ['k_pexlst()','( idx -- ) print execution list starting with index idx'],
            'plist':        ['k_plist()','( list -- ) print list as enumerated items'],
            'pcomp':        ['k_pcompdef()','( -- ) print compiler definitions dictionary'],
            'print':        ['k_print()','( item -- ) print item'],
            'printf':       ['k_printf()','( formatstr n -- ) print n according to format string'],
            'printnl':      ['k_printnl()','( -- ) print newline'],
            'printend':     ['k_printend()','( item endstr -- ) print item followed by end string'],
# List words
            '###10':        ['k_pass()','  ===List words==='],
            'list':         ['k_list()','( str -- list ) create list from str '],
            'listcre':      ['k_listcre()','( "[]" item1 item2 ... itemn -- list ) create list of items'],
            'listexp':      ['k_listexp()','( list -- item1 item2 ... itemn ) expand list of items'],
            'append':       ['k_append()','( list item -- list ) append item to list'],
            'clear':        ['k_clear()','( list -- [] ) clear list'],
            'copy':         ['k_copy()','( list -- list listcopy) return original and shallow copy of list'],
            'count':        ['k_count()','( list value -- n ) count instances of value in list'],
            'extend':       ['k_extend()','( list iterable -- list ) extend list with iterable'],
            'index':        ['k_index()','( list item -- index ) return index of item in list'],
            'insert':       ['k_insert()','( list index item -- list ) insert item before index in list'],
            'len':          ['k_len()','( list -- n ) return lenght of list'],
            'pop':          ['k_pop()','( list -- list item ) pop last item from list'],
            'popidx':       ['k_popidx()','( list index -- list item ) pop item at index in list'],
            'remove':       ['k_remove()','( list index -- list ) remove item at index in list'],
            'reverse':      ['k_reverse()','( list -- list ) reverse list in place'],
            'sortasc':      ['k_sortasc()','( list -- list ) sort list in ascending order'],
            'sortdes':      ['k_sortdes()','( list -- list ) sort list in descending order'],
            's[i]':         ['k_si()','( list -- list item ) extract item at index given in register I'],
            's[i:j]':       ['k_sij()','( list -- list slice ) extract slice given in registers I:J'],
            's[i:]':        ['k_siend()','( list -- list slice ) extract slice starting at I until end'],
            's[:j]':        ['k_sjstart()','( list -- list slice ) extract slice from start until J'],
            's[i][j]':      ['k_sijsecond()','( list -- list item ) extract item at J from item at I'],
            's[i][j][k]':   ['k_sijkthird()','( list -- list item ) extract item at K from item at J from item at I'],
            'del[i]':       ['k_deli()','( list -- list ) delete item at index given in register I'],
            'del[i:j]':     ['k_delij()','( list -- list ) delete slice given in registers I:J'],
            'del[i:]':      ['k_deliend()','( list -- list ) delete slice starting at I until end'],
            'del[:j]':      ['k_deljstart()','( list -- list ) delete slice from start until J'],
            'del[i][j]':    ['k_delijsecond()','( list -- list ) delete item at J from item at I'],
            'del[i][j][k]': ['k_delijkthird()','( list -- list ) delete item at K from item at J from item at I'],
# Dictionary words
            '###11':        ['k_pass()','  ===Dictionary words==='],
            'dict':         ['k_dict()','( str -- dict ) create dictionary from str '],
            'dictcre':      ['k_dictcre()','( keylist valuelist -- dict ) create dictionary from list of keys & values'],
            'dictexp':      ['k_dictexp()','( dict -- keylist valuelist ) expand dictionary to list of keys & values'],
            'get':          ['k_get()','( dict key -- value ) get value for key'],
            'items':        ['k_items()','( dict -- list ) return a list of all dict items as tuples (key,value)'],
            'popkey':       ['k_popkey()','( dict key -- dict value ) return and remove value for key'],
            'popitem':      ['k_popitem()','( dict -- dict item ) return and remove last item (Python 3.7+)'],
            'setdefault':   ['k_setdefault()','( dict key value -- dict ) insert the pair key:value'],
            'update':       ['k_update()','( dict seq -- dict ) update dict with sequence seq'],
# Tuple words
            '###12':        ['k_pass()','  ===Tuple words==='],
            'tuple':        ['k_tuple()','( str -- tuple ) create tuple from str '],
            'tupcre':       ['k_tupcre()','( valuelist -- tuple ) create tuple from list of values'],
            'tupexp':       ['k_tupexp()','( tuple -- valuelist ) expand tuple to list of values'],
# Set words
            '###13':        ['k_pass()','  ===Set words==='],
            'setstr':       ['k_setstr()','( str -- set ) create set from single string'],
            'set':          ['k_set()','( stritems -- set ) create set from string of multiple items'],
            'setcre':       ['k_setcre()','( valuelist -- set ) create set from list of values'],
            'setexp':       ['k_setexp()','( set -- valuelist ) expand set to list of values'],
            'add':          ['k_add()','( set item -- set ) add item to set'],
            'difference':   ['k_difference()','( set1 set2 -- set ) return set of differences between set1 and set2'],
            'sdifference':  ['k_sdifference()','( set1 set2 -- set ) return set of symmetric differences between set1 and set2'],
            'udifference':  ['k_udifference()','( set1 set2 -- set ) differences update: remove all elements of set2 from set1'],
            'discard':      ['k_discard()','( set item -- set ) remove item from set'],
            'intersection': ['k_intersection()','( set1 set2 -- set ) return intersection of set1 and set2'],
            'isdisjoint':   ['k_isdisjoint()','( set1 set2 -- ) ZF=1 if intersection of set1/set2 is null'],
            'issubset':     ['k_issubset()','( set1 set2 -- ) ZF=1 if set1 is a subset of set2'],
            'issuperset':   ['k_issuperset()','( set1 set2 -- ) ZF=1 if set1 is a superset of set2'],
            'union':        ['k_union()','( set1 set2 -- set ) return union of set1 with set2'],
# String words
            '###14':        ['k_pass()','  ===String words==='],
            'capitalize':   ['k_capitalize()','( str -- str ) return a string with first char capitalized, rest is lowercase'],
            'casefold':     ['k_casefold()','( str -- str ) return a string with all chars lowercase'],
            'center':       ['k_center()','( str width -- str ) return centered string of lenght width, space padded'],
            'centerfill':   ['k_centerfill()','( str width fill -- str ) return centered string of lenght width, fill char padded'],
            'count':        ['k_count()','( str substr -- n ) return count of substr occurences in str'],
            'emptystr':     ['k_emptystr()','( -- "") leave an empty string'],
            'endswith':     ['k_endswith()','( str suffix -- ) ZF=1 if str ends with suffix'],
            'expandtabs':   ['k_expandtabs()','( str tabsize -- str ) return string with tabs expanded'],
            'find':         ['k_find()','( str substr -- n ) return lowest index of substr found in str, -1 if not found'],
            'isalnum':      ['k_isalnum()','( str -- ) ZF=1 if all chars in str are alphanumeric'],
            'isalpha':      ['k_isalpha()','( str -- ) ZF=1 if all chars in str are alphabetic'],
            'isascii':      ['k_isascii()','( str -- ) ZF=1 if all chars in str are ASCII or str is empty'],
            'isdecimal':    ['k_isdecimal()','( str -- ) ZF=1 if all chars in str are decimal'],
            'isdigit':      ['k_isdigit()','( str -- ) ZF=1 if all chars in str are digits'],
            'islower':      ['k_islower()','( str -- ) ZF=1 if all chars in str are lowercase'],
            'isnumeric':    ['k_isnumeric()','( str -- ) ZF=1 if all chars in str are numeric'],
            'isprintable':  ['k_isprintable()','( str -- ) ZF=1 if all chars in str are printable or str is empty'],
            'isspace':      ['k_isspace()','( str -- ) ZF=1 if all chars in str are whitespaces'],
            'istitle':      ['k_istitle()','( str -- ) ZF=1 if str is titlecased'],
            'isupper':      ['k_isupper()','( str -- ) ZF=1 if all chars in str are uppercase'],
            'join':         ['k_join()','( str seq -- str ) return a string concatenated with all the strings in seq'],
            'ljust':        ['k_ljust()','( str width -- str ) return left justified string of width lenght, space padded'],
            'ljustfill':    ['k_ljustfill()','( str width fill -- str ) return left justified string of width lenght, fill char padded'],
            'lower':        ['k_lower()','( str -- str ) return a string with all chars converted to lowercase'],
            'lstrip':       ['k_lstrip()','( str -- str ) return a string with all leading spaces removed'],
            'lstripchr':    ['k_lstripchr()','( str strchr -- str ) return a string with all leading strchr chars combinations removed'],
            'partition':    ['k_partition()','( str strsep -- tuple ) split str at first occurence of strsep; return a 3-element tuple: part before separator, separator itself, part after separator'],
            'removeprefix': ['k_removeprefix()','( str strpref -- str ) return a string with strpref removed'],
            'removesuffix': ['k_removesuffix()','( str strsuff -- str ) return a string with strsuff removed'],
            'replace':      ['k_replace()','( str oldstr newstr -- str ) return a string with all occurences of oldstr replaced by newstr'],
            'replacecnt':   ['k_replacecnt()','( str oldstr newstr count -- str ) return a string with count occurences of oldstr replaced by newstr'],
            'rfind':        ['k_rfind()','( str substr -- n ) return highest index of substr found in str, -1 if not found'],
            'rjust':        ['k_rjust()','( str width -- str ) return right justified string of width lenght, space padded'],
            'rjustfill':    ['k_rjustfill()','( str width fill -- str ) return right justified string of width lenght, fill char padded'],
            'rpartition':   ['k_rpartition()','( str strsep -- tuple ) split str at last occurence of strsep; return a 3-element tuple: part before separator, separator itself, part after separator'],
            'rsplit':       ['k_rsplit()','( str strsep maxsplit -- list ) return list of maxsplit words splitted from right by strsep'],
            'rstrip':       ['k_rstrip()','( str -- str ) return a string with all trailing spaces removed'],
            'rstripchr':    ['k_rstripchr()','( str strchr -- str ) return a string with all trailing strchr chars combinations removed'],
            'split':        ['k_split()','( str strsep maxsplit -- list ) return list of maxsplit words splitted by strsep'],
            'splitlines':   ['k_splitlines()','( str -- list ) return list of lines split at line breaks without including line breaks'],
            'splitlnbrk':   ['k_splitlnbrk()','( str -- list ) return list of lines split at line breaks, including line breaks'],
            'startswith':   ['k_startswith()','( str prefix -- ) ZF=1 if str starts with prefix'],
            'strip':        ['k_strip()','( str -- str ) return a string with all spaces removed'],
            'stripchr':     ['k_stripchr()','( str strchr -- str ) return a string with all strchr chars combinations removed'],
            'swapcase':     ['k_swapcase()','( str -- str ) return a string with uppercase chars converted to lovercase and vice versa'],
            'title':        ['k_title()','( str -- str ) return a titlecased string with words starting with uppercase'],
            'upper':        ['k_upper()','( str -- str ) return a string with all chars converted to uppercase'],
            'zfill':        ['k_zfill()','( str width -- str ) return a string of lenght width left filled with "0" '],
# File I/O words
            '###15':        ['k_pass()','  ===File I/O words==='],
            'open':         ['k_open()','( filename filemode -- filehandle ) open filename with given filemode'],
            'read':         ['k_read()','( filehandle -- filecontent ) read whole file'],
            'readline':     ['k_readline()','( filehandle -- linecontent ) read a single line from file'],
            'readlines':    ['k_readlines()','( filehandle -- list ) read all lines into list'],
            'readsize':     ['k_readsize()','( filehandle size -- sizecontent ) read size bytes from file'],
            'seek':         ['k_seek()','( filehandle offset origin -- n ) file content pointer n = origin+offset'],
            'tell':         ['k_tell()','( filehandle -- n ) n = current pointer in file'],
            'write':        ['k_write()','( filehandle str -- n ) write str to file, n= nb. of chars written'],
            'close':        ['k_close()','( filehandle -- ) close file'],
# JSON words
            '###16':        ['k_pass()','  ===JSON words==='],
            'jsdump':       ['k_jsdump()','( filename pyobj -- ) write Python object as JSON object to filename'],
            'jsload':       ['k_jsload()','( filename -- pyobj ) load JSON object as Python object from filename'],
            'jsdumps':      ['k_jsdumps()','( pyobj -- jsonstring ) code Python object to JSON string'],
            'jsloads':      ['k_jsloads()','( jsonstring -- pyobj ) decode JSON string to Python object'],
# Edit/Load/Save words
            '###17':        ['k_pass()','  ===Edit/Load/Save words==='],
            'deldef':       ['k_deldef()','( defname -- ) delete definition defname'],
            'edit':         ['k_edit()','( defname -- ) edit definition defname'],
            'refdef':       ['k_refdef()','( defname -- list ) list of all definitions including a reference to defname'],
            'repdef':       ['k_repdef()','( defname -- ) replace old definitions of defname with the last one defined'],
            'load':         ['k_load()','( filename -- ) load RPPy user generated words from filename'],
            'save':         ['k_save()','( filename -- ) save RPPy user generated words to filename'],
            's.':           ['k_sdot()','( -- ) save RPPy user generated words to file "tempsave.rpp"'],
# Miscellaneous words
            '###18':        ['k_pass()','  ===Miscellaneous words==='],
            'abort':        ['k_abort()','( str -- ) print abort message str, switch to REPL'],
            'all':          ['k_all()','( seq -- ) ZF=1 if all elements in seq are true or seq is empty'],
            'any':          ['k_any()','( seq -- ) ZF=1 if any element in seq is true; ZF=0 if seq is empty'],
            'bin':          ['k_bin()','( n -- strbin ) convert integer n to binary string'],
            'chr':          ['k_chr()','( n -- strchr ) convert integer n to string representing associated glyph'],
            'complex':      ['k_complex()','( str -- n ) convert str to complex number n'],
            'choose':       ['k_choose()','( idx1 idx2 -- ) if ZF=1 execute word with idx1, else idx2'],
#            'dellast':      ['k_dellast()','( -- ) delete last definition declared'],
            'enumerate':    ['k_enumerate()','( seq -- list ) list of tuples (count,value) iterating over seq'],
            'eval':         ['k_evaluate()','( str -- item ) TOS = eval(str)'],
            'execidx':      ['k_execidx()','( idx -- ) execute word with index idx'],
            'exec':         ['k_exec()','( str -- ... ) exec(str), stack depends of what exec does'],
            'float':        ['k_float()','( str/int -- n ) convert string or integer to floating point number'],
            'format':       ['k_format()','( formatstr n -- str ) convert value n to str according to formatstr'],
            'help':         ['h.k_help()','( -- ) print help chapters'],
            'hex':          ['k_hex()','( n -- strhex ) convert integer n to hexadecimal string'],
            'input':        ['k_input()','( -- str ) read a line from input and convert data to a string'],
            'inputprompt':  ['k_inputprompt()','( strprompt -- str ) write strprompt to standard output, then read a line'],
            'int':          ['k_int()','( str/n -- n ) convert str or number n to integer n'],
            'intbase':      ['k_intbase()','( str base -- n ) convert str to integer n according to base'],
            'intro':        ['h.k_intro()','( -- ) print introduction to RPPy'],
            'license':      ['k_license()','( -- ) print RPPy license'],
            'oct':          ['k_oct()','( n -- stroct ) convert integer n to octal string'],
            'ord':          ['k_ord()','( strchr -- n ) convert string representing one character to integer n'],
            'quit':         ['k_quit()','( ... -- ... ) end execution of RPPy'],
            'str':          ['k_str()','( item -- str ) return a string interpretation of item'],
            'type':         ['k_type()','( item -- itemtype ) TOS = type of item']
            
        }
#
#           
#
#
#============================
#
#   Compiler words dictionary - words executed at compile phase
#       - pairs of key:value where:
#           - key = name of RPPy word (equivalent of an "immediate" word)
#           - value = name of python def used to compile respective word & attached docstring
CompDef =   {
            
            ' ':    ['c_compblk()','( -- ) empty line, do nothing'],
            '\t':   ['c_comptab()','( -- ) only tabs, do nothing'],
            '#':    ['c_compcomment()','( -- ) comment, skip rest of line'],
            '.':    ['c_compdot()','( -- ) mark end of compile phase, start execution phase'],
            '""':   ['c_compdocstr()','( -- ) mark start of docstring to embed in definition'],
            '"""':  ['c_compmlstr()','( -- ) mark start of multiline string'],
            '"':    ['c_compstr()','( -- ) mark start of string with blanks and without double quotes'],
            '->':   ['c_compstrall()','( -- ) mark start of string with blanks/quotes of all sort'],
            ';':    ['c_compret()','( -- ) compile return or compile jump (if tail call optimisation)'],
            'if':   ['c_compif()','( -- ) compile if: continue execution if ZF == 1, else branch to "then"'],
            'ifz':  ['c_compifnot()','( -- ) compile ifz: same as if, but for ZF == 0'],
            'ifneq':['c_compifneq()','( x y -- x y ) compile ifneq: continue execution if x!=y, else branch to "then"'],
            'then': ['c_compthen()','( -- ) compile then: branch there if condition not satisfied']
            }
#
#============================
#
#   Core words dictionary (composed of high level definitions added by user)
#       - pairs of key:value , where:
#           - key = name of high level word
#           - value = index to ExecList where the word is compiled & attached docstring
#
CoreDef = {

           }
#
#
#============================    
#
#   Execution List : new words are compiled here as pairs of [ Execution Token, Parameter],
#   where:
#       - Execution Token (XT): name of the Kernel function (Python coded)
#       - Parameter: optional, depends of XT (data to be pushed on the stack, call pointer, etc.)
#   Format: Token Threaded Code (TTC)
#
ExecList = [
#
#   Code Field  Parameter Field
#       Area        Area
#    CFA         PFA    
#    |           |
#    v           v
    
    ['REPL()'   ,'REPL'],     
    ['doRet()'  ,';'],
    ['REPL()'   ,'REPL']
    ]
#
#============================
#	Instruction Pointer IP
#	- advances sequentially through the execution token list
#	- post-incremented by NEXT
#	- modified accordingly by flow control words
#
coldstart = 2
IP = coldstart
#
#============================
#
#	Code Field Area CFA index
#	- points to the CFA of each entry in the exec list
#
CFA = 0
#
#============================
#
#	Parameter Field Area PFA index
#	- points to the PFA of each entry in the exec list
#
PFA = 1
#
#============================
#============================
#	NEXT - the execution engine - inner(index) interpreter of RPPy
#	- fetch the Execution Token (XT) & execute it
#	- post-increment IP to the next word to execute
#
def NEXT():
    global IP,CFA           # IP points to the current XT to execute
    exec(ExecList[IP][CFA])
    IP += 1
#
#============================
#============================
#
#   REPL - Read Eval Print Loop - outer(text) interpreter of RPPy
#   - read user input
#   - tokenise input as whitespace delimited strings (words)
#   - compile words as execution tokens 
#   - execute compiled words
#   - print result 
#   - repeat until user exit or unwanted crash...
#
#============================
#============================
#
tib = ""       # Terminal Input Buffer
itib = 0       # index in TIB

IndExec = 0     # 0 = compile ; 1 = execute 
IfList =[]      # store index of 'if's there, used by 'then' to fill with endif index
CompErr = 0     # return nb. of compile error, if one
LastDef = ''    # name of last definition encountered
IsDef = 0       # 0 no def, 1 def(s) encountered
Here = 2        # pointer to start execution from last compiled execution string in ExecList
IdxRetJmp = Here    # index of last compiled return/jump
brk = None      # returned from compiling words, used by compiler; True means break, False means continue compiling
switchpds = 1   # printing data stack ON
IndSave = 0     # holds nb. of saved definitions
#
#============================
#
def REPL():                 # Read Eval Print Loop - the outer (text) interpreter of RPPY

    global IP,ExecList,Here
    global IndExec, IfList, CompErr, LastDef, IsDef
    global tib, itib
    global IdxRetJmp
    global IndSave
    global switchpds
    
    CtrlQ = 17              # end RPPY execution, press only at newline
    CtrlS = 19              # save user defs to file "tempsave.rpp", continue execution, press only at newline 

#   reset compile/exec cycle data
    IndExec = 0 ; IfList =[] ; CompErr = 0 ; LastDef = '_anonymous_' ; IsDef = 0
    
    if ExecList[-1][0] == 'REPL()':  # wipe out last entry leaved by REPL's previous cycle
        del ExecList[-1:]
    Here = len(ExecList)    # last entry completed, new words compiled from here downwards
#
    if switchpds:           # print data stack only if switch ON
        k_pds()
    
    while IndExec == 0 :    # compile until execution demanded
                            
#   start gathering input ; works multiline
        tib = "" ; itib = 0 
        if IsDef == 0 :
            s_input = input('ex> ') # get user input for execution until empty line or "." arrives
        else:
            s_input = input('co> ') # get user input for compiling defs until "." arrives
            
        if len(s_input) == 0 and IsDef == 0 :   # if no input and no def compiling        
            tib = s_input + '. '    # mark "." for first empty line to start executing previous line(s)
        else:
            tib = s_input + ' '     # add always a blank at line end, as input does not deliver \n
            
        if ord(tib[0]) == CtrlQ :   # end RPPy execution
            k_quit()
            
        if ord(tib[0]) == CtrlS :   # save user defs to file "tempsave.rpp"
            if len(CoreDef) :       # save only if there are already definitions made
                lsave=[]
                lastret = ['IdxR',IdxRetJmp]
                ExecList.append(lastret)
                lsave.append(ExecList)
                lsave.append(CoreDef)
                try:
                    f=open('tempsave.rpp','w')
                    json.dump(lsave,f)
                    f.close()
                    IndSave = len(CoreDef)
                    print('Saved:',IndSave,'definitions to tempsave.rpp')
                    del ExecList[-1]
                    REPL()          # continue execution after save
                except (OSError) as e:
                    abort(str(e))
            else:
                print('No definitions to save')
                REPL()
                
            
#    call compiler
        compile()
   
        if CompErr :            # compile error encountered
            CompErr = 0         # restart compile cycle, to correct error
            continue

# end of compile phase, start execution phase
             
 
    if len(IfList) > 0 :    # see if unresolved 'if's remainded
        print('Compile error: "if/ifz/ifneq" without closing "then": ' , len(IfList) , ' unresolved')
        REPL()
    if len(ExecList) == Here :
        print('Empty line, nothing to execute')
        REPL()
    
    if IsDef == 1 :             # a new def was compiled
        
        Here = len(ExecList)    # jump over the XTs of the def, as they cannot be executed yet
                                # because there's no call for it, so the ";" sends you to outer space...
        IsDef = 0               # mark end of def compiling

    lastentry = ['REPL()','REPL']   # append as last XT REPL itself    
    ExecList.append(lastentry)  # so at execution end it'll restart the loop
    IP = Here - 1               # start execution of last compiled input stream
#
#============================
#
def word():                 # tokeniser: extract a word (whitespace delimited string of chars)
    global tib,itib

    whitespaces = ' \t\n\r\v\f' # the \n\r are not delivered and the \v,\f are superfluous...

    while itib < (len(tib) - 1):
        chr = tib[itib]
        itib += 1
        if (chr not in whitespaces):
            break
    w = chr
    while itib < (len(tib) - 1):
        chr = tib[itib]
        itib += 1
        if (chr in whitespaces):
            break
        w = w + chr
    return w
#
#============================
#
def compile():             # parse tib & compile XTs to ExecList

    global KernDef,CoreDef,ExecList,tib,itib,CompErr
    global LastDef,IndExec,IfList,IsDef,Here
    global IdxRetJmp
    global brk
    
    while itib < len(tib) - 1 :
        w = word()          # get token delimited by whitespace
        
        tkname = CompDef.get(w,None)    # first, search compiling words , to execute them immediate
        if tkname :
            exec(tkname[0])
            if brk :
                break
            continue

        tkname = CoreDef.get(w,None)    # second, search high level word in Core Dict
        if tkname :
            ExecListIdx = tkname[0]     # get corresponding index in ExecList where the word starts
            newentry = ['doCall()',ExecListIdx]    # create a call to respective word
            ExecList.append(newentry)
            continue
        
        tkname = KernDef.get(w,None)     # third, search word in Kernel Dict as a primitive
        if tkname :
            pycode = tkname[0]           # get XT (name of python function)
            newentry = [pycode,w]        # create an execute to the python function
            ExecList.append(newentry)
            continue
#
#   until here, no predefined word was found
#   continue to identify if there is:
#       - a new def to create - namedef:
#       - a pointed def to get their index - *namedef
#       - a single quoted string without blanks - 'str
#
        if w.endswith(':') and len(w) > 1 :    # new def to create
            if tib.find(w) == 0 :             # found word at start of TIB
            
                if IdxRetJmp != 1 :            # now wipe out all non-definition part already compiled
                    del ExecList[IdxRetJmp:]   # delete all previous entries, until last ret/jmp compiled
                                               # this way only definitions remain in the exec list
                IsDef =  1                     # mark presence of def 
                LastDef = w.removesuffix(':')
                newentry = {LastDef : [len(ExecList),'']}   # {name : starting point for execution}
                CoreDef.update(newentry)                    # add/modify new def to dict
                ExecList.append(['Def()',LastDef])  # store a NOP at starting point , used at decompiling
                continue
            else:
                CompErr = 1                     # def must start at begin of input
                print('Compile error: definitions must start at newline')
                break
                                
        if w.startswith("*") and len(w) > 1 :        #  get index in ExecList for the "'name"
            tkname = CoreDef.get(w.removeprefix("*"),None)  # search "name" in high level defs
            if tkname :
                ExecListIdx = tkname[0]     # get corresponding index in ExecList where de word starts
                newentry = ['doLitx()',ExecListIdx]    # push index to stack at execution
                ExecList.append(newentry)
                continue
            else:
                CompErr = 6             # "name" not found 
                print('Compile error: word "' + w.removeprefix("*") + '" not found')
                break
                
        if  w.startswith("'") and len(w) > 1 :      # literal string without blanks
            newentry = ['doLit()',w.removeprefix("'")]
            ExecList.append(newentry)
            continue
#
#   none of the above; see if integer  number 
#                
        if w.isdigit() :        # see if number string
            newentry = ['doLit()',int(w)]
            ExecList.append(newentry)   # integer literal
            continue
#
#   finally try to evaluate as float, hex, complex , expression, iterable, etc.
#   if invalid result, reject input as undefined word
#        
        try:
            number = eval(w)    # actually it's an expression to evaluate ( in INFIX !)
                                # can be a float, complex,  hex nb. or any expression with numbers
                                # even list, dict, etc. are permitted, but without any blank inside!!
            newentry = ['doLit()',number]
            ExecList.append(newentry)
            continue
        except ZeroDivisionError as e:
            CompErr = 7     # zerodiv in expression
            print('Compile error: ' + str(e) + ' in expression: ' + w)
            break
        except (SyntaxError,NameError,TypeError,ValueError) as e :
            CompErr = 8     # string incompatible with eval
            print('Compile error: ' + str(e) + ' in expression: ' + w)
            print(' Undefined: "' + w + '"')
            break
#
#============================
#   Compiler words definitions
#============================ 
#                         
def c_compblk():             # blank line, do nothing
    global brk
    brk = True
#============================    
def c_comptab():             # tab line, do nothing
    global brk
    brk = True
#============================       
def c_compcomment():         # "#" comment encountered, skip rest of line
    global brk
    brk = True
#============================       
def c_compdot():             # "." encountered, mark end of edit/compile phase, start execution phase
    global IndExec,IsDef,ExecList,CFA,IdxRetJmp
    global brk
    
    if IsDef == 1 :         # if end of def compile, compile a ret/call to always properly finish the def
        if ExecList[-1][CFA] == 'doRet()' or ExecList[-1][CFA] == 'doJmp()' :  # if already a ret/jmp present, do nothing
            IndExec = 1
            brk = True
            return
        else:  
            if ExecList[-1][CFA] == 'doCall()' : # tail call optimisation if last XT is a call
                ExecList[-1][CFA] = 'doJmp()'    # replace call before ret with jump to word
                            # that way recursive calls don't fill the return stack
                            # do not compile return
            else:
                newentry = ['doRet()',';']   # compile return unconditionally
                ExecList.append(newentry)
            IdxRetJmp = len(ExecList)        # mark index of last compiled ret/jmp, to be used by next def
                                         # as starting point to compile it
    IndExec = 1             # signal to REPL to start execution of compiled tokens
    brk = True              # exit compiler loop
#============================       
def c_compdocstr():          # '""' encountered, create docstring in last def
    global IsDef,CompErr,CoreDef,LastDef
    global brk
    if IsDef == 0 :         # no def encountered, ignore rest of line
        brk = True
        return
    s = substring('""')    # search closing delimiter
    if s == '' :            # no closing delimiter found
        CompErr = 4         # error '##' without closing '##'
        print('Compile error: '""' without closing marker '""'')
        brk = True
        return
    tkval = CoreDef.get(LastDef,None)  # search corresponding def
    if tkval :
        sl = s.lstrip()     # strip off leading blanks, if one(s)
        updtentry = {LastDef : [tkval[0],sl]}
        CoreDef.update(updtentry)
        brk = False
        return
    else:
        print('Unexpected compile error, no last definition name match: ',LastDef) 
        # normally this can't arrive...
        brk = True
        return
#============================
def c_compmlstr():          # """ encountered, create multiline string
    global tib,itib    
    global brk
    s = substring('"""')
    if s != '' :
        slstr = '"""'+s+'"""'   # end found on single input line, same as string start
        sls = eval(slstr)
        newentry = ['doLit()',sls]   
        ExecList.append(newentry)
        brk = False
        return
    else:
        mlstr = '"""'+tib[itib:]+'\n' # get rest of current line after """ 
        s_input = input('""> ')+'\n'  # add a newline at end of every readed line
        while s_input.find('"""') == -1 :   # read input until closing """ found
            mlstr = mlstr + s_input
            s_input = input('""> ')+'\n'
        mls = mlstr+s_input[0:s_input.find('"""')+3]    # get remnant of mlstr
        if len(s_input) > s_input.find('"""')+3 :       # verify if text after """ present
            print('Compile warning: all data after closing triple-quote in current line is ignored!')
        sls = eval(mls)                 # beware that all input after closing """ is ignored!
        newentry = ['doLit()',sls]      # that means in definitions you can loose the closing ";" !!   
        ExecList.append(newentry)
        brk = True
        return

#============================   
def c_compstr():             # '"' encountered, create string with embedded whitespaces only : "  ...  ...  ... " as literal
    global CompErr,ExecList
    global brk
    s = substring('"')     # search end marker 
    if s == '' :
        CompErr = 5         # no end of string marker found
        print('Compile error: " without closing marker "')
        brk = True
        return
    newentry = ['doLit()',s]   # append execution of respective string literal
    ExecList.append(newentry)
    brk = False
    return
#============================  
def c_compstrall():          # "->" encountered, create string with all sorts of single/double quotes
                            # string with embedded quotes/whitespaces: -> "  ... "' ... "  ... " <-
    global CompErr,ExecList
    global brk
    s = substring('<-')    # search end marker 
    if s == '' :
        CompErr = 5         # no end of string marker found
        print('Compile error: -> without closing marker <-')
        brk = True
        return
    newentry = ['doLit()',s]   # append execution of respective string literal
    ExecList.append(newentry)
    brk = False
    return
#============================ 
def c_compret():             # ";" encountered, compile return 
    global IsDef,CompErr,ExecList,CFA,IdxRetJmp
    global brk
    if IsDef == 0 :         # see if there is a def already to be compiled
        CompErr = 2         # ';' without starting 'xxx:'
        print('Compile error: return without definition starting')
        brk = True
        return
    else:
        if ExecList[-1][CFA] == 'doCall()' : # tail call optimisation if last XT is a call
            ExecList[-1][CFA] = 'doJmp()'    # replace call before ret with jump to word
            IdxRetJmp = len(ExecList)        # mark index of last compiled ret/jmp
            brk = False                      # that way recursive calls don't fill the return stack
            return                           # do not compile return
        else:
            newentry = ['doRet()',';']       # compile return unconditionally
            ExecList.append(newentry)
            IdxRetJmp = len(ExecList)       # mark index of last compiled ret/jmp, to be used by next def
            brk = False                     # as starting point to compile it
            return
#============================
def c_compif():          # "if" encountered, compile void jump to next "then"
    global ExecList,IfList
    global brk
                                            # create void PFA entry to be filled afterwards by 'then'
    IfList.append(len(ExecList))            # store current index, where 'if' is stored
    newentry = ['doIf()',0]                # PFA = 0 here, replace afterwards with index of following 'then'
    ExecList.append(newentry)
    brk = False
    return
#============================
def c_compifnot():          # "ifnot" encountered, compile void jump to next "then"
    global ExecList,IfList
    global brk
                                            # create void PFA entry to be filled afterwards by 'then'
    IfList.append(len(ExecList))            # store current index, where 'if' is stored
    newentry = ['doIfnot()',0]             # PFA = 0 here, replace afterwards with index of following 'then'
    ExecList.append(newentry)
    brk = False
    return
#============================
def c_compifneq():          # "ifneq" encountered, compile void jump to next "then"
    global ExecList,IfList
    global brk
                                            # create void PFA entry to be filled afterwards by 'then'
    IfList.append(len(ExecList))            # store current index, where 'if' is stored
    newentry = ['doIfneq()',0]             # PFA = 0 here, replace afterwards with index of following 'then'
    ExecList.append(newentry)
    brk = False
    return
#============================
def c_compthen():            # "then" encountered
    global IfList,ExecList,PFA,CompErr
    global brk
                            # go to last 'if' and update PFA with index of 'then'
    if len(IfList) >= 1 :           # see if a preceeding 'if' is present
        idxthen = len(ExecList)
        idxif = IfList.pop()        # get saved 'if' index
        ExecList[idxif][PFA] = idxthen  # store 'then' index to PFA of 'if'
        newentry = ['k_pass','then']      # nothin' to do here
        ExecList.append(newentry)
        brk = False
        return
    else:
        CompErr = 3                 # error 'then' without 'if'
        print('Compile error: no matching "if/ifz/ifneq" for "then"')
        brk = True
        return
#
#============================
#                          
def substring(delim):       # extract a substring with given end delimiter
    global tib,itib

    idx = tib.find(delim,itib)
    if idx == -1 :          # not found 
        s = ''
        return s
    s = tib[itib:idx]     # slice portion between start-stop delimiter
    itib = idx + len(delim)         # advance index after delimiter
    return s
#
#============================
#
#   Internal Control Flow execution routines attached to external compiling words
#
#============================
#
def doCall():              # call word to execute
    global IP,PFA,ExecList
    rpush(IP)               # save current index, will be popped by 'doRet()' and post-incremented by NEXT
                            # so it will point to the word following the call, as expected
    IP = ExecList[IP][PFA]  # get index of callee & continue execution from here
#
#============================
#
def doJmp():               # jump to word to execute
    global IP,PFA,ExecList
    IP = ExecList[IP][PFA]  # get index of word  & continue execution from here
                            # same as doCall() but without return saving
#
#============================
#
def doRet():               # return to caller
    global IP
    IP = rpop()
#
#============================
#
def doIf():                # continue execution if ZF=1, else jump to corresponding 'then'
    global ZF
    if not ZF :
        doJmp()            # jump to 'then' index   
#
#============================
#
def doIfnot():             # continue execution if ZF=0, else jump to corresponding 'then'
    global ZF
    if ZF :
        doJmp()            # jump to 'then' index
#
#============================
#
def doIfneq():             # ( x y -- x y ) continue execution if x!=y, else branch to "then"
    try:
        if tos() == nos() :
            doJmp()
    except(TypeError,ValueError) as e:
        abort(str(e))
#
#============================
#
def doLit():                # literal treatment: push PFA to Data Stack
    global IP,PFA,ExecList
    dpush(ExecList[IP][PFA])
#
#============================
#
def doLitx():               # literal treatment: push PFA to Data Stack
    global IP,PFA,ExecList  # same as doLit(), but used to differentiate between call by index or ordinary literal
    dpush(ExecList[IP][PFA])
#
#============================
# end of REPL/compiler part
#============================
#
#============================
#
def k_clrdstk():             # ( ... -- ) clear data stack
    global dstack
    dstack = []
    
#
#============================
#
def k_clrustk():             # ( ... -- ) clear user stack
    global ustack
    ustack = []


#
#============================
#
#   Printer definitions
#
#============================
#
def k_pds():                    # ( -- ) print Data Stack in raw form as list
    if len(dstack) == 0 :
        print(' Data stack empty')
    else:
        print(' Data stack items: ' + str(len(dstack)))
        if len(dstack) <= 10 :
            print(dstack)
        else:
            print(' Top 10 data stack items:')
            print(dstack[-10:])      # max. nb of items to print, arbitrary value (even 10 is way too much!)
#
#============================
#
def k_pdson():          # switch data stack printing to ON
    global switchpds
    switchpds = 1
#
#============================
#
def k_pdsoff():          # switch data stack printing to OFF
    global switchpds
    switchpds = 0
#
#============================
#
def k_pus():                    # ( -- ) print User Stack in raw form as list
    if len(ustack) == 0 :
        print(' User stack empty')
    else:
        print(' User stack items: ' + str(len(ustack)))
        if len(ustack) <= 10 :
            print(ustack)
        else:
            print(' Top 10 user stack items:')
            print(ustack[-10:])      # max. nb of items to print
#
#============================
#
def k_prs():                    # ( -- ) print Return Stack
    global ExecList,CFA,PFA
    if len(rstack) == 0 :
        print(' Return stack empty')
    else:
        print(' Return stack items:' + str(len(rstack)-1))
        for i in range(len(rstack)-1,0,-1) :
            idxret = rstack[i]
            if ExecList[idxret][CFA] == 'doCall()' :
                idxcall = ExecList[idxret][PFA]
                print(i,'return from:',ExecList[idxcall][PFA])
            else:
                print(i,'return at: ',idxret)
#
#============================
#
def  k_pkerndefall():                # ( -- ) print all kernel words
    l1=list(KernDef)
    l2=list(KernDef.values())
    commentkey = 0
    for i in range(len(KernDef)):
        if l1[i].startswith('###'):
            commentkey += 1
    for i in range(len(KernDef)):
        if l1[i].startswith('###') and l1[i] != '###1' :
            s=input()
            if len(s) != 0 :
                break
        print(' ',l1[i].ljust(8),l2[i][1])
    print()
    print(' Kernel Definitions: ',len(KernDef)-commentkey)
#
#============================
#
def  k_pkerndef():                # ( -- ) print kernel words per category
    l1=list(KernDef)
    l2=list(KernDef.values())
    commentkey = 0
    for i in range(len(l1)):
        if l1[i].startswith('###'):
            print((l1[i].removeprefix('###')).rjust(4),l2[i][1])
            commentkey += 1
    s=input(" Enter your choice: ")
    if len(s) == 0 :
        return
    elif not s.isdigit() or int(s) not in range(1,commentkey+1) :
        print("Value out of range or not a number")
        return
    else:
        print()
        startidx = l1.index('###'+s)
        print(' ',l1[startidx].ljust(8),l2[startidx][1])
        for i in range(startidx+1,len(l1)):
            if l1[i].startswith('###'):
                break
            print(' ',l1[i].ljust(8),l2[i][1])
        print()
    return

#
#============================
#
def k_pcompdef():           # ( -- ) print compiler words
    l1=list(CompDef)
    l2=list(CompDef.values())
    print('             ===Compiler words===')
    for i in range(2,len(CompDef)):
        print(' ',l1[i].ljust(8),l2[i][1])
    print()
    print(' Compiler Definitions: ',len(CompDef)-2)
#
#============================
#
def k_pdefall():                  # ( -- ) print all definitions dict

    l1=list(CoreDef)
    l2=list(CoreDef.values())
    for i in range(len(CoreDef)) :
        if i%10 == 0 and i != 0 :
            s=input()
            if len(s) != 0 :
                break
        print(' ',l1[i].ljust(10),end=' ')
        print(' at index: ',l2[i][0],end=' ')
        print('""',l2[i][1],'""')
    print()
    print(' High Level Dictionary Definitions: ',len(CoreDef))
#
#============================
#
def k_pddef():                  # ( defname -- ) print a definition 
    if len(dstack) < 1 :
        abort('Missing argument for "pdef"')
    elif not isinstance(tos(),str) :
        abort('Definition name must be a string')
    else:
        defval = KernDef.get(tos(),None)
        if defval :
            print('Kernel primitive:',tos(),'; XT:',defval[0],'; action:',defval[1])
            dpop()
        else:
            defval = CoreDef.get(tos(),None)
            if not defval :
                abort('Name "'+tos()+'" undefined')
            else:
                print(' ',tos().ljust(10),end=' ')
                print(' at index: ',defval[0],end=' ')
                print('""',defval[1],'""')
                idx = defval[0]
                k_pddef_aux(idx)    # print last declared definition with same name, found in CoreDef
#               see if duplicate present 
                nbdef = ExecList.count(['Def()',tos()])
                if nbdef == 1 :
                    print('  No duplicate (older definitions) present')
                else:
                    print('  There are',nbdef-1,'older definitions')
                    idxcontinue = 0
                    for i in range(nbdef-1) :
                        idx = ExecList.index(['Def()',tos()],idxcontinue)
                        print('  Duplicate',i+1,'at index',idx)
                        k_pddef_aux(idx)
                        idxcontinue = idx+1
                k_drop()
                
#============================
def k_pddef_aux(idx):
    global ExecList,CFA,PFA
    while idx < len(ExecList) - 1 :
        if ExecList[idx][CFA] == 'Def()' :
            print(' ',ExecList[idx][PFA]+':',end=' ')
        elif ExecList[idx][CFA] == 'doRet()' :
            print(';',end=' ')
            idx += 1
            if ExecList[idx][PFA] == 'then' :
                continue
            else:
                print()
            break
        elif ExecList[idx][CFA] == 'doJmp()':
            jdx = ExecList[idx][PFA]
            print(ExecList[jdx][PFA]+' ;',end=' ')
            idx += 1
            if ExecList[idx][PFA] == 'then' :
                continue
            else:
                print()
                break
        elif ExecList[idx][CFA] == 'doCall()' :
            jdx = ExecList[idx][PFA]
            print(ExecList[jdx][PFA],end=' ')
        elif ExecList[idx][CFA] == 'doIf()' :
            print('if',end=' ')
        elif ExecList[idx][CFA] == 'doIfnot()' :
            print('ifz',end=' ')
        elif ExecList[idx][CFA] == 'doIfneq()' :
            print('ifneq',end=' ')
        elif ExecList[idx][CFA] == 'doLitx()' :
            jdx = ExecList[idx][PFA]
            print('*'+ExecList[jdx][PFA],end=' ')
        elif ExecList[idx][CFA] == 'doLit()' :
            if isinstance(ExecList[idx][PFA],str) :
                print('"',ExecList[idx][PFA]+'"',end=' ')
            else:
                print(ExecList[idx][PFA],end=' ')
        else:
            print(ExecList[idx][PFA],end=' ')
        idx += 1
    print()
#
#============================
#
def k_pexlst():                  # ( idx -- ) print execution list starting with index idx
    if len(dstack) == 0 :
        abort('Stack empty, missing start index')
    elif not isinstance(tos(),int) :
        abort('Index to start printing must be an integer')
    elif tos() > len(ExecList)-1 or tos() < 0 :
        abort('Index is negative or out of range 0:' + str(len(ExecList) - 1))
    else:
        n = dpop()
        fin = len(ExecList)-1
        if fin-n > 50 :             # arbitrary upper limit of items to print
            print('Printing max. 50 entries; endlist-startindex is: ' + str(fin-n) + ' entries')
            fin = 50 + n
        for i in range(n,fin) :
            print(str(i).rjust(5),end=' ')
            if ExecList[i][CFA] == 'Def()' :
                print(ExecList[i][PFA] + ':')
                continue
            elif ExecList[i][CFA] == 'doCall()' :
                j = ExecList[i][PFA]
                print('call ' + ExecList[j][PFA])
                continue
            elif ExecList[i][CFA] == 'doJmp()' :
                j = ExecList[i][PFA]
                print('jump ' + ExecList[j][PFA])
                continue
            elif ExecList[i][CFA] == 'doLit()' :
                print('lit ',end = ' ')
                print(ExecList[i][PFA])
                continue
            elif ExecList[i][CFA] == 'doLitx()' :
                j = ExecList[i][PFA]
                print('pointer to ' + ExecList[j][PFA])
                continue
            elif ExecList[i][CFA] == 'doIf()' :
                print('if - then at: ' + str(ExecList[i][PFA]))
                continue
            elif ExecList[i][CFA] == 'doIfnot()' :
                print('ifz - then at: ' + str(ExecList[i][PFA]))
                continue
            elif ExecList[i][CFA] == 'doIfneq()' :
                print('ifneq - then at: ' + str(ExecList[i][PFA]))
                continue
            else:
                print(ExecList[i][PFA])
                continue
#
#============================
#
def k_printnl():              # ( -- ) print newline
    print()
#
#============================
#
def k_printend():              # ( item endstr -- ) print item followed by end string
    if len(dstack) < 2  :
        abort('Missing arguments for printend')
    elif not isinstance(tos(),str) :
        abort('End argument must be a string')
    else:
        endstr = dpop()
        item = dpop()
        if endstr == '\\n' :    #>>> patch for unresolved pb. with \\ special chars
            endstr = '\n'       # as there is no 'r' prefixed string yet
        if endstr == '\\t' :
            endstr = '\t'      #<<< end of patch
        try:
            print(item,end=endstr)
        except (AttributeError, SyntaxError, NameError, TypeError,ValueError,KeyError,IndexError) as e:
            dpush(item)
            dpush(endstr)
            abort('Print error: '+str(e))
#
#============================
#
def k_print():               # ( item -- ) print item 
    if len(dstack) == 0 :
        abort('Missing argument for print')
    else:
        item = dpop()
        try:
            print(item)
        except (AttributeError, SyntaxError, NameError, TypeError,ValueError,KeyError,IndexError) as e:
            dpush(item)
            abort('Print error: '+str(e))
#
#============================
#
def k_printf():               # ( formatstr item -- ) print item according to format string
    if len(dstack) < 2 :
        abort('Missing arguments for printf')
    elif not isinstance(nos(),str) :
        abort('Format argument must be a string')
    else:
        item = dpop()
        form = dpop()
        try:
            print(form.format(item))
        except (AttributeError, SyntaxError, NameError, TypeError,ValueError,KeyError,IndexError) as e:
            dpush(form)
            dpush(item)
            abort('Print error: '+str(e))
    
#
#============================
#
def k_plist():                  # ( list -- ) print list as enumerated elements
    if len(dstack) < 1 :
        abort('Missing argument for "plist"')
    elif not isinstance(tos(),list) :
        abort('Argument for "plist" must be a list')
    else: 
        for i,item in enumerate(tos()) :
            print('  ',i,item)
        k_drop()
#
#============================
#
def abort(serr):               # show TOS & NOS at *execution* errors
    global rstack
    print('"'+ExecList[IP][PFA]+'"'+' aborted: ' + serr)
    print(' Aborted at Execution List Index: ' ,IP)
    idx = IP
    while idx > 0 :
        if ExecList[idx][CFA] == 'Def()' :
            print(' In definition: '+'"'+ExecList[idx][PFA]+'" at index: '+str(idx))
            break
        elif ExecList[idx][CFA] == 'doRet()' or ExecList[idx][CFA] == 'doJmp()':
            print(' Aborted in execution string or in definition with multiple returns')
            break
        elif idx == 1 :
            print(' Aborted in execution string')
            break
        else:
            idx -= 1
    if len(dstack) >= 2 :
        print('  TOS: ',type(tos()),tos())
        print('  NOS: ',type(nos()),nos())
    elif len(dstack) == 1 :
        print('  TOS: ',type(tos()),tos())
    else:
        print(' Stack empty, cannot print TOS & NOS')
    if len(rstack) > 1 :        # print Return Stack
        k_prs()
        rstack = [0]            # empty Return Stack, as unsolved RETs may remain after aborting
    REPL()                      
#
#============================
#
def k_abort():              # ( str -- ) abort with user message
    if len(dstack) < 1:
        abort('Missing argument for "abort"')
    elif not isinstance(tos(),str) :
        abort('Abort argument must be a string')
    else:
        print('User Abort')
        abort(dpop())
#
#============================
#
def abortstk(serr):        # show error messages at stack manipulation
    global rstack
    print('"'+ExecList[IP][PFA]+'"'+' aborted: ' + serr)
    print(' Index: ' ,IP)
    idx = IP
    while idx > 0 :
        if ExecList[idx][CFA] == 'Def()' :
            print(' In definition: '+'"'+ExecList[idx][PFA]+'" at index: '+str(idx))
            break
        elif ExecList[idx][CFA] == 'doRet()' or ExecList[idx][CFA] == 'doJmp()':
            print(' Aborted in execution string or in definition with multiple returns')
            break
        elif idx == 1 :
            print(' Aborted in execution string')
            break
        else:
            idx -= 1
    if len(rstack) > 1 :     # print Return Stack
        k_prs()
        rstack = [0]         # empty Return Stack, as unsolved RETs may remain after aborting
    REPL()                    
#
#============================
#
def k_pass():                # no op ; invoked by '###i'
    pass
#
#============================
#
def Def():                 # no op, used at decompiling definition
    pass
#
#
#============================
#
#   Kernel Stack definitions
#
#============================
#
def tos():                  #return TOS of Data Stack ; stack unmodified
    if len(dstack) >= 1 :
        return dstack[-1]
    else:
       abortstk(' Stack empty, cannot pick TOS') 
#
#============================
#
def nos():                  #return NOS of Data Stack ; stack unmodified
    if len(dstack) >= 2 :
        return dstack[-2]
    else:
        abortstk(' Stack has only 1 item, cannot pick NOS')
#
#============================
#
def dpush(val):             #push value on Data Stack
    dstack.append(val)
#
#============================
#
def dpop():                 #pop value from Data Stack
    
    if len(dstack) > 0:
        return dstack.pop()       
    else:
        abortstk(' Data Stack Underflow')
    
#
#============================
#
def rpush(val):             #push value on Return Stack
    rstack.append(val)
#
#============================
#
def rpop():                 #pop value from Return Stack
    if len(rstack) > 0:
        return rstack.pop()
    else:                   #as rstack is not user accessible, underflow may appear 
                            #only for unmatched pair call-ret : ret without call
        abortstk(' Return Stack Underflow')
#
#============================
#
def k_uspush():              #push value on User Stack
    ustack.append(dpop())
#
#============================
#
def k_uspop():                 #pop value from User Stack
    if len(ustack) > 0:
        dstack.append(ustack.pop())
    else:
        abortstk(' User Stack Underflow')
#
#============================
#
def k_dup():                 # ( n -- n n ) duplicate TOS
    n = dpop()
    dpush(n)
    dpush(n)
#
#============================ 
#
def k_ddup():                 # ( x y -- x y x y  ) duplicate NOS and TOS
	y = dpop() ; x = dpop() ; dpush(x) ; dpush(y) ; dpush(x) ; dpush(y) 
#
#============================
#
def k_swap():                # ( x y -- y x ) exchange TOS with NOS
	y = dpop() ;  x = dpop() ; dpush(y) ; dpush(x)
#
#============================
#
def k_drop():                # ( n -- ) drop TOS
	dpop()
#
#============================
#
def k_ddrop():                # ( x y -- ) drop TOS and NOS
	dpop() ; dpop()
#
#============================
#
def k_over():                # ( x y -- x y x ) copy NOS over TOS
    y = dpop() ; x = dpop() ; dpush(x) ; dpush(y) ; dpush(x)
#
#============================
#
def k_nip():                 # ( x y -- y ) drop NOS
    k_swap()
    k_drop()
#
#============================
#
def k_tuck():                 # ( x y -- y x y ) insert TOS before NOS
    k_swap()
    k_over()
#
#============================
#
def k_rot():                 # ( x y z -- y z x ) rotate rightwise top three items
    z = dpop()
    y = dpop()
    x = dpop()
    dpush(y)
    dpush(z)
    dpush(x)
#
#============================
#
def k_rotl():                 # ( x y z -- z x y ) rotate leftwise top three items
    z = dpop()
    y = dpop()
    x = dpop()
    dpush(z)
    dpush(x)
    dpush(y)
#
#============================
#
def k_pick():    # ( xn xn-1 xn-2 ... x0 n -- xn xn-1 xn-2 ... x0 xn ) replace TOS with a copy of the n-th item
    if type(tos()) != int :
        abort('Index of item to pick must be an integer')
    elif tos() > len(dstack)-2 or tos() < 0 :
        abort('Index of item to pick is > stacklenght, or negative')
    else:
        n = -(tos()+1)
        dpop()
        dpush(dstack[n])
#
#============================
#
#   Kernel Math definitions (basic ops only)
#
#============================
#
def k_commonmath(op):
    if len(dstack) < 2 :
        abort('Math "' + op + '" needs 2 items, stack has 1 item or is empty')
    else:
        try:
            y = dpop()
            x = dpop()
            exec('dpush(x ' + op + ' y)')
        except (ZeroDivisionError,TypeError) as e:
            dpush(x)
            dpush(y)
            abort(str(e))
#
#============================
#
def k_plus():                # ( x y -- x+y ) add TOS to NOS
    op = '+'
    k_commonmath(op)
#
#============================
#
def k_minus():                # ( x y -- x-y ) subtract TOS from NOS
    op = '-'
    k_commonmath(op)
#
#============================
#
def k_star():                 # ( x y -- x*y ) multiply TOS by NOS
    op = '*'
    k_commonmath(op)
#
#============================
#
def k_slash():                 # ( x y -- x/y ) divide NOS by TOS - floating point division
    op = '/'
    k_commonmath(op)
#
#============================
#
def k_dblslash():                 # ( x y -- x//y ) divide NOS by TOS - floored (integer) division
    op = '//'
    k_commonmath(op)
#
#============================
#
def k_rem():                     # ( x y -- rem ) leave remainder of x/y division
    op = '%'
    k_commonmath(op)  
#
#============================
#
def k_divmod():                     # ( x y -- quot rem ) leave quotient & remainder of x/y division
    if len(dstack) < 2 :
        abort('Math "divmod" needs 2 items, stack has 1 item or is empty')
    else:
        try:
            y = dpop()
            x = dpop()
            q,r = (divmod(x,y)) 
            dpush(q)
            dpush(r) 
        except (ZeroDivisionError,TypeError) as e:
            dpush(x)
            dpush(y)
            abort(str(e))
#
#============================
#
def k_dblstar():                     # ( x y -- x**y ) NOS at TOS power
    op = '**'
    k_commonmath(op)  
#
#============================
#
def k_plusone():                    # increment TOS by 1
    if len(dstack) < 1 :
        abort('Math "++" needs 1 item, stack empty')
    elif not isinstance(tos(), (int,float,complex)):
        abort('Value for "++" must be of type (int,float,complex)')
    else:
        n = dpop()
        dpush(n+1)
#
#============================
#
def k_minusone():                  # decrement TOS by 1
    if len(dstack) < 1 :
        abort('Math "--" needs 1 item, stack empty')
    elif not isinstance(tos(), (int,float,complex)):
        abort('Value for "--" must be of type (int,float,complex)')
    else:
        n = dpop()
        dpush(n-1)
#
#============================
#
def k_negate():                      # ( n -- neg(n) ) negate n 
    if len(dstack) < 1 :
        abort('Negation "neg" needs 1 item, stack empty')
    elif not isinstance(tos(), (int,float,complex)):
        abort('Value for "neg" must be of type (int,float,complex)')
    else:
        n = dpop()
        dpush(0-n)
#
#============================
#
def k_abs():                     # ( x  -- abs(x) ) absolute value of x
    if len(dstack) < 1 :
        abort('Absolute "abs" needs 1 item, stack empty')
    elif not isinstance(tos(), (int,float,complex)):
        abort('Value for "abs" must be of type (int,float,complex)')
    else:
        x = dpop()
        dpush(abs(x))
#
#============================
#
def k_round():                   # ( n i -- round(n))  n rounded to i digits
    if len(dstack) < 2 :
        abort('Math "round" needs 2 items, stack has 1 item or is empty')
    elif not isinstance(tos(), (int)):
        abort('Nb. of digits to round must be of type (int)')
    elif not isinstance(nos(),(int,float)):
        abort('Value to be rounded must be of type (int,float)')
    else:
        i = dpop()
        n = dpop()
        dpush(round(n,i))
#
#============================
#
def k_min():                     # ( seq  -- min(seq) ) minimum of values in sequence seq
  if not isinstance (tos(), (tuple,list,dict,set))  : 
    abort('Argument of "min" must be a sequence with at least 2 items')
  else:
    seq = dpop()
    dpush(min(seq))  
#
#============================
#
def k_max():                     # ( seq  -- max(seq) ) maximum of values in sequence seq
  if not isinstance (tos(), (tuple,list,dict,set))  :
    abort('Argument of "max" must be a sequence with at least 2 items')
  else:
    seq = dpop()
    dpush(max(seq))  
#
#============================
#
def k_sum():                     # ( seq -- sum(seq) ) sum of  items in sequence seq
  if not isinstance (tos(), (tuple,list,dict,set))  :
    abort('Argument of "sum" must be a sequence')
  else:
    seq = dpop()
    dpush(sum(seq)) 
#
#============================
#
def k_sumval():                     # ( n1 n2 ... ni i -- sum(ni) ) sum of top i values, i >= 1
    global TOS
    if type(tos()) != int :
        abort('Nb. of values to sum must be an integer')
    elif tos() > len(dstack)-1 or tos() < 1 :
        abort('Nb. of values to sum is > stacklenght, or < 1')
    else:
        n = dpop()
        TOS = 0
        for i in range (n):
            if not isinstance(tos(), (int,float,complex)) :
                abort('Values to sum must be of type (int,float,complex)')
            TOS += dpop()
        dpush(TOS)
#
#============================
#
def k_sumstr():                     # ( str1 str2 ... stri i -- str ) concatenate top i strings, i >= 1
    global TOS
    if type(tos()) != int :
        abort('Nb. of strings to concatenate must be an integer')
    elif tos() > len(dstack)-1 or tos() < 1 :
        abort('Nb. of strings to concatenate is > stacklenght, or < 1')
    else:
        n = dpop()
        TOS = ''
        l1 = dstack[-n:]
        l1.reverse()
        dstack[-n:] = l1
        for i in range (n):
            if not isinstance(tos(), str) :
                abort('Items to concatenate must be of type str')
            TOS += dpop()
        dpush(TOS)
#
#============================
#
def k_sumlst():                     # ( list1 list2 ... listi i -- list ) concatenate top i lists, i >=1
    global TOS
    if type(tos()) != int :
        abort('Nb. of lists to concatenate must be an integer')
    elif tos() > len(dstack)-1 or tos() < 1 :
        abort('Nb. of lists to concatenate is > stacklenght, or < 1')
    else:
        n = dpop()
        TOS = []
        l1 = dstack[-n:]
        l1.reverse()
        dstack[-n:] = l1
        for i in range (n):
            if not isinstance(tos(), list) :
                abort('Items to concatenate must be of type list')
            TOS += dpop()
        dpush(TOS)
#
#============================
#
def k_mulval():                     # ( n1 n2 ... ni i -- product(ni) ) product of top i values, i >= 1
    global TOS
    if type(tos()) != int :
        abort('Nb. of values to multiply must be an integer')
    elif tos() > len(dstack)-1 or tos() < 1 :
        abort('Nb. of values to multiply is > stacklenght, or < 1')
    else:
        n = dpop()
        TOS = 1
        for i in range (n):
            if not isinstance(tos(), (int,float,complex)) :
                abort('Values to multiply must be of type (int,float,complex)')
            TOS *= dpop()
        dpush(TOS)
#                                  
#
#============================
#
#   Kernel Comparison definitions 
#
#============================
#
def k_commoncompare(op):
    global ZF 
    if len(dstack) < 2 :
        abort('Comparison "' + op + '" needs 2 items, stack has 1 item or is empty')
    else:
        try:
            if eval('nos()' + op + 'tos()') :
                ZF = 1
            else:
                ZF = 0
        except TypeError as e:
            abort(str(e))
#
#============================
#
   
def k_le():                      # ( x y -- x y ) ZF = 1 if x<y
    op = '<'
    k_commoncompare(op)
#
#============================
#
def k_gt():                      # ( x y -- x y ) ZF = 1 if x>y
    op = '>'
    k_commoncompare(op)
#
#============================
#
def k_leeq():                      # ( x y -- x y ) ZF = 1 if x<=y
    op = '<='
    k_commoncompare(op)
#
#============================
#
def k_gteq():                      # ( x y -- x y ) ZF = 1 if x>=y
    op = '>='
    k_commoncompare(op)
#
#============================
#
def k_eq():                      # ( x y -- x y ) ZF = 1 if x==y
    op = '=='
    k_commoncompare(op)
#
#============================
#
def k_neq():                      # ( x y -- x y ) ZF = 1 if x!=y
    op = '!='
    k_commoncompare(op)
#
#============================
#
def k_commonzerocomp(op):
    global ZF
    if len(dstack) < 1 :
        abort('Comparison with 0 needs 1 item, stack empty')
    else:
        try:
            if eval('tos()' + op + ' 0') :
                ZF = 1
            else:
                ZF = 0
        except TypeError as e:
            abort(str(e))
#
#============================
#
def k_zeq():                      # ( n -- n ) ZF = 1 if n=0
    op = '=='
    k_commonzerocomp(op)
#
#============================
#
def k_zneq():                      # ( n -- n ) ZF = 1 if n!=0
    op = '!='
    k_commonzerocomp(op)
#
#============================
#
def k_zle():                      # ( n -- n ) ZF = 1 if n<0
    op = '<'
    k_commonzerocomp(op)
#
#============================
#
def k_zgt():                      # ( n -- n ) ZF = 1 if n>0
    op = '>'
    k_commonzerocomp(op)
#
#============================
#
def k_lesszeq():                 # ( idx1 idx2 idx3 n -- ) if n<0 execute idx1; if n=0 execute idx2; else idx3
    global IP
    
    if len(dstack) < 4 :
        abort('Comparison "<0>" needs 4 items "idx1 idx2 idx3 n" ')
    elif not isinstance(tos(), (int,float)):
        abort('Value to compare with 0 must be of type int/float')
    else:
        n = dpop()
        idx3 = dpop()
        idx2 = dpop()
        idx1 = dpop()
        if idx3 < 0 or idx3 not in range (len(ExecList)) :
            dpush(idx3)
            abort('Index idx3 out of execution list range 0:' + str(len(ExecList)))
        elif idx2 < 0 or idx2 not in range (len(ExecList)) :
            dpush(idx2)
            abort('Index idx2 out of execution list range 0:' + str(len(ExecList)))
        elif idx1 < 0 or idx1 not in range (len(ExecList)) :
            dpush(idx1)
            abort('Index idx1 out of execution list range 0:' + str(len(ExecList)))
        else:
            rpush(IP)
            if n < 0 :
                IP = idx1
                return
            elif n == 0 :
                IP = idx2
                return
            IP = idx3
#
#============================
#
def k_lesseqgt():                 # ( idx1 idx2 idx3 x y -- ) if x<y execute idx1; if x=y execute idx2; else idx3
    global IP
    
    if len(dstack) < 5 :
        abort('Comparison "<=>" needs 5 items "idx1 idx2 idx3 x y" ')
    elif type(tos()) != type(nos()) :
        abort('Values to compare must be of same type')
    else:
        y = dpop()
        x = dpop()
        idx3 = dpop()
        idx2 = dpop()
        idx1 = dpop()
        if idx3 < 0 or idx3 not in range (len(ExecList)) :
            dpush(idx3)
            abort('Index idx3 out of execution list range 0:' + str(len(ExecList)))
        elif idx2 < 0 or idx2 not in range (len(ExecList)) :
            dpush(idx2)
            abort('Index idx2 out of execution list range 0:' + str(len(ExecList)))
        elif idx1 < 0 or idx1 not in range (len(ExecList)) :
            dpush(idx1)
            abort('Index idx1 out of execution list range 0:' + str(len(ExecList)))
        else:
            rpush(IP)
            if x < y :
                IP = idx1
                return
            elif x == y :
                IP = idx2
                return
            IP = idx3
#
#============================
#
def k_setZF():                   # ( n -- ) pop TOS to ZF
    global ZF
    ZF = dpop()
#
#============================
#
def k_ZF():                   # ( -- ZF ) push ZF
    global ZF
    dpush(ZF)
#
#============================
#
def k_in():                  # ( seq item -- seq item ) ZF = 1 if item found in sequence
  global ZF
  if len(dstack) < 2 :
    abort('Comparison "in" needs 2 items, stack has 1 item or is empty')
  elif not isinstance(nos(), (str,list,dict,set,tuple)):
    abort('Item to be searched for is not a sequence')
  else:
    if tos() in nos() :
      ZF = 1
    else:
      ZF = 0
#
#============================
#
def k_notin():                  # ( seq item -- seq item ) ZF = 1 if item not found in sequence
  global ZF
  if len(dstack) < 2 :
    abort('Comparison "notin" needs 2 items, stack has 1 item or is empty')
  elif not isinstance(nos(), (str,list,dict,set,tuple)):
    abort('Item to be searched for is not a sequence')
  else:
    if tos() not in nos() :
      ZF = 1
    else:
      ZF = 0
#
#============================
#
def k_is():                  # (item1 item2 -- item1 item2 ) ZF = 1 if item1 and item2 are the same object
  global ZF
  if len(dstack) < 2 :
    abort('Comparison "is" needs 2 items, stack has 1 item or is empty')
  else:
    if tos() is nos() :
      ZF = 1
    else:
      ZF = 0
#
#============================
#
def k_isnot():                  # (item1 item2 -- item1 item2 ) ZF = 1 if item1 and item2 are not the same object
  global ZF
  if len(dstack) < 2 :
    abort('Comparison "isnot" needs 2 items, stack has 1 item or is empty')
  else:
    if tos() is not nos() :
      ZF = 1
    else:
      ZF = 0
#
#============================
#
#   Kernel Logical definitions 
#
#============================
#
def k_and():                     # ( x y -- x y ) ZF = 1 if both x and y are True
    global ZF
    if len(dstack) < 2 :
        abort('Logical "and" needs 2 items, stack has 1 item or is empty')
    else:
        if bool(tos() and nos()) == True :
            ZF = 1
        else:
            ZF = 0
#
#============================
#
def k_or():                      # ( x y -- x y ) ZF = 1 if either x or y or both are True
    global ZF
    if len(dstack) < 2 :
        abort('Logical "or" needs 2 items, stack has 1 item or is empty')
    else:
        if bool(tos() or nos()) == True :
            ZF = 1
        else:
            ZF = 0
#
#============================
#
def k_xor():                     # ( x y -- x y ) ZF = 1 if either (x is True and y is False) or (x is False and y is True)
    global ZF
    if len(dstack) < 2 :
        abort('Logical "xor" needs 2 items, stack has 1 item or is empty')
    else:
        if bool((tos() and not nos()) or (nos() and not tos())) == True :
            ZF = 1
        else:
            ZF = 0
#
#============================
#
def k_not():                     # ( n -- n ) ZF = 1 if n is False or None
    global ZF
    if len(dstack) < 1 :
        abort('Logical "not" needs 1 item, stack empty')
    else:
        if bool(tos()) == False or bool(tos()) == None :
            ZF = 1
        else:
            ZF = 0
#
#============================
#
def k_notnot():                  # ( n -- n ) ZF = 1 if n is True
    global ZF
    if len(dstack) < 1 :
        abort('Logical "-not" needs 1 item, stack empty')
    else:
        if bool(tos()) == True :
            ZF = 1
        else:
            ZF = 0
#
#============================
#
#   Kernel Bitwise definitions 
#
#============================
#
def k_commonbitwise(op,bitop):
    if len(dstack) < 2 :
        abort('Bitwise "' + op + '" needs 2 items, stack has 1 item or is empty')
    elif not (isinstance(tos(), int) and isinstance(nos(), int)):
        abort('Bitwise "' + op + '" needs 2 integers')
    else:
        y = dpop()
        x = dpop()
        exec ('dpush(x '+bitop+' y)')
#
#============================
#
def k_bitand():                  # ( x y -- x&y ) bitwise and
    op,bitop = 'and','&'
    k_commonbitwise(op,bitop)
#
#============================
#
def k_bitor():                  # ( x y -- x|y ) bitwise or
    op,bitop = 'or','|'
    k_commonbitwise(op,bitop)
#
#============================
#
def k_bitxor():                  # ( x y -- x^y ) bitwise xor
    op,bitop = 'xor','^'
    k_commonbitwise(op,bitop)
#
#============================
#
def k_bitcompl():                # ( n -- ~n ) one's complement
    if len(dstack) < 1 :
        abort('Bitwise "one\'s complement" needs 1 item, stack empty')
    elif not isinstance(tos(), int):
        abort('Nb. to complement must be an integer')
    else:
        n = dpop()
        dpush(~n)
#
#============================
#
def k_commonshift(op):
    if len(dstack) < 2 :
        abort('Bitwise "' + op + '" needs 2 items, stack has 1 item or is empty')
    elif not isinstance(tos(), int):
        abort('Nb. of bits to shift must be an integer')
    elif not isinstance(nos(), int):
        abort('Nb. to shift must be an integer')
    else:
        i = dpop()
        n = dpop()
        exec('dpush(n ' + op +' i)')
#
#============================
#
def k_lshift():                  # ( n i -- n ) shift left n by i bits
    op = '<<'
    k_commonshift(op)
#
#============================
#
def k_rshift():                  # ( n i -- n ) shift right n by i bits
    op = '>>'
    k_commonshift(op)
#
#============================
#
#   Kernel Assignment definitions
#
#============================
#
def k_commonassign(op):
    if len(dstack) < 2 :
        abort('Assignment "' + op + '" needs 2 items, stack has 1 item or is empty')
    elif not isinstance(tos(),int):
        abort('Index of variable is not an integer')
    elif tos() < 0 or tos() not in range (len(ExecList)) :
        abort('Index out of execution list range 0:' + str(len(ExecList)))
    elif not str(ExecList[tos()+1][CFA]) == 'doLit()' and not str(ExecList[tos()+1][CFA]) == 'doLitx()':
        abort('"' + str(ExecList[tos()][PFA]) + '"' + ' is not a variable, no assignment allowed')
    else:
        exec('ExecList[tos()+1][PFA]' + op + ' nos()')
        k_ddrop()
#
#============================
#
def k_store():                   # ( idx n -- ) store n to var[idx]: variable with index idx
    op = '='
    k_commonassign(op)
#
#============================
#
def k_plusstore():               # ( idx n -- ) var[idx] += n
    op = '+='
    k_commonassign(op)
#
#============================
#
def k_minusstore():              # ( idx n -- ) var[idx] -= n
    op = '-='
    k_commonassign(op)
#
#============================
#
def k_starstore():               # (idx n -- ) var[idx] *= n
    op = '*='
    k_commonassign(op)
#
#============================
#
def k_slashstore():               # (idx n -- ) var[idx] /= n
    op = '/='
    k_commonassign(op)
#
#============================
#
def k_dblslashstore():            # (idx n -- ) var[idx] //= n
    op = '//='
    k_commonassign(op)
#
#============================
#
def k_remstore():                 # (idx n -- ) var[idx] %= n
    op = '%='
    k_commonassign(op)
#
#============================
#
def k_dblstarstore():               # (idx n -- ) var[idx] **= n
    op = '**='
    k_commonassign(op)
#
#============================
#
#   Kernel Index Register definitions
#
#============================
#
def k_setI():                    # ( n -- ) pop TOS to I
    global I
    if not isinstance(tos(), int):
        abort('Index value must be an integer')
    I = dpop()

#============================
def k_setJ():                    # ( n -- ) pop TOS to J
    global J
    if not isinstance(tos(), int):
        abort('Index value must be an integer')
    J = dpop()
    
#============================
def k_setK():                    # ( n -- ) pop TOS to K
    global K
    if not isinstance(tos(), int):
        abort('Index value must be an integer')
    K = dpop()

#============================
def k_I():                       # ( -- n ) push I
    global I
    dpush(I)

#============================
def k_J():                       # ( -- n ) push J
    global J
    dpush(J)

#============================
def k_K():                       # ( -- n ) push K
    global K
    dpush(K)
    
#============================
def k_incI():                    # ( -- ) I += 1
    global I
    I += 1

#============================
def k_incJ():                    # ( -- ) J += 1
    global J
    J += 1

#============================
def k_incK():                    # ( -- ) K += 1
    global K
    K += 1
    
#============================
def k_decI():                    # ( -- ) I -= 1
    global I
    I -= 1

#============================
def k_decJ():                    # ( -- ) J -= 1
    global J
    J -= 1
    
#============================
def k_decK():                    # ( -- ) K -= 1
    global K
    K -= 1

#============================
def k_Iloop():                   # ( idx -- ) execute word with index idx I times
    global I
    if not isinstance(tos(), (int)) :
        abort('Index of word for "iloop" must be of type int')
    elif tos() < 0 or tos() not in range (len(ExecList)) :
        abort('Index out of execution list range 0:' + str(len(ExecList)))
    else:
        idx = dpop()
    for i in range(I) :
        dpush(idx)
        k_execidx()
        
#============================
def k_Jloop():                   # ( idx -- ) execute word with index idx J times
    global J
    if not isinstance(tos(), (int)) :
        abort('Index of word for "jloop" must be of type int')
    elif tos() < 0 or tos() not in range (len(ExecList)) :
        abort('Index out of execution list range 0:' + str(len(ExecList)))
    else:
        idx = dpop()
    for i in range(J) :
        dpush(idx)
        k_execidx()

#============================
def k_Kloop():                   # ( idx -- ) execute word with index idx K times
    global K
    if not isinstance(tos(), (int)) :
        abort('Index of word for "kloop" must be of type int')
    elif tos() < 0 or tos() not in range (len(ExecList)) :
        abort('Index out of execution list range 0:' + str(len(ExecList)))
    else:
        idx = dpop()
    for i in range(K) :
        dpush(idx)
        k_execidx()
#
#============================
#
def k_list():               # ( str -- list ) create list from string str: [item1,item2,...]
    if len(dstack) == 0 :
        abort('Missing argument for "list"')
    elif not isinstance(tos(),str):
        abort('Argument for "list" must be a string')
    else:
        lst = dpop()
        try:
            dpush(eval('['+lst+']'))
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            dpush(lst)
            abort(str(e))
#
#============================
#
def k_listcre():            # ( "[]" item1 item2 ... itemn -- list ) create a list from items
    if len(dstack) == 0 :
        abort('Missing arguments for "listcre"')
    else:
        lst = []
        while tos() != "[]" :
            lst.append(dpop())
            if len(dstack) == 0 :
                lst.reverse()
                dpush(lst)
                return
        dpop()
        lst.reverse()
        dpush(lst)
#
#============================
#
def k_listexp():            # ( list -- item1 item2 ... itemn ) expand list of items 
    if len(dstack) == 0 :
        abort('Missing argument for "listexp"')
    elif not isinstance(tos(),list):
        abort('Argument for "listexp" must be a list')
    else:
        lst = dpop()
        for i in range(len(lst)) :
            dpush(lst[i])
#
#============================
#
def k_append():             # ( list item -- list ) append item to list
    if len(dstack) < 2  :
        abort('Missing arguments for "append"')
    else:
        try:
            nos().append(tos())
            k_drop()
        except (SyntaxError,ValueError,TypeError,AttributeError) as e:
            abort(str(e))
#
#============================
#
def k_clear():             # ( list -- [] ) clear list
    if len(dstack) < 1  :
        abort('Missing argument for "clear"')
    else:
        try:
            tos().clear()
        except(TypeError,AttributeError) as e:
            abort(str(e))
#
#============================
#
def k_copy():             # ( list -- list listcopy) return original and shallow copy of list
    if len(dstack) < 1  :
        abort('Missing argument for "copy"')
    else:
        try:
            dpush(tos().copy())
        except(TypeError,AttributeError) as e:
            abort(str(e))
#
#============================
#
def k_count():             # ( list value -- n ) count instances of value in list
    if len(dstack) < 2  :
        abort('Missing arguments for "count"')
    else:
        try:
            dpush(nos().count(tos()))
            k_rotl()
            k_ddrop()
        except (TypeError,ValueError,AttributeError) as e:
            abort(str(e))
#
#============================
#
def k_extend():             # ( list iterable -- list ) extend list with iterable
    if len(dstack) < 2  :
        abort('Missing arguments for "extend"')
    elif not isinstance(nos(),list):
        abort('First argument for "extend" must be a list')
    else:
        try:
            nos().extend(tos())
            k_drop()
        except TypeError as e:
            abort(str(e))
#
#============================
#
def k_index():             # ( list item -- index ) return index of item in list
    if len(dstack) < 2  :
        abort('Missing arguments for "index"')
    else:
        try:
            dpush(nos().index(tos()))
            k_rotl()
            k_ddrop()
        except (TypeError,ValueError,AttributeError) as e:
            abort(str(e))
#
#============================
#
def k_insert():             # ( list index item -- list ) insert item before index in list
    if len(dstack) < 3  :
        abort('Missing arguments for "index"')
    elif not isinstance(nos(),int):
        abort('Index to insert item must be an integer')
    else:
        try:
            dstack[-3].insert(nos(),tos())
            k_ddrop()
        except (TypeError,ValueError,IndexError,AttributeError) as e:
            abort(str(e))
#
#============================
#
def k_len():             # ( list -- n ) return lenght of list
    if len(dstack) < 1  :
        abort('Missing argument for "len"')
    else:
        try:
            dpush(len(tos()))
            k_nip()
        except (TypeError,AttributeError) as e:
            abort(str(e))
#
#============================
#
def k_pop():             # ( list -- list item ) pop last item of list
    if len(dstack) < 1  :
        abort('Missing argument for "pop"')
    else:
        try:
            dpush(tos().pop())
        except (TypeError,IndexError,AttributeError,KeyError) as e:
            abort(str(e))
#
#============================
#
def k_popidx():             # ( list index -- list item ) pop item at index of list
    if len(dstack) < 2  :
        abort('Missing arguments for "popidx"')
    else:
        try:
            dpush(nos().pop(tos()))
            k_swap()
            k_drop()
        except (TypeError,IndexError,AttributeError) as e:
            abort(str(e))
#
#============================
#
def k_remove():              # ( list item -- list ) remove item from list
    if len(dstack) < 2  :
        abort('Missing arguments for "remove"')
    else:
        try:
            nos().remove(tos())
        except (TypeError,IndexError,AttributeError,ValueError,KeyError) as e:
            abort(str(e))
#
#============================
#
def k_reverse():              # ( list -- list ) reverse list in place
    if len(dstack) < 1  :
        abort('Missing argument for "reverse"')
    else:
        try:
            tos().reverse()
        except (TypeError,AttributeError) as e:
            abort(str(e))
#
#============================
#
def k_sortasc():              # ( list -- list ) sort list in ascending order
    if len(dstack) < 1  :
        abort('Missing argument for "sortasc"')
    else:
        try:
            tos().sort()
        except (TypeError,AttributeError) as e:
            abort(str(e))
#
#============================
#
def k_sortdes():              # ( list -- list ) sort list in descending order
    if len(dstack) < 1  :
        abort('Missing argument for "sortdes"')
    else:
        try:
            tos().sort(reverse=True)
        except (TypeError,AttributeError) as e:
            abort(str(e))
#
#============================
#
def k_si():                     # ( list -- list item ) extract item at index given in register I
    global I
    if len(dstack) == 0 :
        abort('Missing argument for "s[i]"')
    else:
        try:
            dpush(tos()[I])
        except(TypeError,ValueError,AttributeError,KeyError,IndexError) as e:
            abort(str(e))
#
#============================
#
def k_sij():                     # ( list -- list slice ) extract slice given in registers I:J
    global I,J
    if len(dstack) == 0 :
        abort('Missing argument for "s[i:j]"')
    else:
        try:
            dpush(tos()[I:J])
        except(TypeError,ValueError,AttributeError,KeyError,IndexError) as e:
            abort(str(e))
#
#============================
#
def k_siend():                     # ( list -- list slice ) extract slice starting at I until end of list
    global I,J
    if len(dstack) == 0 :
        abort('Missing argument for "s[i:]"')
    else:
        try:
            dpush(tos()[I:])
        except(TypeError,ValueError,AttributeError,KeyError,IndexError) as e:
            abort(str(e))
#
#============================
#
def k_sjstart():                     # ( list -- list slice ) extract slice from start until J
    global I,J
    if len(dstack) == 0 :
        abort('Missing argument for "s[:j]"')
    else:
        try:
            dpush(tos()[:J])
        except(TypeError,ValueError,AttributeError,KeyError,IndexError) as e:
            abort(str(e))
#
#============================
#
def k_sijsecond():                     # ( list -- list item ) extract item at J from item at I
    global I,J
    if len(dstack) == 0 :
        abort('Missing argument for "s[i][j]"')
    else:
        try:
            dpush(tos()[I][J])
        except(TypeError,ValueError,AttributeError,KeyError,IndexError) as e:
            abort(str(e))
#
#============================
#
def k_sijkthird():                     # ( list -- list item ) extract item at K from item at J from item at I
    global I,J,K
    if len(dstack) == 0 :
        abort('Missing argument for "s[i][j][k]"')
    else:
        try:
            dpush(tos()[I][J][K])
        except(TypeError,ValueError,AttributeError,KeyError,IndexError) as e:
            abort(str(e))
#
#============================
#
def k_deli():                     # ( list -- list ) delete item at index given in register I
    global I
    if len(dstack) == 0 :
        abort('Missing argument for "del[i]"')
    else:
        try:
            del tos()[I]
        except(TypeError,ValueError,AttributeError,KeyError,IndexError) as e:
            abort(str(e))
#
#============================
#
def k_delij():                     # ( list -- list ) delete slice given in registers I:J
    global I,J
    if len(dstack) == 0 :
        abort('Missing argument for "del[i:j]"')
    else:
        try:
            del tos()[I:J]
        except(TypeError,ValueError,AttributeError,KeyError,IndexError) as e:
            abort(str(e))
#
#============================
#
def k_deliend():                     # ( list -- list ) delete slice starting at I until end of list
    global I,J
    if len(dstack) == 0 :
        abort('Missing argument for "del[i:]"')
    else:
        try:
            del tos()[I:]
        except(TypeError,ValueError,AttributeError,KeyError,IndexError) as e:
            abort(str(e))
#
#============================
#
def k_deljstart():                     # ( list -- list ) delete slice from start until J
    global I,J
    if len(dstack) == 0 :
        abort('Missing argument for "del[:j]"')
    else:
        try:
            del tos()[:J]
        except(TypeError,ValueError,AttributeError,KeyError,IndexError) as e:
            abort(str(e))
#
#============================
#
def k_delijsecond():                     # ( list -- list ) delete item at J from item at I
    global I,J
    if len(dstack) == 0 :
        abort('Missing argument for "del[i][j]"')
    else:
        try:
            del tos()[I][J]
        except(TypeError,ValueError,AttributeError,KeyError,IndexError) as e:
            abort(str(e))
#
#============================
#
def k_delijkthird():                     # ( list -- list ) delete item at K from item at J from item at I
    global I,J,K
    if len(dstack) == 0 :
        abort('Missing argument for "del[i][j][k]"')
    else:
        try:
            del tos()[I][J][K]
        except(TypeError,ValueError,AttributeError,KeyError,IndexError) as e:
            abort(str(e))
#
#============================
#
def k_dict():               # ( str -- dict ) create dictionary from string str: [item1,item2,...]
    if len(dstack) == 0 :
        abort('Missing argument for "dict"')
    elif not isinstance(tos(),str):
        abort('Argument for "dict" must be a string')
    else:
        dct = dpop()
        try:
            dpush(eval('{'+dct+'}'))
        except (SyntaxError,TypeError,ValueError,NameError,KeyError) as e:
            dpush(dct)
            abort(str(e))
#
#============================
#
def k_dictcre():            # ( keylist valuelist -- dict ) create dictionary from list of keys & values
    if len(dstack) < 2 :
        abort('Missing arguments for "dictcre"')
    elif not isinstance(tos(),list):
        abort('Argument for list of values must be a list')
    elif not isinstance(nos(),list):
        abort('Argument for list of keys must be a list')
    elif len(tos()) != len(nos()) :
        abort('Lenght of list of keys must be equal to lenght of list of values')
    else:
        dictx = {}
        values = dpop()
        keys = dpop()
        for i in range(len(keys)) :
            newentry = {keys[i]:values[i]}
            dictx.update(newentry)
        dpush(dictx)
#
#============================
#
def k_dictexp():                # ( dict -- keylist valuelist ) expand dictionary to list of keys & values
    if len(dstack) < 1 :
        abort('Missing argument for "dictexp"')
    elif not isinstance(tos(),dict):
        abort('Argument for "dictexp" must be a dictionary')
    else:
        dictx = dpop()
        keylist = list(dictx)
        valuelist = list(dictx.values())
        dpush(keylist)
        dpush(valuelist)
#
#============================
#
def k_get():                    # ( dict key -- value ) get value from key
    if len(dstack) < 2 :
        abort('Missing arguments for "get"')
    elif not isinstance(nos(),dict):
        abort('Argument for "get" must be a dictionary')
    else:
        try:
            key = dpop()
            dictx = dpop()
            dpush(dictx.get(key,None))
        except(TypeError,ValueError) as e:
            dpush(dictx)
            dpush(key)
            abort(str(e))
#
#============================
#
def k_items():                    # ( dict -- list ) return a list of all dict items as tuples (key,value)
    if len(dstack) < 1 :
        abort('Missing argument for "items"')
    elif not isinstance(tos(),dict):
        abort('Argument for "items" must be a dictionary')
    else:
        try:
            dictx = dpop()
            dpush(list(dictx.items()))
        except(TypeError,AttributeError) as e:
            dpush(dictx)
            abort(str(e))
#
#============================
#
def k_popkey():                    # ( dict key -- dict value ) return and remove value for key
    if len(dstack) < 2 :
        abort('Missing arguments for "popkey"')
    elif not isinstance(nos(),dict):
        abort('Argument for "popkey" must be a dictionary')
    else:
        try:
            key = dpop()
            dpush(tos().pop(key,None))
        except(TypeError,ValueError,KeyError) as e:
            dpush(key)
            abort(str(e))
#
#============================
#
def k_popitem():                    # ( dict -- dict item ) return and remove last item (Python 3.7+)
    if len(dstack) < 1 :
        abort('Missing argument for "popitem"')
    elif not isinstance(tos(),dict):
        abort('Argument for "popitem" must be a dictionary')
    else:
        try:
            dpush(tos().popitem())
        except(TypeError,ValueError,KeyError) as e:
            abort(str(e))
#
#============================
#
def k_setdefault():                    # ( dict key value -- dict ) insert the pair key:value
                                       # 
    if len(dstack) < 3 :
        abort('Missing arguments for "setdefault"')
    elif not isinstance(dstack[-3],dict):
        abort('First argument for "setdefault" must be a dictionary')
    else:
        try:
            val = dpop()
            key = dpop()
            tos().setdefault(key,val)
            
        except(TypeError,ValueError,KeyError) as e:
            dpush(key)
            dpush(val)
            abort(str(e))
#
#===========================
#
def k_update():                     # ( dict seq -- dict ) update dict with sequence seq
    if len(dstack) < 2 :
        abort('Missing arguments for "update"')
    elif not isinstance(nos(),(dict,set)):
        abort('First argument for "update" must be a dictionary')
    else:
        try:
            seq = dpop()
            tos().update(seq)
        except(TypeError,ValueError,KeyError) as e:
            dpush(seq)
            abort(str(e))

#
#============================
#
def k_tuple():               # ( str -- tuple ) create tuple from string str
    if len(dstack) == 0 :
        abort('Missing argument for "tuple"')
    elif not isinstance(tos(),str):
        abort('Argument for "tuple" must be a string')
    else:
        tup = dpop()
        try:
            dpush(eval('('+tup+')'))
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            dpush(tup)
            abort(str(e))
#
#============================
#
def k_tupcre():               # ( valuelist -- tuple ) create tuple from list of values
    if len(dstack) == 0 :
        abort('Missing argument for "tupcre"')
    elif not isinstance(tos(),list):
        abort('Argument for "tupcre" must be a list')
    else:
        lst = dpop()
        try:
            dpush(tuple(lst))
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            dpush(lst)
            abort(str(e))
#
#============================
#
def k_tupexp():               # ( tuple -- valuelist ) expand tuple to list of values
    if len(dstack) == 0 :
        abort('Missing argument for "tupexp"')
    elif not isinstance(tos(),tuple):
        abort('Argument for "tupexp" must be a tuple')
    else:
        tup = dpop()
        try:
            dpush(list(tup))
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            dpush(tup)
            abort(str(e))
#
#============================
#
def k_setstr():               # ( str -- set ) create set from single string
    if len(dstack) == 0 :
        abort('Missing argument for "setstr"')
    elif not isinstance(tos(),str):
        abort('Argument for "setstr" must be a string')
    else:
        st = dpop()
        try:
            dpush(set(st))
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            dpush(st)
            abort(str(e))
#
#============================
#
def k_set():               # ( stritems -- set ) create set from string of multiple items
    if len(dstack) == 0 :
        abort('Missing argument for "set"')
    elif not isinstance(tos(),str):
        abort('Argument for "set" must be a string')
    else:
        st = dpop()
        try:
            dpush(eval('{'+st+'}'))
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            dpush(st)
            abort(str(e))
#
#============================
#
def k_setcre():               # ( valuelist -- set ) create set from list of values
    if len(dstack) == 0 :
        abort('Missing argument for "setcre"')
    elif not isinstance(tos(),list):
        abort('Argument for "setcre" must be a list')
    else:
        lst = dpop()
        try:
            dpush(set(lst))
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            dpush(lst)
            abort(str(e))
#
#============================
#
def k_setexp():               # ( set -- valuelist ) expand set to list of values
    if len(dstack) == 0 :
        abort('Missing argument for "setexp"')
    elif not isinstance(tos(),set):
        abort('Argument for "setexp" must be a set')
    else:
        st = dpop()
        try:
            dpush(list(st))
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            dpush(st)
            abort(str(e))

#
#============================
#
def k_add():                # ( set item -- set ) add item to set
    if len(dstack) < 2 :
        abort('Missing arguments for "add"')
    elif not isinstance(nos(),set):
        abort('First argument for "add" must be a set')
    else:
        try:
            nos().add(tos())
            k_drop()
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_difference():                # ( set1 set2 -- set ) return set of differences between set1 and set2
    if len(dstack) < 2 :
        abort('Missing arguments for "difference"')
    elif not isinstance(nos(),set) or not isinstance(tos(),set):
        abort('Arguments for "difference" must be sets')
    else:
        try:
            dpush(nos().difference(tos()))
            k_nip()
            k_nip()
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_sdifference():                # ( set1 set2 -- set ) return set of symmetric differences between set1 and set2
    if len(dstack) < 2 :
        abort('Missing arguments for "sdifference"')
    elif not isinstance(nos(),set) or not isinstance(tos(),set):
        abort('Arguments for "sdifference" must be sets')
    else:
        try:
            dpush(nos().symmetric_difference(tos()))
            k_nip()
            k_nip()
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_udifference():                # ( set1 set2 -- set ) differences update: remove all elements of set2 from set1
    if len(dstack) < 2 :
        abort('Missing arguments for "udifference"')
    elif not isinstance(nos(),set) or not isinstance(tos(),set):
        abort('Arguments for "udifference" must be sets')
    else:
        try:
            nos().difference_update(tos())
            k_drop()
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_discard():                # ( set item -- set ) remove item from set
    if len(dstack) < 2 :
        abort('Missing arguments for "discard"')
    elif not isinstance(nos(),set):
        abort('First argument for "discard" must be a set')
    else:
        try:
            nos().discard(tos())
            k_drop()
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_intersection():                # ( set1 set2 -- set ) return intersection of set1 and set2
    if len(dstack) < 2 :
        abort('Missing arguments for "intersection"')
    elif not isinstance(nos(),set) or not isinstance(tos(),set):
        abort('Arguments for "intersection" must be sets')
    else:
        try:
            dpush(nos().intersection(tos()))
            k_nip()
            k_nip()
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_isdisjoint():                # ( set1 set2 --  ) ZF=1 if intersection of set1 with set2 is null
    global ZF
    if len(dstack) < 2 :
        abort('Missing arguments for "isdisjoint"')
    elif not isinstance(nos(),set) or not isinstance(tos(),set):
        abort('Arguments for "isdisjoint" must be sets')
    else:
        try:
            if nos().isdisjoint(tos()):
                ZF = 1
            else:
                ZF = 0
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_issubset():                # ( set1 set2 --  ) ZF=1 if set1 is a subset of set2
    global ZF
    if len(dstack) < 2 :
        abort('Missing arguments for "issubset"')
    elif not isinstance(nos(),set) or not isinstance(tos(),set):
        abort('Arguments for "issubset" must be sets')
    else:
        try:
            if nos().issubset(tos()):
                ZF = 1
            else:
                ZF = 0
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_issuperset():                # ( set1 set2 --  ) ZF=1 if set1 is a superset of set2
    global ZF
    if len(dstack) < 2 :
        abort('Missing arguments for "issuperset"')
    elif not isinstance(nos(),set) or not isinstance(tos(),set):
        abort('Arguments for "issuperset" must be sets')
    else:
        try:
            if nos().issuperset(tos()):
                ZF = 1
            else:
                ZF = 0
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_union():                # ( set1 set2 -- set ) return union of set1 and set2
    if len(dstack) < 2 :
        abort('Missing arguments for "union"')
    elif not isinstance(nos(),set) or not isinstance(tos(),set):
        abort('Arguments for "union" must be sets')
    else:
        try:
            dpush(nos().union(tos()))
            k_nip()
            k_nip()
        except (SyntaxError,TypeError,ValueError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_capitalize():                # ( str -- str ) return a string with first char capitalized, the rest to lowercase
    if len(dstack) < 1 :
        abort('Missing argument for "capitalize"')
    else:
        try:
            dpush(tos().capitalize())
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_casefold():                # ( str -- str ) return a string with all chars lowercase
    if len(dstack) < 1 :
        abort('Missing argument for "casefold"')
    else:
        try:
            dpush(tos().casefold())
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_center():                 # ( str width -- str ) return centered string of lenght width, blank padded
    if len(dstack) < 2 :
        abort('Missing arguments for "center"')
    else:
        try:
            dpush(nos().center(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_centerfill():                 # ( str width fill -- str ) return centered string of lenght width, fill char padded
    if len(dstack) < 3 :
        abort('Missing arguments for "centerfill"')
    else:
        try:
            dpush(dstack[-3].center(nos(),tos()))
            k_nip()
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_count():                  # ( str substr -- n ) return count of substr occurences in str
    if len(dstack) < 2 :
        abort('Missing arguments for "count"')
    else:
        try:
            dpush(nos().count(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_emptystr():                     # ( -- "" ) leave an empty string
    dpush("")
#
#===========================
#
def k_endswith():                  # ( str suffix -- ) ZF=1 if str ends with suffix
    global ZF
    if len(dstack) < 2 :
        abort('Missing arguments for "endswith"')
    else:
        try:
            if nos().endswith(tos()) :
                ZF = 1
            else:
                ZF = 0
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_expandtabs():                  # ( str tabsize -- str ) return string with tabs expanded
    if len(dstack) < 2 :
        abort('Missing arguments for "expandtabs"')
    else:
        try:
            dpush(nos().expandtabs(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_find():                  # ( str substr -- n ) return lowest index of substr found in str, -1 if not found
    if len(dstack) < 2 :
        abort('Missing arguments for "find"')
    else:
        try:
            dpush(nos().find(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_iscommon(op,fnop):                # common routine for isMETHOD
    global ZF
    if len(dstack) < 1 :
        abort('Missing argument for "'+op+'"')
    else:
        try:
            if eval(fnop) :
                ZF = 1
            else:
                ZF = 0
            k_drop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_isalnum():                # ( str -- ) ZF=1 if all chars in str are alphanumeric
    op = 'isalnum'
    fnop = "tos().isalnum()"
    k_iscommon(op,fnop)
#
#============================
#
def k_isalpha():                # ( str -- ) ZF=1 if all chars in str are alphabetic
    op = 'isalpha'
    fnop = "tos().isalpha()"
    k_iscommon(op,fnop)
#
#============================
#
def k_isascii():                # ( str -- ) ZF=1 if all chars in str are ASCII or str is empty
    op = 'isascii'
    fnop = "tos().isascii()"
    k_iscommon(op,fnop)
#
#============================
#
def k_isdecimal():                # ( str -- ) ZF=1 if all chars in str are decimal
    op = 'isdecimal'
    fnop = "tos().isdecimal()"
    k_iscommon(op,fnop)
#
#============================
#
def k_isdigit():                # ( str -- ) ZF=1 if all chars in str are digits
    op = 'isdigit'
    fnop = "tos().isdigit()"
    k_iscommon(op,fnop)
#
#============================
#
def k_islower():                # ( str -- ) ZF=1 if all chars in str are lowercase
    op = 'islower'
    fnop = "tos().islower()"
    k_iscommon(op,fnop)
#
#============================
#
def k_isnumeric():                # ( str -- ) ZF=1 if all chars in str are numeric
    op = 'isnumeric'
    fnop = "tos().isnumeric()"
    k_iscommon(op,fnop)
#
#============================
#
def k_isprintable():                # ( str -- ) ZF=1 if all chars in str are printable or str is empty
    op = 'isprintable'
    fnop = "tos().isprintable()"
    k_iscommon(op,fnop)
#
#============================
#
def k_isspace():                # ( str -- ) ZF=1 if all chars in str are whitespaces
    op = 'isspace'
    fnop = "tos().isspace()"
    k_iscommon(op,fnop)
#
#============================
#
def k_istitle():                # ( str -- ) ZF=1 if str is titlecased
    op = 'istitle'
    fnop = "tos().istitle()"
    k_iscommon(op,fnop)
#
#============================
#
def k_isupper():                # ( str -- ) ZF=1 if all chars in str are uppercase
    op = 'isupper'
    fnop = "tos().isupper()"
    k_iscommon(op,fnop)
#
#============================
#
def k_join():                # ( str seq -- str ) return a string concatenated with all the strings in seq
    if len(dstack) < 2 :
        abort('Missing arguments for "join"')
    else:
        try:
            dpush(nos().join(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_ljust():                 # ( str width -- str ) return left justified string of lenght width, space padded
    if len(dstack) < 2 :
        abort('Missing arguments for "ljust"')
    else:
        try:
            dpush(nos().ljust(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_ljustfill():                 # ( str width fill -- str ) return left justified string of lenght width, fill char padded
    if len(dstack) < 3 :
        abort('Missing arguments for "ljustfill"')
    else:
        try:
            dpush(dstack[-3].ljust(nos(),tos()))
            k_nip()
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_lower():                # ( str -- str ) return a string with all chars converted to lowercase
    if len(dstack) < 1 :      # NB: casefold works similarly but more "aggressive", see Python docs
        abort('Missing argument for "lower"')
    else:
        try:
            dpush(tos().lower())
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_lstrip():                 # ( str -- str ) return a string with all leading spaces removed
    if len(dstack) < 1 :
        abort('Missing argument for "lstrip"')
    else:
        try:
            dpush(tos().lstrip())
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_lstripchr():                 # ( str strchr -- str ) return a string with all leading strchr chars combinations removed 
    if len(dstack) < 2 :
        abort('Missing arguments for "lstripchr"')
    else:
        try:
            dpush(nos().lstrip(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_partition():                 # ( str strsep -- tuple ) return a 3-element tuple: part before separator, separator itself, part after separator
    if len(dstack) < 2 :           # if separator not found, return tuple: (originalstr,'','')
        abort('Missing arguments for "partition"')
    else:
        try:
            dpush(nos().partition(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_removeprefix():                 # ( str strpref -- str ) return a string with strpref removed
    if len(dstack) < 2 :
        abort('Missing arguments for "removeprefix"')
    else:
        try:
            dpush(nos().removeprefix(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_removesuffix():                 # ( str strsuff -- str ) return a string with strsuff removed
    if len(dstack) < 2 :
        abort('Missing arguments for "removesuffix"')
    else:
        try:
            dpush(nos().removesuffix(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_replace():                 # ( str oldstr newstr -- str ) return a string with all occurences of oldstr replaced by newstr
    if len(dstack) < 3 :
        abort('Missing arguments for "replace"')
    else:
        try:
            dpush(dstack[-3].replace(nos(),tos()))
            k_nip()
            k_nip()
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_replacecnt():                 # ( str oldstr newstr count -- str ) return a string with count occurences of oldstr replaced by newstr
    if len(dstack) < 4 :
        abort('Missing arguments for "replacecnt"')
    else:
        try:
            dpush(dstack[-4].replace(dstack[-3],nos(),tos()))
            k_nip()
            k_nip()
            k_nip()
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_rfind():                  # ( str substr -- n ) return highest index of substr found in str, -1 if not found
    if len(dstack) < 2 :
        abort('Missing arguments for "rfind"')
    else:
        try:
            dpush(nos().rfind(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_rjust():                 # ( str width -- str ) return right justified string of lenght width, space padded
    if len(dstack) < 2 :
        abort('Missing arguments for "rjust"')
    else:
        try:
            dpush(nos().rjust(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_rjustfill():                 # ( str width fill -- str ) return right justified string of lenght width, fill char padded
    if len(dstack) < 3 :
        abort('Missing arguments for "rjustfill"')
    else:
        try:
            dpush(dstack[-3].rjust(nos(),tos()))
            k_nip()
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_rpartition():                # ( str strsep -- tuple ) split string at the last occurence of strsep
                                   # return a 3-element tuple: part before separator, separator itself, part after separator
    if len(dstack) < 2 :           # if separator not found, return tuple: (originalstr,'','')
        abort('Missing arguments for "rpartition"')
    else:
        try:
            dpush(nos().rpartition(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_rsplit():                 # ( str strsep maxsplit -- list ) return list of maximum maxsplit words separated by strsep, starting from right
                                # if maxsplit =-1 , all words separated by strsep are returned
    if len(dstack) < 3 :
        abort('Missing arguments for "rsplit"')
    else:
        if nos() == "None" :
            dstack[-2] = None
        try:
            dpush(dstack[-3].rsplit(nos(),tos()))
            k_nip()
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_rstrip():                 # ( str -- str ) return a string with all trailing spaces removed
    if len(dstack) < 1 :
        abort('Missing argument for "rstrip"')
    else:
        try:
            dpush(tos().rstrip())
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_rstripchr():                 # ( str strchr -- str ) return a string with all trailing strchr chars combinations removed 
    if len(dstack) < 2 :
        abort('Missing arguments for "rstripchr"')
    else:
        try:
            dpush(nos().rstrip(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_split():                 # ( str strsep maxsplit -- list ) return list of maximum maxsplit words separated by strsep
                                # if maxsplit =-1 , all words separated by strsep are returned
    if len(dstack) < 3 :
        abort('Missing arguments for "split"')
    else:
        if nos() == "None" :
            dstack[-2] = None
        try:
            dpush(dstack[-3].split(nos(),tos()))
            k_nip()
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_splitlines():                 # ( str -- list ) return list of lines split at line breaks without including line breaks
    if len(dstack) < 1 :
        abort('Missing argument for "splitlines"')
    else:
        try:
            dpush(tos().splitlines())
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_splitlnbrk():                 # ( str -- list ) return list of lines split at line breaks, including line breaks
    if len(dstack) < 1 :
        abort('Missing argument for "splitlnbrk"')
    else:
        try:
            dpush(tos().splitlines(keepends=True))
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_startswith():                  # ( str prefix -- ) ZF=1 if str starts with prefix
    global ZF
    if len(dstack) < 2 :
        abort('Missing arguments for "startswith"')
    else:
        try:
            if nos().startswith(tos()) :
                ZF = 1
            else:
                ZF = 0
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_strip():                 # ( str -- str ) return a string with all spaces removed
    if len(dstack) < 1 :
        abort('Missing argument for "strip"')
    else:
        try:
            dpush(tos().strip())
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_stripchr():                 # ( str strchr -- str ) return a string with all strchr chars combinations removed 
    if len(dstack) < 2 :
        abort('Missing arguments for "stripchr"')
    else:
        try:
            dpush(nos().strip(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_swapcase():                 # ( str -- str ) return a string with uppercase chars converted to lovercase and vice versa
    if len(dstack) < 1 :
        abort('Missing argument for "swapcase"')
    else:
        try:
            dpush(tos().swapcase())
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#===========================
#
def k_title():                 # ( str -- str ) return a titlecased string with words starting with uppercase
    if len(dstack) < 1 :
        abort('Missing argument for "title"')
    else:
        try:
            dpush(tos().title())
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))  
#
#============================
#
def k_upper():                # ( str -- str ) return a string with all chars converted to uppercase
    if len(dstack) < 1 :
        abort('Missing argument for "upper"')
    else:
        try:
            dpush(tos().upper())
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_zfill():                 # ( str width -- str ) return a string of lenght width left filled with "0" 
    if len(dstack) < 2 :
        abort('Missing arguments for "zfill"')
    else:
        try:
            dpush(nos().zfill(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_open():                       # ( filename filemode -- filehandle) open file 
    if len(dstack) < 2 :
        abort('Missing arguments for "open"')
    else:
        try:
            dpush(open(nos(),tos()))
            k_nip()
            k_nip()
        except (AttributeError,ValueError,TypeError,OSError) as e:
            abort(str(e))
        
#
#===========================
#
def k_read():                       # ( filehandle -- filecontent) read file 
    if len(dstack) < 1 :
        abort('Missing argument for "read"')
    else:
        try:
            dpush(tos().read())
            k_nip()
        except (AttributeError,ValueError,TypeError,OSError) as e:
            abort(str(e))
#
#===========================
#
def k_readline():                       # ( filehandle -- linecontent) read a single line from file 
    if len(dstack) < 1 :
        abort('Missing argument for "readline"')
    else:
        try:
            dpush(tos().readline())
            k_nip()
        except (AttributeError,ValueError,TypeError,OSError) as e:
            abort(str(e))
#
#===========================
#
def k_readlines():                       # ( filehandle -- list ) read all lines from file into list
    if len(dstack) < 1 :
        abort('Missing argument for "readlines"')
    else:
        try:
            dpush(tos().readlines())
            k_nip()
        except (AttributeError,ValueError,TypeError,OSError) as e:
            abort(str(e))
#
#===========================
#
def k_readsize():                       # ( filehandle size -- sizecontent ) read size bytes from file
    if len(dstack) < 2 :
        abort('Missing arguments for "readsize"')
    else:
        try:
            dpush(nos().read(tos()))
            k_nip()
            k_nip()
        except (AttributeError,ValueError,TypeError,OSError) as e:
            abort(str(e))
#
#===========================
#
def k_seek():                       # ( filehandle offset origin -- n ) file content pointer n = origin+offset
    if len(dstack) < 3 :            # origin=0 filestart ; origin=1 current file pointer ; origin=2 file end
        abort('Missing arguments for "seek"')
    else:
        try:
            dpush(dstack[-3].seek(nos(),tos()))
            k_nip()
            k_nip()
            k_nip()
        except (AttributeError,ValueError,TypeError,OSError) as e:
            abort(str(e))
#
#===========================
#
def k_tell():                       # ( filehandle -- n ) n = current file pointer
    if len(dstack) < 1 :
        abort('Missing argument for "tell"')
    else:
        try:
            dpush(tos().tell())
            k_nip()
        except (AttributeError,ValueError,TypeError,OSError) as e:
            abort(str(e))
#
#===========================
#
def k_write():                       # ( filehandle str -- n ) write str to file , n=nb. of chars written
    if len(dstack) < 2 :
        abort('Missing arguments for "write"')
    else:
        try:
            dpush(nos().write(tos()))
            k_nip()
            k_nip()
        except (AttributeError,ValueError,TypeError,OSError) as e:
            abort(str(e))
#
#===========================
#
def k_close():                       # ( filehandle -- ) close file 
    if len(dstack) < 1 :
        abort('Missing argument for "close"')
    else:
        try:
            tos().close()
            k_drop()
        except (AttributeError,ValueError,TypeError,OSError) as e:
            abort(str(e))
#
#===========================
#
def k_load():
    global CoreDef
    
    if len(CoreDef):
        wmsg=input('! Warning: all current definitions will be lost - proceed? (y/n): ')
        if wmsg == 'y' or wmsg == 'Y' :
            k_load_aux()
        else:
            return
    else:
        k_load_aux()
#============================        
def k_load_aux():                       # ( filename -- ) load ExecList & UserDict
    global ExecList, CoreDef, IdxRetJmp
    
    if len(dstack) < 1 :
        abort('Missing argument for "load"')
    elif not isinstance(tos(),str):
        abort('Filename must be of type string')
#    elif not tos().isalnum():
#        abort('Filename must be alphanumeric')
    else:
        try:
            f=open(tos()+'.rpp','r')
            lload=json.load(f)
            f.close()
            ExecList=lload[0]
            CoreDef=lload[1]
            IdxRetJmp = ExecList[-1][1]
            del ExecList[-1]
            lastentry = ['REPL()','REPL']
            ExecList.append(lastentry)
            print('  Definitions loaded:')
            for i,value in enumerate(CoreDef):
                print('   ',i,value)
            k_drop()
            REPL()
        except (AttributeError,ValueError,TypeError,OSError) as e:
            abort(str(e))
#
#===========================
#
def k_save():                       # ( filename -- ) save ExecList & UserDict 
    global IndSave, IdxRetJmp
    if len(dstack) < 1 :
        abort('Missing argument for "save"')
    elif not isinstance(tos(),str):
        abort('Filename must be of type string')
#    elif not tos().isalnum():
#        abort('Filename must be alphanumeric')
    else:
        if len(CoreDef) :
            lsave=[]
            lastret = ['IdxR',IdxRetJmp]
            ExecList.append(lastret)
            lsave.append(ExecList)
            lsave.append(CoreDef)
            try:
                f=open(tos()+'.rpp','w')
                json.dump(lsave,f)
                f.close()
                IndSave = len(CoreDef)
                print('Saved:',IndSave,'definitions to '+dpop()+'.rpp')
                del ExecList[-1]
            except (AttributeError,ValueError,TypeError,OSError) as e:
                abort(str(e))
        else:
            print('No definitions to save')
#
#===========================
#
def k_sdot():                       # ( -- ) save ExecList & UserDict to file "tempsave.rpp" ; substitute for Ctrl-S
    global IndSave, IdxRetJmp
    if len(CoreDef) :               # save only if there are already definitions made
        lsave=[]
        lastret = ['IdxR',IdxRetJmp]
        ExecList.append(lastret)
        lsave.append(ExecList)
        lsave.append(CoreDef)
        try:
            f=open('tempsave.rpp','w')
            json.dump(lsave,f)
            f.close()
            IndSave = len(CoreDef)
            print('Saved:',IndSave,'definitions to tempsave.rpp')
            del ExecList[-1]
        except (AttributeError,ValueError,TypeError,OSError) as e:
            abort(str(e))
    else:
        print('No definitions to save')
#
#===========================
#
def k_jsdump():                     # ( filename pyobj -- ) write Python object as JSON object to filename
    if len(dstack) < 2 :
        abort('Missing arguments for "jsdump"')
    elif not isinstance(nos(),str):
        abort('Filename must be of type string')
    else:
        try:
            f=open(nos(),'w')
            json.dump(tos(),f)
            f.close()
            k_ddrop()
        except (AttributeError,ValueError,TypeError,OSError) as e:
            abort(str(e))    
#
#===========================
#
def k_jsload():                     # ( filename -- pyobj )  load JSON object as Python object from filename
    if len(dstack) < 1 :
        abort('Missing argument for "jsload"')
    elif not isinstance(tos(),str):
        abort('Filename must be of type string')
    else:
        try:
            f=open(tos(),'r')
            dpush(json.load(f))
            f.close()
            k_nip()
        except (AttributeError,ValueError,TypeError,OSError,JSONDecodeError) as e:
            abort(str(e))  
#
#===========================
#
def k_jsdumps():                     # ( pyobj -- jsonstring ) code Python object to JSON string
    if len(dstack) < 1 :
        abort('Missing argument for "jsdumps"')
    else:
        try:
            dpush(json.dumps(tos()))
            k_nip()
        except (AttributeError,ValueError,TypeError) as e:
            abort(str(e))      
#
#===========================
#
def k_jsloads():                     # ( jsonstring -- pyobj ) code JSON string to Python object
    if len(dstack) < 1 :
        abort('Missing argument for "jsloads"')
    elif not isinstance(tos(),str):
        abort('JSON object must be of type string')
    else:
        try:
            dpush(json.loads(tos()))
            k_nip()
        except (AttributeError,ValueError,TypeError,JSONDecodeError) as e:
            abort(str(e)) 
#
#===========================
#
def k_all():                        # ( seq -- ) ZF=1 if all elements in seq are true or seq is empty
    global ZF
    if len(dstack) < 1 :
        abort('Missing argument for "all"')
    else:
        try:
            if all(tos()):
                ZF = 1
            else:
                ZF = 0
            k_drop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#===========================
#
def k_any():                        # ( seq -- ) ZF=1 if any element in seq is true; ZF=0 if seq is empty
    global ZF
    if len(dstack) < 1 :
        abort('Missing argument for "any"')
    else:
        try:
            if any(tos()):
                ZF = 1
            else:
                ZF = 0
            k_drop()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))    
#
#============================
#
def k_bin():                # ( n -- strbin ) convert integer n to binary string prefixed with '0b'
    if len(dstack) < 1 :
        abort('Missing argument for "bin"')
    else:
        try:
            dpush(bin(tos()))
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_chr():                # ( n -- strchr ) convert integer n to string representing the associated glyph
    if len(dstack) < 1 :
        abort('Missing argument for "chr"')
    else:
        try:
            dpush(chr(tos()))
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_complex():                # ( str -- n ) convert str to complex number n
    if len(dstack) < 1 :
        abort('Missing argument for "complex"')
    else:
        try:
            dpush(complex(tos()))
            k_nip()
        except (AttributeError,TypeError,NameError,ValueError) as e:
            abort(str(e))
#
#============================
#
def k_choose():              # ( idx1 idx2 -- ) if ZF=1 execute idx1, else idx2
                            # both idx must be valid indexes in ExecList, obtained with 'namedef
    global IP
    if not (isinstance(tos(), (int)) and isinstance(nos(), (int))) :
        abort('Indexes for "choose" must be of type int')
    elif (tos() < 0 or tos() not in range (len(ExecList))) or \
        (nos() < 0 or nos() not in range (len(ExecList))) :
        abort('Index idx1 or idx2 out of execution list range 0:' + str(len(ExecList)))
    else:
        idxf = dpop()
        idxt = dpop()
        rpush(IP)           # execute true/false branch & return by means of callee
        if ZF == True :
            IP = idxt
        else:
            IP = idxf            
#
#===========================
#
def k_deldef():             # ( defname -- ) delete definition defname from high level defs dictionary
    if len(dstack) < 1 :
        abort('Missing argument for "deldef"')
    elif not isinstance(tos(),str):
        abort('Argument for "deldef" must be a string')
    else:
        defval = CoreDef.pop(tos(),None)
        if defval :
            print('"'+tos()+'" at index',defval[0],'deleted')
            k_drop()
        else:
            abort('Definition "'+tos()+'" not found')
#
#===========================
#
def k_dellast():             # ( -- ) delete last definition ; shorten ExecList accordingly !
    global IP
    if len(CoreDef):
        tkname = CoreDef.popitem()
        print('"'+tkname[0]+'" at index',tkname[1][0],'deleted')
        del ExecList[tkname[1][0]:]
        ExecList.append(['REPL()','REPL'])
        IP = len(ExecList) - 2
    else:
        print('CoreDef empty, no definition to delete')
#
#===========================
#
def k_edit():                 # ( defname -- ) edit definition defname 
    if len(dstack) < 1 :
        abort('Missing argument for "edit"')
    elif not isinstance(tos(),str):
        abort('Argument for "edit" must be a string')
    else:
        print('  Warning: works only in Windows Command Prompt !')
        print('   Type Ctrl-M, cursor changes shape')
        print('   Use arrow keys to move cursor at beginning of displayed definition')
        print('   Hold Shift pressed, move right arrow to select entire definition')
        print('   Type Ctrl-Insert to copy selected text to clipboard, cursor moves back to input line')
        print('   Type Ctrl-V to paste clipboard to input line')
        print('   Edit input line , terminate as usually with "." plus Enter')
        k_pddef()
        
#    
#===========================
#  
def k_enumerate():          # ( seq -- list ) create a list of tuples of the form (count,value)
    if len(dstack) < 1 :
        abort('Missing argument for "enumerate"')
    else:
        try:
            dpush(list(enumerate(tos())))
            k_nip()
        except (AttributeError,TypeError,NameError,ValueError) as e:
            abort(str(e))
#
#============================
#
def k_evaluate():            # ( str -- item ) TOS = eval(str)
    if not isinstance(tos(), (str)) :
        abort('Item to evaluate must be a string')
    try:
        dpush(eval(tos()))
        k_nip()
    except (ZeroDivisionError,SyntaxError,NameError,TypeError,AttributeError) as e:
        abort(str(e))            
#
#============================
#
def k_execidx():             # (idx -- ) execute word with "idx" index & return
    global IP
    if not isinstance(tos(), (int)) :
        abort('Index of word for "execute" must be of type int')
    elif tos() < 0 or tos() not in range (len(ExecList)) :
        abort('Index out of execution list range 0:' + str(len(ExecList)))
    else:
        rpush(IP)
        IP = dpop()
#
#============================
#
def k_exec():                # ( str -- ... )  exec(str)
    try:
        err = tos()
        exec(dpop())
    except(ZeroDivisionError, SyntaxError, NameError, TypeError) as e:
        dpush(err)
        abort(str(e))
#
#============================
#
def k_float():                # ( str/int -- n ) convert string or integer to floating point number n
    if len(dstack) < 1 :
        abort('Missing argument for "float"')
    else:
        try:
            dpush(float(tos()))
            k_nip()
        except (AttributeError,TypeError,NameError,ValueError) as e:
            abort(str(e))

#
#===========================
#
def k_format():                 # ( formstr n  -- str ) convert value n to str according to format specification 
    if len(dstack) < 2 :
        abort('Missing arguments for "format"')
    else:
        try:
            dpush(nos().format(tos()))
            k_rotl()
            k_ddrop()
        except (AttributeError,TypeError,NameError,ValueError) as e:
            abort(str(e))
#
#============================
#
def k_hex():                # ( n -- strhex ) convert integer n to hexadecimal string prefixed with "0x"
    if len(dstack) < 1 :
        abort('Missing argument for "hex"')
    else:
        try:
            dpush(hex(tos()))
            k_nip()
        except (AttributeError,TypeError,NameError,ValueError) as e:
            abort(str(e))
#
#============================
#
def k_input():              # ( -- str ) read a line from input and convert data to a string
    try:
        dpush(input())
    except (EOFError) as e:
        abort(str(e)+'EOFError')    
#
#============================
#
def k_inputprompt():              # ( strprompt -- str ) write strprompt to standard output, then input line
    if len(dstack) < 1 :
        abort('Missing argument for "inputprompt"')
    else:
        try:
            dpush(input(tos()))
            k_nip()
        except (EOFError) as e:
            abort(str(e)+'EOFError')    
#
#============================
#
def k_int():                # ( str/n -- n ) convert str or number n to integer n
    if len(dstack) < 1 :
        abort('Missing argument for "int"')
    else:
        try:
            dpush(int(tos()))
            k_nip()
        except (AttributeError,TypeError,NameError,ValueError) as e:
            abort(str(e))
#
#============================
#
def k_intbase():                # ( str base -- n ) convert str to integer n according to base
    if len(dstack) < 2 :
        abort('Missing arguments for "intbase"')
    else:
        try:
            dpush(int(nos(),tos()))
            k_nip()
            k_nip()
        except (AttributeError,TypeError,NameError,ValueError) as e:
            abort(str(e))
#
#============================
#
def k_oct():                # ( n -- stroct ) convert integer n to octal string prefixed with "0O"
    if len(dstack) < 1 :
        abort('Missing argument for "oct"')
    else:
        try:
            dpush(oct(tos()))
            k_nip()
        except (AttributeError,TypeError,NameError,ValueError) as e:
            abort(str(e))
#
#============================
#
def k_ord():                # ( strchr -- n ) convert string representing one character to integer n
    if len(dstack) < 1 :
        abort('Missing argument for "ord"')
    else:
        try:
            dpush(ord(tos()))
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_quit():
    global IndSave
    if IndSave == len(CoreDef) and len(CoreDef) != 0 :
        print('RPPy ended; last saved:',IndSave,'definitions')
        exit (0)
    elif IndSave != 0 :
        print('Saved only',IndSave,'definitions from a total of',len(CoreDef))
        s = input('Quit anyway? (y/n):')
        if s == 'y' or s == 'Y' :
            print('RPPy ended;',len(CoreDef)-IndSave,'definitions not saved')
            exit(0)
        else:
            REPL()
    else:
        if len(CoreDef):
            s = input('! Warning: quit without save; proceed anyway? (y/n):')
            if s == 'y' or s == 'Y' :
                print('RPPy ended;',len(CoreDef),'definitions not saved')
                exit (0)
            else:
                REPL()
        else:
            print('RPPy ended; no definitions to save')
            exit (0)
#
#===========================
#
def k_refdef():             # ( defname -- list ) list of all definitions including a reference to defname
    global CFA,PFA
    if len(dstack) < 1 :
        abort('Missing argument for "refdef"')
    elif not isinstance(tos(),str):
        abort('Argument for "refdef" must be a string')
    else:
        defval = CoreDef.get(tos(),None)
        if defval :
            idx = 1
            reflst = []
            idxlastretjmp = len(ExecList)-1
            while ExecList[idxlastretjmp][CFA] != 'doRet()' and ExecList[idxlastretjmp][CFA] != 'doJmp()' :
                idxlastretjmp -= 1
            while idx < idxlastretjmp -1 :
                if ExecList[idx][CFA] == 'Def()' :
                    defname = ExecList[idx][PFA]
                    idx += 1
                if ExecList[idx][CFA] == 'doCall()' or ExecList[idx][CFA] == 'doJmp()' or ExecList[idx][CFA] == 'doLitx()' :
                    if ExecList[idx][PFA] == defval[0] :
                        reflst.append(defname)
                idx += 1
            k_drop()
            dpush(reflst)
        else:
            abort('Definition "'+tos()+'" not found')    
#
#===========================
#
def k_repdef():             # ( defname -- ) replace old definitions of defname with the last one defined
    global CFA,PFA
    if len(dstack) < 1 :
        abort('Missing argument for "repladef"')
    elif not isinstance(tos(),str):
        abort('Argument for "repladef" must be a string')
    else:
        defval = CoreDef.get(tos(),None)
        if not defval :
            abort('Name "'+tos()+'" undefined')
        else:
            nbrepl = ExecList.count(['Def()',tos()])
            if nbrepl == 1 :
                print('  No old definitions to replace')
                k_drop()
                return
            else:
                print('  Replacing',nbrepl-1,'older definitions')
                nbrepleff = 0
                idxdef = ExecList.index(['Def()',tos()])
                idx = idxdef+1
                while idx < defval[0] :
                    if ExecList[idx][CFA] == 'doCall()' or ExecList[idx][CFA] == 'doJmp()' or ExecList[idx][CFA] == 'doLitx()' :
                        if ExecList[idx][PFA] == idxdef :
                            ExecList[idx][PFA] = defval[0]
                            nbrepleff += 1
                        else:
                            if ExecList[idx][PFA] > idx :
                                idxforward = ExecList[idx][PFA]
                                if ExecList[idxforward] == ['Def()',tos()] :
                                    ExecList[idx][PFA] = defval[0]
                                    nbrepleff += 1
                        idx += 1
                        continue                  
                    elif ExecList[idx] == ['Def()',tos()] :
                        idxdef = idx
                        idx = idxdef+1
                        continue
                    else:
                        idx += 1
                print('  Replaced in',nbrepleff,'definitions')
                k_drop()
#
#============================
#
def k_str():                # ( item -- str  ) return a string interpretation of item
    if len(dstack) < 1 :
        abort('Missing argument for "str"')
    else:
        try:
            dpush(str(tos()))
            k_nip()
        except (AttributeError,TypeError,NameError) as e:
            abort(str(e))
#
#============================
#
def k_type():                # ( item -- itemtype ) TOS = type of item
    dpush(type(dpop()))
#
#===========================
#
def k_license() :             # ( -- ) print license
    licensetxt = """
ISC License www.isc.org/licenses

Copyright 2024 Radu BERINDEANU

Permission to use, copy, modify, and/or distribute this software 
for any purpose with or without fee is hereby granted, provided 
that the above copyright notice and this permission notice appear 
in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL 
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE 
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR 
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM 
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, 
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN 
CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""
    print(licensetxt)
    
#
#===========================
#
def fatal_error() :
    print('>>>Fatal error , execution index out of range 0:' + str(len(ExecList)))
    print('>>>Last IP:',IP)
    input('>>>Press any key to quit or any other to continue :)))')
#
#============================
#============================
#
# start RPPy
#
print('Welcome to Reverse Polish Python - RPPy')
print('  Version '+ str(veryy) + '.'+str(vermm) + ' (yy.mm)')
print('  Type "intro .(Enter)" for introduction, "help .(Enter)" for help,')
print('  "license .(Enter)" for license')
print('  Press Ctrl-Q at line input or "quit .(Enter)" to exit RPPy')
print()
#
while IP < len(ExecList) :
    NEXT()
fatal_error()
exit(1)


#====
# EOP
#====