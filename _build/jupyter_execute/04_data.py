#!/usr/bin/env python
# coding: utf-8

# # Working with Data 
# Several libraries offer useful tools to work with data in order to allow for a meaningful analysis. One of the most popular and powerful is [**Pandas**](https://pandas.pydata.org/pandas-docs/stable/index.html). Beside including efficient ways for cleaning and manipulating data, pandas also includes functions for statistical analysis and graphics.
# 
# Usually, pandas is imported under the alias ```pd```.

# In[1]:


import pandas as pd


# ## Pandas - DataFrames and Series
# 
# ### Indexing
# The basic elements for data are *DataFrames* and *Series*. A DataFrame is a whole matrix- or table-like representation of data with column and row names. A Series can be understood as a single column of such a data matrix (but without the need for a table).\
# There are respective functions to turn other objects, e.g. lists or dicts, into DataFrames or Series. Indexing, similar to lists or dicts, uses square brackets.

# In[2]:


my_list = [1,2,3,4,5,6,7]
my_df = pd.DataFrame(my_list, columns=['var1'])
print('df:\n', my_df)

my_series = pd.Series(my_list)
print('series:\n',my_series)

# selecting a single column from a DataFrame
print('select column from df:\n', my_df['var1'])


# To select specific rows or columns, the ```iloc``` method, for selecting based on an index, and ```loc``` method, based on labels, are recommended. Especially when several columns are to be selected. Indexing can also be done by boolean Series (or lists) and thus conditionally. \
# Another way to select a single column is by chaining the column's name to the DataFrame's name by a dot (like in method chaining).

# In[3]:


my_df = pd.DataFrame(
{'age': [20, 34, 56],
 'height': [183, 179, 172]
}, index=['person_a', 'person_b', 'person_c'])
print(my_df)
print('1.:', my_df.loc['person_b','age'], 'is the same as',  my_df.iloc[1,0])

# age > 27
print('indexing by condition/list\n', my_df.loc[my_df.age >27], '\ncorresponds to \n', my_df.loc[[False, True, True]])
print(type(my_df.age >27))


# ### Useful Methods
# 
# Pandas includes many useful methods that will help you get to know and manipulate a dataset. Some of these methods are shown in the following, others are introduced later when needed.\
# More often than not, a dataset will contain missing values, i.e. cells in a data table contain no value. They will be depicted as ```NaN```, **N**ot **a** **N**umber.

# In[4]:


import numpy as np
my_df =  pd.DataFrame(
{'age': [20, 34, 56, np.nan, 44],
 'height': [183, 179, np.nan,  163, np.nan]
})
my_df


# In[5]:


# view the first rows (view last rows with .tail())
print('0.\n', my_df.head(n=5))

# general information
print('\n1.')
my_df.info()

# descriptive statistsics on dataset
print('\n2.\n',my_df.describe())

# number of missing values per column
print('\n3.\n',my_df.isnull().sum())

# single statistics are included as methods, also for single columns
print('\n4.\n', my_df.age.mean())

# fill missing values (e.g. with mean of column)
print('\n 5.\n', my_df.fillna(my_df.mean()))    

# note that you must assign this to my_df (or a different variable) in order to impute missing values permanently!
my_df = my_df.fillna(my_df.mean())

# sort values by column(s)
print('\n6.\n', my_df.sort_values(by=['height']))    


# In[6]:


# get column names (useful for looping)
print('7.\n', my_df.columns)

# drop rows containing missing values
print('8.\n', my_df.dropna()) 

# drop rows or columns
print('9.\n', my_df.drop(['age'], axis=1))

# merge DataFrames (automatically on shared variable if not specified otherwise)
df2 = pd.DataFrame(
{'age': [20, 34, 56, np.nan, 44],
 'weight': [83, 63, 98,  50, 77]
})
print('10.\n', my_df.merge(df2))
my_df = my_df.merge(df2)

# correlation matrix
print('11.\n', my_df.corr())

# adding new columns
my_df = my_df.assign(bmi = my_df.weight/(my_df.height/100)**2)
my_df


