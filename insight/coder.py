from simpy import PriorityStore

from base import Actor
from jobs import JobFragment, Placeholder


class Coder(Actor):
    def post_init(self):
        self.queue = PriorityStore(self.sim)

    def run(self):
        while True:
            self.log("waiting")
            job = yield from self.get()
            job.coder_id = self.id
            job.start()
            if job.needs_decomp():
                self.log("decomposing")
                yield from self.decompose(job)
            elif not job.is_complete():
                self.log("working")
                yield self.sim.timeout(job.t_code)
                yield job.complete()

    def decompose(self, job):
        size = self.sim.params.t_decomposition
        num = int(job.t_code / size)
        extra = job.t_code - (num * size)
        durations = [extra, *[size for _ in range(num)]]
        placeholder = Placeholder(job=job, count=len(durations))
        for d in durations:
            yield self.queue.put(JobFragment(self, placeholder, d))

    def get(self):
        new_req = self.sim.code_queue.get()
        own_req = self.queue.get()
        result = yield (new_req | own_req)
        if (len(result.events) == 2) or (own_req in result):
            new_req.cancel()
            job = result[own_req]
        else:
            own_req.cancel()
            job = result[new_req]
        return job
