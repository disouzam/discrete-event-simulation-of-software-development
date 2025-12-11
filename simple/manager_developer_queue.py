from itertools import count
import json
import random
from simpy import Environment, Store
import sys

T_SIM = 100
T_JOB_ARRIVAL_MIN = 20
T_JOB_ARRIVAL_MAX = 30
T_WORK_MIN = 10
T_WORK_MAX = 50
SEED = 12345
PREC = 3


def rt(env):
    return round(env.now, PREC)


def t_job_arrival():
    return random.uniform(T_JOB_ARRIVAL_MIN, T_JOB_ARRIVAL_MAX)


def t_work():
    return random.uniform(T_WORK_MIN, T_WORK_MAX)


def manager(env, queue, log):
    job_id = count()
    while True:
        log.append({"time": rt(env), "id": "manager", "event": "create job"})
        yield queue.put(next(job_id))
        yield env.timeout(t_job_arrival())


def programmer(env, queue, log):
    while True:
        log.append({"time": rt(env), "id": "worker", "event": "start wait"})
        job = yield queue.get()
        log.append({"time": rt(env), "id": "worker", "event": "start work"})
        yield env.timeout(t_work())
        log.append({"time": rt(env), "id": "worker", "event": "end work"})


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else SEED
    random.seed(seed)

    env = Environment()
    queue = Store(env)
    log = []

    env.process(manager(env, queue, log))
    env.process(programmer(env, queue, log))
    env.run(until=T_SIM)

    json.dump(log, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