# As a last tool in this section, we will look at the ```get_dummies()``` function. Dummy variables are used to encode categorical variables with zero and one, for example in order to calculate the correlation with some other numerical variable.

# In[7]:


df3 = pd.DataFrame(
{'hair': ['blonde', 'black', 'red', 'red', 'black']
})

print(pd.get_dummies(df3.hair))


# ### Plots
# Methods for standard pot types are available. For a histogram of the data, just use ```.hist()```. Other types are available by chaining ```.plot.``` and the plot type. 

# In[8]:


# histogram
my_df.hist()


# In[9]:


# lineplot
my_df.sort_values(by='age').plot.line(x='age', y='height')


# In[10]:


# scatter plot
my_df.plot.scatter(x='age', y='weight')


# ### Importing and Exporting Data
# 
# Your data may come to you in various file formats. Pandas enables you to import data from all common formats. The respective functions are usually called ```read_``` and ```to_``` followed by the respective file type.

# To read a *.csv* for example, use the ```read_csv()``` function. Note that the file need not be stored locally on your computer.

# In[11]:


# import from csv
import pandas as pd
dax = pd.read_csv('data/DAX.csv')
print(dax.head(3))
print(dax.tail(3))


# In[12]:


# save data frame to excel
dax.to_excel('DAX.xlsx')


#  

# Lets do some exploration and manipulation of the historical data from the DAX index we just imported.
# $ $

# In[13]:


print('shape:', dax.shape)


# In[14]:


dax.info()    # the 'Date' column is of dtype object 


# In[15]:


# check type of first entry in 'Date'
print(type(dax.Date[0]))


# Transform it to *datetime*, a special type for dates in python.

# In[16]:


dax['Datetime'] = pd.to_datetime(dax.Date)
print(dax.Datetime.head(3))    # check dtype now


# In[17]:


print(dax.columns)


# In[18]:


print(f'of {len(dax)} rows:\n{dax.notna().sum()}')
print('')
print(f'makes a total of {dax.isnull().sum().sum()} missing values')


# In[19]:


dax.plot(x='Datetime', y=['Open', 'Close'])    # using Datetime for plotting


# In[20]:


dax.describe()


# For statistics on one variable, index the result as usual. 

# In[21]:


mean_open = dax.describe().loc['mean', 'Open']
print(mean_open)


# Create a new column, with a flag if the closing price was higher than the opening price.

# In[22]:


dax = dax.assign(positive = dax.Close > dax.Open)
print(dax.head(3))

print('')
# fraction of days when this was the case
print('fraction of positive days:', dax.positive.mean())
print('\ncheck: \n', dax.positive.value_counts())


# Extract same fraction for every day in the week. Days are counted from 0 (Monday) to 6 (Sunday). 

# In[23]:


for i in range(7):
    print(f'day {i}: ', dax[dax.Datetime.dt.dayofweek == i].positive.mean())


# A more straight forward way using built-in methods.

# In[24]:


dax = dax.assign(wday = dax.Datetime.dt.dayofweek)
dax.groupby(['wday']).mean(numeric_only=True)  # rows with nans are not calculated


# ## Database and SQL
# 
# Beside CSV (or Excel) files, another way to work with data is using databases. From there, data can be accessed using a query language. A very common one for relational databases is **SQL** (**S**tructured **Q**uery **L**anguage). It allows to extract specific records, i.e. records which meet special requirements, from a database using single commands.
# 
# ### Store in Database
# First, saving a data frame to a database is conveniently done with a built-in method in Pandas. However, to access a database, a connection must first be established. In the following, we will use the **sqlalchemy** package for working with a database and use a _SQLite_ database engine.

# In[25]:


from sqlalchemy import create_engine, Table


# In[26]:


# setup SQLite engine and connect
path = 'data/dax_db.sqlite'
engine = create_engine('sqlite:///' + path, echo=False)  # if 'echo = False', information is not printed 
conn = engine.connect()


# In[27]:


# save dataframe to database and close connection
dax.to_sql('historical_data', con=conn, if_exists='replace')
conn.close()       # close connection
engine.dispose()   # dispose engine


# ### Load from Database
# 
# To import data from a database, at first a connection must be created the same way as before. Then, **SQL** statements are used to fetch the data and store it in a Pandas dataframe. 

