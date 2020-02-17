#!/usr/bin/env python
# coding: utf-8

# In[2]:


import json
import os


# ## read patent
with open('patent_example.json', 'r') as f:
    patent = json.load(f)



with open('patent_example.json', 'r') as f:
    file_content  = f.readlines()
    file_content = [k.strip() for k in file_content]


p_tmp = '{' + ''.join(k for k in file_content[:-1]) + '}}'
patent = json.loads(p_tmp)


# In[8]:
patent.keys()


# In[9]:
patent['10429177'].keys()


# In[10]:
patent['10429177']['assignees']


# In[11]:
# list - dict
patent['10429177']['assignees'][0]['assignee_organization']


# In[ ]:




