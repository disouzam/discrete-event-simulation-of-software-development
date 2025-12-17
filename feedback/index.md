# Feedback

-   Because programmers don't always get it right the first time

## Adding Testers

-   Parameter sweeping once again

```{.python data-file=simple_testing.py}
PARAMS = {
    "n_programmer": (2, 3, 4),
    "n_tester": (2, 3, 4),
    "p_rework": (0.2, 0.4, 0.6, 0.8),
    …as before…
}

def main():
    random.seed(PARAMS["seed"])
    result = []
    combinations = product(PARAMS["n_programmer"], PARAMS["n_tester"], PARAMS["p_rework"])
    for (n_programmer, n_tester, p_rework) in combinations:
        sweep = {"n_programmer": n_programmer, "n_tester": n_tester, "p_rework": p_rework}
        params = {**PARAMS, **sweep}
        sim = Simulation(params)
        sim.run()
        result.append({
            "params": params,
            "lengths": sim.lengths,
            "jobs": [job.as_json() for job in Job._all],
        })
    json.dump(result, sys.stdout, indent=2)
```

-   Two queues

```{.python data-file=simple_testing.py}
class Simulation:
    def __init__(self, params):
        self.params = params
        self.env = Environment()
        self.prog_queue = Store(self.env)
        self.test_queue = Store(self.env)
        self.lengths = []
```

-   Programmers get from one queue and add to another

```{.python data-file=simple_testing.py}
def programmer(sim, worker_id):
    while True:
        job = yield sim.prog_queue.get()
        start = sim.env.now
        yield sim.env.timeout(sim.rand_dev())
        job.n_prog += 1
        job.t_prog += sim.env.now - start
        yield sim.test_queue.put(job)
```

-   Testers get from the second queue and either recirculate the job or mark it as done

```{.python data-file=simple_testing.py}
def tester(sim, tester_id):
    while True:
        job = yield sim.test_queue.get()
        start = sim.env.now
        yield sim.env.timeout(sim.rand_dev())
        job.n_test += 1
        job.t_test += sim.env.now - start
        if sim.rand_rework():
            yield sim.prog_queue.put(job)
        else:
            job.done = True
```

-   Queue lengths

<div class="center">
  <img src="analyze_simple_testing_queues_1000.svg" alt="queue lengths">
</div>

-   Times for jobs that were started

</div>
  <img src="analyze_simple_testing_times_1000.svg" alt="Programming and testing times">
</div>

-   Gosh, this is hard to understand…
