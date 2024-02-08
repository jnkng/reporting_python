#!/usr/bin/env python
# coding: utf-8

# # Web Scraping
# 
# The process of retrieving data displayed on websites automatically with your computer is called web scraping. It means instead of clicking, selecting and copying data yourself, your python script does it for you. You would only need to define how and where to look. Scraping information from the internet can be very time consuming, even when your machine does it for you. However, it may also be very rewarding because of the vast amount of data and possibilities - which come for free.
# 
# Before we can turn to the actual scraping online, we will deepen our understanding of html and how to navigate through a file.

# ## Xpath
# 
# The **E**xtensible **M**arkup **L**anguage **XML** provides something like a framework to markup languages to encode structured, hierarchical data for transfer. It is thus a related to HTML, just less for displaying data than storing and transferring it. While the differences are not of interest here (learn about them yourself anytime, though), the similarities are: in the way, we can use them to navigate html documents. 
# 
# The **XML Path Language** (**Xpath**) allows to select items from an xml document by addressing tag names, attributes and structural characteristics. We can use the respective commands to retrieve elements from html documents, i.e. websites.
# 
# The two basic operators are
# 
# - a forward slash ```/```: to look into the next generation
# 
# - square brackets ```[]```: select a specific element
# 
# The forward slash works basically the same way as in an URL or path when navigating a directory on your computer. The square brackets on the other hand have a very similar functionality to the usage of square brackets in python.
# 
# Lets have a look at a slightly extended version of the html document from the previous chapter to see how we can use these operators for navigation.\
# 
# As usual, we first import the package (actually only one class for now) providing the desired functionality: **Scrapy** 
# 

# In[1]:


from scrapy import Selector


# In[2]:


my_html = \
"""<html><body><div id='div_1'><p class='parag-1' id ='intro'>This is a brief introduction to <b>HTML</b>.</p>
<p class='parag-1-1' id ='main'>Part 2.</p></div id='div_2' href='www.uni-passau.de'>
<p class='parag-2' id ='outro'>Part 3. <a href='www.uni-passau.de'>Homepage</a></p></body></html>
"""

#formatted version to better visualise the structure

# <html>
#   <body>
#     <div id='div_1'>
#       <p class='parag-1' id ='intro'>
#         This is a brief introduction to <b>HTML</b>.
#       </p>
#       <p class='parag-1-1' id ='main'>
#         Part 2.
#       </p>
#     </div id='div_2' >
#     <p class='parag-2' id ='outro'>
#         Part 3.
#         <a href='www.uni-passau.de'>Homepage</a>
#     </p>
#   </body>
# </html>


# Because of the tree like structure elements are labeled in on the basis of a family tree.\
# The html consists of the **body** inside the **html** tags.\
# In the next generation, called *child generation*, we see one **div** element, itself containing two **p** elements, i.e. *children*.\
# Another **p** element appears as a *sibling* to the only **div** element.
# 
# Now let's select single elements from this html using the ```xpath()``` method to which we pass our statement as string. To do so, we must first instantiate an Selector object with ```my_html```. Note that chaining the ```extract()``` method to the selector object gives the desired result.

# In[3]:


sel = Selector(text=my_html)

# navigate to p elements inside div
print('both p elements:\n', sel.xpath('/html/body/div/p').extract())


# In the special case here, where all child elements are the *p* elements we are looking for, we can use the wildcard character ```*```. It wil select any element, no matter the tag in the next generation (or in all future generations with a double forward slash).

# In[4]:


# use wildcard character *
print('\nwildcard *:\n', sel.xpath('/html/body/div/*').extract())


# To select only the first *p* element, index the result with square brackets. 
# :::{admonition}Caution
# :class: caution
# Xpath indexing starts with 1 and not 0 like python does!:::
# 
# Another way is to use scrapy's ```extract_first()``` method.

# In[5]:


# select first p with [1]
print('slelect only first p\n',sel.xpath('/html/body/div/p[1]').extract())

