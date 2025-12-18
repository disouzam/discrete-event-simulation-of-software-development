"""Analyze testing with priority."""

import json
import polars as pl
import plotly.express as px
import sys


def main():
    data = json.load(sys.stdin)
    df = pl.from_dicts(data["jobs"]).sort("t_create")
    unstarted = df \
        .filter(pl.col("n_prog") == 0) \
        .with_columns(pl.lit("unstarted").alias("state")) \
        .with_row_index("num", offset=1)
    in_progress = df \
        .filter(~pl.col("done") & (pl.col("n_prog") > 0)) \
        .with_columns(pl.lit("in_progress").alias("state")) \
        .with_row_index("num", offset=1)
    completed = df \
        .filter(pl.col("done")) \
        .with_columns(pl.lit("completed").alias("state")) \
        .with_row_index("num", offset=1)
    df = pl.concat([unstarted, in_progress, completed])
    fig = px.line(df, x="t_create", y="num", color="state")
    fig.update_layout(margin={"l": 0, "r": 0, "t": 0, "b": 0})
    if len(sys.argv) == 1:
        fig.show()
    else:
        fig.write_image(sys.argv[1])
    

if __name__ == "__main__":
    main()
