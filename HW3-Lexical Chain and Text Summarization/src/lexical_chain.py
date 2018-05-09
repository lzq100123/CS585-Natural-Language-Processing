'''
@Author: Zhiquan Li
@CWID: A20381063
@IIT_CS584
'''
import nltk
from nltk.corpus import wordnet as wn
from Chain import Chain

def to_string(chain, word_counter):
    chain_to_print = ''
    size = chain.get_size()
    for idx, element in enumerate(chain.get_lexical_chain()):
        if idx < size - 1:
            chain_to_print += '%s(%d), ' %(element, word_counter[element])
        else:
            chain_to_print += '%s(%d)' %(element, word_counter[element])
    return chain_to_print


def get_relationships(word):
    syn_list = []
    anto_list = []
    hypo_list = []
    hyper_list = []
    for synset in wn.synsets(word):
        if synset.pos() == 'n':
            # synonyms extraction
            syn_list += synset.lemma_names()
                
            # antonyms extraction
            for lemma in synset.lemmas():
                for anto in lemma.antonyms():
                    anto_list += anto.synset().lemma_names()
            
            # hyponyms extraction
            for hypo in synset.hyponyms():
                hypo_list += hypo.lemma_names()
                    
            # hypernyms extraction
            for hyper in synset.hypernyms():
                hyper_list += hyper.lemma_names()

    return list(set(syn_list)), list(set(anto_list)), list(set(hypo_list)), list(set(hyper_list))


def chain_builder(nouns):
    chains = {}
    word_dict = {}
    for noun in nouns:
        if noun not in word_dict.keys():
            word_dict[noun] = 1
            is_new_chain = True
            
            for chain_key in chains.keys():
                if noun in chains[chain_key].syn_list or noun in chains[chain_key].anto_list or noun in chains[chain_key].hypo_list or noun in chains[chain_key].hyper_list:
                    chains[chain_key].add_word_to_lexical_chain(noun)
                    is_new_chain = False
                    break
                  
            if is_new_chain:
                syn_list, anto_list, hypo_list, hyper_list = get_relationships(noun)
                chains[noun] = Chain(noun, syn_list, anto_list, hypo_list, hyper_list)
        else:
            word_dict[noun] += 1
    return chains, word_dict

def core_words_extraction(word_chains, word_counter, avg_chain_lens, avg_word_freq):
    core_words = []
    for key in word_chains.keys():
        if word_chains[key].get_size() > avg_chain_lens:
            for word in word_chains[key].get_lexical_chain():
                if word_counter[word] > avg_word_freq:
                    core_words.append(word)

    return core_words


def text_summarization(sentences, core_words, noun_type, ratio = 0.1):
    result = []
    for sentence in sentences:
        s_tag = nltk.pos_tag(nltk.word_tokenize(sentence))
        s_nouns = [st[0] for st in s_tag if st[1] in noun_type]
        count = 0
        for cw in core_words:
            if cw in s_nouns:
                count += 1

        if (count / len(core_words)) > ratio:
            result.append(sentence)
    return result