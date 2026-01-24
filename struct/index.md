# Introducing Structure

-   Requirements
    -   Save results as JSON to simplify analysis
    -   Simulation may have several pieces, so put them in one object
    -   Support [parameter sweeping](g:parameter-sweeping)
-   Store parameters in a [dataclass](g:dataclass)
    -   Each parameter must have a default value so utilities can construct instances
        without knowing anything about specific parameters
    -   Use `@dataclass_json` decorator so that utilities can [serialize](g:serialize) as JSON

```{.py data-file=introduce_structure.py}
@dataclass_json
@dataclass
class Params:
    """Simulation parameters."""

    n_seed: int = 13579
    t_sim: float = 30
    t_wait: float = 8
```

-   Define another class to store the entire simulation
    -   Derive from SimPy `Environment`
    -   Store simulation parameters as `.params`
    -   May have other structures (e.g., a log to record output)
    -   Give it a `.result()` method that returns simulation result (e.g., the log)

```{.py data-file=introduce_structure.py}
class Simulation(Environment):
    """Complete simulation."""

    def __init__(self):
        super().__init__()
        self.params = Params()
        self.log = []

    def result(self):
        return {"log": self.log}
```

-   All of the simulation process generator functions take an instance of the simulation class as an argument
    -   `sim.whatever` for elements of the SimPy `Environment`
    -   `sim.params.whatever` for parameters

```{.py data-file=introduce_structure.py}
def coder(sim):
    """Simulate a single coder."""

    while True:
        sim.log.append(f"{sim.now}: Is there any work?")
        yield sim.timeout(sim.params.t_wait)
```

-   Define a `Simulation.simulate` method that creates processes and runs the simulation
    -   Can't call it `run` because we need that method from the parent class `Environment`

```{.py data-file=introduce_structure.py}
class Simulation
    def simulate(self):
        self.process(coder(self))
        self.run(until=self.params.t_sim)
```

-   Use `util.run(…)` to run scenarios with varying parameters and get result as JSON
    -   Look in project's `utilities` directory for implementation

```{.py data-file=introduce_structure.py}
if __name__ == "__main__":
    args, results = util.run(Params, Simulation)
    if args.json:
        json.dump(results, sys.stdout, indent=2)
    else:
        results = util.as_frames(results)
        for key, frame in results.items():
            print(f"## {key}")
            print(frame)
```

-   Sample command line invocation

```{.sh data-file=introduce_structure_json.sh}
python introduce_structure.py --json t_wait=12,20 t_sim=20,30
```

-   Output

```{.json data-file=introduce_structure_json.json}
{
  "results": [
    {
      "params": {"n_seed": 13579, "t_sim": 20, "t_wait": 12},
      "log": [
        {"time": 0, "message": "loop 0"},
        {"time": 12, "message": "loop 1"}
      ]
    },
    {
      "params": {"n_seed": 13579, "t_sim": 30, "t_wait": 12},
      "log": [
        {"time": 0, "message": "loop 0"},
        {"time": 12, "message": "loop 1"},
        {"time": 24, "message": "loop 2"}
      ]
    },
    {
      "params": {"n_seed": 13579, "t_sim": 20, "t_wait": 20},
      "log": [
        {"time": 0, "message": "loop 0"}
      ]
    },
    {
      "params": {"n_seed": 13579, "t_sim": 30, "t_wait": 20},
      "log": [
        {"time": 0, "message": "loop 0"},
        {"time": 20, "message": "loop 1"}
      ]
    }
  ]
}
```

-   Convert to [Polars][polars] dataframes)
    -   Include all parameters in each dataframe to simplify later analysis

```{.sh data-file=introduce_structure_df.sh}
python introduce_structure.py --tables t_wait=12,20 t_sim=20,30
```

```{.txt data-file=introduce_structure_df.txt}
## log
shape: (8, 5)
## log
shape: (8, 6)
┌──────┬─────────┬─────┬────────┬───────┬────────┐
│ time ┆ message ┆ id  ┆ n_seed ┆ t_sim ┆ t_wait │
│ ---  ┆ ---     ┆ --- ┆ ---    ┆ ---   ┆ ---    │
│ i64  ┆ str     ┆ i32 ┆ i32    ┆ i32   ┆ i32    │
╞══════╪═════════╪═════╪════════╪═══════╪════════╡
│ 0    ┆ loop 0  ┆ 0   ┆ 13579  ┆ 20    ┆ 12     │
│ 12   ┆ loop 1  ┆ 0   ┆ 13579  ┆ 20    ┆ 12     │
│ 0    ┆ loop 0  ┆ 1   ┆ 13579  ┆ 30    ┆ 12     │
│ 12   ┆ loop 1  ┆ 1   ┆ 13579  ┆ 30    ┆ 12     │
│ 24   ┆ loop 2  ┆ 1   ┆ 13579  ┆ 30    ┆ 12     │
│ 0    ┆ loop 0  ┆ 2   ┆ 13579  ┆ 20    ┆ 20     │
│ 0    ┆ loop 0  ┆ 3   ┆ 13579  ┆ 30    ┆ 20     │
│ 20   ┆ loop 1  ┆ 3   ┆ 13579  ┆ 30    ┆ 20     │
└──────┴─────────┴─────┴────────┴───────┴────────┘
```
