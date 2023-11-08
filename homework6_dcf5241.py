############################################################
# CMPSC 442: Homework 6
############################################################

student_name = "Daniel Ferguson"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import os

############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    big_list=[]
    fd = os.open(path,os.O_RDONLY)
    fo = os.fdopen(fd)
    
    for line in fo:
        small_list=[]
        for token in line.split():
            small_list.append(tuple(token.split("=")))
            
        big_list.append(small_list)
    
    return big_list
    

class Tagger(object):

    def __init__(self, sentences):
        smooth = 1e-4
        self.num_POS = {"NOUN":0,"VERB":0,"ADJ":0,"ADV":0,"PRON":0,"DET":0,"ADP":0,
                         "NUM":0,"CONJ":0,"PRT":0,".":0,"X":0}
        
        init_num_POS = {"NOUN":0,"VERB":0,"ADJ":0,"ADV":0,"PRON":0,"DET":0,"ADP":0,
                         "NUM":0,"CONJ":0,"PRT":0,".":0,"X":0}
        
        POS_num_tokens_dic = {"NOUN":{},"VERB":{},"ADJ":{},"ADV":{},"PRON":{},"DET":{},"ADP":{},
                         "NUM":{},"CONJ":{},"PRT":{},".":{},"X":{}}
        
        POS_to_POS_dic= {"NOUN":{},"VERB":{},"ADJ":{},"ADV":{},"PRON":{},"DET":{},"ADP":{},
                         "NUM":{},"CONJ":{},"PRT":{},".":{},"X":{}}
        
        last_POS = None
        for line in sentences:
            init_num_POS[line[0][1]]+=1
            
            for token,POS in line:
                self.num_POS[POS]+=1
                
                if last_POS != None:
                    next_POS_dic = POS_to_POS_dic[last_POS]
                    if POS not in next_POS_dic:
                        next_POS_dic[POS] = 1+smooth
                    else:
                        next_POS_dic[POS] +=1
                
                POS_tokens = POS_num_tokens_dic[POS]
                if token not in POS_tokens:
                    POS_tokens[token] = 1+smooth
                else:
                    POS_tokens[token] += 1
                                    
                last_POS = POS
                
        for POS in self.num_POS.keys():
            POS_count = self.num_POS[POS]
            
            # transition
            next_POS_dic = POS_to_POS_dic[POS]
            for next_POS in next_POS_dic.keys():
                next_POS_dic[next_POS] = next_POS_dic[next_POS]/(POS_count+smooth*12)
            # emission
            POS_tokens = POS_num_tokens_dic[POS]
            for token in POS_tokens.keys():
                POS_tokens[token] = POS_tokens[token]/(POS_count+len(POS_tokens)*smooth)
                
        self.transition_prob = POS_to_POS_dic
        self.emission_prob = POS_num_tokens_dic
        
        holder = {}
        for POS in init_num_POS.keys():
            holder[POS] = (init_num_POS[POS]+smooth)/(len(sentences)+smooth*12)
        self.init_POS_prob = holder            

    def most_probable_tags(self, tokens):
        prob_tags = []
        for token in tokens:
            argmax = 0
            start_POS = "NOUN"
            for POS in self.num_POS.keys():
                POS_emission_dic = self.emission_prob[POS]
                if token in POS_emission_dic and POS_emission_dic[token]>argmax:
                    argmax=POS_emission_dic[token]
                    start_POS = POS
            
            prob_tags.append(start_POS)
        return prob_tags

