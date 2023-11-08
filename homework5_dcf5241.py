############################################################
# CMPSC442: Homework 5
############################################################

student_name = "Daniel Ferguson"

############################################################
# Imports
############################################################

import email
import math
import os

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    return_list = []
    
    obj = open(email_path,encoding="utf-8")
    msg = email.message_from_file(obj)
    msg_iter = email.iterators.body_line_iterator(msg)

    for x in msg_iter:
        line = x.split()
        for y in line:
            return_list.append(y)

    return return_list

def log_probs(email_paths, smoothing):
    frequency = {}
    log = {}
    count = 0
    
    for path in email_paths:
        for word in load_tokens(path):
            if word in frequency:
                frequency[word]+=1
            else:
                frequency[word]=1
            count+=1
            
    V = len(frequency)
    
    for x in frequency:
        log[x] = math.log((frequency[x]+smoothing)/(count+(smoothing*(V+1))))
    log["<UNK>"] = math.log(smoothing/(count+(smoothing*(V+1))))
    
    return log        

class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        spam_list=[]
        ham_list=[]
        spam_handle = spam_dir+"/"
        ham_handle = ham_dir+"/"
        
        for path in os.listdir(spam_dir):
            spam_list.append(spam_handle+path)
        for path in os.listdir(ham_dir):
            ham_list.append(ham_handle+path)
            
        self.spam_dic = log_probs(spam_list,smoothing)
        self.ham_dic = log_probs(ham_list,smoothing)
        
        spams = len(os.listdir(spam_dir))
        hams = len(os.listdir(ham_dir))
        total = spams+hams
        self.spam_prob = spams/total
        self.ham_prob = hams/total
    def is_spam(self, email_path):
        frequency = {}
        
        for word in load_tokens(email_path):
            if word in frequency:
                frequency[word]+=1
            else:
                frequency[word]=1
          
        spam_givenc = 0
        ham_givenc=0
        for word in frequency:
            #computing in log space. so * = + and ^ = *
            if word in self.spam_dic:
                spam_givenc += self.spam_dic[word]*frequency[word]
            else:
                spam_givenc += self.spam_dic["<UNK>"]*frequency[word]
                
            if word in self.ham_dic:
                ham_givenc += self.ham_dic[word]*frequency[word]
            else:
                ham_givenc += self.ham_dic["<UNK>"]*frequency[word]
                
        spam_percent=self.spam_prob*spam_givenc
        ham_percent=self.ham_prob*ham_givenc
        
        if spam_percent>ham_percent:
            return True
        else:
            return False

    def most_indicative_spam(self, n):
        ind_key_val={}
        hold=[]
        return_val=[]
        for key in self.spam_dic:
            if key in self.ham_dic:
                ind_key_val[key]=self.spam_dic[key]-math.log(math.exp(self.ham_dic[key])+math.exp(self.spam_dic[key]))
        hold = sorted(ind_key_val.items(),key=lambda x:x[1],reverse=True)
        for item in range(len(hold)):
            return_val.append(hold[item][0])
        return return_val[:n]

    def most_indicative_ham(self, n):
        ind_key_val={}
        hold=[]
        return_val=[]
        for key in self.ham_dic:
            if key in self.spam_dic:
                ind_key_val[key]=self.ham_dic[key]-math.log(math.exp(self.spam_dic[key])+math.exp(self.ham_dic[key]))
        hold = sorted(ind_key_val.items(),key=lambda x:x[1],reverse=True)
        for item in range(len(hold)):
            return_val.append(hold[item][0])
        return return_val[:n]

