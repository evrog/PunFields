# coding: "utf-8"
import re
 
def open_thes():
    n = range(1, 1001)
    with open('roget-body.txt', 'r') as bodyfile:  #put 'roget-body.txt' in the same directory with 'roget-struct.py'
        thesaurus = bodyfile.read()

    thesaurus = thesaurus.splitlines()
    list_of_pos = []
    field_names = []
    for line in enumerate(thesaurus):
        name = 'SECTION'
        regexp = r'SECTION[ ]\w+'
        l_sec = re.match(r'SECTION[ ]\w+', line[1])
        if l_sec != None:
            list_of_pos.append(line[0])
            field_names.append([thesaurus[line[0]+1], line[0]])
    list_of_pos = sorted(list_of_pos)

    for p in enumerate(list_of_pos):
        pp = p[0]
        if pp < len(list_of_pos)-1 and (list_of_pos[pp+1]-p[1] == 2 or list_of_pos[pp+1]-p[1] == 3):
            list_of_pos.remove(p[1])

    wordlist = []
    field_list = []
    for num in enumerate(list_of_pos):
        if num[0]<len(list_of_pos)-1:
            txt = thesaurus[num[1]:list_of_pos[num[0]+1]]
            txt_s = "\n".join(txt)
            chunks = re.findall(r'\d+\.[ ]\w+\s*.*,*--|\d+\.\s\[[A-Z].+\][ ]\w+\s+--|\d+\w\.[ ]\w+\s*--|\d+\w\.\s\[[A-Z].+\][ ]\w+\s+--', txt_s)
            x = ''
            for f in field_names:
                if f[1] == num[1]:
                    x=f[0]

            wordlist.append([x, [wd[:wd.find(". ")] for wd in chunks]])
        else:
            txt = thesaurus[num[1]:]
            txt_s = "\n".join(txt)
            chunks = re.findall(r'\d+\.[ ]\w+\s*.*,*--|\d+\.\s\[[A-Z].+\][ ]\w+\s+--|\d+\w\.[ ]\w+\s+--|\d+\w\.\s\[[A-Z].+\][ ]\w+\s+--', txt_s)
            x = ''
            for f in field_names:
                if f[1] == num[1]:
                    x=f[0]

            wordlist.append([x, [wd[:wd.find(". ")] for wd in chunks]])
            
    # to see what sections of thesaurus are currently used for annotation, uncomment the fllowing two lines:
##    for i in enumerate(wordlist):
##        print i[0], i[1][0]
    
    return wordlist


def finder(word, wordlist):
    
    check_items = [x[1] for x in wordlist]
    check = [item for sublist in check_items for item in sublist]

    if word in check:
        for group in enumerate(wordlist):
            if word in group[1][1]:
                return group[0], group[1][0]
    else:
        print word, "Word not found!"

#INPUT: number of cluster plus letter index, if any, in Roget's Thesaurus where the word was found (between 1 and 1000)
#OUTPUT: number of Section (in Thesaurus, Sections are subdivisions of six primary Classes)
if __name__ == "__main__":
    thes = open_thes()
    print finder('374a', thes)
    print finder('800', thes)
