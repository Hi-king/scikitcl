#! /usr/bin/python
# -*- coding: utf-8 -*- 
'''
================================
SVM cross validation
--------------------------------
input
   |- $svmdata.dat
(  |- $k = len(svmdata)  )
output
   |- crossvalid.csv
=================================
ogaki@iis.u-tokyo.ac.jp
2012/12/8 -> 2012/12/12
=================================
'''

import sys
import re
import os
import os.path
import csv
import math
import subprocess

##=======##
## const ##
##=======##
SVMEASY = "myeasy_multiclass.py"
TMPTESTDATA = "tmptest.dat"
TMPTRAININGDATA = "tmptrain.dat"

if __name__ == '__main__':
    ##======##
    ## init ##
    ##======##
    NEEDARGNUM = len(re.search(r'input.*?\n(( .*?\n)*)', __doc__, re.DOTALL).group(1).split("\n")) -1
    if(len(sys.argv)<=NEEDARGNUM):
        print("need at least %d arguments" % NEEDARGNUM)
        print(__doc__)
        exit(1)

    inputfilename = sys.argv[1]
    inputlines = open(inputfilename).readlines()
    base,ext = os.path.splitext(inputfilename)

    K = int(sys.argv[2]) if len(sys.argv)>2 else len(inputlines)
    
    outputfilename = base+"_k"+str(K)+".csv"

    ##======##
    ## main ##
    ##======##
    linenum = int(math.ceil(float(len(inputlines))/K))
    svmoutfile = os.path.splitext(TMPTESTDATA)[0]+".predict"

    labels = []
    predicts = []
    
    for i in range(0, len(inputlines), linenum):
        print(str(i)+"th validation..."+str(len(inputlines)-linenum*i)+"samples left.")
        
        testlines = inputlines[i:i+linenum]
        open(TMPTESTDATA, "w+").writelines(testlines)

        trainlines = inputlines[:i]+inputlines[i+linenum:]
        open(TMPTRAININGDATA, "w+").writelines(trainlines)

        cmd = '{0} "{1}" "{2}"'.format(SVMEASY, TMPTRAININGDATA, TMPTESTDATA)
        subprocess.Popen(cmd, shell = True).communicate()

        for line in open(svmoutfile):
            predicts.append(line.rstrip())

    ## remove ##
    for suffix in ['dat', 'range', 'scale', 'model', 'out']: os.remove(os.path.splitext(TMPTRAININGDATA)[0]+"."+suffix)
    for suffix in ['dat', 'predict', 'scale']: os.remove(os.path.splitext(TMPTESTDATA)[0]+"."+suffix)
            

    labels = [ line.split(" ")[0] for line in inputlines ]        

    ofile = open(outputfilename, "w+")
    for line in zip(predicts, labels):
        ofile.write(line[0]+","+line[1]+"\n")
    
    exit(0)
