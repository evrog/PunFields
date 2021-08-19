# -*- coding: utf-8 -*-

# Semantic vectorizer based on Roget's Thesaurus.
# See: Mikhalkova, Elena, and Yuri Karyakin. "PunFields at SemEval-2017 Task 7: Employing Roget's Thesaurus in Automatic Pun Recognition and Interpretation." 
# arXiv preprint arXiv:1707.05479 (2017). https://arxiv.org/pdf/1707.05479.pdf
"""## Imports"""

import spacy
nlp = spacy.load('en')

from collections import Counter

import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize

"""## Globals"""
# Roget's Thesaurus without any preprocessing. Needed only for ngram indices that signify semantic categories that these ngrams fall under.
with open('Roget_1.txt', 'r') as index_file:
    raw_index = index_file.read().splitlines()

# A list of part-of-speech tags corresponding to every ngram in Roget's Thesaurus: line per line. Hence, the Thesaurus and this list are of the same length.
with open('Roget_pos_tags.txt', 'r') as one_file:
  index_pos_tags=one_file.read().splitlines()

# 100 most frequent part-of-speech combinations from the Thesaurus, for ngrams of length > 1.
unique_combinations=Counter(index_pos_tags)
frequent_pos_combinations=[]
for k, v in unique_combinations.items():
  if len(k.split())>1 and v>100:
    frequent_pos_combinations.append(k)

# Lemmatized ngrams from Roget's. Again, the Thesaurus and this list are of the same length.
with open('Roget_lemmas.txt', 'r') as two_file:
  index_lemmas=two_file.read().lower().splitlines()

"""## Main functions"""
# Function check_ngram_in_roget (sub-function of get_ngram_indices)
# Aim: to find the lemmatized ngram in the lemmatized Thesaurus and find the corresponding ngram in the original Thesaurus to extract semantic categories (there can be more than one category).
# Input: lemmatized ngram
# Output: list of ngram's indices (semantic categories)
def check_ngram_in_roget(ngram):
  pos = index_lemmas.index(ngram)
  item = raw_index[pos]
  nums = item[item.find(' % ')+3:].split(',')[:-1]
  nums = [n[n.find('::')+2:] for n in nums]
  return nums

# Function get_ngram_indices
# Aim: to check whether a lemmatized ngram is in the list of lemmatized ngrams from Roget's. If it is not, to check the lemmatized ngram in Wordnet and find synsets that it belongs to.
# If there are such synsets, to check the ngram's nearest hypernym in the lemmatized Thesaurus.
# Input: lemmatized ngram
# Output: list of ngram's indices (semantic categories)
def get_ngram_indices(ngram):
  list_of_indices = []
  if ngram in index_lemmas:
    list_of_indices = check_ngram_in_roget(ngram)
  else:
    sn = wn.synsets(ngram)
    if len(sn)>0:
      for syns in wn.synsets(ngram):
        hyps = []
        for h in syns.hypernyms():
          extra = str(h)
          extra = extra[extra.find("'")+1:extra.find('.')].replace('_', ' ')
          hyps.append(extra)
        if len(hyps)>0:
          for h in hyps:
            if h in index_lemmas:
              list_of_indices.extend(check_ngram_in_roget(h))

  return list_of_indices

# Function process_text
# Aim: process a text with spacy, extract lemmas and part-of-speech tokens, for unigrams get their indices at once,
# for collocations (combinations of two and more tokens) check whether they are in the list of most frequent
# part-of-speech combinations. If they are, look for them in the lemmatized Thesaurus, and get their indices.
# Calculate how many indices of each of the 39 Roget's semantic categories there are in the final list of indices.
# Input: a text of any length
# Output: a semantic vector of length 39
def process_text(text):

  text_split = text.splitlines()
  list_of_sentences = []
  for ts in text_split:
    list_of_sentences.extend(sent_tokenize(ts))

  list_of_collocations=[]
  list_of_indices=[]

  for los in list_of_sentences:

    sentence_spacy=nlp(los)

    for token in sentence_spacy:
      if token.is_alpha == True:
        list_of_indices.extend(get_ngram_indices(token.lemma_.lower()))

    list_of_pos=[ss.pos_ for ss in sentence_spacy]
    string_of_pos=' '.join(list_of_pos)
    for fpc in frequent_pos_combinations:
      if fpc in string_of_pos:
        len_fpc=fpc.count(' ')
        start=string_of_pos.index(fpc)
        index_combination=string_of_pos[:start].count(' ')
        list_of_collocations.append(' '.join([s.lemma_.lower() for s in sentence_spacy[index_combination:index_combination+len_fpc+1]]))

  for loc in list_of_collocations:
    list_of_indices.extend(get_ngram_indices(loc))
  
  semantic_groups=[0]*39
  for loi in list_of_indices:
    pos=int(loi)
    semantic_groups[pos]+=1
  
  return semantic_groups

"""## Test"""

if __name__ == "__main__":
  text_1="""
Police had previously gone to home where Ohio patrol officers were killed

CLEVELAND — Police invstigating domestic disputes had previously gone to the home where a man fatally shot two police officers over the weekend, but no arrests were ever made, police reports from the Columbus suburb of Westerville show.
Westerville Officers Eric Joering, 39, and Anthony Morelli, 54, were killed shortly after noon Saturday in this normally quiet suburb while responding to a 911 hang-up call.
The suspect, 30-year-old Quentin Smith, was shot and wounded by the officers and taken to Ohio State University Wexner Medical Center in critical condition Saturday.
Advertisement
A series of 911 calls released by the city of Westerville provide some details about what happened Saturday at a complex of town houses.
Smith lived there with his wife, Candace, and a young daughter.
Get Ground Game in your inbox: Daily updates and analysis on national politics from James Pindell.
Sign Up Thank you for signing up!
Sign up for more newsletters here
Westerville Police Chief Joe Morbitzer said at a news conference Saturday that Joering and Morelli were shot immediately upon entering.
After the initial hang-up call at noon, a dispatcher called the number back and reached a woman who was crying and could be heard saying, ‘‘won’t let me in.’’
Officers were then sent to the home.
At 12:12 p.m., an officer tells a dispatcher that it’s ‘‘all quiet right now,’’ followed by a door knock.
At 12:13 p.m., after a dispatcher confirmed contact has been made, a man’s voice could be heard yelling, ‘‘We have shots fired.’’
Four minutes later, someone, presumably a police officer, told a dispatcher: ‘‘We have two officers down.
Child on couch, one at gunpoint.’’
Advertisement
ASSOCIATED PRESS
"""
  text_2 = "I used to be a banker but I lost interest."
  
  print(process_text(text_1))
  print(process_text(text_2))
