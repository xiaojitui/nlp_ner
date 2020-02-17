#!/usr/bin/env python
# coding: utf-8


# pip install fuzzywuzzy
# python -m spacy download en_core_web_lg
# python -m nltk.downloader all
### or python -m nltk.downloader punkt

import pickle
import os
import glob
#from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np
from tqdm import tqdm
import re
import copy
import spacy
import en_core_web_lg
import nltk
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import multiprocessing as mp 
from functools import partial
from tqdm import tqdm



spacynlp = en_core_web_lg.load()
st3 = StanfordNERTagger('stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner-2018-10-16/stanford-ner.jar',
                        encoding='utf-8')
st4 = StanfordNERTagger('stanford-ner-2018-10-16/classifiers/english.conll.4class.distsim.crf.ser.gz',
                       'stanford-ner-2018-10-16/stanford-ner.jar',
                        encoding='utf-8')
st7 = StanfordNERTagger('stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
                       'stanford-ner-2018-10-16/stanford-ner.jar',
                        encoding='utf-8')


with open('./skip_names.txt', 'r') as f:
    lines = f.readlines()
add_skip_names = eval(lines[0])


def parse_worker(file):
    with open(file, 'rb') as f:
        text_dict = pickle.load(f)
    _k = list(text_dict.keys())[0]
    
    texts = text_dict[_k]['competition_text']
    # 'texts' is a list of sentence 
      
    texts_ = get_text(texts)
    ners = get_all_ner(texts_)
    compnames = clean_ner(ners)
    newcoms = add_ner(texts_, compnames) ### this is optional
    
    #newcoms = compnames### if no need to add new items
    newcoms = preprocess_ner(newcoms)
    newcoms = clean_ner(newcoms)
    
    if newcoms:
        new_dict= {}
        sec_index = text_dict[_k]['comp_index']
        new_dict = {'filename': _k, 'sections': text_dict[_k]['sections'][sec_index[0]: sec_index[1]], 'text': texts, 'compnames': newcoms}
        with open(os.path.join('/data/',os.path.basename(_k)[:-4] + '.pkl'), 'wb') as pf:
            pickle.dump(new_dict, pf)
    return


# In[ ]:





# In[19]:


def get_stanford_ner(tokenized_text, st):
    ners = []
    classified_text = st.tag(tokenized_text)
    org = ''
    for ele in classified_text:

        if ele[1] == 'ORGANIZATION':
            org = org + ' ' + ele[0]
        else:
            if org != '':
                ners.append(org.strip())
                org = ''
    return ners


# In[24]:


def preprocess_ner(ners):
    
    ners = [re.sub('^the|^The|^THE|and$|AND$|And$', '', k) for k in ners]
    ners = [re.sub(' ,', ',', k) for k in ners]
    ners = [k.strip().strip('.').strip(',').strip() for k in ners]
    
    #### check 'and'
    skip_eles = []
    for eles in ners:
        eles1 = [k.strip().strip('.').strip(',') for k in eles.split('and')]
        if len(eles1) > 1 and np.all([k in ners for k in eles1]):
            skip_eles.append(eles)
    #### 

    ners_clean = []  
    for eles in ners:
        if eles not in ners_clean and eles not in skip_eles:
            ners_clean.append(eles)
    return ners_clean


# In[25]:


def get_all_ner(text):

    ners = []
    
    # Spacy
    doc = spacynlp(text)
    for ele in doc.ents:
        if ele.label_ == 'ORG':
            ners.append(ele.text)
    
    
    # Stanford:
    tokenized_text = word_tokenize(text)
    
    # standford: 3, 4, 7 class
    ners.extend(get_stanford_ner(tokenized_text, st3))
    ners.extend(get_stanford_ner(tokenized_text, st4))
    ners.extend(get_stanford_ner(tokenized_text, st7))
    
    # clean
    ners_clean = preprocess_ner(ners)
            
    return ners_clean


# In[ ]:





# In[26]:


def get_text(data):
    
    #text = ''.join([k.strip() for k in data])
    text = ''.join([k for k in data])
    text = re.sub('\/', ', ', text)
    text = re.sub("’s|’", ', ', text)
    text = re.sub('\xa0|\n|\t|●|•', ' ', text)
    text = re.sub('\s+', ' ', text)
    
    
    text = text.replace('FDA approval', '')
    text = text.replace('FDA approved', '')
    text = text.replace('FDA-cleared', '')
    
    return text.strip()