# indexing the python list starts with 0!
print('\nslelect only first p\n',sel.xpath('/html/body/div/p').extract()[0])

# with extract_first()
print('\nslelect only first p\n',sel.xpath('/html/body/div/p').extract_first())


# We see, that a forward slash navigates one generation deeper into the structure, from *html* over *body* and *div* to both(!) *p* elements. Here, we get back a list (first print statement) of the *p* elements, where we can intuitively use the square brackets to select only the first one.\
# What we get back, however, is still a *selector object*. To extract the text only, we need to modify the statement further by ```/text()```.

# In[6]:


# select text from first p element
to_print = sel.xpath('/html/body/div/p[1]/text()').extract()

print('text in first p:\n',to_print)


# Now again, we do not see all of the text, just the string before the *b* tags and the dot after it as elements of a list. Even though the *b* tags for bold printing appear in-line, they still define a child generation for the enclosed 'HTML' string. Here, we could navigate further down the tree using a path to the b element for exampe.\
# Instead, we will make use of the double forward slash ```//```, which selects everything '**from future generations**'. Meaning it will select all the text from all generations that follow this first *p* element. 

# In[7]:


# select text from first p element and all future generations by a double forward slash
to_print = sel.xpath('/html/body/div/p[1]//text()').extract()
print('text in first p and future generations with double slash:\n',to_print)

# for one string, use the join() function
print('\ncomplete string:\n', ''.join(to_print))


# Beside specifying a path explicitly, we can leverage built-in methods to extract our desired elements. Scrapy's ```getall()``` returns all elements of a given tag as list

# In[8]:


print('scrapy:\n', sel.xpath('//p').getall())


# As mentioned before, elements can be addressed using attributes, like ID or class name. The attribute is addressed in square brackets, with ```@attr = 'attr_name'```. If the same attribute applies to several tags, a list of all results is returned.

# In[9]:


# search all elements in document (leading //*) by id
print('ID with wildcard:\n', sel.xpath('//*[@id="div_1"]').extract())

# same as (tag must be known)
print('\nID with div:\n', sel.xpath('//div[@id="div_1"]').extract())


# The ```contains``` function provides access to attributes based on (parts of) the attribute name.

# In[10]:


# find all elements where attr contains string
print('contains string:\n', sel.xpath('//*[contains(@class, "parag-1")]').extract())


# Finally, an attribute can be returned by addressing it in the path.

# In[11]:


print('get attribute:\n', sel.xpath('/html/body/div/p[1]/@id').extract())


# ## CSS
# 
# The **C**ascading **S**tyle **S**heets language is another way to work with markup languages and thus html. Of special interest for us is that it also provides selectors. Even more convenient is that scrapy includes these selectors and the respective language. CSS uses a different syntax, which can offer much simpler and shorter statements for the same element than xpath (or sometime, the opposite) 
# 
# The basic syntax changes from xpath like this:
# - a single generation forward: ```/``` is replaced by ```>```
# 
# - all future generations: ```//``` is replaced by a blank space (!)
# 
# - not so short anymore: indexing with ```[k]``` becomes ```:nth-of-type(k)```
# 
# For scrapy, nothing changes really, except using ```.css()``` method. The selector object is the same as before.\
# Some examples: 

# In[12]:


# navigate to p elements inside div
print('xpath:\n', sel.xpath('/html/body/div/p').extract())
print('\ncss:\n', sel.css('html>body>div>p').extract())

# navigate to all p elements in document
print('\nall p elements')
print('xpath:\n', sel.xpath('//p').extract())
print('\ncss:\n', sel.css('p').extract())


# The css locator provides short notation when working with *id* or *class*:
# - to select elements by class: use ```tag.class-name``` (similiar to method chaining)
# 
# - to select elements by id: use ```tag#id-name```
# 
# Examples from the toy html above:

# In[13]:


# select by id
print('select by class:\n', sel.css('*.parag-1').extract())

