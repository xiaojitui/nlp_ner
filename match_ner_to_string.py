#!/usr/bin/env python
# coding: utf-8


import pickle
import os

# pip install fuzzywuzzy
from fuzzywuzzy import fuzz

import pandas as pd
import numpy as np

from tqdm import tqdm
from collections import Counter


import multiprocessing as mp
from functools import partial 
from tqdm import tqdm
from datetime import datetime

with open('./skip_names.txt', 'r') as f:
    lines = f.readlines()
add_skip_names = eval(lines[0])

def is_sub_name(name, target, skip_names, thresh = 1):
    
    in_target = 0
    in_skip = 0            
                
    eles = name.lower().strip().split()
    eles = [k.strip(' ,.() ') for k in eles]
    target_eles = target.lower().strip().split()
    target_eles = [k.strip(' ,.() ') for k in target_eles]

    for ele in eles:
        
        if len(ele) < 3:
            continue
        if ele in skip_names:
            in_skip += 1
        
        if ele in target_eles:
            if ele not in skip_names:
                in_target += 1
        
        # special case
        if '.' in ele:
            ele = ele.replace('.', '')
            if ele in target_eles and ele not in skip_names:
                in_target += 1
        #
        
        # special case
        if '-' in ele:
            ele = ele.replace('-', '')
            if ele in target_eles and ele not in skip_names:
                in_target += 1
        #
        
        # special case
        if np.any([(ele in k) and (len(ele)/len(k) > 0.6) for k in target_eles]):
            if ele not in skip_names:
                in_target += 1
        
    if in_target == 0 and in_skip == len(eles) and len(eles) > 1:
        in_target = 1

    return in_target



def match_factset_id(name, factset_id_map, skip_names, thresh = 70):
    
    results = []
    
    eles = name.lower().strip().split()
    eles = [k.strip('.').strip(',') for k in eles]
    for target in factset_id_map:
        factset_ids = eval(factset_id_map[target])
        
        for factset_id in factset_ids:
            for ele in eles:
                if ele in skip_names:
                    continue
                ratio = fuzz.ratio(ele, factset_id.lower())
                #if (ele in factset_id.lower() or factset_id.lower() in ele) and (ratio >= thresh):
                if ratio >= thresh:
                    results.append([target, ratio])
                    #in_target += 1
                    #print(ele, '\t', factset_id)
    
    if results:
        is_in_name_max = max([k[1] for k in results])
        results = [k for k in results if k[1] == is_in_name_max]
        
    return results

def match_company_v1(name_list, target_names, skip_names, factset_id_ratio = 70, fuzz_ratio = 70, string_ratio = 1):
    
    record = {}
    
    for name in name_list:
        record[name] = {}
            
        if len(name.strip(' ,.() ')) < 3:
            record[name]['match_target'] = 'Not Found'
            record[name]['fuzzy_results'] = []
            record[name]['string_results'] = []
            record[name]['factset_id_results'] = []
            continue
        
        found_names = []
        check_names = []
        factset_names = []
        
        for target in target_names:
    
            ratio1 = fuzz.ratio(name.lower(), target.lower())
            ratio2 = fuzz.token_sort_ratio(name.lower(), target.lower())
            is_in_name = is_sub_name(name, target, skip_names, thresh = string_ratio)

            if is_in_name:
                if ratio1 >= fuzz_ratio:
                    found_names.append([target, ratio1])
                    #print(name, '\t', ratio1, '\t', 'r1')
                elif ratio2 >= fuzz_ratio:
                    found_names.append([target, ratio2])
                    #print(name, '\t', ratio2, '\t', 'r2')
                else:
                    check_names.append([target, is_in_name])
    


        found_names = sorted(found_names, key = lambda x: x[1], reverse = True)

        #if found_names:
            #max_ratio = max([k[1] for k in found_names])
            #found_names = [k for k in found_names if k[1] == max_ratio]

        if check_names:
            is_in_name_max = max([k[1] for k in check_names])
            check_names = [k for k in check_names if k[1] == is_in_name_max]
            
        
        if not found_names and not check_names:
            factset_names = match_factset_id(name, factset_id_map, skip_names, thresh = factset_id_ratio)
        
        if found_names:
            most_possible_target = found_names[0][0]
        elif check_names:
            most_possible_target = check_names[0][0]
        elif factset_names:
            most_possible_target = factset_names[0][0]
        else:
            most_possible_target = 'Not Found'
            
    
        record[name]['match_target'] = most_possible_target
        record[name]['fuzzy_results'] = found_names
        record[name]['string_results'] = check_names
        record[name]['factset_id_results'] = factset_names
        
    return record

