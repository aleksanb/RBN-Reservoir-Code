from argparse import ArgumentParser
import json
import itertools
import os.path

def make_plot(plot_data):
    boxplot_preamble = "\\myboxplot{\n"
    boxplot_template=\
"""
\\addplot[mark=*, boxplot, boxplot/draw position={index}]
table[row sep=\\\\, y index=0] {{
data
{data}
}};
"""
    boxplot_postamble = "}}{{{scale}}}{{{label}}}\n"

    final_plot = boxplot_preamble

    xs = sorted([plot[0] for plot in plot_data])
    scale = xs[1] - xs[0] if len(xs) > 1 else xs[0]

    for (x_index, samples) in plot_data:
        data = "\n".join(["{} \\\\".format(sample)
                          for sample in samples])

        index = x_index / scale
        final_plot += boxplot_template.format(
            index=index,
            data=data)

    final_plot += boxplot_postamble.format(
        scale=1.0/scale,
        label='')
    return final_plot

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('results', help='Path to results file')
    parser.add_argument('column', help='Column to plot against accuracy')
    parser.add_argument('--output_dir', help='where to store output')
    arguments = parser.parse_args()

    output_dir = results_dir =\
        os.path.dirname(os.path.join(os.getcwd(), arguments.results))
    if arguments.output_dir:
        output_dir = os.path.join(os.getcwd(), arguments.output_dir)

    with open(arguments.results) as f:
        datasets = json.load(f)

    for n_nodes, reservoir_configurations in datasets.iteritems():
        plot_data = [
                (configuration[arguments.column],
                 configuration['accuracies'])
                for configuration in reservoir_configurations]

        latex_plot = make_plot(plot_data)

        filename = "boxplot-{}-N{}-K{}-S{}.tex".format(
                arguments.column,
                reservoir_configurations[0]['n_nodes'],
                3,  # This is fine
                reservoir_configurations[0]['n_samples'])
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w') as f:
            f.write(latex_plot)
            print "Wrote: " + filepath
