# PunFields
This is a start of the project for annotating sentences that contain semantic ambiguity, i.e. where a word or phrase is intentionally used in two meanings.
The scientific side of it is described in:

@InProceedings{mikhalkova-karyakin:2017:SemEval,
  author    = {Mikhalkova, Elena  and  Karyakin, Yuri},
  title     = {PunFields at SemEval-2017 Task 7: Employing Roget's Thesaurus in Automatic Pun Recognition and Interpretation},
  booktitle = {Proceedings of the 11th International Workshop on Semantic Evaluation (SemEval-2017)},
  month     = {August},
  year      = {2017},
  address   = {Vancouver, Canada},
  publisher = {Association for Computational Linguistics},
  pages     = {417--422},
  abstract  = {The article describes a model of automatic interpretation of English puns,
	based on Roget{'}s Thesaurus, and its implementation, PunFields. In a pun, the
	algorithm discovers two groups of words that belong to two main semantic
	fields. The fields become a semantic vector based on which an SVM classifier
	learns to recognize puns. A rule-based model is then applied for recognition of
	intentionally ambiguous (target) words and their definitions. In SemEval Task 7
	PunFields shows a considerably good result in pun classification, but requires
	improvement in searching for the target word and its definition.},
  url       = {http://www.aclweb.org/anthology/S17-2072}
}

This is not a ready-made package, but a number of Python-2.7 files that can be added to your project.
Any help in improving it and making it an installable toolkit is welcome! 

Files 'roget-body.txt' and 'roget-index.txt' belong to: 
Peter Mark Roget. 2004.  Roget’s thesaurus of English words and phrases. Project Gutenberg.
