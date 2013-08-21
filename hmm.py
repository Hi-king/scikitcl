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
  testset_svmdata_rforest_predict.dat
=========================================================
ogaki@iis.u-tokyo.ac.jp
2013/1/10
=========================================================
''')
parser.add_argument('input_svmdata', help='.dat')
parser.add_argument('testset_svmdata', help='.dat')

parser.add_argument('--n_components', type=int, default=6,
                    help='number of components')
parser.add_argument('--n_mixture', type=int, default=10,
                    help='mixture of GMM')

##========##
## Import ##
##========##
import sys
import os
import re

import scipy
import csv
import sklearn.hmm

herepath = os.path.dirname(sys.argv[0])
sys.path.append(herepath+"/..")
import egovision
    
def main(args):
    ##==========##
    ## Constant ##
    ##==========##
    SUFFIX = "_hmm"
    flag_proba = True
    
    ##======##
    ## init ##
    ##======##
    
    inputfilename = args.input_svmdata
    testsetfilename = args.testset_svmdata
    n_components = args.n_components
    n_mixture = args.n_mixture
    
    base,ext = os.path.splitext(testsetfilename)
    outputfilename = base+SUFFIX+"_predict_labeled.csv"
    outputpredictname = base+SUFFIX+"_predict.dat"
    probabilities_filename = base+SUFFIX+"_probabilities.csv"

    ##======##
    ## main ##
    ##======##
    if inputfilename.find(".csv")>0:
        inputdata = scipy.array(egovision.readcsvtolist_float(inputfilename))
    else:
        inputdata,inputlabels = egovision.read_libsvmdata(inputfilename)

    if testsetfilename.find(".csv")>0:
        testdata= scipy.array(egovision.readcsvtolist_float(testsetfilename))
    else:
        testdata, testlabels = egovision.read_libsvmdata(testsetfilename)

    classifier = sklearn.hmm.GMMHMM(n_components,n_mixture, covariance_type="diag", n_iter=1000)

    # tmpdata = []
    # for i in xrange(0, len(inputdata)-3199, 3200):
    #     print i
    #     tmpdata.append(inputdata[i:i+3200, :])
    # inputdata = scipy.array(tmpdata)
    print inputdata.shape
    

    
    #print inputdata.shape
    classifier.fit([inputdata])
    
    predictlabels = map(int, classifier.predict(testdata))
    if flag_proba: probabilities = classifier.predict_proba(testdata)

    csv.writer(open(outputpredictname, "w+")).writerows( map(lambda x: [x], predictlabels) )
    if flag_proba: csv.writer(open(probabilities_filename, "w+")).writerows( probabilities )
    
    exit(0)

if __name__ == '__main__':
    args = parser.parse_args()
    print args
    main(args)
