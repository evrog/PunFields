# -*- coding: utf-8 -*-
import nltk.data
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords

stopwords=stopwords.words('english')
#stopwords=[]
        
with open('Roget_1.txt', 'r') as index_file:
    index = index_file.read().splitlines()
    index = [i.lower() for i in index]
    raw_index = [wd[:wd.find(" % ")] for wd in index]

def get_words(word):
    if word not in stopwords:
        try:
            word=word.encode('utf-8')
        except:
            pass
        nums=[]
        if word in raw_index:
            pos = raw_index.index(word)
            item = index[pos]
            nums = item[item.find(' % ')+3:].split(',')[:-1]
            nums = [n[n.find('::')+2:] for n in nums]
        else:
            try:
                for syns in wn.synsets(word):
                    hyps=[]
                    for h in syns.hypernyms():
                        extra=str(h)
                        extra=extra[extra.find("'")+1:extra.find('.')].replace('_', ' ')
                        hyps.append(extra)
                    if len(hyps)>0:
                        for h in hyps:
                            if h in raw_index:
                                pos = raw_index.index(h)
                                item = index[pos]
                                nums = item[item.find(' % ')+3:].split(',')[:-1]
                                nums = [n[n.find('::')+2:] for n in nums]
            except:
                pass

        return list(set(nums))
    else:
        return []

def colloq(sent, lemmes):
    colloqs = []
    for s in enumerate(sent):
        s_pos = s[0]
        w = s[1]
        if s_pos<len(sent)-1:
            next_w = sent[s_pos+1]
            if w.startswith('V'):
                if next_w.startswith('DT') and s_pos<len(sent)-2:
                    next_next_w = sent[s_pos+2]
                    if next_next_w.startswith('N'):
                        colloq = lemmes[s_pos][0]+' '+lemmes[s_pos+1][0]+' '+lemmes[s_pos+2][0]
                        x = get_words(colloq)
                        if len(x)>0:
                            colloqs.append([colloq, "collocation", x])
                    elif next_next_w.startswith('R'):
                        colloq = lemmes[s_pos+1][0]+' '+lemmes[s_pos+2][0]
                        x = get_words(colloq)
                        if len(x)>0:
                            colloqs.append([colloq, "collocation", x])
                elif next_w.startswith('P') and s_pos<len(sent)-2:
                    next_next_w = sent[s_pos+2]
                    if next_next_w.startswith('N'):
                        colloq = lemmes[s_pos][0]+' '+"one's"+' '+lemmes[s_pos+2][0]
                        x = get_words(colloq)
                        if len(x)>0:
                            colloqs.append([colloq, "collocation", x])
                elif next_w.startswith('N') and s_pos<len(sent)-2:
                    next_next_w = sent[s_pos+2]
                    if next_next_w.startswith('CC') and s_pos<len(sent)-3:
                        next_next_next_w = sent[s_pos+3]
                        if next_next_next_w.startswith('N'):
                            colloq = lemmes[s_pos][0]+' '+lemmes[s_pos+1][0]+' '+lemmes[s_pos+2][0]+' '+lemmes[s_pos+3][0]
                            x = get_words(colloq)
                            if len(x)>0:
                                colloqs.append([colloq, "collocation", x])
                    else:
                        colloq = lemmes[s_pos][0]+' '+lemmes[s_pos+1][0]
                        x = get_words(colloq)
                        if len(x)>0:
                            colloqs.append([colloq, "collocation", x])
                elif next_w.startswith('R') or next_w.startswith('I') or next_w.startswith('J'):
                    colloq = lemmes[s_pos][0]+' '+lemmes[s_pos+1][0]
                    x = get_words(colloq)
                    if len(x)>0:
                        colloqs.append([colloq, "collocation", x])
            elif w.startswith('J') and next_w.startswith('N'):
                colloq = lemmes[s_pos][0]+' '+lemmes[s_pos+1][0]
                x = get_words(colloq)
                if len(x)>0:
                    colloqs.append([colloq, "collocation", x])
            elif w.startswith('RB') and next_w.startswith('VBN'):
                colloq = lemmes[s_pos][0]+' '+lemmes[s_pos+1][0]
                x = get_words(colloq)
                if len(x)>0:
                    colloqs.append([colloq, "collocation", x])
            elif w.startswith('N') and next_w.startswith('CC') and s_pos<len(sent)-2:
                next_next_w = sent[s_pos+2]
                if next_next_w.startswith('N'):
                    colloq = lemmes[s_pos][0]+' '+lemmes[s_pos+1][0]+' '+lemmes[s_pos+2][0]
                    x = get_words(colloq)
                    if len(x)>0:
                        colloqs.append([colloq, "collocation", x])

    return colloqs


def analyze_words(sentence):
    sentence=sentence.lower()
    groups = [0]*39
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    try:
        los = sent_detector.tokenize(sentence.strip())
    except:
        sentence=sentence.decode('utf-8', errors='replace')
        los = sent_detector.tokenize(sentence.strip())
    list_of_l = []
    bugs = '[]()@#$%&^*+:;!?.,/=|,-"\/+'
    for s in los:
        for bug in bugs:
            s=s.replace(bug, '')
        try:
            s=s.decode('utf-8', errors='replace')
        except:
            pass
        pos_tags = word_tokenize(s)
        for wd in enumerate(pos_tags):
            if wd[1] == "n't":
                pos = wd[0]
                pos_tags[pos] = 'not'
            elif wd[1] == "'s" or wd[1] == "'ll" or wd[1] == "'m" or wd[1] == "'re":
                pos = wd[0]
                pos_tags[pos] = 'be'
            elif wd[1] == "'ve":
                pos = wd[0]
                pos_tags[pos] = 'have'
            elif wd[1] == "'d":
                pos = wd[0]
                pos_tags[pos] = 'would'
        
        list_of_lemmes = []
        for pos in nltk.pos_tag(pos_tags):
            if pos not in list_of_lemmes:
                list_of_lemmes.append(pos)
                
        wordnet_lemmatizer = WordNetLemmatizer()
        lemmes = []
        
        for wd in list_of_lemmes:
            pos_lemme = list_of_lemmes.index(wd)
            topics = []
            
            if wd[1].startswith("V"):
                lemme = wordnet_lemmatizer.lemmatize(wd[0], pos='v')
                lemmes.append([lemme, wd[1], get_words(lemme)])

            else:
                lemme = wd[0]
                lemmes.append([lemme, wd[1], get_words(lemme)])

        sent = [x[1] for x in lemmes]
        colloqs = colloq(sent, lemmes) 
        list_of_l.extend(colloqs)

        for wd in lemmes:
            pos_lemme = lemmes.index(wd)
            topics = []
            
            if wd[1].startswith("J"):
                lemmes.remove(wd)
                lemme = wordnet_lemmatizer.lemmatize(wd[0], pos='a')
                lemmes.append([lemme, wd[1], get_words(lemme)])

            elif wd[1].startswith("N"):
                lemmes.remove(wd)
                try:
                    lemme = wordnet_lemmatizer.lemmatize(wd[0], pos='n')
                except:
                    lemme = wordnet_lemmatizer.lemmatize(wd[0].decode('utf-8', errors='replace'), pos='n')
                lemmes.append([lemme, wd[1], get_words(lemme)])
        list_of_l.extend(lemmes)

    list_of_topics = [x[2] for x in list_of_l]
    check = [val for sublist in list_of_topics for val in sublist]
    for item in check:
        if item!=None:
            pos = int(item)
            groups[pos]+=1

    return groups

    
if __name__ == "__main__": 
    print analyze_words("I used to be a banker but I lost interest.")

