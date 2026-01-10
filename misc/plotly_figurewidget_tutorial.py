import marimo

__generated_with = "0.18.4"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    import plotly.graph_objects as go

    f = go.FigureWidget()
    f.add_scatter(y=[2, 1, 4, 3]);
    f.add_bar(y=[1, 4, 3, 2]);
    f.layout.title = 'Hello FigureWidget'

    # update scatter data
    scatter = f.data[0]
    scatter.y = [3, 1, 4, 3]

    # update bar data
    bar = f.data[1]
    bar.y = [5, 3, 2, 8]

    f.layout.title.text = 'This is a new title'
    f
    return


if __name__ == "__main__":
    app.run()
