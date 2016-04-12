import os
import json
import time
from argparse import ArgumentParser


def create_scatterplot(tuples):
    boxplot = []
    boxplot.append("x y")

    for (x, y) in tuples:
        boxplot.append("{} {}".format(x, y))

    return "\n".join(boxplot)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('infile', help='file containing data')
    arguments = parser.parse_args()

    with open(os.getcwd() + '/' + arguments.infile, 'r') as f:
        json_samples = json.load(f)

        for attribute in ("mean_transient_time", "mean_attractor_length", "n_attractors"):
            tuples = map(
                lambda s: (s[attribute], s["accuracy"]),
                json_samples)

            plot = create_scatterplot(tuples)
            plot = "% {}, accuracy\n".format(attribute) + plot
            filename = '{}-scatter-{}.dat'.format(attribute, int(time.time()))

            with open(os.getcwd() + '/' + filename, 'w') as f:
                f.write(plot)
                print "Wrote", filename
