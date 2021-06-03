#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import time


# In[2]:


#reading the database
APP_PATH = "C:/users/ishan"
data = pd.read_excel(
     os.path.join(APP_PATH, "Online Retail.xlsx"),
     engine='openpyxl',
)
data.head()


# In[3]:


#finding recency using invoice date and customer ID
recency = data[['InvoiceDate', 'CustomerID']]


# In[4]:


recency.apply(pd.Series.nunique)


# In[5]:


recency


# In[6]:


recency['InvoiceDate'] = pd.to_datetime(recency.InvoiceDate)
recent = max(recency['InvoiceDate'])


# In[7]:


recency = recency.groupby(['CustomerID']).max()
recency


# In[9]:


#determine quantitatively which customers are the best ones by examining how recently a customer has purchased
recent_purchase = recent - recency['InvoiceDate']
recent_purchase = pd.DataFrame(recent_purchase)
recent_purchase.head()


# In[10]:


#how often they purchase
frequency = data[['CustomerID', 'InvoiceDate']]
frequency = frequency.groupby(['CustomerID']).count()
frequency.head()


# In[11]:


#how much the customer spends
monetary = data[['CustomerID', 'UnitPrice']]
monetary = monetary.groupby(['CustomerID']).sum()
monetary.head()


# In[12]:


recency = pd.DataFrame(recent_purchase['InvoiceDate'].astype('timedelta64[D]'))
recency.columns = ['recency']
rfm = pd.concat([recency, frequency, monetary], axis=1)
rfm.columns=['recency', 'frequency', 'monetary']
rfm.head()


# In[13]:


rfm.quantile([.25, .5, .75, 1], axis=0)


# In[14]:


RFMscores = rfm.copy()
RFMscores['recency'] = [4 if x <= 22 else x for x in RFMscores['recency']]
RFMscores['recency'] = [3 if 22 < x <= 53 else x for x in RFMscores['recency']]
RFMscores['recency'] = [2 if 53 < x <= 111 else x for x in RFMscores['recency']]
RFMscores['recency'] = [1 if x > 111 else x for x in RFMscores['recency']]
RFMscores['frequency'] = [1 if a < 14 else a for a in RFMscores['frequency']]
RFMscores['frequency'] = [2 if 18 > a >= 14 else a for a in RFMscores['frequency']]
RFMscores['frequency'] = [3 if 22 > a >= 18 else a for a in RFMscores['frequency']]
RFMscores['frequency'] = [4 if a >= 22 else a for a in RFMscores['frequency']]
RFMscores['monetary'] = [1 if x < 781 else x for x in RFMscores['monetary']]
RFMscores['monetary'] = [2 if 781 <= x < 1227 else x for x in RFMscores['monetary']]
RFMscores['monetary'] = [3 if 1227 <= x < 1520 else x for x in RFMscores['monetary']]
RFMscores['monetary'] = [4 if 1520 <= x else x for x in RFMscores['monetary']]


# In[15]:


#80% of your business comes from 20% of your customers
RFMscores.apply(pd.Series.nunique)
score = pd.DataFrame((RFMscores['recency'] + RFMscores['frequency'] + RFMscores['monetary'])/3, columns=['AggrScore'])
RFMscores = pd.concat([RFMscores, score], axis = 1)
RFMscores.quantile([.80, 1], axis=0)


# In[16]:


loyalty = RFMscores['AggrScore'].iloc[[x >= 3.333333 for x in RFMscores['AggrScore']]]
loyal = pd.DataFrame(loyalty, columns = ['AggrScore'])
LoyalCustomers = list(loyal.index)
LoyalCustomers


# In[28]:


lost = RFMscores['AggrScore'].iloc[[x <= 1.0 for x in RFMscores['AggrScore']]]
lost_customer = pd.DataFrame(lost, columns = ['AggrScore'])
Lost_Customer = list(lost_customer.index)
Lost_Customer

