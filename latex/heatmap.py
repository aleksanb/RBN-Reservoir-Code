from argparse import ArgumentParser
import json
import os

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('infile', help='file containing data')
    parser.add_argument('--accuracy', type=float, default=0.90)
    arguments = parser.parse_args()

    samples = None
    with open(arguments.infile, 'r') as f:
        samples = json.load(f)

    na = 'n_attractors'
    mal = 'mean_attractor_length'

    xs = [x[na] for x in samples]
    ys = [x[mal] for x in samples]

    xmin, xmax, xscale = min(xs), max(xs), 1.0
    ymin, ymax, yscale = min(ys), max(ys), 0.5

    xbuckets = int((xmax - xmin + 1) / xscale)
    ybuckets = int((ymax - ymin + 1) / yscale)

    buckets = [[0] * xbuckets for _ in range(ybuckets)]

    count = 0
    for sample in samples:
        if sample['accuracy'] >= arguments.accuracy:
            xpos = int((sample[na] - xmin) / xscale)
            ypos = int((sample[mal] - ymin) / yscale)

            buckets[ypos][xpos] += 1
            count += 1

    print '%', count

    for i, row in enumerate(buckets):
        if i != 0:
            print

        for j, elm in enumerate(row):
            x = j * xscale + xmin
            y = i * yscale + ymin

            print x, y, elm