# select by id
print('\nselect by id:\n', sel.css('*#intro').extract())


# Attributes are in general addressed by a double colon ```::attr(attribute-name)```, for example to extract a link from the ```href``` attribute:

# In[14]:


# select by attribute
print('\nselect by attribute:\n', sel.css('*::attr(href)').extract())


# The double colon is also used to extract ```::text```, like we used ```/text()``` in xpath:

# In[15]:


# extract all (blank space!) text descending from p elements inside div elements with class 'div_1' 
print('\nextract text:\n', sel.css('div#div_1>p ::text').extract())


# Look for exampe at [this cheatsheet](https://devhints.io/xpath) for more commands with xpath and css.
# 
# Lastly, let's look at BeautifulSoup again. It offers basically the same functionality to address and select any element based on its tag or attributes, but can make life easier with its prewritten methods. Keep in mind however, that BeautifulSoup is a python package, while the xpath and css syntax is standalone and will thus transfer to other software, e.g. **R**.

# In[16]:


from bs4 import BeautifulSoup
soup = BeautifulSoup(my_html)
# select by id
print('by id:\n',soup.find_all('div', id='div_1'))

# select by class 
print('\n by class:\n',soup.find_all('p', class_='parag-1'))    # note class_ (not class)

# by s


# ## Inspecting a webpage
# 
# Common internet browsers like firefox, chrome, safari, etc. include functionality to inspect webpages, meaning to look at the underlying html. To view the html, right-click on a specific element on the webpage, e.g. a headline, and select "Inspect Element" (or something similar), like shown in this screenshot taken from [this page](https://finance.yahoo.com/quote/AAPL/analysis?p=AAPL):
# 
# ![title](graphics/inspect.png)

# You will then see a small window open at the bottom of your browser, showing the html in hierarchical structure where elements can be expanded to show its child generations:
# 
# ![title](graphics/html.png)
# 
# While hovering with the mouse over
# an element from the list, your browser should highlight the respective element on the website. So hovering over the ```<table>``` element will highlight the complete displayed table, while hovering over a ```<tr>``` element will only highlight a specific row of the table. This facilitates the setup of your code for selection. Furthermore, a right-click on the element in the list let's one copy several characteristics like the path or the attributes directly to avoid spelling or selection errors.

# In this example, we see that information is stored in a ```<table>``` and we could select it by specifying the data-reactid' (we would have to check if there are more elements of this class, tough ids should generally be unique).

# In order to collect the displayed information, we use the methods from before.

# ### scrapy selector

# In[17]:


import requests as re
from scrapy import Selector

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
}
url = 'https://finance.yahoo.com/quote/AAPL/analysis?p=AAPL'
response = re.get(url, headers=headers)


# In[18]:


response.ok


# In[19]:


sel = Selector(response)


# column names:

# In[20]:


# select column names based on order, as no id is given for the tables
columns = sel.xpath('//table[1]/thead[1]/*').css(' ::text').extract()
print(columns)    # unfortunately gives unsatisfying result with parentheses


# In[21]:


# filter by hand...
columns = [el for el in columns[1:] if any(['Year' in el, 'Qtr.' in el])]
print(columns)


# table data:

# In[22]:


# select table entries based on data-reactid
table_body = sel.xpath('//table[1]/tbody/*').css(' ::text').extract()
print(table_body)  


# In[23]:


labels = [el for i, el in enumerate(table_body) if i%5==0]
data = [el for i, el in enumerate(table_body) if i%5!=0]


# In[24]:


{labels[x]:[el for el in data[x:x+4]] for x in range(len(labels))}


# In[25]:


import pandas as pd
df = pd.DataFrame.from_dict({labels[x]:[el for el in data[x:x+4]] for x in range(len(labels))},\
                            orient='index', columns = columns)
df


# ### pandas
# 
# The ```read_html()```function returns a list of all available tables when we pass the response object as argument.

# In[26]:


