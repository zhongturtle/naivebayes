import random
import csv
import numpy as np
from numpy import ceil, floor, histogram2d, sum, array
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from brown_testing import build_all_brown

### functions for cross-validation of MultinomialNB
def cross_validate(docs, cats, nfolds=10, **kwargs):
    nsamples = len(cats)
    cats_types = list(set(cats))
    shuffled_indices = range(nsamples)
    random.shuffle(shuffled_indices)

    scores = []

    start_idx = 0
    foldsize = float(nsamples) / (nfolds)

    for k in range(nfolds):
        stop_idx = int(round((k+1) * foldsize))

        train_indices = shuffled_indices[:start_idx]+shuffled_indices[stop_idx:]
        test_indices = shuffled_indices[start_idx:stop_idx]

        train_docs, train_cats = docs[train_indices], cats[train_indices]
        test_docs, test_cats = docs[test_indices], cats[test_indices]

        nb = MultinomialNB(**kwargs)
        nb.partial_fit(train_docs, train_cats, classes=cats_types)
        start_idx = stop_idx

        score = nb.score(test_docs, test_cats)
        scores.append(score)

    return scores


def build_confusion_matrix(nb, test_docs, test_cats):
    ''' THIS IS BROKEN IN A WAY I CAN'T FIGURE OUT 
        
        should get confusion matrix m such that
        sum(m.diagonal()) / sum(m)
        == nb.score(test_docs, test_cats)
        
        but for some reason these two are not always equal'''
    class_size = len(nb.classes_)
    predicted = nb.predict(test_docs)
    #return test_cats,predicted,class_size
    m, xe, ye = histogram2d(test_cats, predicted, bins=((class_size,class_size)))

    return m


def build_crossval_indices(n,k):
    indices = [int(ceil((float(n)/k)*i)) for i in range(k+1)]
    return indices


def get_crossval_split(l, indices, i):
    test_start_idx = indices[i]
    test_end_idx = indices[i+1]

    train_l = l[:test_start_idx] + l[test_end_idx:]
    test_l = l[test_start_idx:test_end_idx]

    return train_l, test_l


def shuffle_paired_lists(l1, l2):
    zipped = zip(l1, l2)
    random.shuffle(zipped)

    unzipped1 = [v[0] for v in zipped]
    unzipped2 = [v[1] for v in zipped]

    return unzipped1, unzipped2
