from datetime import datetime
from pathlib import Path
from textwrap import dedent as dedent_to_lowest

from plotly.graph_objs import Figure

from app.server._config import EXPERIMENTS_DIRECTORY
from app.server.logic.actions import open_file


def dedent_to_zero(message: str) -> str:
    content = ""
    for line in message.splitlines():
        content += line.lstrip() + "\n"
    return content


def get_results_directory(experiment_name: str) -> Path:
    try:
        date_time = datetime.strptime(experiment_name, "%Y-%m-%d %H_%M_%S")
        date, time = date_time.strftime("%Y-%m-%d"), date_time.strftime("%H_%M_%S")
        results_directory = EXPERIMENTS_DIRECTORY / date / time
    except ValueError:
        results_directory = EXPERIMENTS_DIRECTORY / experiment_name
    results_directory.mkdir(parents=True, exist_ok=True)
    return results_directory


def write_plot_image(name: str, plot: Figure, results_directory: Path) -> str:
    images_directory = results_directory / "images"
    images_directory.mkdir(exist_ok=True)
    image_file = f"{name}.svg"
    image_path = images_directory / image_file
    if not image_path.exists():
        plot.write_image(images_directory / image_file)
    return image_file


def save_results_to_markdown(**kwargs) -> None:
    results_directory = get_results_directory(kwargs["experiment_name"])

    calculation_time_plot_file = write_plot_image(
        "calculation_time", kwargs["calculation_time"], results_directory
    )
    memory_usage_plot_file = write_plot_image(
        "memory_usage", kwargs["memory_usage"], results_directory
    )

    results = dedent_to_zero(f"""\
        # **Results of experiment `{kwargs["experiment_name"]}`**
        ## Metadata
        * Preprocessing function: `{kwargs['preprocessing_function'] or "Not used"}`
        * Streaming algorithm: `{kwargs['streaming_algorithm'] or "Not used"}`
        * Batch algorithm: `{kwargs['batch_algorithm'] or "Not used"}`
        ## Properties and metrics
        * Total edge count: `{kwargs['total_edge_count']}`
        * Size of dataset: `{kwargs['dataset_size']}`  \
    """)
    if kwargs["batch_algorithm"]:
        results += dedent_to_zero(f"""\
            * Jaccard similarity: `{kwargs['jaccard_similarity']:.4g}` (order: `{kwargs['order']}`, cardinality: `{kwargs['cardinality']}`)
            * Streaming accuracy: `{kwargs['streaming_accuracy']:.4g}`  \
        """)
    results += dedent_to_zero(f"""\
        ## Streaming node rank
        {kwargs["streaming_node_rank"].to_markdown()}\
    """)
    if kwargs["batch_algorithm"]:
        results += dedent_to_zero(f"""\
            ## Batch node rank
            {kwargs["batch_node_rank"].to_markdown()}\
        """)
    results += dedent_to_zero(f"""\
        ## Calculation time
        ![calculation_time](images/{calculation_time_plot_file})
        ## Memory usage history
        ![memory_usage](images/{memory_usage_plot_file})  \
    """)

    results_file = results_directory / "results.md"
    with Path.open(results_file, "w", encoding="utf-8") as file:
        file.write(results)
    open_file(results_file)


def save_results_to_latex(**kwargs) -> None:
    results_directory = get_results_directory(kwargs["experiment_name"])

    calculation_time_plot_file = write_plot_image(
        "calculation_time", kwargs["calculation_time"], results_directory
    )
    memory_usage_plot_file = write_plot_image(
        "memory_usage", kwargs["memory_usage"], results_directory
    )

    experiment_name = kwargs["experiment_name"].replace("_", "\\_")

    results = dedent_to_lowest(f"""\
        \\documentclass{{article}}

        \\usepackage{{booktabs}}
        \\usepackage[justification=centering]{{caption}}
        \\usepackage{{float}}
        \\usepackage[T1]{{fontenc}}
        \\usepackage[a4paper, margin=1.2in]{{geometry}}
        \\usepackage{{longtable}}
        \\usepackage{{svg}}

        \\graphicspath{{{{./images/}}}}

        \\title{{\\huge Results of experiment\\\\\\texttt{{{experiment_name}}}}}
        \\author{{}}
        \\date{{}}

        \\begin{{document}}
        \\maketitle

        \\section*{{Metadata}}
        \\begin{{itemize}}
            \\item Preprocessing function: \\texttt{{{kwargs['preprocessing_function'] or "Not used"}}}
            \\item Streaming algorithm: \\texttt{{{kwargs['streaming_algorithm'] or "Not used"}}}
            \\item Batch algorithm: \\texttt{{{kwargs['batch_algorithm'] or "Not used"}}}
        \\end{{itemize}}

        \\section*{{Properties and metrics}}
        \\begin{{itemize}}
            \\item Total edge count: \\texttt{{{kwargs['total_edge_count']}}}
            \\item Size of dataset: \\texttt{{{kwargs['dataset_size']}}}
        \\end{{itemize}}
    """)
    if kwargs["batch_algorithm"]:
        results += dedent_to_lowest(f"""\
            \\begin{{itemize}}
                \\item Jaccard similarity: \\texttt{{{kwargs['jaccard_similarity']:.4g}}} (order: \\texttt{{{kwargs['order']}}}, cardinality: \\texttt{{{kwargs['cardinality']}}})
                \\item Streaming accuracy: \\texttt{{{kwargs['streaming_accuracy']:.4g}}}
            \\end{{itemize}}
        """)
    results += "\n" + kwargs["streaming_node_rank"].to_latex(
        index=False, longtable=True, float_format="%.4g", caption="Streaming node rank"
    )
    if kwargs["batch_algorithm"]:
        results += "\n" + kwargs["batch_node_rank"].to_latex(
            index=False, longtable=True, float_format="%.4g", caption="Batch node rank"
        )
    results += dedent_to_lowest(f"""
        \\begin{{figure}}[H]
            \\centering
            \\includesvg[width=\\linewidth]{{{calculation_time_plot_file}}}
            \\caption{{Calculation time}}
        \\end{{figure}}
        \\begin{{figure}}[H]
            \\centering
            \\includesvg[width=\\linewidth]{{{memory_usage_plot_file}}}
            \\caption{{Memory usage history}}
        \\end{{figure}}

        \\end{{document}}
    """)

    results_file = results_directory / "results.tex"
    with Path.open(results_file, "w", encoding="utf-8") as file:
        file.write(results)
    open_file(results_file)
