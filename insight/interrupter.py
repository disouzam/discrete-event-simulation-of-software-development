from random import choice, expovariate

from base import Actor
from jobs import JobInterrupt


class Interrupter(Actor):
    def run(self):
        while True:
            yield self.sim.timeout(self.rand_t_arrival())
            coder = choice(self.sim.coders)
            yield coder.queue.put(JobInterrupt(self.sim))

    def rand_t_arrival(self):
        return expovariate(1.0 / self.sim.params.t_interrupt_arrival)
