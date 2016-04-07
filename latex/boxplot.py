from argparse import ArgumentParser
import json

def make_plot(distributions, column_to_plot_against, scale):
    boxplot_preamble = "\\myboxplot{\n"
    boxplot_template=\
"""
\\addplot[mark=*, boxplot, boxplot/draw position={index}]
table[row sep=\\\\, y index=0] {{
data
{data}
}};
"""
    boxplot_postamble = "}}{{{scale}}}\n"

    plot = ""
    plot += boxplot_preamble

    for distribution in distributions:
        data = map(str, distribution["accuracies"])
        data = map(lambda s: s + " \\\\", data)
        data = "\n".join(data)

        index = distribution[column_to_plot_against] / scale
        plot += boxplot_template.format(
            index=index,
            data=data)

    plot += boxplot_postamble.format(scale=1.0/scale)

    return plot

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('directory', help='path to dump directory')
    parser.add_argument('output_directory', nargs="?", help='where to store output')
    column_to_plot_against = "output_connectivity"
    arguments = parser.parse_args()

    with open('/'.join([arguments.directory, 'result.json'])) as f:
        datasets = json.load(f)

    with open('/'.join([arguments.directory, 'config.json'])) as f:
        config = json.load(f)

    for n_nodes, distributions_for_n in datasets.iteritems():
        #keys = sorted([d[column_to_plot_against] for d in distributions_for_n])
        #print keys
        #scale = keys[1] - keys[0] if len(keys) > 1 else keys[0]
        scale = 10

        latex_plot = make_plot(
            distributions_for_n,
            column_to_plot_against,
            scale)

        filename = "{}/boxplot-N{}-K{}-S{}-{}.tex".format(
            arguments.output_directory or arguments.directory,
            n_nodes,
            config["reservoir"]["connectivity"],
            config["distribution"]["n_samples"],
            column_to_plot_against)

        with open(filename, 'w') as f:
            f.write(latex_plot)

        print "Wrote: " + filename

    print "Finished writing plots"
