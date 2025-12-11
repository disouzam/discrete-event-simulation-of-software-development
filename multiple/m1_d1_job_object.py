from itertools import count
import json
import math
from random import expovariate, lognormvariate
from simpy import Environment, Store
import sys

ARRIVAL_RATE = 0.5
JOB_LENGTH_MU = math.log(2.0)
JOB_LENGTH_SIGMA = 0.5
T_SIM = 10
SEED = 12345
PREC = 3


class Env(Environment):
    @property
    def rnow(self):
        return round(self.now, PREC)


class Task:
    _id = count()

    def __init__(self, length):
        self.id = next(Task._id)
        self.length = length

    def __str__(self):
        return f"task-{self.id}"


class Worker:
    def __init__(self, env, log, queue):
        self.env = env
        self.log = log
        self.queue = queue
        self.env.process(self.run())


class Manager(Worker):
    def __init__(self, env, log, queue):
        super().__init__(env, log, queue)
        self.jobs = count()

    def run(self):
        while True:
            job = next(self.jobs)
            self.log.append(
                {"id": "manager", "time": self.env.rnow, "job": job, "event": "create"}
            )
            yield self.queue.put(job)
            job_arrival = self.t_job_arrival()
            yield self.env.timeout(job_arrival)

    def t_job_arrival(self):
        return expovariate(1 / ARRIVAL_RATE)


class Programmer(Worker):
    def run(self):
        while True:
            job = yield self.queue.get()
            job_length = self.t_job_length()
            self.log.append(
                {
                    "id": "programmer",
                    "time": self.env.rnow,
                    "job": job,
                    "event": "start",
                }
            )
            yield self.env.timeout(job_length)
            self.log.append(
                {"id": "programmer", "time": self.env.rnow, "job": job, "event": "end"}
            )

    def t_job_length(self):
        return lognormvariate(JOB_LENGTH_MU, JOB_LENGTH_SIGMA)


def main():
    env = Env()
    log = []
    queue = Store(env)
    Manager(env, log, queue)
    Programmer(env, log, queue)
    env.run(until=T_SIM)
    json.dump(log, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
