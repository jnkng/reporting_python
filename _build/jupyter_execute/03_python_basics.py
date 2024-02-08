#!/usr/bin/env python
# coding: utf-8

# # First steps
# 
# This chapter provides an introduction to basic commands and useful built-in libraries.  
# 
# As mentioned, this course will rely on jupyter notebooks. Code will be written in cells, which can be run independently. 
# To run a cell, one can use the run symbol above the cells by clicking on it. A more convenient way is again using the corresponding keyboard shortcut: holding **shift** and  pressing **enter**.\
# This will run the current cell and select the next cell below.

# In[1]:


import sys
sys.version


# In[2]:


import this


# ## Basic Python
# 
# Just starting a jupyter notebook and thus a python kernel already allows several basicoperations. The perhaps most obvious functionality would be to use a cell to calculate a mathematical expression. To do so, just enter the expression and run the cell:

# In[3]:


999+1


# In[4]:


# comments inside the cell, starting with '#' help readers to understand your code. 
# These lines are not run! 
2 * (2 + 2) - 4


# While jupyter will print the result of such one line expressions immediately, writing both expressions in one cell will print only the last computed result:

# In[5]:


999+1
2 * (2 + 2) - 4


# In the common case, where code inside one cell will exceed one line or will produce more than just on result, the ```print()``` function can be used. Functions in python get their parameters in parentheses (more on functions later):

# In[6]:


print(999+1)
print(2 * (2 + 2) - 4)


# Some basic operations and functions are

# In[7]:


