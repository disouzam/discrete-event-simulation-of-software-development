from collections import defaultdict
from itertools import count
import json
import random
from simpy import Environment, Store
import sys

T_SIM = 10
SEED = 12345
PREC = 3


class Env(Environment):
    @property
    def rnow(self):
        return round(self.now, PREC)


class Worker:
    _ids = defaultdict(count)

    @staticmethod
    def make_id(obj):
        stem = obj.__class__.__name__.lower()
        num = next(Worker._ids[stem])
        return f"{stem}-{num}"
    
    def __init__(self, env, log):
        self.env = env
        self.log = log
        self.id = Worker.make_id(self)
        self.env.process(self.run())


class Manager(Worker):
    def __init__(self, env, log, queue):
        super().__init__(env, log)
        self.queue = queue

    def run(self):
        while True:
            job_length = self.t_job_length()
            self.log.append(
                {"id": self.id, "time": self.env.rnow, "event": f"create job {job_length}"}
            )
            yield self.queue.put(job_length)
            yield self.env.timeout(self.t_job_arrival())

    def t_job_length(self):
        return 3

    def t_job_arrival(self):
        return 4


class Programmer(Worker):
    def __init__(self, env, log, queue):
        super().__init__(env, log)
        self.queue = queue

    def run(self):
        while True:
            job_length = yield self.queue.get()
            self.log.append(
                {"id": self.id, "time": self.env.rnow, "event": f"get job {job_length}"}
            )
            yield self.env.timeout(job_length)
            self.log.append(
                {"id": self.id, "time": self.env.rnow, "event": f"complete job {job_length}"}
            )


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else SEED
    random.seed(seed)
    env = Env()
    log = []
    queue = Store(env)
    manager = Manager(env, log, queue)
    programmer = Programmer(env, log, queue)
    env.run(until=T_SIM)
    json.dump(log, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