# In[28]:


from sqlalchemy import inspect, select, MetaData


# In[29]:


path = 'data/dax_db.sqlite'
engine = create_engine('sqlite:///' + path, echo=False)  # if 'echo = True', information is printed in every step
conn = engine.connect()


# In[30]:


# show tables and columns with inspector
inspector = inspect(engine)
tables = inspector.get_table_names()
print(tables)

# show columns
for col in inspector.get_columns(tables[0]):
    print(f"Col: {col['name']},\t type: {col['type']}")


# Use a MetaData Object, which holds information about the database.

# In[31]:


m = MetaData()
m.reflect(engine)
print(m.tables.keys())


# In[32]:


for table in m.tables.values():
    print(table.name)
    for column in table.c:
        print(f'Col: {column.name},\t, Type: {column.type}')


# Knowing all components, a query can be sent to get the required data from the database to a dataframe.
# By convention, SQL is written in all CAPS, even though this is not required for the statement to work.
# 
# To select all columns from a table, the wildcard character ```*``` is used. The syntax is ```SELECT <col1>, <col2> FROM <table>```.

# In[33]:


my_query = 'SELECT * FROM historical_data'

results = conn.execute(my_query)
df = pd.DataFrame(results.fetchall(), columns=results.keys())
df.head(2)


# In[34]:


# built-in function in Pandas
df2 = pd.read_sql_query(my_query, conn)
df2.head(2)


# For some sanity checks, not only regarding imports, the ```assert``` keyword will raise an error, if the trailing statement is not True. 

# In[35]:


assert df.equals(df2)


# To select specific columns only, the can be listed, separated by a comma

# In[36]:


my_query = 'SELECT open, close FROM historical_data'

df = pd.read_sql_query(my_query, conn)
print(df.head(2))

print('')
# select only first 10 entries with LIMIT
my_query = 'SELECT open, close FROM historical_data LIMIT 10'

df = pd.read_sql_query(my_query, conn)
print('only 10 rows:', df.shape)


# The dataset can be filtered before being loaded into a dataframe. To pose restrictions on the import of records, use ```WHERE``` after the table name.

# In[37]:


# select only first 10 entries with LIMIT
my_query = 'SELECT open, close FROM historical_data WHERE wday=0'   # note that 'wday' does not need to be imported

df = pd.read_sql_query(my_query, conn)
print('only mondays:\n', df.head())


# Only some of the other functions and commands will be shown, for a quick overview, see [this collection](https://www.sqltutorial.org/sql-cheat-sheet/).

# In[38]:


# Count occurrence
my_query = 'SELECT Count(*) FROM historical_data WHERE wday=0'   
mon = pd.read_sql_query(my_query, conn).values
print('number of monday records in dataset:\n', mon)


# In[39]:


# get distinct values
my_query = 'SELECT DISTINCT(wday) FROM historical_data'   
weekdays = pd.read_sql_query(my_query, conn).values
print('distinct weekdays in dataset:\n', weekdays)


# In[40]:


# calculate mean
my_query = 'SELECT ROUND(AVG(open),2) as mean_open FROM historical_data'   
mean_open = pd.read_sql_query(my_query, conn)
print(mean_open)


# In[41]:


# import Variable under different name
my_query = 'SELECT ROUND(open,2) as opening_price, ROUND(close, 2) as closing_price FROM historical_data'
df = pd.read_sql_query(my_query, conn)
print(df.columns.to_list())


# In order to automatically close connections after import or export, python offers the so-called *connection manager*. Usually, it is called with the keyword ```with``` and a variable after ```as```. The connection is only active in the indented block afterwards and is closed when leaving this body of the context manager.

# In[42]:


# engine is already created
with engine.connect() as conn:
    my_q = 'SELECT * FROM historical_data LIMIT 1'
    df = pd.read_sql_query(my_q, conn)
    
print(df)


# In[43]:


import os
os.getcwd()


# SQL offers a wide functionality, which is way beyond the scope of this course. To name just one more big advantage, not shown above, is that data from several related tables can be merged and loaded at once. 
