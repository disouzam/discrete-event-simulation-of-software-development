import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **About this notebook**
    A developer ask for work at regular intervals.

    A Scrum Master answers one single time informing there is available and ready work.

    There is no interaction between them at this moment.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Imports and paramters**
    """)
    return


@app.cell
def _():
    from simpy import Environment

    # Duration of simulation is 30 units of time
    T_SIM = 30

    # Time between coder asks for more available work. 8 units of time
    # if unit of time is hour, it means that coder asks once per day
    T_WAIT = 8
    return Environment, T_SIM, T_WAIT


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Function definitions to represent a coder and a scrum master
    """)
    return


@app.cell
def _(T_WAIT):
    def coder(env):
        """
        A generator that emulates some behavior of a code such as asking for more available work
        """
        while True:
            print(f"{env.now}: Is there any work?")
            yield env.timeout(T_WAIT)
    return (coder,)


@app.function
def scrum_master(env):
    """
    A generator that emulates some behavior of a Scrum Master such as making sure that
    there is available work for the developers
    (here concepts like Definition of Ready - DoR jumps in)
    """
    yield env.timeout(14)
    print(f"{env.now}: There is a new task available for you, developer.")


@app.cell
def _(Environment, coder, mo):
    # Create a SimPy environment
    env = Environment()

    # Create a process where coder is the generator function
    env.process(coder(env))

    with mo.capture_stdout() as output:
        # Create a process where a scrum master is the generator function
        env.process(scrum_master(env))
    return (env,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Run the simulation for the specified duration**
    """)
    return


@app.cell
def _(T_SIM, env):
    env.run(until=T_SIM)
    return


if __name__ == "__main__":
    app.run()
