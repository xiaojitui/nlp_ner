# nlp_ner

The scripts are used to do NER and extract company names from html or text file. 

Need to download stanford ner packages into 'stanford-ner-2018-10-16' folder and stanford full packages into 'stanford-corenlp-full-2018-10-05' folder. 

<br><br>
The descriptions of each script:
- 'general_ner_methods.py' shows how to use 3 NER packages: Spacy, StanfordNLP Server, and NLTK
- 'stanfordner_wrapper.py' is a personalized wrapper to run StanfordNLP NER in terminal

- 'parse_html_to_txt.py' is used to parse html into text
- 'extract_ner_from_txt.py' is used to extract NER (e.g. company names) from text
- 'match_ner_to_string.py' is used to match NERs with strings (e.g. map parsed companies to known company list)

The workflow is to run 'parse_html_to_txt.py', then 'extract_ner_from_txt.py', then 'match_ner_to_string.py'.

The 'skip_names.txt' lists some common words which should not be recognized as company names. 
