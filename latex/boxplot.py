from argparse import ArgumentParser
import json

def make_plot(columns):
    boxplot_preamble = "\\myboxplot{\n"
    boxplot_template=\
"""
\\addplot[mark=*, boxplot, boxplot/draw position={index}]
table[row sep=\\\\, y index=0] {{
data
{data}
}};
"""
    boxplot_postamble = "}{{0.1}}\n"

    plot = ""
    plot += boxplot_preamble

    for column, values in columns.iteritems():
        data = map(str, values)
        data = map(lambda s: s + " \\\\", data)
        data = "\n".join(data)
        plot += boxplot_template.format(
            index=int(column)/10,
            data=data)

    plot += boxplot_postamble

    return plot

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('directory', help='path to dump directory')
    parser.add_argument('output_directory', nargs="?", help='where to store output')
    arguments = parser.parse_args()

    with open(arguments.directory + '/result.json') as f:
        datasets = json.load(f)

    with open(arguments.directory + '/config.json') as f:
        config = json.load(f)

    print "Writing plots"
    for n_nodes in datasets.keys():
        latex_plot = make_plot(datasets[n_nodes])
        filename = "{}/boxplot-N{}-K{}-S{}.tex".format(
            arguments.output_directory or arguments.directory,
            n_nodes, config["reservoir"]["connectivity"],
            config["distribution"]["n_samples"])
        with open(filename, 'w') as f:
            f.write(latex_plot)
        print filename

    print "Finished writing plots"