pd_df = pd.read_html(response.content)
print(f'type: {type(pd_df)}, length: {len(pd_df)}')


# In[27]:


pd_df[0]


# ##  Webcrawler
# 
# A webcrawler or spider will automatically 'crawl' the web in order to collect data. Once set up, it can be run every day in the morning, every couple of hours, etc.
# Such rugular scraping is used to build a database, e..g with newspaper articles. Commonly, for this kind of data collection, the webcrawler is deployed using cloud computing which is not part of this course.
# 
# We will, however, take a look at a very basic spider not diving in too deep.
# In scrapy, spiders are defined as **classes** including the respective methods for scraping:
# 
# - providing the seed pages to start
# 
# - parsing and storing the data
# 
# It is important to note that scrapy spiders make use of **callbacks**. A callback is a function, which is run as soon as some criterion is met, usually when some other task is finished. In a scrapy spider, the parsing function is used as callback for the request method: The request must be complete so that the parsing may commence.
# 
# ### callback
# The following is a basic example for a callback. The function will print the string and the callback will print the length of the string.

# In[28]:


def enter_string(string, callback):
    print(string)
    callback(string)
    
def print_len(x):
    print(len(x))
    
enter_string('onomatopoeia', callback=print_len)


# Let's take a look at the basic structure of a spider, found in the [scrapy docs](https://docs.scrapy.org/en/latest/intro/tutorial.html).

# In[29]:


import scrapy
scrapy.spiders.logging.getLogger('scrapy').propagate = False    # suppress logging output in cell


class mySpider(scrapy.Spider):
    name = "my_first"

    custom_settings = {
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
    }
    def start_requests(self):
        urls = [
            'http://www.example.com'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response.css('p::text').extract())


# The `start_requests` method provides the start or url or seed. For every url in this starting list, we send a `Request` using the respective function. We provide to this function the callback to be the `parse` method defined subsequently. It is important to use `yield`, i.e. to create a generator, as this is required by scrapy.
# 
# In `parse()`, we use the already familiar `css` method to extract all text found in p elements from the website.
# 
# In order to let the spider crawl, we need to import `CrawlerProcess` instantiate an according object, link the spider to it and start the process.

# In[30]:


from scrapy.crawler import CrawlerProcess
proc = CrawlerProcess()
proc.crawl(mySpider)
proc.start()


# After some output (red window), we see the text from the website.
# 
# In order to really crawl the web, we would need to extend the spider:
# 
# 1. find all links on the starting page 
# 
# 2. parse all text on the starting page
# 
# 3. find all links on the pages found the step before
# 
# 4. parse all text from the pages found the step before
# 
# then repeat steps 3 and 4.
# 
# We will now expand the spider from above to print the text from the starting page, then follow the provided links to the next page and print that text. 

# In[1]:


from scrapy.crawler import CrawlerProcess
import scrapy
scrapy.spiders.logging.getLogger('scrapy').propagate = False    # suppress logging output in cell

class followSpider(scrapy.Spider):
    name = "my_second"
    custom_settings = {
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
    }
    def start_requests(self):
        urls = [
            'http://www.example.com'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_links)

    def parse_links(self, response):
        links = response.css('a::attr(href)').extract()
        print(''.join(response.xpath('//p/text()').extract()))
        for link in links:
            yield response.follow(url=link, callback=self.parse)
            
    def parse(self, response):
        print(response.url)
        print(''.join(response.xpath('//p/text()').extract()))


# In[2]:


proc = CrawlerProcess()
proc.crawl(followSpider)
proc.start()


# Writing several parse functions may also be necessary when dealing with 'nested' websites: One parse function may extract a specific block from an overview page, the other from all children of the overview pages.
# 
# We used the `scrapy.follow` method, to go to the next link. Using this method enables us to write the `parse` method recursively, i.e. the spider would not stop until arriving at a page with no links. Thus, in order to set up a functional spider, not only the webpages must be selected accordingly, but one should always include some filters before starting the spider and storing the scraped data. 
