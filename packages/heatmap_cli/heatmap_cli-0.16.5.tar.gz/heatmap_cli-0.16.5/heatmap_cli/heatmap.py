# Copyright (C) 2023,2024,2025 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Main logic to generate heatmap."""

import argparse
import calendar
import datetime
import logging
import multiprocessing
import os
import shutil
import subprocess
import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# generating matplotlib graphs without a x-server
# see http://stackoverflow.com/a/4935945
mpl.use("agg")

# Suppress logging from matplotlib in debug mode
logging.getLogger("matplotlib").propagate = False
logger = multiprocessing.get_logger()


def run(config: argparse.Namespace) -> None:
    """Run the main flow.

    Args:
        config (argparse.Namespace): Config from command line arguments

    Returns:
        None
    """
    logger.debug(config)
    logger.debug("number of cpu: %d", multiprocessing.cpu_count())

    _refresh_output_dir(config)

    dataframe = _massage_data(config)
    args = [
        (*seq_cmap, config, dataframe)
        for seq_cmap in enumerate(config.cmap, 1)
    ]

    # fork, instead of spawn process (child) inherit parent logger config
    # see https://stackoverflow.com/q/14643568
    with multiprocessing.get_context("fork").Pool() as pool:
        pool.starmap(_generate_heatmap, args)


def _massage_data(config: argparse.Namespace) -> pd.core.frame.DataFrame:
    """Filter the data from CSV file.

    Args:
        config (argparse.Namespace): Config from command line arguments

    Returns:
        dataframe (pd.core.frameDataFrame): Filtered Dataframe
    """
    dataframe = pd.read_csv(
        config.input_filename, header=None, names=["date", "count"]
    )
    dataframe["date"] = pd.to_datetime(dataframe["date"])
    dataframe["weekday"] = dataframe["date"].dt.weekday + 1
    dataframe["year"] = dataframe["date"].dt.isocalendar().year
    dataframe["week"] = (
        dataframe["date"].dt.isocalendar().week.astype(str).str.zfill(2)
    )
    dataframe["count"] = dataframe["count"].apply(_truncate_rounded_count)

    if config.end_date:
        steps = dataframe[
            (dataframe["year"] == config.year)
            & (dataframe["date"] <= config.end_date)
        ]
    elif config.week >= 52:
        steps = dataframe[dataframe["date"].dt.year == config.year]
    else:
        steps = dataframe[
            (dataframe["year"] == config.year)
            & (dataframe["week"] <= str(config.week).zfill(2))
        ]

    duplicate_dates = dataframe[dataframe["date"].duplicated(keep=False)]
    if len(duplicate_dates):
        raise ValueError(f"duplicate dates: {duplicate_dates} found!")

    if steps.empty:
        raise ValueError("no data extracted from csv file!")

    logger.debug(
        "last date: %s of current week: %s",
        max(steps["date"]).date(),
        config.week,
    )

    pre_missing_steps = pd.DataFrame(
        {
            "date": pd.date_range(
                start=f"{config.year}-01-01",
                end=min(steps["date"]).date() - datetime.timedelta(days=1),
            )
        }
    )
    pre_missing_steps["weekday"] = pre_missing_steps["date"].dt.weekday + 1
    pre_missing_steps["week"] = (
        pre_missing_steps["date"]
        .dt.isocalendar()
        .week.astype(str)
        .str.zfill(2)
    )
    pre_missing_steps["count"] = 0

    post_missing_steps = pd.DataFrame(
        {
            "date": pd.date_range(
                start=max(steps["date"]).date() + datetime.timedelta(days=1),
                end=f"{config.year}-12-31",
            )
        }
    )
    post_missing_steps["weekday"] = post_missing_steps["date"].dt.weekday + 1
    post_missing_steps["week"] = (
        post_missing_steps["date"]
        .dt.isocalendar()
        .week.astype(str)
        .str.zfill(2)
    )
    post_missing_steps["count"] = 0

    if not pre_missing_steps.empty:
        steps = pd.concat([pre_missing_steps, steps], ignore_index=True)

    if not post_missing_steps.empty:
        steps = pd.concat([steps, post_missing_steps], ignore_index=True)

    steps.reset_index(drop=True, inplace=True)

    year_dataframe = steps.pivot_table(
        values="count", index=["weekday"], columns=["week"], fill_value=0
    )
    return year_dataframe


def _truncate_rounded_count(count):
    return int(round(count, -2) / 100)


