from simpy import PriorityStore, Store


class LogPriorityStore(PriorityStore):
    def __init__(self, sim, name):
        super().__init__(sim.env)
        self.sim = sim
        self.name = name

    def _do_get(self, event):
        super()._do_get(event)
        self.sim.log.queue(self.name, "get", len(self.items))

    def _do_put(self, event):
        super()._do_put(event)
        self.sim.log.queue(self.name, "put", len(self.items))


class LogStore(Store):
    def __init__(self, sim, name):
        super().__init__(sim.env)
        self.sim = sim
        self.name = name

    def _do_get(self, event):
        super()._do_get(event)
        self.sim.log.queue(self.name, "get", len(self.items))

    def _do_put(self, event):
        super()._do_put(event)
        self.sim.log.queue(self.name, "put", len(self.items))
