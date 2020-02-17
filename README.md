# nlp_ner

The scripts are used to do NER and extract company names from html or text file. 

Need to download stanford ner packages into 'stanford-ner-2018-10-16' folder and stanford full packages into 'stanford-corenlp-full-2018-10-05' folder. 


The descriptions of each script:
(1) 'general_ner_methods.py' shows how to use 3 NER packages: Spacy, StanfordNLP Server, and NLTK
(2) 'stanfordner_wrapper.py' is a personalized wrapper to run StanfordNLP NER in terminal

(3) 'parse_html_to_txt.py' is used to parse html into text
(4) 'extract_ner_from_txt.py' is used to extract NER (e.g. company names) from text
(5) 'match_ner_to_string.py' is used to match NERs with strings (e.g. map parsed companies to known company list)

The workflow is to run (3), then (4), then (5).

The 'skip_names.txt' lists some common words which should not be recognized as company names. 
