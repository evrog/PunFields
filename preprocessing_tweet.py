# encoding=utf8
import re
from nltk.corpus import names
import wordninja


NAMES = [n.encode('utf-8').lower() for n in names.words()]

with open('./chat_slang', 'r') as slang_dict:
    slang_dict = slang_dict.read().splitlines()[0::2]
    wds = [wd.lower() for wd in slang_dict[0::2]]
    means = slang_dict[1::2]

SLANG = zip(wds, means)

def check_slang(word):
    for x in SLANG:
        if word==x[0] or word.lower()==x[0]:
            word=x[1]
    return word

BUGS_1 = '()!?.[]$%&^*+;,=/\\:|"'
BUGS_2 = '#@'
BUGS_3 = '_'

def preprocess_tweet(tweet):
    
    text=tweet

    for b1 in BUGS_1:
        text = text.replace(b1, ' '+b1+' ')
    for b2 in BUGS_2:
        text = text.replace(b2, ' '+b2)
    for b3 in BUGS_3:
        text=text.replace(b3, ' ')
    
    text = text.split()
    
    full_text=''

    for wd in text:
                
        wd=wd.replace("'", '')
        
        emph_1 = re.findall(r'(([a-zA-Z])\2{2,})', wd)
        if len(emph_1)>0:
            for x in emph_1:
                wd = wd.replace(x[0], x[1])
        
        if wd.startswith('#') or wd.startswith('@'):
            wd=wd[1:]
            sort_1 = re.findall(r'[A-Z]{2,}', wd)
            for x in sort_1:
                if len(x)>0:
                    wd=wd.replace(x, ' '+x[0]+x[1:].lower())
            
            sort_2 = re.findall(r'[0-9]*', wd)
            for x in sort_2:
                if len(x)>0:
                    wd=wd.replace(x, ' '+x+' ')

            sort_3 = re.findall(r'[A-Z][^A-Z]*', wd)
            for x in sort_3:
                if len(x)>0:
                    wd=wd.replace(x, x+' ')

            check_wd=wd.split()
            for cw in check_wd:

                def cor_names(word):
                    list_cand=[]
                    for n in NAMES:
                        if word.lower().startswith(n):
                            list_cand.append(n)
                    if len(list_cand)>0:
                        fin_name=max(list_cand, key=len)
                        if len(fin_name)>3:
                            return fin_name
                        else:
                            return word
                    
                    else:
                        return word

                prob_name=cor_names(cw)
                if prob_name!=cw:
                    x=len(prob_name)
                    try:
                        full_text+=cw[0].upper()+cw[1:x]+' '+cw[x].upper()+cw[x+1:]+' '
                    except:
                        full_text+=cw[0].upper()+cw[1:x]+' '

                else:
                    if len(cw)>3:
                        split_wd=wordninja.split(cw)
                        if len(split_wd)<len(cw):
                            for s_wd in split_wd:
                                full_text+=check_slang(s_wd)+' '
                        else:        
                            full_text+=check_slang(cw)+' '
                    else:
                        full_text+=check_slang(cw)+' '
        else:
            if len(wd)>3:
                split_wd=wordninja.split(wd)
                if len(split_wd)<len(wd):
                    for s_wd in split_wd:
                        full_text+=check_slang(s_wd)+' '
                else:        
                    full_text+=check_slang(wd)+' '
            else:
                full_text+=check_slang(wd)+' '

    return full_text

if __name__ == "__main__":
    print preprocess_tweet("@YankeesWFAN @Ken_Rosenthal trading a SP for a defense-only SS? Brilliant trade.")
    print preprocess_tweet("WE R #ElektrikBLOOM #ElektrikFANTASY #iwant2DRIFT #Elev8TheUnderground!")
    print preprocess_tweet("American Kids starting playing and now I'm super missing #summer2k14 #kennychesney")
    print preprocess_tweet("About once a yr I get a little nutty and reach for the orange marmalade. #livingontheedge  http://t.co/sF9o6OWE1v")
    print preprocess_tweet("@TheView,@WhoopiGoldberg, women say 1 man asltd them, y so long 2 say sumtin? & the young 1s, where the parents? Hotel wit grn ass man? Smh")
    print preprocess_tweet("Why YES! Of course I use  a lot in my day....because violence is illegal.")
    print preprocess_tweet("Youve got to just love the efficiency @usps two-day service!  #7DayService #prioritymail #hahahaha http://t.co/oQsqUAo5a9")
    print preprocess_tweet("That was one long walk :ok_hand_sign::ok_hand_sign::ok_hand_sign: #GoMe http://t.co/liRaGZvLyF")
    print preprocess_tweet("#New#color#new#beginning#new#goals#dont#giveup#never#life#should#be#easy @ skdar http://t.co/bzmXE0K98i")
    print preprocess_tweet("Love these cold winter mornings :grimacing_face: best feeling everrrrrrr !")
