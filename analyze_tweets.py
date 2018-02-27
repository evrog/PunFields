from twit_to_vec import analyze_words
import random
import numpy as np
from sklearn import svm
from sklearn import metrics

with open('./ironic_tweet_vecs.txt', 'r') as itv:
    ironic = itv.read().splitlines()

irvecs=[]
for irv in ironic:
    irvecs.append([int(i) for i in irv.split()])

with open('./not_ironic_tweet_vecs.txt', 'r') as nitv:
    not_ironic = nitv.read().splitlines()

nirvecs=[]
for nirv in not_ironic:
    nirvecs.append([int(i) for i in nirv.split()])

x=min(len(irvecs), len(nirvecs))
if x%2!=0:
    x-=1

random.shuffle(irvecs)
random.shuffle(nirvecs)

lim=x/2
X_train = np.array(irvecs[:lim]+nirvecs[:lim], dtype=np.float64)
y_train = np.array([1]*lim+[0]*lim, dtype=np.float64)
X_test = np.array(irvecs[lim:lim*2]+nirvecs[lim:lim*2], dtype=np.float64)
y_test = y_train

model_1 = svm.SVC(kernel='linear')
model_1.fit(X_train, y_train)
predicted = model_1.predict(X_test)
expected = y_test
print metrics.classification_report(expected, predicted), metrics.confusion_matrix(expected, predicted)