def _generate_heatmap(
    seq: int,
    cmap: str,
    config: argparse.Namespace,
    dataframe: pd.core.frame.DataFrame,
) -> None:
    """Generate a heatmap.

    Args:
        config (argparse.Namespace): Config from command line arguments
        dataframe (pd.core.frameDataFrame): Dataframe with data loaded from CSV
        file

    Returns:
        None
    """
    _fig, axis = plt.subplots(figsize=(8, 5))
    axis.tick_params(axis="both", which="major", labelsize=9)
    axis.tick_params(axis="both", which="minor", labelsize=9)

    cbar_options = {
        "orientation": "horizontal",
        "label": (
            "generated by: pypi.org/project/heatmap_cli, " f"colormap: {cmap}"
        ),
        "pad": 0.10,
        "aspect": 60,
        "extend": "max",
    }
    options = {
        "ax": axis,
        "fmt": "",
        "square": True,
        "cmap": cmap,
        "cbar": config.cbar,
        "cbar_kws": cbar_options,
    }

    if config.cmap_min:
        options.update({"vmin": config.cmap_min})

    if config.cmap_max:
        options.update({"vmax": config.cmap_max})

    if config.annotate:
        cbar_options.update(
            {
                "label": f"{cbar_options['label']}, count: by hundred",
            }
        )
        options.update(
            {
                "annot": True,
                "annot_kws": {"fontsize": 8},
                "linewidth": 0,
            }
        )

    # convert value larger than 100 to >1
    res = sns.heatmap(dataframe, **options)
    for text in res.texts:
        count = int(float(text.get_text()))
        if count >= 100:
            text.set_text(">" + str(count)[0])
        else:
            text.set_text(count)

    img_filename = Path(
        os.getcwd(),
        config.output_dir,
        _generate_filename(config, seq, cmap),
    )
    img_filename.parent.mkdir(parents=True, exist_ok=True)

    axis.set_title(_generate_title(config), fontsize=11, loc="left")
    axis.set_title("kianmeng.org", fontsize=11, loc="right")
    plt.tight_layout()
    plt.savefig(
        img_filename,
        bbox_inches="tight",
        transparent=False,
        dpi=76,
        format=config.format,
    )
    logger.info("generate heatmap: %s", img_filename)

    if config.open:
        _open_heatmap(img_filename)


def _open_heatmap(filename):
    """Open generated heatmap using default program."""
    if sys.platform == "linux":
        subprocess.call(["xdg-open", filename])
    elif sys.platform == "darwin":
        subprocess.call(["open", filename])
    elif sys.platform == "win32":
        os.startfile(filename)
    else:
        logger.warning("unsupported platform for opening files: %s", sys.platform)

    logger.info("open heatmap: %s using default program.", filename.resolve())


def _generate_filename(config: argparse.Namespace, seq: int, cmap: str) -> str:
    """Generate a image filename.

    Args:
        config (argparse.Namespace): Config from command line arguments

    Returns:
        str: A generated file name for the PNG image
    """
    annotated = ""
    if config.annotate:
        annotated = "_annotated"

    filename = (
        f"{annotated}_heatmap_of_total_daily_walked_steps_count"
        f".{config.format}"
    )
    if config.week >= 52:
        return f"{seq:03}_{config.year}_{cmap}" + filename

    return f"{seq:03}_{config.year}_week_{config.week}_{cmap}" + filename


def _generate_title(config: argparse.Namespace) -> str:
    """Run the main flow.

    Args:
        config (argparse.Namespace): Config from command line arguments

    Returns:
        str: A generated title for the heatmap title
    """
    if not config.title:
        title = f"Year {config.year}: Total Daily Walking Steps"
        last_week = 53 if calendar.isleap(config.year) else 52
        if config.week != last_week:
            title += f" Through Week {config.week:02d}"
    else:
        title = config.title

    logger.debug(title)
    return title


def _refresh_output_dir(config: argparse.Namespace) -> None:
    """Delete, and recreate the output folder.

    Args:
        config (argparse.Namespace): Config from command line arguments

    Returns:
        None
    """
    output_dir = _get_output_dir(config)

    if not config.purge or not output_dir.exists():
        return

    if config.yes:
        _recrete_output_dir(output_dir)
        return

    prompt = (
        "Are you sure to purge output folder: "
        f"{output_dir.absolute()}? [y/N] "
    )
    answer = input(prompt)
    if answer.lower() == "y":
        _recrete_output_dir(output_dir)


def _recrete_output_dir(output_dir: Path) -> None:
    """Recreate the output folder.

    Args:
        output_dir (str): Output directory path

    Returns:
        None
    """
    logger.info("purge output folder: %s", output_dir.absolute())
    shutil.rmtree(output_dir)
    logger.info("create output folder: %s", output_dir.absolute())
    output_dir.mkdir(parents=True, exist_ok=True)


def _get_output_dir(config: argparse.Namespace) -> Path:
    """Get the current working directory.

    Args:
        config (argparse.Namespace): Config from command line arguments

    Returns:
        str
    """
    output_dir = Path(config.output_dir)
    if output_dir.is_absolute():
        return output_dir

    return Path(os.getcwd(), config.output_dir)
