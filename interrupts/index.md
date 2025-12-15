# Interruptions

## A Simple Model

-   Jobs don't have priorities
-   The manager interrupts
-   Any work done on the current job is lost
    -   We'll fix this later
-   Parameters

```{.python data-file=panic_and_discard.py}
PARAMS = {
    "n_programmer": 1,
    "seed": 12345,
    "t_develop_mu": 0.5,
    "t_develop_sigma": 0.6,
    "t_interrupt": 5.0,       # new
    "t_job_arrival": 1.0,
    "t_monitor": 5,
    "t_sim": 20,
}
```

-   Simulation
    -   Go back to a regular `Store` (first in, first out, no priority, no triage)
    -   Keep a list of programmers' processes
    -   Rename `manager` to `creator` and add `interruptor`

```{.python data-file=panic_and_discard.py}
class Simulation:
    def __init__(self, params):
        self.params = params
        self.env = Environment()
        self.queue = Store(self.env)
        self.queue_length = []
        self.programmers = []

    def run(self):
        Job.clear()
        self.env.process(self.monitor())
        self.env.process(creator(self))
        self.env.process(interruptor(self))
        self.programmers = [
            self.env.process(programmer(self, i)) for i in range(self.params["n_programmer"])
        ]
        self.env.run(until=self.params["t_sim"])
```

-   `Job` keeps track of whether it was discarded or not

```{.python data-file=panic_and_discard.py}
    def __init__(self, sim):
        …as before…
        self.discarded = False
```

-   `interruptor` waits a random interval, chooses a programmer at random, and interrupts her
    -   Need the generator object
    -   Call its `interrupt` method to send a `simpy.Interrupt` exception into the generator

```{.python data-file=panic_and_discard.py}
def interruptor(sim):
    while True:
        yield sim.env.timeout(sim.rand_interrupt())
        programmer = random.choice(sim.programmers)
        programmer.interrupt()
```

-   `programmer` needs to handle these interruption exceptions
    -   Throw away current job and start again

```{.python data-file=panic_and_discard.py}
def programmer(sim, worker_id):
    while True:
        try:
            job = yield sim.queue.get()
            job.t_start = sim.env.now
            job.worker_id = worker_id
            yield sim.env.timeout(job.t_develop)
            job.t_end = sim.env.now
        except Interrupt:
            job.t_end = sim.env.now
            job.discarded = True
```

-   Works fine until we add one line to clear the job each time around the loop

```{.python data-file=panic_and_discard_reset.py}
def programmer(sim, worker_id):
    while True:
        job = None
        try:
            job = yield sim.queue.get()
            job.t_start = sim.env.now
            job.worker_id = worker_id
            yield sim.env.timeout(job.t_develop)
            job.t_end = sim.env.now
        except Interrupt:
            job.t_end = sim.env.now
            job.discarded = True
```

-   Problem is that the interruption can occur inside `sim.queue.get()`
-   Only update the job if we got one

```{.python data-file=panic_and_discard_corrected.py}
def programmer(sim, worker_id):
    while True:
        job = None
        try:
            job = yield sim.queue.get()
            job.t_start = sim.env.now
            job.worker_id = worker_id
            yield sim.env.timeout(job.t_develop)
            job.t_end = sim.env.now
        except Interrupt:
            if job is not None:
                job.t_end = sim.env.now
                job.discarded = True
```
