"""Ask for work at regular intervals."""

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
