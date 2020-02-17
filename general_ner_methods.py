#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os

# pip install --user stanfordnlp
from stanfordnlp.server import CoreNLPClient
# python -m spacy download en_core_web_lg
import spacy
import en_core_web_lg

import nltk
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

import re


# In[ ]:


'''

stanfordnlp is the wrapper of stanford nlp client, can do all functions including nre, open-ie, ...
spacy use OntoNotes 5 corpus
nltk is the wrapper of the stanford nlp ner part


'''


# In[ ]:


## spacy
nlp = en_core_web_lg.load()
doc = nlp(text)
for ele in doc.ents:
    print(ele.text, '\t\t\t', ele.label_)


# In[ ]:





# In[ ]:


## stanfordnlp client

'''
default: 
"ner.model": "edu/stanford/nlp/models/ner/english.all.3class.distsim.crf.ser.gz,"
                 "edu/stanford/nlp/models/ner/english.muc.7class.distsim.crf.ser.gz," 
                 "edu/stanford/nlp/models/ner/english.conll.4class.distsim.crf.ser.gz", 
can specify path as:
properties = {'ner.model': './stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz'}
'''


# In[ ]:


os.environ['CORENLP_HOME'] = './stanford-corenlp-full-2018-10-05'
properties = {'ner.model': './stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz,'
                            './stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz,'
                             './stanford-ner-2018-10-16/classifiers/english.conll.4class.distsim.crf.ser.gz'}
client = CoreNLPClient(annotators = ['tokenize', 'pos', 'lemma', 'ner'], 
                       memory = '8g', endpoint = 'http://localhost:9001') 
doc = client.annotate(text)
for sent in doc.sentence:
    for m in sent.mentions:
        print(m.entityMentionText, '\t\t\t', m.entityType)
client.stop() ## do not forget to stop the client


# In[ ]:





# In[ ]:


## nltk
nltk.download() # d-punkt-q
st = StanfordNERTagger('stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner-2018-10-16/stanford-ner.jar',
                        encoding='utf-8')

rt = 'this is a test, to see the result of nltk.'

tokenized_text = word_tokenize(rt)
classified_text = st.tag(tokenized_text)

orgs = []
org = ''
for ele in classified_text:
    
    if ele[1] == 'ORGANIZATION':
        org = org + ' ' + ele[0]
    else:
        if org != '':
            orgs.append(org.strip())
            org = ''
orgs


# In[ ]:





# In[ ]:




