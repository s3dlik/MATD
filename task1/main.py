import sys

def brute_force(text, word):
    for i in range(len(text) - len(word)+1):
        j = 0
        
        while(j < len(word)):
            if(text[i+j] != word[j]):
                break;
            j +=1
        
        if(j == len(word)):
            print(f'Word found at index: {i}')
        
    
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
    
    state = 0
    for i in range(len(txt)):
        
        symbol_index = alphabet.index(txt[i])
        state = table[state][symbol_index]
        print(f'i: {i}; State: {state}; patternlen: {len(pattern)}')
        if state == len(pattern):
            #print(f'i: {i}; State: {state}; patternlen: {len(pattern)}')
            lst.append(i - len(pattern) +1)
            state = 0 #reset state because we would start over where we were
            
    print(f"Given text: {txt} and given pattern: {pattern} found on {', '.join(str(e) for e in lst)}")

if __name__ == "__main__":
   
    n = len(sys.argv)
    print(sys.argv[0])
    if(n > 2):
        pattern = sys.argv[1]
        txt_bef = sys.argv[2]
        text = handle_file(txt_bef)
        
        alphabet = list(set(text))
        if text and pattern:
            print('Brute force output:')
            brute_force(text, pattern)
            print()
            print("DFA output")
            dfa(pattern, text, alphabet)
    else:
        print(f'You passed incorrect number of arguments, you passed only {n} arguments')