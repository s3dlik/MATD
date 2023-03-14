import sys
import time
from collections import defaultdict

def read_ten_words(fileName):
    fileContent = []
    with open(fileName, "r", encoding='cp1252') as f:
        for line in f:
            for word in line.split():
                if len(fileContent) > 5:
                    break
                fileContent.append(word)          
    f.close()
    return fileContent

def read_big_file(fileName):
    with open(fileName, "r", encoding='cp1252') as f:
        lines = f.read()
        f.close()
    return lines

def brute_force(text, word):
    out_arr = []
    output_dct = {}
    for i in range(len(text) - len(word)+1):
        j = 0
        
        while(j < len(word)):
            if(text[i+j] != word[j]):
                break;
            j +=1
        
        if(j == len(word)):
            if not word in output_dct:
                    output_dct[word] = 0
            else:
                    output_dct[word] = output_dct[word] +1
                    #output.append(i+1)
    #print(f"Given pattern: {word} found on {', '.join(str(e) for e in out_arr)}")
    print(f"Word: {word} was found {output_dct.get(word)}x")
        
    
def handle_file(file):
    with open(file, "r") as f:
        lines = f.read()
        f.close()
    return lines
    
    
def next_state_ret(pattern, state, symbol, alphabet):
    
    if state < len(pattern) and alphabet[symbol] == pattern[state]: #check if state is < than length of pattern (it has to be lower) and check if symbol in alphabet (set of given text) is same as symbol in pattern
        return state +1
    iter = 0
    
    for next_state in range(state, 0, -1): #start from the largest number
        if pattern[next_state-1] == symbol:
            while(iter < next_state -1):
                if pattern[iter] != pattern[state-next_state+1+iter]: #stop when actual value is prefix and also suffix
                    break
                iter+=1
            if iter == next_state-1:
                return next_state
    return 0

def table_creation(pattern, alphabet):
    table = [[0] * len(alphabet) for _ in range(len(pattern) +1)]
    
    for state in range(len(pattern)+1):
        for symbol in range(len(alphabet)):
            next_state = next_state_ret(pattern, state, symbol, alphabet)
            table[state][symbol] = next_state
    return table

def dfa(pattern, txt, alphabet):
    
    table = table_creation(pattern, alphabet)
    lst = list()
    output_dct = {}
    state = 0
    for i in range(len(txt)):
        
        symbol_index = alphabet.index(txt[i])
        state = table[state][symbol_index]
        #print(f'i: {i}; State: {state}; patternlen: {len(pattern)}')
        if state == len(pattern):
            if not pattern in output_dct:
                    output_dct[pattern] = 0
            else:
                output_dct[pattern] = output_dct[pattern] +1
                    #output.append(i+1)
            #print(f'i: {i}; State: {state}; patternlen: {len(pattern)}')
            lst.append(i - len(pattern) +1)
            state = 0 #reset state because we would start over where we were
            
    #print(f"Given pattern: {pattern} found on {', '.join(str(e) for e in lst)}")
    print(f"Word: {pattern} was found {output_dct.get(pattern)}x")


def KMP(pattern, text):
    longest_sp = [0]*len(pattern)
    iterJ = 0
    out_arr = []
    output_dct = {}
    computeLSC(pattern, longest_sp)

    iter =0
    while (len(text)-iter) >= (len(pattern)-iterJ):
        if pattern[iterJ] == text[iter]:
            iter+=1
            iterJ+=1
            
        if iterJ == len(pattern):
            if not pattern in output_dct:
                output_dct[pattern] = 0
            else:
                output_dct[pattern] = output_dct[pattern] +1
           #out_arr.append(iter-iterJ)
            iterJ = longest_sp[iterJ-1]
            
        elif iter < len(text) and pattern[iterJ] != text[iter]:
            if iterJ != 0:
                iterJ = longest_sp[iterJ-1]
            else:
                iter+=1
    print(f"Word: {pattern} was found {output_dct.get(pattern)}x")

def computeLSC(pattern, longest_sp):
    len_prev = 0 #to hold previous longest suffix
    
    longest_sp[0] = 0 #first index is always zero
    iter = 1
    
    while iter < len(pattern):
        if pattern[iter] == pattern[len_prev]:
            len_prev+=1
            longest_sp[iter] = len_prev
            iter+=1
        else:
            if len_prev!= 0:
                len_prev = longest_sp[len_prev-1]
            else:
                longest_sp[iter] = 0
                iter+=1


def bad_char(pattern):
    m = len(pattern)
    dct = defaultdict(lambda: m)

    #print(pattern[0])
    iter = 0
    for i in range(m):
        if i == m-1:
            if pattern[i] not in dct:
                dct[pattern[i]] = m
        else:
            dct[pattern[i]] = m - i-1
        iter+=1
    return dct
    
    

def solveBMH(pattern, text):
    
    m = len(pattern)
    n = len(text)
    output = []
    output_dct = {}
    badCharArr = bad_char(pattern)
    
    if m> n:
        return -1
    
    k = m-1
    while(k < n):
        j = m-1
        i = k
        while j>= 0 and pattern[j] == text[i]:
            j -=1
            i -=1
            if j==-1:
                if not pattern in output_dct:
                    output_dct[pattern] = 0
                else:
                    output_dct[pattern] = output_dct[pattern] +1
                    #output.append(i+1)
        k += badCharArr[text[k]]
    print(f"Word: {pattern} was found {output_dct.get(pattern)}x")
    

if __name__ == "__main__":
   
    # n = len(sys.argv)
    # if(n > 2):
        # pattern = sys.argv[1]
        # txt_bef = sys.argv[2]
        # text = handle_file(txt_bef)
        
        #alphabet = list(set(text))
        
    patterns = read_ten_words("english.50MB")
    text_long = read_big_file("english.50MB")
    alphabet_long = list(set(text_long))
    
    if text_long and patterns:
        for pat in patterns:
            start = time.time()
            brute_force(text_long, pat)
            end = time.time()
            print(f'brute force time elapsed: {end-start}', "ns")
            
            start = time.time()
            dfa(pat, text_long, alphabet_long)
            end = time.time()
            print(f'DFA time elapsed: {end-start}', "ns")
            
            start = time.time()
            KMP(pat, text_long)
            end = time.time()
            print(f'KMP time elapsed: {end-start}', "ns")
           
            start = time.time()
            solveBMH(pat, text_long)
            end = time.time()
            print(f'BMH time elapsed: {end-start}', "ns")            
            
            
    # else:
    #     print(f'You passed incorrect number of arguments, you passed only {n} arguments')