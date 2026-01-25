import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    import time
    import math
    import csv
    from itertools import count
    from simpy import Environment, Store
    import colored as cd
    import numpy as np

    rand = np.random.default_rng(seed=2026)
    WHITE_ON_BLACK = f"{cd.fore_rgb(255, 255, 255)}{cd.back_rgb(0, 0, 0)}"
    WHITE_ON_RED = f"{cd.fore_rgb(255, 255, 255)}{cd.back_rgb(255, 0, 0)}"

    def calculateLight(colorItem: int):
        c = colorItem / 255

        if c < 0.03928:
            c /= 12.92
        else:
            c = math.pow((c + 0.055) / 1.055, 2.4)

        return c

    def calculateLuminosity(r: int, g: int, b: int):
        return (
            0.2126 * calculateLight(r)
            + 0.7152 * calculateLight(g)
            + 0.0722 * calculateLight(b)
        )

    def getContrastColor(r: int, g: int, b: int):
        LUMINOSITY_LIMIT = 0.579  # This is the Contrast Threshold, the higher it is, the more likely text will be white
        if calculateLuminosity(r, g, b) > LUMINOSITY_LIMIT:
            return cd.back_rgb(0, 0, 0)

        return cd.back_rgb(230, 230, 230)

    class Job:
        _next_id = count(start=0)

        def __init__(self, job_duration):
            self.id = next(Job._next_id)
            self.duration = job_duration
            red = rand.uniform(0, 255)
            green = rand.uniform(0, 255)
            blue = rand.uniform(0, 255)
            self.fore = cd.fore_rgb(red, green, blue)
            self.back = getContrastColor(red, green, blue)

        def __str__(self):
            return (
                f"job {self.fore}{self.back} {cd.Style.bold}{self.id} {cd.Style.reset}"
            )

        def __repr__(self):
            return self.__str__()

    def manager(env, queue, time_between_new_tasks, job_duration, tracing=True):
        while True:
            job = Job(job_duration)

            if tracing:
                print(
                    f"\nQueue items before manager creates one more job: {queue.items}"
                )
                print(
                    f"At {WHITE_ON_BLACK} {env.now:>2}  {cd.Style.reset}, manager creates {job}"
                )

            yield queue.put(job)
            yield env.timeout(time_between_new_tasks)

    def coder(env, queue, tracing=True):
        while True:
            wait_starts = env.now

            if tracing:
                print(f"\nQueue items before coder takes one job: {queue.items}")

            job = yield queue.get()

            get_job_at = env.now

            if tracing:
                if get_job_at - wait_starts > 0:
                    print(
                        f"{WHITE_ON_RED}At {WHITE_ON_BLACK} {wait_starts:>2}  {WHITE_ON_RED}, coder waits{cd.Style.reset}"
                    )
                    print(
                        f"At {WHITE_ON_BLACK} {get_job_at:>2}  {cd.Style.reset}, coder gets {job}"
                    )
                else:
                    print(
                        f"At {WHITE_ON_BLACK} {get_job_at:>2}  {cd.Style.reset}, coder gets {job} without waiting"
                    )

            yield env.timeout(job.duration)

            completed_job_at = env.now

            if tracing:
                print(
                    f"At {WHITE_ON_BLACK} {completed_job_at:>2}  {cd.Style.reset}, coder completes {job}"
                )

    def run_simulation(
        time_between_new_tasks, job_duration, simulation_time, tracing=True
    ):
        fieldnames = ["time", "queue_length"]

        env = Environment()
        queue = Store(env)
        env.process(manager(env, queue, time_between_new_tasks, job_duration, tracing))
        env.process(coder(env, queue, tracing))

        until = simulation_time
        time_list = []
        queue_length_list = []

        while env.peek() < until:
            if env.now not in time_list:
                time_list.append(env.now)
                queue_length_list.append(queue.items)

                if tracing:
                    print(
                        f"\n{cd.Fore.yellow}{cd.Back.black}{cd.Style.bold}Environment time: {env.now} - Queue items: {cd.Style.reset}{queue.items}"
                    )

            env.step()

        print(
            f"\n\n{cd.Fore.blue}{cd.Back.green}{cd.Style.bold}Simulation completed at: {simulation_time} - Queue items: {cd.Style.reset}{queue.items}"
        )

    _T_CREATE = 2
    _T_JOB = 8
    _T_SIM = 16

    run_simulation(_T_CREATE, _T_JOB, _T_SIM, tracing=True)
    return


if __name__ == "__main__":
    app.run()
