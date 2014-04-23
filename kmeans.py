#! /usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import csv
import os
import sklearn.cluster

parser = argparse.ArgumentParser()
parser.add_argument('input_tsv', help='.tsv')
parser.add_argument('k', type=int)

def readtsv(filename):
    return [
        map(float, line.rstrip().split("\t"))
        for line in open(filename)]

if __name__=='__main__':
    args = parser.parse_args()
    basename = os.path.splitext(args.input_tsv)[0]
    output_labels_filename = "%s_%d_means_labels.dat" % (basename, args.k)
    output_centroids_filename = "%s_%d_means_centroids.tsv" % (basename, args.k)

    data = readtsv(args.input_tsv)

    classifier = sklearn.cluster.KMeans(n_clusters=args.k)
    classifier.fit(data)

    labels = classifier.predict(data)
    centroids = classifier.cluster_centers_

    open(output_labels_filename, "w+").writelines(map(lambda x: str(x)+"\n", labels))
    csv.writer(open(output_centroids_filename, "w+"), delimiter="\t").writerows([[x for x in line] for line in centroids])
