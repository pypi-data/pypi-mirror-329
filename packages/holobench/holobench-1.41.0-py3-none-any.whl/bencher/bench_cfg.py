from __future__ import annotations

import argparse
import logging

from typing import List

import param
import panel as pn
from datetime import datetime

from bencher.variables.sweep_base import hash_sha1, describe_variable
from bencher.variables.time import TimeSnapshot, TimeEvent
from bencher.variables.results import OptDir
from bencher.job import Executors
from bencher.results.laxtex_result import to_latex


class BenchPlotSrvCfg(param.Parameterized):
    port: int = param.Integer(None, doc="The port to launch panel with")
    allow_ws_origin = param.Boolean(
        False,
        doc="Add the port to the whilelist, (warning will disable remote access if set to true)",
    )
    show: bool = param.Boolean(True, doc="Open the served page in a web browser")


class BenchRunCfg(BenchPlotSrvCfg):
    """A Class to store options for how to run a benchmark parameter sweep"""

    repeats: bool = param.Integer(1, doc="The number of times to sample the inputs")

    over_time: bool = param.Boolean(
        False,
        doc="If true each time the function is called it will plot a timeseries of historical and the latest result.",
    )

    use_optuna: bool = param.Boolean(False, doc="show optuna plots")

    summarise_constant_inputs = param.Boolean(
        True, doc="Print the inputs that are kept constant when describing the sweep parameters"
    )

    print_bench_inputs: bool = param.Boolean(
        True, doc="Print the inputs to the benchmark function every time it is called"
    )

    print_bench_results: bool = param.Boolean(
        True, doc="Print the results of the benchmark function every time it is called"
    )

    clear_history: bool = param.Boolean(False, doc="Clear historical results")

    print_pandas: bool = param.Boolean(
        False, doc="Print a pandas summary of the results to the console."
    )

    print_xarray: bool = param.Boolean(
        False, doc="Print an xarray summary of the results to the console"
    )

    serve_pandas: bool = param.Boolean(
        False,
        doc="Serve a pandas summary on the results webpage.  If you have a large dataset consider setting this to false if the page loading is slow",
    )

    serve_pandas_flat: bool = param.Boolean(
        True,
        doc="Serve a flattened pandas summary on the results webpage.  If you have a large dataset consider setting this to false if the page loading is slow",
    )

    serve_xarray: bool = param.Boolean(
        False,
        doc="Serve an xarray summary on the results webpage. If you have a large dataset consider setting this to false if the page loading is slow",
    )

    auto_plot: bool = param.Boolean(
        True, doc=" Automatically dedeuce the best type of plot for the results."
    )

    raise_duplicate_exception: bool = param.Boolean(False, doc=" Used to debug unique plot names.")

    cache_results: bool = param.Boolean(
        False,
        doc="This is a benchmark level cache that stores the results of a fully completed benchmark. At the end of a benchmark the values are added to the cache but are not if the benchmark does not complete.  If you want to cache values during the benchmark you need to use the cache_samples option. Beware that depending on how you change code in the objective function, the cache could provide values that are not correct.",
    )

    clear_cache: bool = param.Boolean(
        False, doc=" Clear the cache of saved input->output mappings."
    )

    cache_samples: bool = param.Boolean(
        False,
        doc="If true, every time the benchmark function is called, bencher will check if that value has been calculated before and if so load the from the cache.  Note that the sample level cache is different from the benchmark level cache which only caches the aggregate of all the results at the end of the benchmark. This cache lets you stop a benchmark halfway through and continue. However, beware that depending on how you change code in the objective function, the cache could provide values that are not correct.",
    )

    only_hash_tag: bool = param.Boolean(
        False,
        doc="By default when checking if a sample has been calculated before it includes the hash of the greater benchmarking context.  This is safer because it means that data generated from one benchmark will not affect data from another benchmark.  However, if you are careful it can be more flexible to ignore which benchmark generated the data and only use the tag hash to check if that data has been calculated before. ie, you can create two benchmarks that sample a subset of the problem during exploration and give them the same tag, and then afterwards create a larger benchmark that covers the cases you already explored.  If this value is true, the combined benchmark will use any data from other benchmarks with the same tag.",
    )

    clear_sample_cache: bool = param.Boolean(
        False,
        doc="Clears the per-sample cache.  Use this if you get unexpected behavior.  The per_sample cache is tagged by the specific benchmark it was sampled from. So clearing the cache of one benchmark will not clear the cache of other benchmarks.",
    )

    overwrite_sample_cache: bool = param.Boolean(
        False,
        doc="If True, recalculate the value and overwrite the value stored in the sample cache",
    )

    only_plot: bool = param.Boolean(
        False, doc="Do not attempt to calculate benchmarks if no results are found in the cache"
    )

    use_holoview: bool = param.Boolean(False, doc="Use holoview for plotting")

    nightly: bool = param.Boolean(
        False, doc="Run a more extensive set of tests for a nightly benchmark"
    )

    time_event: str = param.String(
        None,
        doc="A string representation of a sequence over time, i.e. datetime, pull request number, or run number",
    )

    headless: bool = param.Boolean(False, doc="Run the benchmarks headlessly")

    render_plotly = param.Boolean(
        True,
        doc="Plotly and Bokeh don't play nicely together, so by default pre-render plotly figures to a non dynamic version so that bokeh plots correctly.  If you want interactive 3D graphs, set this to true but be aware that your 2D interactive graphs will probably stop working.",
    )

    level = param.Integer(
        default=0,
        bounds=[0, 12],
        doc="The level parameter is a method of defining the number samples to sweep over in a variable agnostic way, i.e you don't need to specify the number of samples for each variable as they are calculated dynamically from the sampling level.  See example_level.py for more information.",
    )

    run_tag = param.String(
        default="",
        doc="Define a tag for a run to isolate the results stored in the cache from other runs",
    )

    run_date = param.Date(
        default=datetime.now(),
        doc="The date the bench run was performed",
    )

    # parallel = param.Boolean(
    #     default=False,
    #     doc="Run the sweep in parallel.  Warning! You need to make sure your code is threadsafe before using this option",
    # )

    executor = param.Selector(
        objects=list(Executors),
        doc="The function can be run serially or in parallel with different futures executors",
    )

    plot_size = param.Integer(default=None, doc="Sets the width and height of the plot")
    plot_width = param.Integer(
        default=None,
        doc="Sets with width of the plots, this will override the plot_size parameter",
    )
    plot_height = param.Integer(
        default=None, doc="Sets the height of the plot, this will override the plot_size parameter"
    )

    @staticmethod
    def from_cmd_line() -> BenchRunCfg:  # pragma: no cover
        """create a BenchRunCfg by parsing command line arguments

        Returns:
            parsed args: parsed args
        """

        parser = argparse.ArgumentParser(description="benchmark")

        parser.add_argument(
            "--use-cache",
            action="store_true",
            help=BenchRunCfg.param.cache_results.doc,
        )

        parser.add_argument(
            "--only-plot",
            action="store_true",
            help=BenchRunCfg.param.only_plot.doc,
        )

        parser.add_argument(
            "--port",
            type=int,
            help=BenchRunCfg.param.port.doc,
        )

        parser.add_argument(
            "--nightly",
            action="store_true",
            help="Turn on nightly benchmarking",
        )

        parser.add_argument(
            "--time_event",
            type=str,
            default=BenchRunCfg.param.time_event.default,
            help=BenchRunCfg.param.time_event.doc,
        )

        parser.add_argument(
            "--repeats",
            type=int,
            default=BenchRunCfg.param.repeats.default,
            help=BenchRunCfg.param.repeats.doc,
        )

        return BenchRunCfg(**vars(parser.parse_args()))


