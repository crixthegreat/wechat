#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/11/22 15:22:32

import sys
import json
import random
from optparse import OptionParser


def read_data():

    with open('./poemdata/pos_top500.json', 'r', encoding='utf-8-sig') as f:
        pos_500_data = json.loads(f.read())

    with open('./poemdata/double_word_dict_head.json', 'r', encoding='utf-8-sig') as f:
        double_word_data = json.loads(f.read())

    with open('./poemdata/double_word_dict_end.json', 'r', encoding='utf-8-sig') as f:
        double_word_end_data = json.loads(f.read())

    with open('./poemdata/pingze_dict_with_prob.json', 'r', encoding='utf-8-sig') as f:
        pingze_data = json.loads(f.read())

    with open('./poemdata/double_word_with_one_word_fix.json', 'r', encoding='utf-8-sig') as f:
        double_word_with_one_word = json.loads(f.read())

    with open('./poemdata/one_word_with_double_word.json', 'r', encoding='utf-8-sig') as f:
        one_word_with_double_word = json.loads(f.read())

    rhyme_list = []
    with open('./poemdata/rhyme-fix.csv', 'r', encoding='utf-8-sig') as f:
        line = f.readline()
        while line:
            rhyme = [_ for _ in line.split(',')[1:] 
                    if _ and _!='\n' and _ in double_word_end_data.keys() ]
            rhyme_list.append(rhyme)
            line = f.readline()

    return (pos_500_data, double_word_data, double_word_end_data, pingze_data, 
            double_word_with_one_word, one_word_with_double_word, rhyme_list)