print('Addition:',       1 + 1 )      
print('Subtraction:',    2 - 1 )      
print('Division:',       1 / 2 )      
print('Multiplication:', 2 * 1 )      
print('Modulus:',        3 % 2 )      
print('Floor division:', 5 // 2 )     
print('Exponent:',       2 ** 3 )     
print('Minimum:',       min(2,5))
print('Maximum:',       max(2,5))


# Autocompletion is a very useful tool for writing code. Not only will it provide already defined variables. It will also show you available methods on different objects (more on objects later).
# 
# Autocompletion or suggestions for completion will appear when pressing **tab** in code, as long as it is not the beginning of a line (where it will indent the line, see loops, functions).\
# For instance, when typing ```pri``` and hitting **tab**, jupyter will complete it to ```print```.

# ### Help
# In order to get information, for example on the ```print()```function, help can be summoned by using yet another function:

# In[8]:


help(print)


# ### Data Types
# 
# The most basic data types in python are numeric, string and boolean. However, there are many, many more. In order for many operations wo work properly, the data types must be compatible with one another. With the ```type()``` function the datatype of an object can be printed. 

# In[9]:


a = 1
b = 1.0
c = 'two'
d = True
print('a:', type(a))
print('b:', type(b))
print('c:', type(c))
print('d:', type(d))


# Changing the type of a variable can be achieved by the respective functions:

# In[10]:


print(int(3.14))

f = "2.5"
print(10 + float(f))


# Some mathematical operations can also be applied to strings/lists:

# In[11]:


a = 'Who would '
b = 'have thought'
c = '?'
print(a+b+(c*5))


# ## Packages and Modules
# 
# Python's functionality can be expanded by loading modules to the namespace. A module may be seen as a chunk of python code for a special task someone has already written for you to use while package signifies the inclusion of the underlying file structure to load the modules. 
# 
# In order to make a module's complete functionality available, it has to be loaded to the namespace trailing the ```import``` statement. Calling a module function in this case requires the module name with a dot before the function: ```package.function()```. 
# 
# A module can be imported under an alias, using the ```as``` statement. This can help someone reading your code to know from which module a function is imported while keeping the code shorter and thus better readable.
# 
# :::{admonition} Tip 
# :class: tip
# By convention all imports are done at the beginning of the code.
# :::

# In[12]:


import math
print(math.sqrt(4))

import numpy as np
print(np.sqrt(4.0))


# To import a single function (or class) from a module one calls ```from <module> import <function>```. Here, the module's name does not need to be added when calling the function. Similarly, an asterisk can be used as a wild card, as in ```from <package> import *```, to import all functions (classes) from one module (so not to add the module prefix every time in the code). \
# The following examples uses the ```math``` module, which contains functions such as the sine, cosine or square root.

# In[13]:


from math import sqrt
print(sqrt(4))


# :::{admonition} Note
# Calling a function which is not imported results in an error.
#     
# Usually, python is rather explicit in where to look for your mistake.
# :::

# In[14]:


#print(cos(0))    # would raise error as cos() function is not imported


# ![](graphics/cos_error.png)

# With the wild card, all functions from the math module are now loaded to the namespace.

# In[15]:


from math import *
cos(0)


# ## Variables
# 
# Objects can be stored in variables by assigning them using ```=```. Since everything in python is an object, anything can be saved in a variable: numbers, strings, lists, etc. Python will automatically recognize the format of a variable to let the user know about incompatibilities. Calling a variable before it is assigned will also throw an error.\
# Note that python is case sensitive, meaning that when assigning variables a ≠ A.

# In[16]:


var_1 = 5 ** 2
print(var_1)
var_2 = 'twenty five'
print(var_2)


# :::{admonition} Caution
# :class: caution
# Do not name your variables like built-in python objects!
# :::
# In jupyter notebooks, built-in objects are automatically coloured green.
# For example:

# In[17]:


list
int
dict


# ## Logical Conditions
# 
# 
# In order to compare values, logical operators can be used. The most common are
# 
# | Operator   | Meaning |
# | :--------- | ------: |
# | ==  | equal  |
# | 1!=  | not equal  |
# | >  | greater than |
# | <  | less than |
# | >=  | greater than or equal to |
# | <=  | less than or equal to |
# 
# The result will be a boolean: either ```True``` or ```False```. \
# Comparing statements may also be combined by ```and``` or ```or``` and can be negated by ```not```.

# In[18]:


a = (1<2)
b = (0 == 1)
print(a, b)
print(a and b)
print(a or b)


# ## Branching
# 
# In a program, code must often be run conditionally on some input or previous result. The ```if```, ```else``` and ```elif```statement can be used to select which branch of code shall be run. The condition is followed by a colon and the respective code for that condition must be indented (automatically with a line break or by pressing ***tab***).
# 
# :::{admonition} Caution
# :class: caution
# Indentation is not to be used for better readability. 
#     
# Instead, it has a function and must not be used when not necessary!
# :::

# In[19]:


a = 4

if a < 0:
    print('a is negative')
elif a > 0:
    print('a is positive')
else:
    print('a equals zero')


# ## Lists and Tuples
# 
# Lists and tuples are both an ordered collection of objects. While tuples cannot be modified, lists are rather flexible. Objects can be added to a list, removed or replaced. Lists appear in square brackets ```[]```, tuples in parentheses ```()```.  \
# Lists and tuples can be nested, meaning elements of a list or tuple can again be a list or tuple. Duplicates are also allowed. (A ```set()``` would not allow duplicates and is not ordered). \
# Elements can be accessed by indexing with square brackets behind the list name.
# 
# 
# 
# :::{admonition} Note
# Indexing in python starts with zero, so the first element of a list will have index 0.
# :::

# In[20]:


my_list = [1,2,0,4,5]
my_tuple = ('a', 'b', 'c')

# length of object:
print('0. the length of my list is', len(my_list),', the length of the word "list"', len('list'))

# access first element
print('1. first element from my_list:', my_list[0])

# print variables more conveniently
print(f'2. second element of my_tuple: {my_tuple[1]}')

# to change an element
my_list[2] = 3
print(f'3. changing the third element in my_list: {my_list}')

# note that strings are lists of characters:
my_str = 'expression'
print(f'4. first letter in my_str: {my_str[0]}')

# last element 
print(f'5. last element of my_tuple: {my_tuple[-1]}')

# slicing
print(f'6. from element 3 to end of my_list: {my_list[2:]}')

# reverse order
print(f'7. reverse order of my_list and slice: {my_list[3::-1]}')

# delete element
del(my_list[4])
print(f'8. add new element: {my_list}')


# Lists also allow for element checks using ```in``` (negated by ```not```):

# In[21]:


my_list = [1,2,3,4]

if 2 in my_list:
    print('2 is an element of my_list')
    
if 10 in my_list:
    print('10 is an element of my_list')


# Beside definition by hand, the the functions ```list()``` and ```tuple()``` can be used to transform a suitable object to a list or tuple.

# In[22]:


print(tuple(my_list))
print(list('python'))


# ## Dictionaries
# 
# Dictionaries allow to store *key - value* pairs in a kind of named list fashion. By convention the *key* element is of type string, while the *value* can be any object (including dictionaries). To define a dictionary, inside curly braces ```{}```, the *key* element is followed by a colon and the *value*. The *keys* must be unique in a dictionary, since the *value* elements are accessed via the respective *key*: as in lists, one uses square brackets. Yet not with an index number but the desired *key*.\
# New key-value pairs can be added to a dict in a similar way as they are accessed. The new *key* in square brackets follows the dict name and a *value* is assigned by an equal sign.\
# Dictionaries are not ordered, as can be seen from the way of accessing and adding new k-v pairs.

# In[23]:


my_dict = {'start': 1, 'end': 20}
print(my_dict['start'])

# new k-v pair
my_dict['mid'] = 10
print(my_dict)


# All *keys* and *value* can be accessed with the ```.keys()``` and ```.values()``` method (more on methods later).

# In[24]:


print(my_dict.keys(), my_dict.values())


# ## (Un)packing
# 
# Python allows to assign multiple variables at once, called (un)packing. This is most common with tuples but can be expanded to other iterables. The variables to be assigned are separated by a comma. 

# In[25]:


my_tuple = ('one', 2, 'three')
a, b, c = my_tuple
print(a, b, c)

# the asterisk assigns all surplus values on the right hand side of the equal sign to a
*a, b = 1, 2, 3, 4
print(a ,b)


# ## Loops
# 
# ### for-loop
# 
# A for-loop is used for iteration, if the number of iterations is known prior to execution. A for loop iterates over any sequence like lists, tuples, strings etc. A common way is to loop over a ```range(n)``` object. Caution: indexing starts from 0 and for range objects ends at ```n-1```!\
# 
# Note that when iterating a list or tuple it might be worth considering to choose an informative name (especially when nesting loops).\ 
# 
# To write a loop, ```for``` is followed by the iterating variable, ```in``` and the sequence to iterate before a colon. The code to execute every step begins in the next line and is indented.  

# In[26]:


# range object for iterating numbers
for i in range(5):
    print(f'{i} squared is {i**2}')  
print('')

# iterate over a tuple/list
for tuple_element in my_tuple:
    print(tuple_element)
print('')
# iterate over tuple/list element and index
for i, tup_el in enumerate(my_tuple):
    print(f'{tup_el} at position {i}')
print('')  
# iterate over keys and values in dict
for k,v in my_dict.items():
    print(f'key: {k}, value: {v} ')


# ### while-loop
# 
# When the number of iterations for a loop is not knwon beforehand, a while-loop can be used. It will run, until a terminal state is reached or some criterion is satisfied. Usually, an initial state is given which will be altered by some operation and thus lead to termination.\
# A while-loop start with ```while``` followed by the condition and a colon. The condition may be negated with ```not```.\
# :::{admonition} Warning
# :class: warning
# Infinit loops may occur when the terminal criterion is not properly defined or the code is otherwise defective.
# :::
# 

# In[27]:


a = 0
while a < 4:
    print(a)
    # use combined operator a += 1, equal to a = a + 1
    a += 1      # when not including this line, a will forever stay a = 0 and the loop will not terminate by itself
                # What will be printed in this case?
    
var = 5
check = True
while check:
    print(f'{var} is greater zero')
    var -= 1 
    check = var > 0


# ## List comprehension
# Python offers a handy way to create lists. It looks like a for-loop in a list and is called list comprehension. It is written in one line instead of indenting as in ordinary for-loops. These expression can also be nested.

# In[28]:


list_1 = [i for i in range(5)]
print('list_1:', list_1)

# a nested expression
list_2 = [[i*j for i in list_1] for j in [0,1]]
print('list_2:', list_2)


# ## Dict comprehension
# 
# Analogous to list comprehension, we can create dictionaries with key and value pairs.
# For example from the list above:

# In[29]:


dict_1 = {str(k): k**2 for k in list_1}
print(dict_1)
print(dict_1['3'])


# ### break and continue
# 
# For more control over a loop, the ```break```and ```continue``` statements can be engaged. Used with a condition, ```break``` will terminate the loop when satisfied while ```continue``` will stop and skip the current iteration to jump to the next.

# In[30]:


for i in range(100):
    if i % 2 != 0:    # % is the modulo operator
        continue      # continue in the if-statement skips printing for odd i
    print(f'{i} is even')
    if i == 8:        # when i equals 8, the loop terminates (the print statement for i == 8 is executed before)
        break


# ## Functions
# 
# Python come with many built in functions, some of which have been shown or used before, as well as the option to define new functions.
# 
# To define a function, use ```def function_name(args):``` before the indented body of the function begins in a new line. ```args``` here means arguments, which are passed to function. 
# 
# Note that a function must not necessarily be defined using arguments.

# In[31]:


def my_print(word):
    print(word)
    
my_print('Greetings')

def print_hi():
    print('hi')
    
print_hi()


# ### Return
# 
# To assign the result of a function to a variable for further use, the ```return``` keyword is used. If more than one object is to be returned, use commas to separate them.
# 
# The ```return``` statement is indented at least once from ```def```, even more than once when using branching, for example.
# With branching, several return statements may appear in one function. 
# 
# The ```return``` command must not be confused with a ```print()``` statement! 

# In[32]:


import numpy as np

data = [1,2,3,4,5,6,7]
print(np.mean(data))

def my_mean(arg_list):
    sum_ = 0
    length_count = 0
    for el in arg_list:
        sum_ += el
        length_count += 1
    return sum_/length_count

print(my_mean(data))


# ### Yield
# 
# Besides ```return```, another option is ```yield```. The main difference is that ```return``` will do a calculation and send the result back at once, while when using ```yield``` a **generator object** is created and results can be returned sequentially.
# 
# Comparing the following two examples, the ```return_list``` function stores the complete list in the memory, while the ```yield_list``` function does not. Instead, it returns the values one after another (when using the ```next()``` function or a loop) remembering the current state of the function.

# In[33]:


def return_list(n):
    return [i for i in range(n)]

def yield_list(n):    # function mimics range()
    i = 0
    while i < n:
        yield i
        i += 1


# In[34]:


return_list(5)


# In[35]:


yield_list(5)   # creates a generator object


# In[36]:


gen = yield_list(5)    # assign generator object to variable


# In[37]:


print(next(gen))    # call next() to jump to next 'yield'
print(next(gen))    # only one value in memory
print(next(gen)) # another next() throws error because the generator is depleted after 4!


# Since the state of the generator is remembered and we have already moved beyond 2 using ```next()```, the following for loop 'finishes' the generator:

# In[38]:


for i in gen:
    print(i)


# Generator object can be useful when working with huge files which do not fit into memory.

# For functions with several arguments, the order of inputs is important. They will be read according to the function definition. When the arguments are specified in the function call, the input order does not matter.

# In[39]:


def divide(numer, denom):
    return numer / denom

print(divide(10,2))
print(divide(2,10))

print(divide(denom=2, numer=10))


# Default values for a function can be set. If an argument is not specified when calling the function, the default value will be used.

# In[40]:


def divide(numer, denom = 1):
    return numer / denom
print(divide(numer=10))


# More advanced function writing involves recursion, meaning python allows a function to call itself.

# In[41]:


import math

def my_factorial(n):
    if n == 0:
        return 1
    else:
        return n * my_factorial(n-1)
    
print(my_factorial(5))
print(math.factorial(5))


# ### Global and Local Variables
# 
# Variables can be defined globally, i.e. outside of functions. A variable definded inside a function will only exist inside the scope of the function. Should a local variable be given the same name as a global variable, the function will use the value locally defined!\
# Global variables inside functions can be defined using the ```global``` keyword before the respective variables.

# In[42]:


x = 7
def f_1():
    print('calling f_1, x =',x)

f_1()
    
def f_2():
    x = 10

f_2()
print('after calling f_2: x =', x)
    
def f_3():
    x = 10
    print('calling f_3: x =', x)
    
f_3()
print('after calling f_3: x =', x)
    
def f_4():
    global x
    x = 10

f_4()
print('after calling f_4: x =', x)


# ## Lambda functions
# It might occur that a function is needed which is only needed once and has only a limited functionality. To spare you and the reader of the code from jumping to a block of defining such a function you can use a **lambda function**. They are written in-line by the keyword ```lambda```, followed by the parameters and a colon before the body.\
# Arguments are passed in parentheses as usual.
# 
# :::{admonition} Note
# The lambda syntax should only be used for simple functions!
# :::

# In[43]:


from math import exp

# regular way
def reg_func(x):
    return 1/exp(x)
print(reg_func(.5))

#lambda function with identifier 
l_func = lambda x: 1/exp(x)        # this way, it is hard to find the origin of a function if it is called elewhere
print(l_func(.5))                  # in your code. It is not recommended, yet still possible.

# for single use, no identifier
print((lambda x: 1/exp(x))(.5) )


# Lambda functions can be easily applied in combination with list comprehension, where the can be defined in place.

# In[44]:


# with list comprehension
l_list = [(lambda x: 1/exp(x))(i) for i in list_1]
print(l_list)

# always consider doing it without a lambda function
print([(1/exp(i)) for i in list_1])


# ## Classes
# 
# Since almost everything in python is an object, classes are a very important element to its functionality. A class can be seen as a constructor for certain objects. \
# 
# To define a class, the ```class``` keyword is followed by the class name. By convention, for class names the CamelCase style is used. 

# In[45]:


# define class Student

class Student():
    uni = 'Passau'
    subject = 'math'
    grades = [1.3, 1.7, 3.0]
        
# instantiate object  
Chris = Student
Tina = Student

# get uni of student Chris
print('Uni:', Chris.uni)

# student changes subject
Chris.subject = 'biology'

print("Chris' subject:", Chris.subject)
print('class name:', Chris.__name__)

print("Tina's subject:", Tina.subject)


# Classes can not only store values but also functions, called methods. Methods are defined just like regular functions, but inside the class body. To make a class more useful (compared to the example above), the ```__init__()``` method is needed. As arguments, it takes ```self``` and all other arguments needed as input to build the object. ```self``` is used for instance variables, i.e. variables that belong to an object and not the whole class.
# 
# Methods and class variables are chained by a ```.``` to the object.
# 

# In[46]:


import numpy as np

class Student():
    def __init__(self, uni, subject, grades):
        self.uni = uni
        self.subject = subject
        self.grades = grades
    
    #define method to show average grade
    def avg_grade(self):
        return np.mean(self.grades)
     
Chris = Student('Passau', 'Art', [1.3, 1.7, 3.0])
Tina = Student('Regensburg', 'Physics', [1.0, 2.0])

Chris.subject = 'engineering'
print(f'Chris: {Chris.subject}')
print(f'Tina: {Tina.subject}')

print(Chris.avg_grade())

# lists have a built-in method append, which adds items given as arguments to the end of the list (see help(list))
Chris.grades.append(5.0)
print(Chris.avg_grade())


# ### Inheritance
# 
# Classes can inherit all properties from other classes by using the ```super()``` function in the constructor. This should be applied, if a new class should expand the functionality of the original class without wanting to change the original class. For example if a Student is also a resident: 

# In[47]:


class LocalResident(Student):
    def __init__(self, uni, subject, grades, address):
        super().__init__(uni, subject, grades)
        self.address = address
        
Chris = LocalResident('Passau', 'Art', [1.3, 1.7, 3.0, 5.0], 'Innstr. 27')

print(f" Uni and address: {Chris.uni}, {Chris.address}")
print(type(Chris))


# ## Files
# 
# Regular python files end with *.py* and code can be written and read in any text editor. Only the suffix will tell the interpreter how to handle the file, in this case as a python script.
# 
# Jupyter Notebook files end with *.ipynb*. The special cell-wise structure leads to more formatting effort which is stored in a .json format (see later chapters), meaning that when a *.ipynb* file is opened in an ordinary text editor, the structure will be very different from what is shown in this jupyter interface. 
# 
# Below a jupyter notebook is shown on the left. The formatting is seen on the right, where the *.ipynb* file was openened using a text editor. 

# ![](graphics/struc.png)

# # Second steps
# 
# In the following, some common operations are shown in order to get used to the python language und its functionality.
# 
# ## NumPy
# One of the most useful and widely used libraries is **NumPy**. It makes working with arrays, and thus vectors and matrices, very efficient and includes a broad variety of mathematical tools. Because of its powerful implementations, it serves many other packages as a basis.
# 
# Even though this course will hardly rely on numpy itself, a short introduction is given in the following.
# 
# We will start with importing as **np**. Information will mainly be given by comments in the code.

# In[48]:


import numpy as np

# mathematical functions:
print('sin(pi) = ',np.sin(np.pi)) 
# note that the sine of the number pi is defined as zero, yet python returns a small number > 0


# One of the most useful concepts is that of *arrays*, which can have an arbitrary number of dimensions (yet three should do here). Arrays correspond mainly to what you should know as scalar, vector or matrix. 

# In[49]:


arr_a = np.array([1,2,3,4,5])
arr_b = np.array([0,0,0,0,1])

#dimensions of an array
print('0. dimension of array a', arr_a.shape)

# operations can be performed by methods and methods chaining on these array objects
print('1. sum of array a:',arr_a.sum())
print('2. variance of array a:', arr_a.var())

# broadcasting a scalar to an array
print('3. one plus array b:', 1 + arr_b)
print('4. element-wise multiplication of arrays:', arr_a * arr_b)

# vector multiplication / dot product
print('5. scalar by dot product:', arr_a.transpose().dot(arr_b))   # this should not yield a scalar for vectors!

# for real vectors, the inner dimension of the product is crucial -> (5x5)
print('5.1 vector multiplication: \n', np.matrix(arr_a).transpose().dot(np.matrix(arr_b)))

# shapes differ for arrays and matrices
print('5.2 transposed array:', arr_a.transpose().shape, 'transp. matrix:', np.matrix(arr_a).transpose().shape )

# to reshape an array, use the reshape method
zero_arr = np.zeros(shape=(2,3))
print('6. array:     reshaped:           same result:\n', 
      zero_arr, zero_arr.reshape(-1,), zero_arr.reshape(6,))  
# -1 is for "unknown" dim (like a wildcard)


# In[50]:


# random number generation with np.random module

# for a list of probability distributions, the autocomplete function can be used (press tab after the dot)
random_expo = np.random.exponential(scale=.5, size=(5,5))
print(random_expo)

