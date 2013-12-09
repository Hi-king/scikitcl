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
================================
Random forest classifier cross validation
--------------------------------
''',epilog = '''
output
   |- $svmdata_k$k_rforest_predict_labeled.csv
   |- $svmdata_k$k_rforest_importance.dat
=================================
ogaki@iis.u-tokyo.ac.jp
2012/12/12
=================================
''')
parser.add_argument('svmdata', help='.dat')
parser.add_argument('-k', help='k fold e.g. 3')
parser.add_argument('-b', dest='classifier', help='e.g. "randomforest.py --max_features=40 --n_estimators=100"', default='randomforest.py -p')

import sys
import re
import os
import os.path
import csv
import math
import subprocess
import scipy

##=======##
## const ##
##=======##
PREFIX = "tmp"

if __name__ == '__main__':
    ##======##
    ## init ##
    ##======##
    args = parser.parse_args()
    print args

    inputfilename = args.svmdata
    inputlines = open(inputfilename).readlines()
    K = int(args.k) if args.k else len(inputlines)
    SVMEASY = args.classifier

    base,ext = os.path.splitext(inputfilename)
    
    outputfilename = base+"_k"+str(K)+"_rforest.csv"
    outputprobafilename = base+"_k"+str(K)+"_rforest_probabilities.csv"
    outputimportancefilename = base+"_k"+str(K)+"_rforest_importance.dat"
    
    PREFIX += base
    TMPTESTDATA = PREFIX + "test.dat"
    TMPTRAININGDATA = PREFIX + "train.dat"

    ##======##
    ## main ##
    ##======##
    linenum = int(math.ceil(float(len(inputlines))/K))
    svmoutfile = os.path.splitext(TMPTESTDATA)[0]+"_rforest_predict_labeled.csv"
    svmprobafile = os.path.splitext(TMPTESTDATA)[0]+"_rforest_probabilities.csv"
    svmimportancefile = os.path.splitext(TMPTESTDATA)[0]+"_rforest_importance.dat"

    labels = []
    predicts = []
    probas = []
    importances = []
    
    for i in range(0, len(inputlines), linenum):
        print(str(i)+"samples done..."+str(len(inputlines)-i)+"samples left.")
        
        testlines = inputlines[i:i+linenum]
        open(TMPTESTDATA, "w+").writelines(testlines)

        trainlines = inputlines[:i]+inputlines[i+linenum:]
        open(TMPTRAININGDATA, "w+").writelines(trainlines)

        cmd = '{0} "{1}" "{2}"'.format(SVMEASY, TMPTRAININGDATA, TMPTESTDATA)
        subprocess.Popen(cmd, shell = True).communicate()

        for line in open(svmoutfile):
            predicts.append(line.rstrip())
        for line in open(svmprobafile):
            probas.append(line.rstrip())

        importances.append(scipy.array(map(float, [line.rstrip() for line in open(svmimportancefile) if line[0].isdigit() or line[0]=="-" ])))

    ## remove ##
    for suffix in ['dat']: os.remove(os.path.splitext(TMPTRAININGDATA)[0]+"."+suffix)
    for suffix in ['dat']: os.remove(os.path.splitext(TMPTESTDATA)[0]+"."+suffix)
    for suffix in ['_rforest_predict_labeled.csv', '_rforest_importance.dat']: os.remove(os.path.splitext(TMPTESTDATA)[0]+suffix)


    importances = scipy.array([ reduce(lambda x,y: scipy.sum((x, y), 0), importances) ])
    importances = importances/K
    

    labels = [ line.split(" ")[0] for line in inputlines ]        

    ofile = open(outputfilename, "w+")
    for line in predicts:
        ofile.write(line+"\n")

    ofile = open(outputprobafilename, "w+")
    for line in probas:
        ofile.write(line+"\n")

    ofile = open(outputimportancefilename, "w+")
    for line in importances[0]:
        ofile.write(str(line)+"\n")
        
    exit(0)