class BenchCfg(BenchRunCfg):
    """A class for storing the arguments to configure a benchmark protocol  If the inputs variables are the same the class should return the same hash and same filename.  This is so that historical data can be referenced and ensures that the generated plots are unique per benchmark"""

    input_vars = param.List(
        default=None,
        doc="A list of ParameterizedSweep variables to perform a parameter sweep over",
    )
    result_vars = param.List(
        default=None,
        doc="A list of ParameterizedSweep results collect and plot.",
    )

    const_vars = param.List(
        default=None,
        doc="Variables to keep constant but are different from the default value",
    )

    result_hmaps = param.List(default=None, doc="a list of holomap results")

    meta_vars = param.List(
        default=None,
        doc="Meta variables such as recording time and repeat id",
    )
    all_vars = param.List(
        default=None,
        doc="Stores a list of both the input_vars and meta_vars that are used to define a unique hash for the input",
    )
    iv_time = param.List(
        default=[],
        item_type=TimeSnapshot | TimeEvent,
        doc="A parameter to represent the sampling the same inputs over time as a scalar type",
    )

    iv_time_event = param.List(
        default=[],
        item_type=TimeEvent,
        doc="A parameter to represent the sampling the same inputs over time as a discrete type",
    )

    over_time: param.Boolean(
        False, doc="A parameter to control whether the function is sampled over time"
    )
    name: str = param.String(None, doc="The name of the benchmarkCfg")
    title: str = param.String(None, doc="The title of the benchmark")
    raise_duplicate_exception: str = param.Boolean(
        False, doc="Use this while debugging if filename generation is unique"
    )
    bench_name: str = param.String(
        None, doc="The name of the benchmark and the name of the save folder"
    )
    description: str = param.String(
        None,
        doc="A place to store a longer description of the function of the benchmark",
    )
    post_description: str = param.String(None, doc="A place to comment on the output of the graphs")

    has_results: bool = param.Boolean(
        False,
        doc="If this config has results, true, otherwise used to store titles and other bench metadata",
    )

    pass_repeat: bool = param.Boolean(
        False,
        doc="By default do not pass the kwarg 'repeat' to the benchmark function.  Set to true if you want the benchmark function to be passed the repeat number",
    )

    tag: str = param.String(
        "",
        doc="Use tags to group different benchmarks together. By default benchmarks are considered distinct from each other and are identified by the hash of their name and inputs, constants and results and tag, but you can optionally change the hash value to only depend on the tag.  This way you can have multiple unrelated benchmarks share values with each other based only on the tag value.",
    )

    hash_value: str = param.String(
        "",
        doc="store the hash value of the config to avoid having to hash multiple times",
    )

    plot_callbacks = param.List(
        None,
        doc="A callable that takes a BenchResult and returns panel representation of the results",
    )

    def __init__(self, **params):
        super().__init__(**params)
        self.plot_lib = None
        self.hmap_kdims = None
        self.iv_repeat = None

    def hash_persistent(self, include_repeats) -> str:
        """override the default hash function because the default hash function does not return the same value for the same inputs.  It references internal variables that are unique per instance of BenchCfg

        Args:
            include_repeats (bool) : by default include repeats as part of the hash except with using the sample cache
        """

        if include_repeats:
            # needed so that the historical xarray arrays are the same size
            repeats_hash = hash_sha1(self.repeats)
        else:
            repeats_hash = 0

        hash_val = hash_sha1(
            (
                hash_sha1(str(self.bench_name)),
                hash_sha1(str(self.title)),
                hash_sha1(self.over_time),
                repeats_hash,
                hash_sha1(self.tag),
            )
        )
        all_vars = self.input_vars + self.result_vars
        for v in all_vars:
            hash_val = hash_sha1((hash_val, v.hash_persistent()))

        for v in self.const_vars:
            hash_val = hash_sha1((v[0].hash_persistent(), hash_sha1(v[1])))

        return hash_val

    def inputs_as_str(self) -> List[str]:
        return [i.name for i in self.input_vars]

    def to_latex(self):
        return to_latex(self)

    def describe_sweep(self, width: int = 800, accordion=True) -> pn.pane.Markdown | pn.Column:
        """Produce a markdown summary of the sweep settings"""

        latex = self.to_latex()
        desc = pn.pane.Markdown(self.describe_benchmark(), width=width)
        if accordion:
            desc = pn.Accordion(("Expand Full Data Collection Parameters", desc))

        sentence = self.sweep_sentence()
        if latex is not None:
            return pn.Column(sentence, latex, desc)
        return pn.Column(sentence, latex, desc)

    def sweep_sentence(self):
        inputs = " by ".join([iv.name for iv in self.all_vars])

        all_vars_lens = [len(iv.values()) for iv in reversed(self.all_vars)]
        if len(all_vars_lens) == 1:
            all_vars_lens.append(1)
        result_sizes = "x".join([str(iv) for iv in all_vars_lens])
        results = ", ".join([rv.name for rv in self.result_vars])

        return f"Sweeping {inputs} to generate a {result_sizes} result dataframe containing {results}. "

    def describe_benchmark(self) -> str:
        """Generate a string summary of the inputs and results from a BenchCfg

        Returns:
            str: summary of BenchCfg
        """
        benchmark_sampling_str = ["```text"]
        benchmark_sampling_str.append("")

        benchmark_sampling_str.append("Input Variables:")
        for iv in self.input_vars:
            benchmark_sampling_str.extend(describe_variable(iv, True))

        if self.const_vars and (self.summarise_constant_inputs):
            benchmark_sampling_str.append("\nConstants:")
            for cv in self.const_vars:
                benchmark_sampling_str.extend(describe_variable(cv[0], False, cv[1]))

        benchmark_sampling_str.append("\nResult Variables:")
        for rv in self.result_vars:
            benchmark_sampling_str.extend(describe_variable(rv, False))

        benchmark_sampling_str.append("\nMeta Variables:")
        benchmark_sampling_str.append(f"    run date: {self.run_date}")
        if self.run_tag:
            benchmark_sampling_str.append(f"    run tag: {self.run_tag}")
        if self.level is not None:
            benchmark_sampling_str.append(f"    bench level: {self.level}")
        benchmark_sampling_str.append(f"    cache_results: {self.cache_results}")
        benchmark_sampling_str.append(f"    cache_samples {self.cache_samples}")
        benchmark_sampling_str.append(f"    only_hash_tag: {self.only_hash_tag}")
        benchmark_sampling_str.append(f"    executor: {self.executor}")

        for mv in self.meta_vars:
            benchmark_sampling_str.extend(describe_variable(mv, True))

        benchmark_sampling_str.append("```")

        benchmark_sampling_str = "\n".join(benchmark_sampling_str)
        return benchmark_sampling_str

    def to_title(self, panel_name: str = None) -> pn.pane.Markdown:
        if panel_name is None:
            panel_name = self.title
        return pn.pane.Markdown(f"# {self.title}", name=panel_name)

    def to_description(self, width: int = 800) -> pn.pane.Markdown:
        return pn.pane.Markdown(f"{self.description}", width=width)

    def to_post_description(self, width: int = 800) -> pn.pane.Markdown:
        return pn.pane.Markdown(f"{self.post_description}", width=width)

    def to_sweep_summary(
        self,
        name=None,
        description=True,
        describe_sweep=True,
        results_suffix=True,
        title: bool = True,
    ) -> pn.pane.Markdown:
        """Produce panel output summarising the title, description and sweep setting"""
        if name is None:
            if title:
                name = self.title
            else:
                name = "Data Collection Parameters"
        col = pn.Column(name=name)
        if title:
            col.append(self.to_title())
        if self.description is not None and description:
            col.append(self.to_description())
        if describe_sweep:
            col.append(self.describe_sweep())
        if results_suffix:
            col.append(pn.pane.Markdown("## Results:"))
        return col

    def optuna_targets(self, as_var=False) -> List[str]:
        targets = []
        for rv in self.result_vars:
            if hasattr(rv, "direction") and rv.direction != OptDir.none:
                if as_var:
                    targets.append(rv)
                else:
                    targets.append(rv.name)
        return targets


class DimsCfg:
    """A class to store data about the sampling and result dimensions"""

    def __init__(self, bench_cfg: BenchCfg) -> None:
        self.dims_name = [i.name for i in bench_cfg.all_vars]

        self.dim_ranges = []
        self.dim_ranges = [i.values() for i in bench_cfg.all_vars]
        self.dims_size = [len(p) for p in self.dim_ranges]
        self.dim_ranges_index = [list(range(i)) for i in self.dims_size]
        self.dim_ranges_str = [f"{s}\n" for s in self.dim_ranges]
        self.coords = dict(zip(self.dims_name, self.dim_ranges))

        logging.debug(f"dims_name: {self.dims_name}")
        logging.debug(f"dim_ranges {self.dim_ranges_str}")
        logging.debug(f"dim_ranges_index {self.dim_ranges_index}")
        logging.debug(f"coords: {self.coords}")
