#! /usr/bin/python
# -*- coding: utf-8 -*- 

##==========##
## argument ##
##==========##
import argparse
import sys
class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)
class MyFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter): pass
    
        
parser = ArgumentParser(
formatter_class=MyFormatter,
description='''
=========================================================
Random Forest Classifier
=========================================================
''',epilog = '''
output:
  testset_svmdata_rforest_predict_labeled.csv
  testset_svmdata_rforest_importance.csv
  testset_svmdata_rforest_predict.dat
  testset_svmdata_rforest_prob.csv
=========================================================
ogaki@iis.u-tokyo.ac.jp
2012/12/6
=========================================================
''')
parser.add_argument('input_svmdata', help='.dat')
parser.add_argument('testset_svmdata', help='.dat')

parser.add_argument('-p', action='store_true', help='Store class probabilities')

parser.add_argument('--n_estimators', type=int, default=100, help='The number of trees in the forest.')
parser.add_argument('--criterion', type=str, default='gini', help='The function to measure the quality of a split. Supported criteria are “gini” for the Gini impurity and “entropy” for the information gain. Note: this parameter is tree-specific.' )
parser.add_argument('--max_depth', type=int, default=None, help='The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples. Note: this parameter is tree-specific.')
parser.add_argument('--min_samples_split', type=int, default=1, help='The minimum number of samples required to split an internal node. Note: this parameter is tree-specific.')
parser.add_argument('--min_samples_leaf', type=int, default=1, help='The minimum number of samples in newly created leaves. A split is discarded if after the split, one of the leaves would contain less then min_samples_leaf samples. Note: this parameter is tree-specific.')
parser.add_argument('--min_density', type=float, default=0.1, help='''
    This parameter controls a trade-off in an optimization heuristic. It controls the minimum density of the sample_mask (i.e. the fraction of samples in the mask). If the density falls below this threshold the mask is recomputed and the input data is packed which results in data copying. If min_density equals to one, the partitions are always represented as copies of the original data. Otherwise, partitions are represented as bit masks (aka sample masks). Note: this parameter is tree-specific.''')
parser.add_argument('--max_features', type=str, default='auto', help='''
    The number of features to consider when looking for the best split:

            If “auto”, then max_features=sqrt(n_features) on classification tasks and max_features=n_features on regression problems.
            If “sqrt”, then max_features=sqrt(n_features).
            If “log2”, then max_features=log2(n_features).
            If None, then max_features=n_features.

    Note: this parameter is tree-specific.''')
parser.add_argument('--bootstrap', type=bool, default=True, help='Whether bootstrap samples are used when building trees.')
parser.add_argument('--random_state', type=int, default=None, help='If int, random_state is the seed used by the random number generator; If RandomState instance, random_state is the random number generator; If None, the random number generator is the RandomState instance used by np.random.')
parser.add_argument('--verbose', type=int, default=0, help='Controls the verbosity of the tree building process.')

##========##
## Import ##
##========##
import sys
import os
import re

import scipy
import csv
import sklearn.ensemble

herepath = os.path.dirname(sys.argv[0])

def read_libsvmdata(filename):
    ''' read_libsvmdata(filename) -> (features, labels) '''
    features, labels = [], []
    for line in open(filename):
        items = line.rstrip().split(" ")
        labels.append(int(items[0]))
        features.append([float(item.split(":")[1]) for item in items[1:]])
    return scipy.array(features), scipy.array(labels)

    
if __name__ == '__main__':
    ##======##
    ## init ##
    ##======##
    args = parser.parse_args()
    print args
    
    inputfilename = args.input_svmdata
    del args.input_svmdata
    testsetfilename = args.testset_svmdata
    del args.testset_svmdata
    flag_proba = args.p
    del args.p
    
    base,ext = os.path.splitext(testsetfilename)
    outputfilename = base+"_rforest_predict_labeled.csv"
    outputpredictname = base+"_rforest_predict.dat"
    featureimportance_filename = base+"_rforest_importance.dat"
    probabilities_filename = base+"_rforest_probabilities.csv"
    
    if args.max_features.isdigit(): args.max_features=int(args.max_features)

    ##======##
    ## main ##
    ##======##
    inputdata, inputlabels = read_libsvmdata(inputfilename) 
    testdata, testlabels = read_libsvmdata(testsetfilename)

    classifier = sklearn.ensemble.RandomForestClassifier(compute_importances = True, n_jobs = -1, **vars(args))
    classifier.fit(inputdata, inputlabels)
    predictlabels = map(int, classifier.predict(testdata))
    if flag_proba: probabilities = classifier.predict_proba(testdata)

    open(outputfilename, "w+").writelines([ str(line[0])+","+str(line[1])+"\n" for line in zip(predictlabels, testlabels)])
    csv.writer(open(outputpredictname, "w+")).writerows( map(lambda x: [x], predictlabels) )
    open(featureimportance_filename, "w+").writelines(map(lambda x: str(x)+"\n", classifier.feature_importances_))
    if flag_proba: csv.writer(open(probabilities_filename, "w+")).writerows( probabilities )
        
    exit(0)
