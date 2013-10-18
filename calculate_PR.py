#! /usr/bin/python
# -*- coding: utf-8 -*- 
mydoc = '''
================================
Visualize optflow
--------------------------------
input
    |- $LABELEDPREDICT.dat : "$PREDICT $LABEL" formatted 2d data
output
    |- $LABELEDPREDICT_PR.txt : result file
    |- $LABELEDPREDICT_CONFMAT.csv : result file
=================================
ogaki@iis.u-tokyo.ac.jp
2012/03/12
'''

import sys
import os.path
import csv


def getdelim(line):
    DELIMTYPES = (",", " ", ":")
    for delim in DELIMTYPES:
        if line.find(delim): return delim
    
if __name__ == '__main__':
    # ======
    #  init
    # ======
    if(len(sys.argv)>1):
        filename_labeled = sys.argv[1]
    else:
        print("need more argument")
        print(mydoc) 
        exit(1)

    with open(filename_labeled) as f:
        delim = getdelim(f.readline())
    data = [ [ int(item) for item in line.rstrip().split(delim)] for line in open(filename_labeled) ]
    
    filename_base = os.path.splitext(filename_labeled)[0]
    
    fo_result = open(filename_base+"_PR.txt", "w+")
    fo_confmat = csv.writer(open(filename_base+"CONFMAT.csv","w+") )
    
    # ======== #
    #  count   #
    # ======== #
    classdict = dict(item[::-1] for item in enumerate(sorted(list(set(item[1] for item in data))))) 
    classdict_inv = dict(item for item in enumerate(sorted(list(set(item[1] for item in data))))) 
    classnum = len(classdict)
    
    counts_predict = [0 for i in xrange(classnum)]
    counts_label = [0 for i in xrange(classnum)]
    counts_matrix = [ [0 for i in xrange(classnum)] for j in xrange(classnum) ]
    
    for line in data:
        counts_predict[classdict[line[0]]]+=1
        counts_label[classdict[line[1]]]+=1
        counts_matrix[classdict[line[1]]][classdict[line[0]]]+=1
    confusion_matrix = [ [item/float(counts_label[j]) for item in counts_matrix[j] ] for j in xrange(len(counts_matrix)) if counts_label[j] !=0]
        
    # ====================== #
    #  precision and recall  #
    # ====================== #
    count_all = len(data)
    precisions = [ 0 for i in xrange(classnum) ]
    recalls = [ 0 for i in xrange(classnum) ]
    accuracies = [ 0 for i in xrange(classnum) ]
    Fmeasures = [ 0 for i in xrange(classnum) ]
    
    for i in xrange(classnum):
        if(counts_predict[i] > 0):
            precisions[i] = counts_matrix[i][i]/float(counts_predict[i])
        else:
            precisions[i] = 0
            
        recalls[i] = counts_matrix[i][i]/float(counts_label[i])
        if(precisions[i]>0 and recalls[i]>0 ):
            Fmeasures[i] = 2 / ( 1.0/precisions[i] + 1.0/recalls[i] )
        else:
            Fmeasures[i] = 0
        accuracies[i] = (counts_matrix[i][i] + count_all-counts_predict[i]-counts_label[i]+counts_matrix[i][i]) / float(count_all)
        
    
    MacroAveragePrecision = sum(precisions) / len(precisions)
    MicroAveragePrecision = sum([ counts_matrix[i][i] for i in xrange(classnum) ]) / float(count_all)

    MacroAverageRecall = sum(recalls) / len(recalls)
    MicroAverageRecall = sum([ counts_matrix[i][i] for i in xrange(classnum) ]) / float(count_all)

    if(MacroAveragePrecision>0 and MacroAverageRecall>0):
        MacroAverageFmeasure = 2*MacroAveragePrecision*MacroAverageRecall / (MacroAveragePrecision+MacroAverageRecall)
    else:
        MacroAverageFmeasure = 0
        
    if(MicroAveragePrecision>0 and MicroAverageRecall>0):
        MicroAverageFmeasure = 2*MicroAveragePrecision*MicroAverageRecall / (MicroAveragePrecision+MicroAverageRecall)
    else:
        MicroAverageFmeasure = 0

    Accuracy_all = sum([counts_matrix[i][i] for i in xrange(classnum) ])/float(count_all)


    # ======== #
    #  output  #
    # ======== # 
    fo_result.write("## Accuracy ##\n")
    fo_result.write(str(Accuracy_all)+"\n" )

    fo_result.write("## precision ##\n")
    for i,line in enumerate(precisions):
        fo_result.write("{0}:{1}\n".format(classdict_inv[i],line))
    fo_result.write("{0}:{1}\n".format("MacroAverage", MacroAveragePrecision))
    fo_result.write("{0}:{1}\n".format("MicroAverage", MicroAveragePrecision))

    fo_result.write("## recall ##\n")
    for i,line in enumerate(recalls):
        fo_result.write("{0}:{1}\n".format(classdict_inv[i],line))
    fo_result.write("{0}:{1}\n".format("MacroAverage", MacroAverageRecall))
    fo_result.write("{0}:{1}\n".format("MicroAverage", MicroAverageRecall))

    fo_result.write("## predict ##\n")
    for i,line in enumerate(counts_predict):
        fo_result.write("{0}:{1}\n".format(classdict_inv[i],line))

    fo_result.write("## F-measure ##\n")
    for i,line in enumerate(Fmeasures):
        fo_result.write("{0}:{1}\n".format(classdict_inv[i],line))
    fo_result.write("{0}:{1}\n".format("MacroAverage", MacroAverageFmeasure))
    fo_result.write("{0}:{1}\n".format("MicroAverage", MicroAverageFmeasure))

    fo_result.write("## accuracy ##\n")
    for i,line in enumerate(accuracies):
        fo_result.write("{0}:{1}\n".format(classdict_inv[i],line))

    fo_result.write("## label ##\n")
    for i,line in enumerate(counts_label):
        fo_result.write("{0}:{1}\n".format(classdict_inv[i],line))
        
    fo_result.write("## matrix ##\n")
    for i, line in enumerate(counts_matrix):
        fo_result.write("{0}:{1}\n".format(classdict_inv[i],line))

    fo_result.write("## confusion matrix ##\n")
    for i, line in enumerate(confusion_matrix):
        fo_result.write("{0}:{1}\n".format(classdict_inv[i],line))
        
    fo_confmat.writerows(confusion_matrix)

        
    print "write:",fo_result.name
    print "done!"
