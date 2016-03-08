from argparse import ArgumentParser
import json

def make_plot(columns, input_connectivity_step_size):
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

    for column, values in columns.iteritems():
        data = map(str, values)
        data = map(lambda s: s + " \\\\", data)
        data = "\n".join(data)
        plot += boxplot_template.format(
            index=int(column)/input_connectivity_step_size,
            data=data)

    plot += boxplot_postamble.format(scale=1.0/input_connectivity_step_size)

    return plot

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('directory', help='path to dump directory')
    parser.add_argument('output_directory', nargs="?", help='where to store output')
    arguments = parser.parse_args()

    with open('/'.join([arguments.directory, 'result.json'])) as f:
        datasets = json.load(f)

    with open('/'.join([arguments.directory, 'config.json'])) as f:
        config = json.load(f)

    for n_nodes in datasets.keys():
        latex_plot = make_plot(
            datasets[n_nodes],
            config["distribution"]["input_connectivity_step_size"])

        filename = "{}/boxplot-N{}-K{}-S{}.tex".format(
            arguments.output_directory or arguments.directory,
            n_nodes, config["reservoir"]["connectivity"],
            config["distribution"]["n_samples"])

        with open(filename, 'w') as f:
            f.write(latex_plot)

        print "Wrote: " + filename

    print "Finished writing plots"
