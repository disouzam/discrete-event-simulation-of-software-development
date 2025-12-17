"""Analyze parameter sweep of simple testing."""

import json
import polars as pl
import plotly.express as px
import sys


def main():
    data = json.load(sys.stdin)
    frames = [json_to_dataframe(d) for d in data]
    lengths = pl.concat(f["lengths"] for f in frames)
    jobs = pl.concat(f["jobs"] for f in frames)

    fig = px.line(
        lengths,
        x="time", y="length", color="queue_rework",
        facet_row="n_programmer", facet_col="n_tester"
    )
    show(fig, 1)

    jobs = jobs.filter(pl.col("n_prog") > 0)
    fig = px.scatter(
        jobs,
        x="t_prog", y="t_test", color="p_rework",
        facet_row="n_programmer", facet_col="n_tester",
        log_x=True, log_y=True
    )
    show(fig, 2)


def json_to_dataframe(data):
    params = data["params"]
    lengths = add_columns(params, pl.from_dicts(data["lengths"])) \
        .with_columns(
            pl.format("queue={}, p_rework={}", pl.col("queue"), pl.col("p_rework")).alias("queue_rework")
        )
    jobs = add_columns(params, pl.from_dicts(data["jobs"]))
    return {"lengths": lengths, "jobs": jobs}


def add_columns(params, df):
    return df.with_columns(
        pl.lit(params["n_programmer"]).alias("n_programmer"),
        pl.lit(params["n_tester"]).alias("n_tester"),
        pl.lit(params["p_rework"]).alias("p_rework")
    )


def show(fig, which):
    if len(sys.argv) == 1:
        fig.show()
    else:
        fig.write_image(sys.argv[which])

if __name__ == "__main__":
    main()
