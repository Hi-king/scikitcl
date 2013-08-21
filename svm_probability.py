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

##========##
## Import ##
##========##
import sys
import os
import re

import scipy
import csv
import sklearn.svm

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
    # flag_proba = args.p
    # del args.p
    
    base,ext = os.path.splitext(testsetfilename)
    cls_suffix = "_svm"
    outputfilename = base + cls_suffix+"_predict_labeled.csv"
    outputpredictname = base + cls_suffix + "_predict.dat"
    featureimportance_filename = base + cls_suffix + "_importance.dat"
    # probabilities_filename = "probabilities.csv"
    
    # if args.max_features.isdigit(): args.max_features=int(args.max_features)

    ##======##
    ## main ##
    ##======##
    inputdata, inputlabels = read_libsvmdata(inputfilename) 
    testdata, testlabels = read_libsvmdata(testsetfilename)

    classifier = sklearn.svm.SVC(kernel='linear', **vars(args))
    classifier.fit(inputdata, inputlabels)
    print classifier.support_vectors_
    print "coef"
    print classifier.coef_
    print "intercept"
    
    print classifier.intercept_
    print inputdata.shape
    pred = scipy.dot(classifier.coef_, inputdata.T)+classifier.intercept_
    predictlabels = map(int, classifier.predict(testdata))
    #if flag_proba: probabilities = classifier.predict_proba(testdata)

    open(outputfilename, "w+").writelines([ str(line[0])+","+str(line[1])+"\n" for line in zip(predictlabels, testlabels)])
    csv.writer(open(outputpredictname, "w+")).writerows( map(lambda x: [x], predictlabels) )
    open(featureimportance_filename, "w+").writelines(map(lambda x: str(x)+"\n", classifier.coef_.tolist()[0]))
    #open("testout", "w+").writelines(map(lambda x: str(x)+"\n", pred.flatten().tolist()))
    # csv.writer(open(probabilities_filename, "w+")).writerows( classifier.coef_.tolist() )
        
    exit(0)
