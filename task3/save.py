class SearchWithMistake:
    def __init__(self, fileName, errors=1) -> None:
        self.current_state = 0
        self.state_number = []
        self.next_state = 0
        self.k = errors
        self.accept_states = []
        self.fileName = fileName
        self.states = [(0,0)] #seznam dvojic pro udrzeni stavu a mista v textu
        self.pos_in_dict = 0
        self.dictionary = []
        
    
    def open_file(self):
        with open(self.fileName, "r") as f:
            self.dictionary = [line.strip() for line in f]
    
    def solver(self, pattern):
        new_states = []

        for i in range(len(pattern)):
            for state in self.states:
                self.state_number, self.pos_in_dict = state
                
                if self.state_number % (len(pattern)+1) == 0: #kontrola pocatecniho stavu, pridani do pole, pro kontrolu
                    self.accept_states.append(i)
                    continue
                
                # elif self.pos_in_dict == len(pattern): #diagonalni posun dolu, jestlize uz jsme prosli cele retezce a zaroven prosli retezce v danem stavu
                #     self.next_state = self.state_number + 1
                    
                elif pattern[self.pos_in_dict] == self.dictionary[i]: #kontrola shody symbolu
                    self.next_state = self.state_number + 1
                    
                elif self.state_number % (len(pattern) +1) == 0: #zde je to trosku tricky, je opet potreba zkontrolovat, zda jsme se posunuli a jestli se symboly shoduji
                    self.next_state = self.state_number + 1
                    print(self.dictionary[i])
                    if pattern[self.pos_in_dict] != self.dictionary[i]:
                        self.next_state = self.state_number + len(pattern) + 2
                else:
                    self.next_state = self.state_number + 1 #shoda symbolu, pokud nevyjde ani jedna z podminek vyse
                    
                    if pattern[self.pos_in_dict] != self.dictionary[i]: #kontrola nadbytecneho symbolu, posun doprava
                        self.next_state = self.state_number + len(pattern) + 2
                        
                        if self.pos_in_dict < len(pattern) -1 and pattern[self.pos_in_dict +1] == self.dictionary[i]:
                            new_states.append((self.state_number + len(pattern) + 2, self.pos_in_dict + 1))
                        
            if self.next_state <= (len(pattern)+1) * (self.k+1) -1: #kontrola nejvyssiho mozneho stavu, ktery lze pouzit
                new_states.append((self.next_state, self.pos_in_dict+1))
                
        self.states = new_states
        
        
        min_distance = float('inf')
        words = []
        for state in self.states:
            self.state_number, self.pos_in_dict = state
            
            if self.state_number % (len(pattern) +1) == 0:
                distance = self.state_number // (len(pattern) +1)
                
                #zde se hleda nejmensi vzdalenost
                if distance <= self.pos_in_dict and distance < min_distance:
                    min_distance = distance
                    words = [self.dictionary[self.state_number // (len(pattern)+1) -1]]
                elif distance == min_distance:
                    words.append(self.dictionary[self.state_number // (len(pattern) +1) -1])

        return words
    

if __name__ == "__main__":
    
    swm = SearchWithMistake("text.txt")
    swm.open_file()
    
    print(swm.solver("dog"))