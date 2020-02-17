#!/usr/bin/env python
# coding: utf-8

# In[ ]:


##########
# get one specific section of a html
##########

import os
from bs4 import BeautifulSoup


# In[ ]:





# In[ ]:


def download_html(soruce_txt_file, outpath):
    # soruce_txt_file: '/path/some.txt'
    file_name = soruce_txt_file.split('/')[-1][:-4]
    with open(os.path.join(outpath, file_name + '.htm'), 'w') as f:
        with open(soruce_txt_file, 'r') as g:
            for line in g.readlines():
                f.write(line)
            
    html_file = os.path.join(outpath, file_name + '.htm')
    
    return html_file


# In[ ]:


def get_contents(eles):
    
    eles_refine = []

    for ele in eles:

        ele_child = [k for k in ele.children]

        if not ele_child:
            eles_refine.append(ele)
        else:
            eles_refine.extend(ele_child)
            
    return eles_refine


# In[ ]:


def get_style(ele):
    try:
        ele_style = ele.font.get('style')
    except:
        try:
            ele_style = ele.get('style')
        except:
            ele_style = None
    return ele_style


# In[ ]:


def find_section_info(eles, keyword = 'Competition'):
    record = {}
    for i in range(len(eles)):
        ele = eles[i]
        
        try:
            ele_text = ele.text.strip()
            if keyword == ele_text: #ele.get_text():
                record['s_idx'] = i
                break
        except:
            continue
    
    if 's_idx' not in record:
        return record

    font_a = get_style(eles[record['s_idx']])
    record['font'] = font_a

    j = record['s_idx'] + 1
    while True:
        b = get_style(eles[j])
        if b is None: 
            j += 1
            continue
        if b == record['font']:
            record['e_idx'] = j
            break
        else:
            j += 1
    
    return record


# In[ ]:


def find_section_info_1(eles, keyword = ['Competition', 'COMPETITION']):
    record = {}
    for i in range(len(eles)):
        ele = eles[i]
        
        try:
            ele_text = ele.text.strip()
            if ele_text in keyword: #ele.get_text():
                record['s_idx'] = i
                break
        except:
            try:
                ele_text = ele.strip()
                if ele_text in keyword: #ele.get_text():
                    record['s_idx'] = i
                    break
            except:
                continue
            continue
    
    if 's_idx' not in record:
        return record

    
    font_a = get_style(eles[record['s_idx']])
    record['font'] = font_a

    j = record['s_idx'] + 1
    while True:
        b = get_style(eles[j])
        if b is None: 
            j += 1
            continue
        if b == record['font']:
            b_text = ''
            try:
                b_text = eles[j].text.strip()
            except:
                b_text = eles[j].strip()
            if b_text != '' and b_text != '\n' and b_text != '\xa0':
                record['e_idx'] = j
                break
            else:
                j += 1
        else:
            j += 1
    
    return record


# In[ ]:


def get_section_text(eles, record):
    
    if record == {}:
        return ''
    text = []
    s_idx = record['s_idx'] + 1
    e_idx = record['e_idx']
    for k in range(s_idx, e_idx):
        try:
            text_ = eles[k].text.strip()
        except:
            text_ = ''
        if text_:
            text.append(text_)
    text = ' '.join([k for k in text])
    text = text.replace('\xa0', ' ')
    text = text.replace('\n', ' ')
    return text


# In[ ]:


def get_section(soup):
    
    text = ''
    
    # div
    eles = list(soup.find_all('div'))
    eles_refine = get_contents(eles)
    record = find_section_info_1(eles_refine)
    text = get_section_text(eles_refine, record) 
    
    if text !='':
        return record, text
    
    # span
    eles = list(soup.find_all('span'))
    eles_refine = eles
    record = find_section_info_1(eles_refine)
    text = get_section_text(eles_refine, record) 
    
    if text !='':
        return record, text
    
    # p
    eles = list(soup.find_all('p'))
    eles_refine = eles
    record = find_section_info_1(eles_refine)
    text = get_section_text(eles_refine, record) 
    
    if text !='':
        return record, text
    
    return {}, ''


# In[ ]:





# In[ ]:


# test
soruce_txt_file = './download/testcase.txt'
outpath = './html_files/'
html_file = download_html(soruce_txt_file, outpath)

soup = BeautifulSoup(open(html_file), "html.parser") #, 'html5lib')
record, text = get_section(soup)


# In[ ]:





# In[ ]:




