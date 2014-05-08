#! /usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import csv
import os
import scipy
import sklearn.cluster

parser = argparse.ArgumentParser()
parser.add_argument('input_tsv', help='.tsv')
parser.add_argument('--bandwidth', help="bandwidth of RBF kernel", type=float)

def readtsv(filename):
    return scipy.array([
        map(float, line.rstrip().split("\t"))
        for line in open(filename)])

if __name__=='__main__':
    args = parser.parse_args()
    basename = os.path.splitext(args.input_tsv)[0]
    bandwidth_suffix = "" if args.bandwidth is None else "_%sband" % str(args.bandwidth).replace(".", "p")
    output_labels_filename = "%s_meanshift%s_labels.dat" % (basename, bandwidth_suffix)
    output_centroids_filename = "%s_meanshift%s_centroids.tsv" % (basename, bandwidth_suffix)

    data = readtsv(args.input_tsv)

    classifier = sklearn.cluster.MeanShift(bandwidth=args.bandwidth)

    labels = classifier.fit_predict(data)
    centroids = classifier.cluster_centers_

    open(output_labels_filename, "w+").writelines(map(lambda x: str(x)+"\n", labels))
    csv.writer(open(output_centroids_filename, "w+"), delimiter="\t").writerows([[x for x in line] for line in centroids])
