'''
@Author: Zhiquan Li
@CWID: A20381063
@IIT_CS584
'''
class Chain():
    
    def __init__(self, head, syn_list, anto_list, hypo_list, hyper_list):
        self.chain_head = head
        self.syn_list = syn_list
        self.anto_list = anto_list
        self.hypo_list = hypo_list
        self.hyper_list = hyper_list
        self.chain = [head]
        
    
    def get_size(self):
        return len(self.chain)

    def get_chain_head(self):
        return self.chain_head
    
    def get_synonyms(self):
        return self.syn_list
    
    def get_antonyms(self):
        return self.anto_list
    
    def get_hyponyms(self):
        return self.hypo_list
    
    def get_hypernyms(self):
        return self.hyper_list
    
    def get_lexical_chain(self):
        return self.chain
    
    def add_word_to_lexical_chain(self,noun):
        self.chain.append(noun)