# In[ ]:





# In[38]:


def clean_ner(compnames, name_len = 8):
 
    compnames_clean = []
    for name in compnames:
        if len(name.split()) == 1:
            if name.strip().strip('.').strip(',').lower() in skip_names:
                continue
            else:
                if name not in compnames_clean:
                    compnames_clean.append(name)
        elif len(name.split()) <= name_len and 'table of contents' not in name.lower().strip(' ,.() '):
            if name not in compnames_clean:
                compnames_clean.append(name)
        else:
            continue
            
    compnames_clean = [k for k in compnames_clean if k]
    compnames_clean = [k.strip(' ,.() ') for k in compnames_clean if k]
    
    return compnames_clean


# In[ ]:





# In[39]:


def find_seg(s_indx, e_indx, delta):
    
    segs = []
    for i in s_indx:
        for j in e_indx:
            if j > i:
                segs.append([i+delta, j])
                break
    return segs
    


# In[ ]:





# In[40]:


def find_add_names(text, compnames, segs):
    add_eles = []
    for seg in segs:
        eles = text[seg[0]: seg[1]]
        eles = re.split(',|;|and', eles)
        eles = [k.strip() for k in eles]
        
        
        if np.any([k in compnames for k in eles]):
            for ele in eles:
                if ':' not in ele and np.sum([k.strip()[0].isupper() for k in ele.split()]) >= 0.6 * len(ele.split()):
                    add_eles.append(ele)

    return add_eles


# In[ ]:





# In[41]:


def find_short_ele(text):
    
    eles = re.split('\.|,|;|and', text)
    eles = [k.strip() for k in eles]
    eles = [k for k in eles if k]
    
    add_eles = []

    for ele in eles:
        
        if ":" in ele:
            continue
        ele1 = [k.strip().strip('.').strip(',') for k in ele.split()]

        upper_w = np.sum([k[0].isupper() for k in ele1])

        if len(ele1) <= 8 and upper_w > 0.6 * len(ele1):
            add_eles.append(ele)
    return add_eles


# In[ ]:





# In[46]:


def add_ner(text, compnames, name_len = 8):
    
    segs = []
    e_indx = [a.start() for a in list(re.finditer('\. ', text))]
    if not e_indx:
        e_indx = [len(text)]
    
    s1 = [a.start() for a in list(re.finditer('including', text))]
    if s1:
        seg = find_seg(s1, e_indx, delta = len('including'))
        segs.extend(seg)
    s2 = [a.start() for a in list(re.finditer('such as', text))]
    if s2:
        seg = find_seg(s2, e_indx, delta = len('such as'))
        segs.extend(seg)
        
    s3 = [a.start() for a in list(re.finditer(':', text))]
    if s3:
        seg = find_seg(s3, e_indx, delta = 1)
        segs.extend(seg)
    s4 = [a.start() for a in list(re.finditer('include', text))]
    if s4:
        seg = find_seg(s4, e_indx, delta = len('include'))
        segs.extend(seg)
    s5 = [a.start() for a in list(re.finditer('competitors are', text))]
    if s5:
        seg = find_seg(s4, e_indx, delta = len('competitors are'))
        segs.extend(seg)
        
    if not segs:
        return compnames
    
    add_coms1 = find_add_names(text, compnames, segs)
    #add_coms2 = find_short_ele(text)
    add_coms2 = []
    add_coms = add_coms1 + add_coms2
    
    compnames_clean = copy.deepcopy(compnames)
    for com in add_coms:
        if com not in compnames_clean and len(com.split()) <= name_len:
            compnames_clean.append(com)
    return compnames_clean


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ## Script run

# In[ ]:


if __name__ == '__main__':

    all_files = glob.glob('/input_files/*parsed_v1.pkl')

    Number_of_workers = 40 
#     parse_worker(all_files[0])
    print("run the job")
    print('multiprocess %d tasks'%len(all_files))
    pool = mp.Pool(Number_of_workers)
    job = partial(parse_worker)
    for _ in pool.imap_unordered(job, tqdm(all_files, total = len(all_files))):
        pass
    pool.close()
    pool.join()
