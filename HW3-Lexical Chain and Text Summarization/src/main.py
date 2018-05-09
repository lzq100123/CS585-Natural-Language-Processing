'''
@Author: Zhiquan Li
@CWID: A20381063
@IIT_CS584
'''
from lexical_chain import (chain_builder, to_string, core_words_extraction, text_summarization)
import sys
import nltk


def main():
    
    if len(sys.argv) == 3:
        file_path = sys.argv[1]
        result_path = sys.argv[2]
    else:
        print('please provide input path and result path')
        return
    with open(file_path,'r',encoding='utf-8') as f:
        lines = f.read()

    word_tag = nltk.pos_tag(nltk.word_tokenize(lines))
    noun_type = ['NN','NNP','NNS','NNPS']
    nouns = [wt[0] for wt in word_tag if wt[1] in noun_type]
    sentence_list = [para.split('.') for para in lines.split('\n')]
    sentences = []
    for sl in sentence_list:
        sentences += sl


    word_chains, word_counter = chain_builder(nouns)

    count = 1
    chains_lens = len(word_chains.keys())
    lens_sum = 0
    for chain_key in word_chains.keys():
        print('Chain %d: %s \n' %(count, to_string(word_chains[chain_key], word_counter)))
        count += 1
        lens_sum += word_chains[chain_key].get_size()

    avg_chain_lens = lens_sum / chains_lens
    word_freq_sum = 0
    words_lens = len(word_counter.keys())
    for key in word_counter.keys():
        word_freq_sum += word_counter[key]
    avg_word_freq = word_freq_sum / words_lens
    core_words = core_words_extraction(word_chains, word_counter, avg_chain_lens, avg_word_freq)
    result = text_summarization(sentences, core_words, noun_type)
    with open(result_path,'w') as f:
        for res in result:
            f.write(res + '.')



if __name__ == '__main__':
    main()