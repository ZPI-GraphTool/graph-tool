import shutil
from datetime import datetime
from pathlib import Path
from textwrap import dedent as dedent_to_lowest

from plotly.graph_objs import Figure

from app.server._config import EXPERIMENTS_DIRECTORY

from .open_file import open_file


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


def copy_used_algorithm(results_directory: Path, algorithm_path: str | Path) -> None:
    if not algorithm_path:
        return
    algorithm_path = Path(algorithm_path).resolve()
    shutil.copy(algorithm_path, results_directory / algorithm_path.name)


def save_results(output_format: str, **kwargs) -> None:
    results_directory = get_results_directory(kwargs["experiment_name"])

    copy_used_algorithm(results_directory, kwargs["preprocessing_path"])
    copy_used_algorithm(results_directory, kwargs["streaming_path"])
    copy_used_algorithm(results_directory, kwargs["batch_path"])

    calculation_time_plot_file = write_plot_image(
        "calculation_time", kwargs["calculation_time"], results_directory
    )
    memory_usage_plot_file = write_plot_image(
        "memory_usage", kwargs["memory_usage"], results_directory
    )

    if output_format == "markdown":
        results = get_results_as_markdown(
            calculation_time_plot_file, memory_usage_plot_file, **kwargs
        )
        results_file = results_directory / "results.md"
    elif output_format == "latex":
        results = get_results_as_latex(
            calculation_time_plot_file, memory_usage_plot_file, **kwargs
        )
        results_file = results_directory / "results.tex"
    with Path.open(results_file, "w", encoding="utf-8") as file:  # type: ignore
        file.write(results)  # type: ignore
    open_file(results_file)  # type: ignore


def get_results_as_markdown(
    calculation_time_plot_file: str, memory_usage_plot_file: str, **kwargs
) -> str:
    results = dedent_to_zero(f"""\
        # **Results of experiment `{kwargs["experiment_name"]}`**\n
        ## Metadata\n
        * Dataset: `{kwargs['dataset']}`
        * Preprocessing function: `{kwargs['preprocessing_name'] or "Not used"}`
        * Streaming algorithm: `{kwargs['streaming_name'] or "Not used"}`
        * Batch algorithm: `{kwargs['batch_name'] or "Not used"}`\n
        ## Properties and metrics\n
        * Total edge count: `{kwargs['total_edge_count']}`
        * Size of dataset: `{kwargs['dataset_size']}
        * Average calculation time per edge of stream algorithm: `{kwargs["calculation_avg"]}
        * Average memory usage of stream algorithm: `{kwargs["memory_avg"]}
    """)
    if kwargs["batch_name"]:
        results += dedent_to_zero(f"""\
            * Jaccard similarity: `{kwargs['jaccard_similarity']:.4g}` (order: `{kwargs['order']}`, cardinality: `{kwargs['cardinality']}`)
            * Streaming accuracy: `{kwargs['streaming_accuracy']:.4g}`
        """)
    results += dedent_to_zero(f"""\
        ## Streaming node rank\n
        {kwargs["streaming_node_rank"].to_markdown()}
    """)
    if kwargs["batch_name"]:
        results += dedent_to_zero(f"""\
            ## Batch node rank\n
            {kwargs["batch_node_rank"].to_markdown()}
        """)
    results += dedent_to_zero(f"""\
        ## Calculation time\n
        ![calculation_time](images/{calculation_time_plot_file})\n
        ## Memory usage history\n
        ![memory_usage](images/{memory_usage_plot_file})
    """)

    return results


def get_results_as_latex(
    calculation_time_plot_file: str, memory_usage_plot_file: str, **kwargs
) -> str:
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
            \\item Dataset: \\texttt{{{kwargs['dataset']}}}
            \\item Preprocessing function: \\texttt{{{kwargs['preprocessing_name'] or "Not used"}}}
            \\item Streaming algorithm: \\texttt{{{kwargs['streaming_name'] or "Not used"}}}
            \\item Batch algorithm: \\texttt{{{kwargs['batch_name'] or "Not used"}}}
        \\end{{itemize}}

        \\section*{{Properties and metrics}}
        \\begin{{itemize}}
            \\item Total edge count: \\texttt{{{kwargs['total_edge_count']}}}
            \\item Size of dataset: \\texttt{{{kwargs['dataset_size']}}}
            \\item Average calculation time per edge of stream algorithm:: \\texttt{{{kwargs["calculation_avg"]}}}
            \\item Average memory usage of stream algorithm: \\texttt{{{kwargs["memory_avg"]}}}
        \\end{{itemize}}
    """)
    if kwargs["batch_name"]:
        results += dedent_to_lowest(f"""\
            \\begin{{itemize}}
                \\item Jaccard similarity: \\texttt{{{kwargs['jaccard_similarity']:.4g}}} (order: \\texttt{{{kwargs['order']}}}, cardinality: \\texttt{{{kwargs['cardinality']}}})
                \\item Streaming accuracy: \\texttt{{{kwargs['streaming_accuracy']:.4g}}}
            \\end{{itemize}}
        """)
    results += "\n" + kwargs["streaming_node_rank"].to_latex(
        index=False, longtable=True, float_format="%.4g", caption="Streaming node rank"
    )
    if kwargs["batch_name"]:
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

    return results
