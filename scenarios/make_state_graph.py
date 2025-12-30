"""Convert sequence of job events into state transition graph."""

from graphviz import Digraph
import json
import polars as pl
import sys


def main():
    data = json.load(sys.stdin)
    jobs = pl.from_dicts(data[0]["events"])

    transitions = jobs.with_columns(
        pl.col("state").shift(-1).over("id").sort_by("time").alias("next_state")
    ).filter(pl.col("next_state").is_not_null())

    probs = (
        transitions.group_by(["state", "next_state"])
        .len()
        .rename({"len": "count"})
        .with_columns(pl.col("count").sum().over("state").alias("total_from_state"))
        .with_columns(
            (pl.col("count") / pl.col("total_from_state")).alias("probability")
        )
        .select("state", "next_state", "probability")
        .sort("next_state", "state")
    )

    dot = Digraph(
        name="StateTransitions",
        graph_attr={"rankdir": "LR", "size": "6,6"},
        node_attr={"shape": "box"},
    )

    for row in probs.iter_rows(named=True):
        src = row["state"]
        dst = row["next_state"]
        prob = row["probability"]
        dot.node(src)
        dot.node(dst)
        dot.edge(src, dst, label=f"{prob:.2f}", penwidth=str(1 + 2 * prob))

    print(dot)


if __name__ == "__main__":
    main()
