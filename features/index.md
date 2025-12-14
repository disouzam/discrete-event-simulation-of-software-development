# More Features

-   Now that we have a useful simulation, let's start seeing if we can fix things

## Strict Priorities

-   Introduce job priorities
    -   Lower number is higher priority
-   Values are probabilities of choosing priorities
    -   20% priority 0, 80% priority 1

```{.python data-file=strict_priorities.py}
PARAMS = {
    …other parameters…
    "p_priority": (0.2, 0.8),
}

class Simulation:
    …other methods…
    def rand_priority(self):
        pri = self.params["p_priority"]
        return random.choices(list(range(len(pri))), pri, k=1)[0]
```

-   Use a `PriorityStore` instead of a plain `Store`
    -   Keeps items sorted according to `<`
-   So add `__lt__` to `Job`
    -   If priorities are the same, sort by oldest first

```{.python data-file=strict_priorities.py}
class Simulation:
    def __init__(self, params):
        …as before…
        self.queue = PriorityStore(self.env)

class Job:
    …as before…
    def __lt__(self, other):
        if self.priority == other.priority:
            return self.t_create < other.t_create
        return self.priority < other.priority
```

-   This implementation means that low-priority jobs are only done
    when there aren't any high-priority jobs in queue
-   Monitoring code keeps track of number of jobs in queue at each priority level

```{.python data-file=strict_priorities.py}
    def monitor(self):
        while True:
            lengths = dict((i, 0) for i in range(len(self.params["p_priority"])))
            for job in self.queue.items:
                lengths[job.priority] += 1
            for pri, num in lengths.items():
                self.queue_lengths.append(
                    {"time": rv(self.env.now), "priority": pri, "length": num}
                )
            yield self.env.timeout(self.params["t_monitor"])
```

<div class="center">
  <img src="strict_priorities.svg" alt="queue length with strict priorities">
</div>

-   High-priority jobs are getting done
-   Backlog of low-priority job is steadily increasing

## Weighted Priorities

-   More realistic scenario is that programmers are more likely to do high-priority work,
    but will occasionally do low-priority work instead
-   So choose a job at random, with probability weighted by inverse priority
    -   Priority 0 has weight 2, priority 1 has weight 1

```{.python data-file=strict_priorities.py}
class Job:
    def __init__(self, sim):
        …as before…
        self.weight = len(sim.params["p_priority"]) - self.priority

class WeightedStore(Store):
    def __init__(self, env):
        super().__init__(env)

    def _do_get(self, event):
        # Block if nothing available.
        if not self.items:
            return

        # Choose and return.
        item = random.choices(self.items, weights=[job.weight for job in self.items], k=1)[0]
        self.items.remove(item)
        event.succeed(item)
```

-   Note that the `WeightedStore` defined above doesn't care about task age
    -   Add that in the exercises
-   Doesn't seem to make much difference over 200 ticks

<div class="center">
  <img src="weighted_priorities_200.svg" alt="queue length with weighted priorities">
</div>

-   Run the simulation longer
    and it looks like the backlog of high-priority jobs is steadily increasing
-   I.e., we've made things worse

<div class="center">
  <img src="weighted_priorities_1000.svg" alt="queue length with weighted priorities and long time">
</div>

## Periodic Triage

-   What if we [triage](g:triage) periodically?
    -   Set a target of (for example) no more than 100 low-priority jobs in the backlog
    -   Go through and clear jobs out periodically (e.g., every 50 ticks)
-   Do this probabilistically
    -   If the number of jobs *N* is greater than the desired number *T*,
        discard jobs with probability *1 - T/N*

```{.python data-file=weighted_triage.py}
PARAMS = {
    …as before…
    "n_triage": 100,
    "t_triage": 50,
}

class Triage:
    def run(self):
        while True:
            yield self.sim.env.timeout(self.sim.params["t_triage"])
            p_triage = self.calculate_prob()
            if p_triage is not None:
                self.discard_items(p_triage)

    …other methods to calculate probability and discard jobs…
```

-   Predictable impact on backlog of low-priority jobs
-   But stabilizes backlog of high-priority jobs
    -   Remember, still using weighted selection
-   This is plausible, but several other outcomes would also have been plausible
    -   Which is why we do simulation

<div class="center">
  <img src="weighted_triage_1000.svg" alt="queue length with weighted priorities and regular triage">
</div>

-   What happens to completion rates?

<div class="center">
  <img src="weighted_triage_completion_1001.svg" alt="completion rates with weighted priorites and regular triage">
</div>

-   Completing more high-priority jobs than low-priority ones
-   Number of low-priority jobs that are discarded slowly overtakes the number completed
