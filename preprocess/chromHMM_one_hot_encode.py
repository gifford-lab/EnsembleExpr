#!/usr/bin/env python2.7
#
# Convert
import pandas
import sys

# Find all possible annotations by loading the entire input file.
labels = pandas.read_csv(sys.argv[1], header=None, sep="\t")
labels = sorted(set(labels[labels.columns[-1]]))

label_mapper = {}

print "\t".join(labels)

# Pre-compute the rows for each label.
for i, label in enumerate(labels):
    one_hot = ["0"] * len(labels)
    one_hot[i] = "1"
    label_mapper[label] = "\t".join(one_hot)

# Print one-hot representation for each input row.
for line in sys.stdin:
    x = label_mapper[line.strip()]
    print x
    print x
