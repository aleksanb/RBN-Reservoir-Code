from argparse import ArgumentParser
import json
import os

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('infile', help='file containing data')
    parser.add_argument('--accuracy', type=float, default=0.90)
    parser.add_argument('--max-mal', type=float, default=float('inf'))
    arguments = parser.parse_args()

    samples = None
    with open(arguments.infile, 'r') as f:
        samples = json.load(f)

    na = 'n_attractors'
    mal = 'mean_attractor_length'

    xs_ys = [(sample[na], sample[mal]) for sample in samples
                    if sample['accuracy'] >= arguments.accuracy
                        and sample[mal] <= arguments.max_mal]
    xs = [e[0] for e in xs_ys]
    ys = [e[1] for e in xs_ys]

    xmin, xmax, xscale = min(xs), max(xs), 1.0
    ymin, ymax, yscale = min(ys), max(ys), 0.5

    xbuckets = int((xmax - xmin + 1) / xscale)
    ybuckets = int((ymax - ymin + 1) / yscale)

    buckets = [[0] * xbuckets for _ in range(ybuckets)]

    count = 0
    for (x, y) in xs_ys:
        xpos = int((x - xmin) / xscale)
        ypos = int((y - ymin) / yscale)

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