def match_company_v2(name_list, target_names, skip_names, factset_id_ratio = 70, fuzz_ratio = 70, string_ratio = 1):
    
    record = {}
    
    for name in name_list:
        record[name] = {}
        
        if len(name.strip(' ,.() ')) < 3:
            record[name]['match_target'] = 'Not Found'
            record[name]['fuzzy_results'] = []
            record[name]['string_results'] = []
            record[name]['factset_id_results'] = []
            continue
        
        found_names = []
        check_names = []
        factset_names = []
        
        for target in target_names:
    
            ratio1 = fuzz.ratio(name.lower(), target.lower())
            ratio2 = fuzz.token_sort_ratio(name.lower(), target.lower())
            is_in_name = is_sub_name(name, target, skip_names, thresh = string_ratio)

            if is_in_name:
                if ratio1 >= fuzz_ratio:
                    found_names.append([target, ratio1])
                    #print(name, '\t', ratio1, '\t', 'r1')
                elif ratio2 >= fuzz_ratio:
                    found_names.append([target, ratio2])
                    #print(name, '\t', ratio2, '\t', 'r2')
                else:
                    check_names.append([target, is_in_name])
    


        found_names = sorted(found_names, key = lambda x: x[1], reverse = True)

        #if found_names:
            #max_ratio = max([k[1] for k in found_names])
            #found_names = [k for k in found_names if k[1] == max_ratio]

        if check_names:
            is_in_name_max = max([k[1] for k in check_names])
            check_names = [k for k in check_names if k[1] == is_in_name_max]
            
        
        if not found_names and not check_names:
            factset_names = match_factset_id(name, factset_id_map, skip_names, thresh = factset_id_ratio)
        
        if found_names:
            most_possible_target = found_names[0][0]
        elif check_names:
            most_possible_target = check_names[0][0]
        elif factset_names:
            most_possible_target = factset_names[0][0]
        else:
            most_possible_target = 'Not Found'
            
    
        record[name]['match_target'] = most_possible_target
        full_results_tmp  = found_names + check_names + factset_names
        
        full_results = []
        if full_results_tmp:
            for k in full_results_tmp:
                if k[0] not in full_results:
                    full_results.append(k[0])
        
        record[name]['full_results'] = full_results
    return record
        
        
def string_match_v1(file_dict, kf):
    files = file_dict[kf]
    ############################# 
    ## parse
    
    record = {}
    for file in tqdm(files):
        with open(os.path.join(path, file), 'rb') as f:
            data = pickle.load(f)
        com_names = data['compnames']

        if not com_names:
            record[file]  = {'match_result': {}, 'fuzzy_results': {}, 'string_results':{}, 'factset_id_results':{}}
            continue

        result = match_company_v1(com_names, names, skip_names, factset_id_ratio = 90, fuzz_ratio = 70, string_ratio = 1)
        
        match_result = dict([(com, result[com]['match_target']) for com in result])
        fuzzy_results = dict([(com, result[com]['fuzzy_results']) for com in result])
        string_results = dict([(com, result[com]['string_results']) for com in result])
        factset_id_results = dict([(com, result[com]['factset_id_results']) for com in result])
        
        record[file] = {'match_result': match_result, 
                        'fuzzy_results': fuzzy_results, 
                        'string_results': string_results, 
                        'factset_id_results': factset_id_results}

        
    with open('/tmp/record_%d.pkl' % kf, 'wb') as f:
        pickle.dump(record, f)
        

def string_match_v2(file_dict, kf):
    files = file_dict[kf]
    ############################# 
    ## parse
    
    record = {}
    for file in tqdm(files):
        with open(os.path.join(path, file), 'rb') as f:
            data = pickle.load(f)
        com_names = data['compnames']

        if not com_names:
            record[file]  = {'match_result': {}, 'full_record': {}}
            continue

        result = match_company_v1(com_names, names, skip_names, factset_id_ratio = 90, fuzz_ratio = 70, string_ratio = 1)
        match_result = dict([(com, result[com]['match_target']) for com in result])
        full_result = dict([(com, result[com]['full_results']) for com in result])
        record[file] = {'match_result': match_result, 'full_record': full_result}

        
    with open('./tmp/record_%d.pkl' % kf, 'wb') as f:
        pickle.dump(record, f)


############################# 
## read parsed company
path = './data/'
files = os.listdir(path)

############################# 
## read company map
with open('./data/company_record.pkl', 'rb') as f:
    comid = pickle.load(f)

names = comid.name.values

factset_id_map = dict(zip(comid.name, comid.factset_id))
factset_ids_ = list([eval(k) for k in factset_id_map.values()])
factset_ids = []
for k in factset_ids_:
    factset_ids.extend(k)
############################# 


############################# 
## prepare skip_words
clean_names = []
for name in names:
    name_eles = name.lower().strip().split()
    clean_names.extend(name_eles)

clean_names = Counter(clean_names)
clean_names = sorted(clean_names.items(), key = lambda x: x[1], reverse = True)
clean_names = dict(clean_names)

#add_skip_names = ['company', 'labs', 'corporation', 'government', 'and', 'supply', 'central', 'lp', 'motor']
skip_names = [k for k in clean_names if clean_names[k] >=10]
for k in add_skip_names:
    if k not in skip_names:
        skip_names.append(k)
############################# 


if __name__ == '__main__':
    
    ############################# 
    ## parse example
    
    #text = ['Bank of America','PNC Bank','Wells Fargo','Investors Bank','Facebook','Microsoft', 'Google Inc.']
    #aaa = match_company(text, names, skip_names, factset_id_ratio = 90, fuzz_ratio = 70, string_ratio = 1)
    #bbb = dict([(com, aaa[com]['match_target']) for com in aaa])
    
    ############################# 
    ## parse
    
    Number_of_workers = 40
    file_dict = {}
    for x in range(Number_of_workers):
        file_dict[x]=[]
    i=0
    for file in files:
        file_dict[i%Number_of_workers].append(file)
        i+=1


    print('multiprocess %d tasks'%len(file_dict))
    t0 = datetime.now()
    pool = mp.Pool(Number_of_workers)
    job = partial(string_match_v1, file_dict)
    for _ in pool.imap_unordered(job, tqdm(range(Number_of_workers), total = Number_of_workers), chunksize = 1):
        pass
    pool.close()
    pool.join()
    
    
    
    allrecord = {}
    for i in tqdm(range(Number_of_workers)):
        with open('./tmp/record_%d.pkl' % i, 'rb') as f:
            record = pickle.load(f)
        allrecord.update(record)
    with open('./match_result.pkl', 'wb') as f:
            pickle.dump(allrecord, f)
            
            
    print("Finished in ", datetime.now() - t0)
