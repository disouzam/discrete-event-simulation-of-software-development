"""
A developer ask for work at regular intervals.
A Scrum Master answers one single time informing there is available and ready work.
There is no interaction between them at this moment.
"""

from simpy import Environment

T_SIM = 30
T_WAIT = 8


def coder(env):
    while True:
        print(f"{env.now}: Is there any work?")
        yield env.timeout(T_WAIT)


def scrum_master(env):
    yield env.timeout(14)
    print(f"{env.now}: There is a new task available for you, developer.")


if __name__ == "__main__":
    env = Environment()
    env.process(coder(env))
    env.process(scrum_master(env))
    env.run(until=T_SIM)
