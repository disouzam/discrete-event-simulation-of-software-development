# Our First Simulations

<p id="terms"></p>

## Our goals

-   Create a SimPy `Environment`
-   Create one or more [generators](g:generator) for it to run
    -   These will almost always need the environment
    -   **Environment works as event loop in Javascript ([Event discrete simulation with SimPy by Stefan Scherfke on EuroPython 2014](https://www.youtube.com/watch?v=Bk91DoAEcjY))**
-   Pass each generator to `env.process(…)`
-   Call `env.run(…)` and specify simulation duration

## A simplified process without interaction

- The process includes only one coder and a scrum master or manager
- Coder asks for work to be done
- Scrum master creates a new task
- There is no interaction between them
    - Task stays unpicked in the backlog

[![Open in molab](https://molab.marimo.io/molab-shield.svg)](https://molab.marimo.io/notebooks/nb_aNfmQJNvbTDdqFHs6t6gSo)
```{.py data-file=ask_for_work.py}
"""
A developer ask for work at regular intervals.
A Scrum Master answers one single time informing there is available and ready work.
There is no interaction between them at this moment.
"""

from simpy import Environment

# Duration of simulation is 30 units of time
T_SIM = 30

# Time between coder asks for more available work. 8 units of time
# if unit of time is hour, it means that coder asks once per day
T_WAIT = 8


def coder(env):
    """
    A generator that emulates some behavior of a code such as asking for more available work
    """
    while True:
        print(f"{env.now}: Is there any work?")
        yield env.timeout(T_WAIT)


def scrum_master(env):
    """
    A generator that emulates some behavior of a Scrum Master such as making sure that
    there is available work for the developers
    (here concepts like Definition of Ready - DoR jumps in)
    """
    yield env.timeout(14)
    print(f"{env.now}: There is a new task available for you, developer.")


if __name__ == "__main__":
    # Create a SimPy environment
    env = Environment()

    # Create a process where coder is the generator function
    env.process(coder(env))

    # Create a process where a scrum master is the generator function
    env.process(scrum_master(env))

    # Run the simulation for the specified duration
    env.run(until=T_SIM)
```

-   Output

```{.txt data-file=ask_for_work.txt}
0: Is there any work?
8: Is there any work?
14: There is a new task available for you, developer.
16: Is there any work?
24: Is there any work?
```

## Interaction

-   Manager creates jobs and puts them in a queue
    -   **Maybe it would be good to be explicit of how jobs are organized (pooled for a sprint in Scrum process or pulled by devs in a continuous queue)**
    -   Jobs arrive at regular intervals
    -   Each job has a duration
    -   **Is there any wish to emulate a planning poker to give estimated duration of jobs?**
    -   Give each job an ID for tracking
-   Coder takes jobs from the queue in order and does them
    -   **How should we handle coder specialization / seniority to decide if a job should be assigned or not to a given coder?**
-   Queue is implemented as a SimPy `Store` with `.put()` and `.get()` methods

<div class="callout" markdown="1">

-   A process (generator) only gives control back to SimPy when it yields
-   So processes must `yield` the results of `queue.put()` and `queue.get()`
    -   Writing `job = queue.get()` rather than `job = yield queue.get()` is a common mistake

</div>

-   Parameters

```{.py data-file=simple_interaction.py}
T_CREATE = 6
T_JOB = 8
T_SIM = 20
```

-   `Job` class

```{.py data-file=simple_interaction.py}
from itertools import count

class Job:
    _next_id = count()

    def __init__(self):
        self.id = next(Job._next_id)
        self.duration = T_JOB

    def __str__(self):
        return f"job-{self.id}"
```

-   `manager` process

```{.py data-file=simple_interaction.py}
def manager(env, queue):
    while True:
        job = Job()
        print(f"manager creates {job} at {env.now}")
        yield queue.put(job)
        yield env.timeout(T_CREATE)
```

-   `coder` process

```{.py data-file=simple_interaction.py}
def coder(env, queue):
    while True:
        print(f"coder waits at {env.now}")
        job = yield queue.get()
        print(f"coder gets {job} at {env.now}")
        yield env.timeout(job.duration)
        print(f"coder completes {job} at {env.now}")
```

-   Set up and run

[![Open in molab](https://molab.marimo.io/molab-shield.svg)](https://molab.marimo.io/notebooks/nb_BGq8nGuCZBEjgiP3G5MVes)

Or this version with named cells:

[![Open in molab](https://molab.marimo.io/molab-shield.svg)](https://molab.marimo.io/notebooks/nb_cn8JWkbuZHxBFd8primLhG)

```{.py data-file=simple_interaction.py}
if __name__ == "__main__":
    env = Environment()
    queue = Store(env)
    env.process(manager(env, queue))
    env.process(coder(env, queue))
    env.run(until=T_SIM)
```

-   Output

```{.txt data-file=simple_interaction.txt}
manager creates job-0 at 0
coder waits at 0
coder gets job-0 at 0
manager creates job-1 at 6
coder completes job-0 at 8
coder waits at 8
coder gets job-1 at 8
manager creates job-2 at 12
coder completes job-1 at 16
coder waits at 16
coder gets job-2 at 16
manager creates job-3 at 18
```

-   Easier to see as columns

<div class="row">
  <div class="col-5" markdown="1">
```{.txt data-file=simple_interaction_manager.txt}
manager creates job-0 at 0
manager creates job-1 at 6
manager creates job-2 at 12
manager creates job-3 at 18
```
  </div>
  <div class="col-1">
  </div>
  <div class="col-5" markdown="1">
```{.txt data-file=simple_interaction_coder.txt}
coder waits at 0
coder gets job-0 at 0
coder waits at 8
coder gets job-1 at 8
coder waits at 16
coder gets job-2 at 16
```
  </div>
</div>

-   But even this is hard to read

**Alternative way of presenting**:

[![Open in molab](https://molab.marimo.io/molab-shield.svg)](https://molab.marimo.io/notebooks/nb_8ZBjhiHtHB3J5ashmkWUV3)

```{.txt data-file=simple_interaction_marimo_alternative_output}
Environment time: 0 - Queue items: []

Queue items before manager creates one more job: []
At  0 , manager creates job 0 
Environment time: 0 - Queue items: [job 0 ]

Queue items before coder takes one job: [job 0 ]
Environment time: 0 - Queue items: []
Environment time: 0 - Queue items: []
At  0 , coder gets job 0 without waiting
Environment time: 0 - Queue items: []

Queue items before manager creates one more job: []
At  2 , manager creates job 1 
Environment time: 2 - Queue items: [job 1 ]
Environment time: 2 - Queue items: [job 1 ]

Queue items before manager creates one more job: [job 1 ]
At  4 , manager creates job 2 
Environment time: 4 - Queue items: [job 1 , job 2 ]
Environment time: 4 - Queue items: [job 1 , job 2 ]

Queue items before manager creates one more job: [job 1 , job 2 ]
At  6 , manager creates job 3 
Environment time: 6 - Queue items: [job 1 , job 2 , job 3 ]
Environment time: 6 - Queue items: [job 1 , job 2 , job 3 ]
At  8 , coder completes job 0 

Queue items before coder takes one job: [job 1 , job 2 , job 3 ]
Environment time: 8 - Queue items: [job 2 , job 3 ]

Queue items before manager creates one more job: [job 2 , job 3 ]
At  8 , manager creates job 4 
Environment time: 8 - Queue items: [job 2 , job 3 , job 4 ]
At  8 , coder gets job 1 without waiting
Environment time: 8 - Queue items: [job 2 , job 3 , job 4 ]
Environment time: 8 - Queue items: [job 2 , job 3 , job 4 ]

Queue items before manager creates one more job: [job 2 , job 3 , job 4 ]
At 10 , manager creates job 5 
Environment time: 10 - Queue items: [job 2 , job 3 , job 4 , job 5 ]
Environment time: 10 - Queue items: [job 2 , job 3 , job 4 , job 5 ]

Queue items before manager creates one more job: [job 2 , job 3 , job 4 , job 5 ]
At 12 , manager creates job 6 
Environment time: 12 - Queue items: [job 2 , job 3 , job 4 , job 5 , job 6 ]
Environment time: 12 - Queue items: [job 2 , job 3 , job 4 , job 5 , job 6 ]

Queue items before manager creates one more job: [job 2 , job 3 , job 4 , job 5 , job 6 ]
At 14 , manager creates job 7 
Environment time: 14 - Queue items: [job 2 , job 3 , job 4 , job 5 , job 6 , job 7 ]
```



