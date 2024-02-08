#!/usr/bin/env python
# coding: utf-8

# # Notebook formatting 
# 
# ## Markdown
# 
# Jupyter notebooks are html based which, beyond other features, enables to work with [**Markdown**](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Working%20With%20Markdown%20Cells.html) directly inside cells. Markdown in general is a lightweight markup language, designed for easy formatting of plain text (like html is a markup language for browser content).
# 
# In order to make use of markdown formatting in jupyter notebooks, we need to convert the (standard) code cells to markdown cells. We can do so by selecting a cell (blue cell frame) and pressing *m* on the keyboard. Alternatively, click on *Cell* in the menu bar, navigate to *Cell Type* and select *Markdown*. 
# 
# When a markdown cell is run, the text and styling/formatting commands will be translated to html: the content will be displayed according to applied rules. The formatting commands are added in the text and usually include (a pair of) *special characters* like asterisks, hyphens or underscores. Conveniently, the respective formatting is mostly applied dynamically when typing (or otherwise highlighted by different coloring), not only after the cell is run.
# 
# This allows for a well structured notebook format, where code and formatted plain text go hand in hand in order to explain the contents of the project. 
# 
# Markdown in general is not proprietary to Python. We can use mostly the same as in this jupyter implementation for example in Dash's `dcc.Markdown()` function to create formatted text. 
# 
# In the following, a collection of useful formatting is provided.

# <u>**Inline text formatting**</u> like bold or italic can be achieved by using either as asterisk or underscore.
# 
# A pair of asterisks/underscores enclosing the text will yield an italic font: 
# - *italic with asterisk*: \*italic with asterisk* 
# - _italic with underscore_: \_italic with underscore_
# 
# 
# A pair of double asterisks/underscores enclosing the text will yield a bold font: 
# - **bold with asterisk**: \*\*bold with asterisk** 
# - __bold with underscore__: \_\_bold with underscore__
# 
# A pair of three asterisks/underscores on each side enclosing the text will yield a ***bold and italic font***. 
# 
# In order to use either of these symbols safely, *escape* the single character by a prefixed backslash.

# <u>**Lists**</u> can be inserted by starting a line with a hyphen. The symbol will be chosen automatically. A two space indent will open a new level of the list.
# 
# - item 1
#   - indented item
#     - further indented item
# 
# Numbered lists are written by starting a line with a number followed by a dot. The sequence is created automatically: starting every line with `1.` will be translated to a sequence of numbers. The next level, indented by two spaces, will be a sequence of capital letters, then lowercase letters, etc.
# Note that starting a new list with for example `3.` will indeed start the sequence at 3 (or C/c).
# 
# 1. item 1
# 1. item 2
#   1. indented item 
#     3. further indented

# <u>**Hyperlinks**</u> are inserted by enclosing the displayed text in square brackets, followed by the url enclosed in parentheses. The text will be emphasized by coloring and underlining: [Python](https://www.python.org). 
# The text can also be displayed bold or italic with the commands from above inside the square brackets.

# <u>**Headlines**</u> are created using a hash followed by one space in front of the headline text. A single # will create a level one headline, ## will create a level two headline with smaller font etc. The font size will already change while typing the #. 
# 
# Note that when you select a markdown cell containing text already (blue cell frame), you can assign a headline level to the first line using the numbers on your keyboard. Pressing the 1 key, will then insert one # and space in front of the first line.
# 
# Possible yet not so handy is to 'underline' your headline text with hyphens, i.e. jump to the next line after writing the headline text and inserting 4 or more ----. 

# <u>**Tables**</u> can be inserted quickly using a sequence of hyphens to separate rows and vertical lines to separate columns. The hyphens appear in the next line after specifying the columns names and must also be separated by vertical lines:
# 
# Col1 | Col2
# -----|------
# A | B
# 
# This table, before the markdown translation is written as:
# 
#     Col1 | Col2
#     -----|------
#     A | B
# 
# An exact count of hyphens or spaces is not required.

# <u>**Code**</u> is displayed inline using a grave accent \`. A bit of text inside a pair of these symbols is rendered as `Code`
# 
# To use python code specifically, we can use a pair of three grave accents. The first triple is followed by 'python' and a line break. This renders code as it would appear inside code cells, i.e. with the same coloring:
# ```python 
# def print_it(string):
#     print(f"this is a {string}")
# ```
# See the same in a code cell:

# In[1]:


def print_it(string):
    print(f"this is a {string}")


# <u>**$LaTeX**</u> expressions can also be implemented, using a pair of enclosing dollar signs. The expression inside follows standard LaTeX syntax and is especially useful for mathematical expressions:
# 
# $\sum_{n=0}^\infty \frac{x^n}{n!} \hspace{1cm}\hat{=}\hspace{1cm}$ \sum_{n=0}^\infty \frac{x^n}{n!} 

# ## HTML
# 
# Working with Markdown is swift but also very limited in formatting options. For advanced customization HTML can be used without altering its syntax inside Markdown cells.
# We have encountered this equivalence in Dash, where we could decide whether to use `dcc.Markdown('# title')` or `html.H1('title)` to produce the exact same output.
# 
# See bold font as one example:
# - using Markdown \*: **bold**
# - using html \<b>: <b>bold</b>
# 
# However, HTML includes more options including, yet of course not limited to, different fonts.
# As a last example we use the 'style' argument (which we have already encountered for Dash):
# <p style="font-family:'Copperplate'">A new font</p>
# 
# 
# which is \<p style="font-family:'Copperplate'">A new font\</p> as raw string.
