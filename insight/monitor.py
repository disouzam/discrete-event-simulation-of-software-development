class QueueMonitor:
    def __init__(self, sim):
        self.sim = sim
        self.sim.process(self.run())

    def run(self):
        watched = (("code", self.sim.code_queue), ("test", self.sim.test_queue))
        while True:
            for name, queue in watched:
                self.sim.log.queue(name, len(queue.items))
            yield self.sim.timeout(self.sim.params.t_queue_monitor)
