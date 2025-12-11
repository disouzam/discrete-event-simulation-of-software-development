## Logging via Instrumentation

-   Use a [context manager](g:context-manager) to create log entries
    -   `__enter__` adds a "start" event
    -   `__exit__` adds an "end" event
-   Work backwards from desired change in `worker`

```{.python data-file=context_manager_log.py}
def worker(env, log):
    while True:
        with LogWork(env, log):
            yield env.timeout(t_work())
        yield env.timeout(T_BREAK)
```

-   Create the `LogWork` class
    -   Don't need to save the instance in a variable

```{.python data-file=context_manager_log.py}
class LogWork:
    def __init__(self, env, log):
        self.env = env
        self.log = log

    def __enter__(self):
        self.log.append({"event": "start", "time": self.env.rnow})

    def __exit__(self, exc_type, exc_value, traceback):
        self.log.append({"event": "end", "time": self.env.rnow})
```

-   Accurate reporting
-   But we have to insert monitoring into our worker
    -   And as it becomes more complex, that's going to be harder to read

## Simulating with Objects

-   Create a class to represe the worker
    -   Its `run` method is a generator
    -   Its constructor creates the process 

```{.python data-file=simulate_with_objects.py}
class Worker:
    def __init__(self, env):
        self.env = env
        self.env.process(self.run())

    def run(self):
        while True:
            print(f"{self.env.rnow} start")
            yield self.env.timeout(t_work())
            print(f"{self.env.rnow} end")
            yield self.env.timeout(T_BREAK)
```

-   Main body just creates the object

```{.python data-file=simulate_with_objects.py}
def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else SEED
    random.seed(seed)
    env = Env()
    worker = Worker(env)
    env.run(until=T_MORNING)
```
```{.python data-file=simulate_with_objects.out}
0 start
26.665 end
36.665 start
47.072 end
57.072 start
100.08 end
110.08 start
132.025 end
142.025 start
166.762 end
176.762 start
194.508 end
204.508 start
237.149 end
```

## Logging via Sampling

-   Define another process that inspects the worker periodically and records its state

```{.python data-file=sampling_log.py}
class Logger:
    def __init__(self, env, worker):
        self.env = env
        self.worker = worker
        self.log = []
        self.env.process(self.run())

    def run(self):
        while True:
            self.log.append({"time": self.env.rnow, "state": self.worker.state})
            yield self.env.timeout(T_LOG)
```

-   Modify the worker to make its state explicit
    -   Initialize in constructor and update in `run`

```{.python data-file=sampling_log.py}
class Worker:
    def __init__(self, env):
        self.env = env
        self.state = "idle"
        self.env.process(self.run())

    def run(self):
        while True:
            self.state = "work"
            yield self.env.timeout(t_work())
            self.state = "idle"
            yield self.env.timeout(T_BREAK)
```

<div class="center">
  <img src="visualize_sampling_log.svg" alt="time-series plot of sampling">
</div>

-   Instrumentation is easier in simple systems
-   Sampling is easier in complex ones
-   [Separation of concerns](g:separation-of-concerns)

## Exercises

1.  Why are the edges in the second plot not quite vertical?
