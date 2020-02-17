stanford_ner_folder = 'stanford-ner-2018-10-16'
# stanford_ner_model = 'classifiers/english.all.3class.distsim.crf.ser.gz'
# 'classifiers/english.conll.4class.distsim.crf.ser.gz'
# 'classifiers/english.muc.7class.distsim.crf.ser.gz'



from subprocess import Popen
from sys import stderr
import os

def stanford_ner(text, model_id = 3):
   
    if model_id == 3:
        stanford_ner_model = 'classifiers/english.all.3class.distsim.crf.ser.gz'
    if model_id == 4:
        stanford_ner_model = 'classifiers/english.conll.4class.distsim.crf.ser.gz'
    if model_id == 7:
        stanford_ner_model = 'classifiers/english.muc.7class.distsim.crf.ser.gz'


    with open('in_file.txt', 'w', encoding = 'utf-8') as input_file:
        input_file.write(text)     
    
    out = 'out.txt'
    command = ''
    # cd {}; 
    command += 'cd {}; java -mx1g -cp "*:lib/*" edu.stanford.nlp.ie.NERClassifierCombiner ' \
               '-ner.model {} ' \
               '-outputFormat tabbedEntities -textFile ../in_file.txt > ../{}' \
        .format(stanford_ner_folder, stanford_ner_model, out)


    java_process = Popen(command, stdout=stderr, shell=True)
    
    java_process.wait()

    with open(out, 'r') as output_file:
        results_str = output_file.readlines()
    os.remove(out)
    os.remove('in_file.txt')
    results = []
    for res in results_str:
        if len(res.strip()) > 0:
            split_res = res.split('\t')
            entity_name = split_res[0]
            entity_type = split_res[1]

            if len(entity_name) > 0 and len(entity_type) > 0:
                results.append([entity_name.strip(), entity_type.strip()])
    
    return results
    
    
    
if __name__ == '__main__':
    text = 'this is a test of JP Morgan Chase. where is Wells Fargo, BOA, and other?'
    
    text = '''
    We currently do not face any direct competition for robotic-assisted PCI as the CorPath System is the only FDA-cleared device for this indication.
    Robocath, a medical device company based in France, is developing a robotic system for use in PCI procedures but it is currently not approved/cleared
    by FDA or available for sale in the United States. We have some indirect competition in regard to other interventional procedures. There are three
    companies that make vascular robotic systems for electrophysiology procedures; Hansen Medical, Catheter Precision and Stereotaxis. Hansen Medical,
    which was acquired by Auris Surgical Robotics in 2016, also has a system used for peripheral vascular procedures. Although Auris Surgical Robotics is
    not currently marketing or selling this system, they may become a direct competitor for those procedures. Our primary focus today is on converting
    customers from the traditional manual procedure to the CorPath robotic procedure.\n'
    '''
    
    text_out = stanford_ner(text, model_id = 7)
    
    print(text_out)
    
    #with open('out_file.txt', 'w', encoding = 'utf-8') as g:
        #g.write(str(text_out)) 
