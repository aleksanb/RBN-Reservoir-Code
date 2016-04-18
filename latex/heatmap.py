from argparse import ArgumentParser
import json
import os

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('infile', help='file containing data')
    arguments = parser.parse_args()

    samples = None
    with open(os.getcwd() + '/' + arguments.infile, 'r') as f:
        samples = json.load(f)

    minimum_accuracy = 0.90
    na = 'n_attractors'
    mal = 'mean_attractor_length'

    xs = map(lambda x: x[na], samples)
    ys = map(lambda x: x[mal], samples)

    xmin, xmax, xscale = min(xs), max(xs), 1.0
    ymin, ymax, yscale = min(ys), max(ys), 0.3

    xbuckets = int((xmax - xmin + 1) / xscale)
    ybuckets = int((ymax - ymin + 1) / yscale)

    buckets = [[0] * xbuckets for _ in range(ybuckets)]

    for sample in samples:
        if sample['accuracy'] >= minimum_accuracy:
            xpos = int((sample[na] - xmin) / xscale)
            ypos = int((sample[mal] - ymin) / yscale)

            buckets[ypos][xpos] += 1

    for i, row in enumerate(buckets[:int(20/0.3)]):
        if i != 0:
            print

        for j, elm in enumerate(row[:15]):
            x = j * xscale + xmin
            y = i * yscale + ymin

            print x, y, elm
