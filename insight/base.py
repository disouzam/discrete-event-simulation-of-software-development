from collections import defaultdict
from itertools import count


class Priority:
    HIGH = 0
    MEDIUM = 1
    LOW = 2


class Recorder:
    _next_id = defaultdict(count)
    _all = defaultdict(list)

    @staticmethod
    def reset():
        Recorder._next_id = defaultdict(count)
        Recorder._all = defaultdict(list)

    def __init__(self, sim):
        cls = self.__class__
        self.id = next(self._next_id[cls])
        self._all[cls].append(self)
        self.sim = sim

    def __str__(self):
        return f"{self.__class__.__name__}_{self.id}"


class Actor(Recorder):
    def __init__(self, sim):
        super().__init__(sim)
        self.post_init()
        proc = self.run()
        self.sim.process(proc)

    def post_init(self):
        pass

    def log(self, state):
        self.sim.log.actor(self.__class__.__name__, self.id, state)
