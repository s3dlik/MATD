import requests
import os
import string
import unicodedata
import re
from nltk.stem import *
import math


class PreText:
    def __init__(self) -> None:
        self.path = os.getcwd() + "/gutenberg"
        self.pathProc = os.getcwd() + "/gutenbergProc"
        self.invertDict = {} 
        self.sortedDict = {}


    def download(self, limit=100):
        
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        
        base_url = "https://www.gutenberg.org/files/"

        i = 1
        num = 0
        while num < limit:    
            book = str(i) + "-0.txt"
            extended_url = base_url + str(i) + "/" + book

            r = requests.get(extended_url)
            content = str(r.content)
            if not "<!DOCTYPE" in content:            
                open("gutenberg/" + book, 'wb').write(r.content)
                num += 1

            i += 1
            
    def handle_file(self):
        stop_list = ["a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
                 "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
                 "to", "was", "were", "will", "with"]
        pathProcessed = os.getcwd() + "/gutenbergProc"
        
        if not os.path.exists(pathProcessed):
            os.mkdir(pathProcessed)
        
        for file in os.listdir(self.path):
            text, file = self.open_file(file)
            text_split = text.split(' ')
            if os.path.isfile(pathProcessed + "/" + file):
                os.remove(pathProcessed + "/" + file)
            
            stemmer = PorterStemmer()
            processed_words = [stemmer.stem(w) for w in text_split if w not in stop_list]
            
            with open(pathProcessed + "/" + file, "w") as f:
                for word in processed_words:
                    f.write(word + '\n')
                
    def open_file(self, file):
        output_str = ''

        with open(self.path + "/" + file, 'r', encoding="iso-8859-15") as f:
            text = f.read()

        text = text.lower()
        text_reg = re.sub(r'[^a-zA-Z0-9\s]+', '', text)
        text_split = text_reg.split()
        text_str = ' '.join(text_split)
        text_norm = unicodedata.normalize('NFD', text_str)
        text_enc = text_norm.encode('ascii', 'ignore')
        text_dec = text_enc.decode('utf-8')

        
        return text_dec, file
    
    def open_file_word(self, file):
        with open(self.pathProc + "/" + file, 'r', encoding="iso-8859-15") as f:
            text = f.read()
        return text
    
    def invert_index(self):
        words = ['almost', 'gutenberg', 'project']
        for file in os.listdir(self.path):
            file_name = file.replace("-0.txt", "")
            whole_text = self.open_file_word(file)
            whole_text_split = whole_text.split('\n')

            for word in words:
                if word in whole_text_split:
                    if word not in self.invertDict:
                        self.invertDict[word] = [int(file_name)]
                    else:
                        if file not in self.invertDict[word]:
                            self.invertDict[word].append(int(file_name))
                        
        self.sortedDict = {k: sorted(v) for k, v in self.invertDict.items()}
    
    def intersect(self):
        answer = {}
        values = self.sortedDict.values()
        sets = [set(l) for l in values]
        result = self.intersection(sets)
        return list(result)
        
    def intersection(self, lsts):
           
        return set.intersection(*lsts)
    
    def intesect_first_alg(self, p1, p2, p3):
        answer = []
        i = j = k = 0
        while i < len(p1) and j < len(p2) and k < len(p3):
            if p1[i] == p2[j] == p3[k]:
                answer.append(p1[i])
                i += 1
                j += 1
                k += 1
            elif p1[i] < p2[j]:
                i += 1
            elif p2[j] < p3[k]:
                j += 1
            else:
                k += 1
        return answer

    def intersetct_second_alg(self, *posting_lists):
            terms = sorted(posting_lists, key=lambda x: len(x))
            result = self.postings(terms[0][0])
            terms = terms[1:]
            while terms and result:
                result = self.intersect_two(result, self.postings(terms[0]))
                terms = terms[1:]
            return result
        
    def postings(self, term):
        posting_list = self.sortedDict
        if term in posting_list:
            return posting_list[term]
        else:
            return []
    
    def intersect_two(self, postings1, postings2):
        result = []
        i = 0
        j = 0
        while i < len(postings1) and j < len(postings2):
            if postings1[i] == postings2[j]:
                result.append(postings1[i])
                i += 1
                j += 1
            elif postings1[i] < postings2[j]:
                i += 1
            else:
                j += 1
        return result
    
    
    def vector_model(self, t):
        tf_t_d = 0
        result = dict()

        N = os.listdir(self.pathProc)
        N_size = len(N)
        df_t = {}
        for d in os.listdir(self.pathProc):
            with open(self.pathProc + '/' + d, "r") as f:
                data = f.read()
            
            #basic frequency
            for term in t:
                if term in data:
                    if term not in df_t:
                        df_t[term] = 1
                    else:
                        df_t[term] += 1    
                if d not in result:
                    result[d] = {term : data.count(term)}    
                else:
                    result[d][term] = data.count(term) 
            
                
                #print(f"N_size: {N_size}, df_t: {df_t}, term: {term}, document: {d}")
        
        
        output = {word: [] for word in t}
        for term in t:
            tmp = []
            for key, value in result.items():
                idf_t = math.log(N_size/df_t[term])
                idf_t_d = idf_t * value[term]
                
                tmp.append([int(key.replace('-0.txt','')), idf_t_d])
            output[term] = tmp
            
        
            
        return output
                
                
    def calc_score(self, dct):
        final_scores = {}
        for lst in dct.keys():
            for item in dct[lst]:
                if item[0] in final_scores:
                    final_scores[item[0]] += item[1]
                else:
                    final_scores[item[0]] = item[1]
        return final_scores
        
    def find_top_ten(self, results):
        return dict(sorted(results.items(), key = lambda item: item[1], reverse = True)[:10])
if __name__ == '__main__':
    pretext = PreText()    
    # pretext.download()
    # pretext.handle_file()
    pretext.invert_index()
    
    tf_idf_weight = pretext.vector_model(['georg', 'almost'])
    #print(tf_idf_weight)
    scores = pretext.calc_score(tf_idf_weight)
    print(pretext.find_top_ten(scores))
    # #(word1 AND word2) AND word3 bude rychlejší než word1 AND (word2 AND word3).
    # # v prvnim pripade se spoji dva mensi seznamy dokumentu a porom se to teprve porovnava s tim tretim
    # #ve druhem prpade se musi spojit dva vetsi a az nasledne potom s tim mensim, coz je pomalejsi
    #16b