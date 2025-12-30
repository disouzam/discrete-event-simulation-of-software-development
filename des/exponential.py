"""Plot the exponential distribution."""

import numpy as np
import plotly.express as px
import polars as pl
from scipy.stats import expon
import sys

lam = 0.5
if len(sys.argv) > 2:
    lam = float(sys.argv[2])

scale = 1 / lam

dist = expon(scale=scale)
x = np.linspace(dist.ppf(0.001), dist.ppf(0.99), 500)
y = dist.pdf(x)

df = pl.DataFrame({"x": x, "y": y})
fig = px.line(df, x="x", y="y")
fig.update_layout(margin={"l": 0, "r": 0, "t": 0, "b": 0})

if sys.argv[1] == "--":
    fig.show()
else:
    fig.write_image(sys.argv[1])
