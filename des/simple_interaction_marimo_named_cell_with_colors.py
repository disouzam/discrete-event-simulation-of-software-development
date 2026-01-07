import marimo

__generated_with = "0.18.4"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Simple interaction between manager and coder
    """)
    return


@app.cell
def imports():
    # Necessary imports
    from itertools import count
    from simpy import Environment, Store
    import colored as cd
    return Environment, Store, cd, count


@app.cell
def _(cd):
    WHITE_ON_BLACK = f"{cd.fore_rgb(255,255,255)}{cd.back_rgb(0,0,0)}"
    return (WHITE_ON_BLACK,)


@app.cell
def sim_constants():
    # Simulation constants
    T_CREATE = 6
    T_JOB = 8
    T_SIM = 20
    return T_CREATE, T_JOB, T_SIM


@app.cell
def job_class(T_JOB, count):
    class Job:
        _next_id = count()

        def __init__(self):
            self.id = next(Job._next_id)
            self.duration = T_JOB

        def __str__(self):
            return f"job {self.id}"
    return (Job,)


@app.cell
def manager_process(Job, T_CREATE, WHITE_ON_BLACK, cd):
    def manager(env, queue):
        while True:
            job = Job()
            print(f"At {WHITE_ON_BLACK} {env.now:>2} {cd.Style.reset}, manager creates {job}")
            yield queue.put(job)
            yield env.timeout(T_CREATE)
    return (manager,)


@app.cell
def _(WHITE_ON_BLACK, cd):
    def coder(env, queue):
        while True:
            wait_starts = env.now
            job = yield queue.get()

            get_job_at = env.now

            if get_job_at - wait_starts > 0:
                print(f"At {WHITE_ON_BLACK} {wait_starts:>2} {cd.Style.reset}, coder waits")
                print(f"At {WHITE_ON_BLACK} {get_job_at:>2} {cd.Style.reset}, coder gets job {job}")
            else:
                print(f"At {WHITE_ON_BLACK} {get_job_at:>2} {cd.Style.reset}, coder gets job {job} without waiting")

            yield env.timeout(job.duration)

            completed_job_at = env.now
            print(f"At {WHITE_ON_BLACK} {completed_job_at:>2} {cd.Style.reset}, code completes job {job}")
    return (coder,)


@app.cell
def entry_point(Environment, Store, T_SIM, coder, manager):
    def main():
        env = Environment()
        queue = Store(env)
        env.process(manager(env, queue))
        env.process(coder(env, queue))
        env.run(until=T_SIM)
    return (main,)


@app.cell
def _(main):
    main()
    return


if __name__ == "__main__":
    app.run()