def make_poem():
    

    def pingze_value(word, ping=True):
        if ping:
            if not(word in pingze_data[1].keys()):
                return True
            else:
                return False
        else:
            if not(word in pingze_data[0].keys()):
                return True
            else:
                return False

    def get_pingze(_list, ping=True):
        random.shuffle(_list)
        for _ in _list:
            if pingze_value(_[0], ping):
                return _[0]

        return _list[0]
    

    def get_double_pingze(_list, ping=0):
        '''ping =
        0 - 平平
        1 - 仄仄
        2 - 平仄
        3 - 仄平
        '''
        random.shuffle(_list)
        for _ in _list:
            if ping == 0:
                if pingze_value(_[0], True) and pingze_value(_[1], True):
                    return _
            elif ping == 1:
                if pingze_value(_[0], False) and pingze_value(_[1], False):
                    return _
            elif ping == 2:
                if pingze_value(_[0], True) and pingze_value(_[1], False):
                    return _
            elif ping == 3:
                if pingze_value(_[0], False) and pingze_value(_[1], True):
                    return _
            else:
                raise Exception('double word pingze type error')
                                
        return _list[0]
            

    def get_double_word(word, end=False, ping=True):
        # 自后字取词，用于配押韵字的词
        if end:
            _list = double_end_data[word][:int(len(double_end_data) / 2) + 1]
            pos = 0
        else:
            _list = double_data[word][:int(len(double_data) / 2) + 1]
            pos = 1

        random.shuffle(_list)
        for _ in _list:
            if ping:
                if not(_[pos] in pingze_data[1].keys()) and (_ in double_word_with_one_word.keys()):
                    return _
            else:
                if not(_[pos] in pingze_data[0].keys()) and (_ in double_word_with_one_word.keys()):
                    return _
        
        for _ in _list:
            if _ in  double_word_with_one_word.keys():
                return _

        return _list[0]
        raise Exception('no double word matched!', _list)

    def get_one_word_from_double_word(double_word):
        if double_word in double_word_with_one_word.keys():
            return double_word_with_one_word[double_word]
        else:
            return random.sample(double_word_with_one_word.items(), 1)[0][1]

    def make_sentence(no, pingze_type, word_type, rhyme):
        '''make a sentence of a 5-jue poem
                   no: the number of the sentence (1 - 4) 
        pingze_type 0: 仄仄平平仄
        pingze_type 1: 平平仄仄平
        pingze_type 2: 平平平仄仄
        pingze_type 3: 仄仄仄平平
          word_type 0:$$@$$
          word_type 1:$$$$@
        '''
        sentence = ''

        if pingze_type == 0:
            # pingze_type 0: 仄仄平平仄
            word_2 = get_pingze(pos_data[str((no - 1) * 5 + 1)][:400], False)
            sentence += get_double_word(word_2, end=True)
            if word_type:
                word_3 = get_pingze(pos_data[str((no - 1) * 5 + 2)][:400])
                double_word = get_double_word(word_3, False, True)
                sentence += double_word
                sentence += get_pingze(get_one_word_from_double_word(double_word), False)
            else:
                word_4 = get_pingze(pos_data[str((no - 1) * 5 + 3)][:400])
                double_word = get_double_word(word_4, end=False, ping=False)
                word_3 = get_pingze(get_one_word_from_double_word(double_word))
                sentence += word_3
                sentence += double_word
        elif pingze_type == 1:
            # pingze_type 1: 平平仄仄平
            word_2 = get_pingze(pos_data[str((no - 1) * 5 + 1)][:400], ping=True)
            sentence += get_double_word(word_2, end=True, ping=True)
            if no == 1:
                word_5 = rhyme[2]
            else:
                word_5 = rhyme[int(no / 2) - 1]
            if word_type:
                double_word = get_double_pingze(one_word_with_double_word[word_5], 1)
                sentence += double_word
                sentence += word_5
            else:
                double_word = get_double_word(word_5, end=True, ping=False)
                word_3 = get_pingze(get_one_word_from_double_word(double_word), ping=False)
                sentence += word_3
                sentence += double_word
        if pingze_type == 2:
            # pingze_type 2: 平平平仄仄
            word_2 = get_pingze(pos_data[str((no - 1) * 5 + 1)][:400], True)
            sentence += get_double_word(word_2, end=True, ping=True)
            if word_type:
                word_3 = get_pingze(pos_data[str((no - 1) * 5 + 2)][:400])
                double_word = get_double_word(word_3, False, False)
                sentence += double_word
                sentence += get_pingze(get_one_word_from_double_word(double_word), False)
            else:
                word_4 = get_pingze(pos_data[str((no - 1) * 5 + 3)][:400], False)
                double_word = get_double_word(word_4, end=False, ping=False)
                word_3 = get_pingze(get_one_word_from_double_word(double_word))
                sentence += word_3
                sentence += double_word
        elif pingze_type == 3:
            # pingze_type 1: 仄仄仄平平
            word_2 = get_pingze(pos_data[str((no - 1) * 5 + 1)][:400], ping=False)
            sentence += get_double_word(word_2, end=True, ping=False)
            if no == 1:
                word_5 = rhyme[2]
            else:
                word_5 = rhyme[int(no / 2) - 1]
            if word_type:
                double_word = get_double_pingze(one_word_with_double_word[word_5], 3)
                sentence += double_word
                sentence += word_5
            else:
                double_word = get_double_word(word_5, end=True, ping=True)
                word_3 = get_pingze(get_one_word_from_double_word(double_word), ping=False)
                sentence += word_3
                sentence += double_word

        return sentence
    
    pos_data, double_data, double_end_data, pingze_data, double_word_with_one_word, one_word_with_double_word, rhyme_list = read_data()

    _poem = []

    # 取韵字
    random.shuffle(rhyme_list)
    random.shuffle(rhyme_list[0])
    rhyme_word = []
    for _ in rhyme_list[0]:
        if _ in one_word_with_double_word.keys():
            rhyme_word.append(_)
            if len(rhyme_word) >=3:
                break

    sentence1_type = random.randrange(0, 2)
    pingze_type = random.randrange(0, 4)

    sentence_structure = [
            [0, 1, 2, 3],
            [3, 1, 2, 3],
            [2, 3, 0, 1],
            [1, 3, 0, 1]]

    for _ in range(0, 4):
        _poem.append(make_sentence(_ + 1, sentence_structure[pingze_type][_], random.randrange(0 ,2), rhyme_word))

    return '\n'.join(_poem)

if __name__=='__main__':

    print(make_poem())

        


