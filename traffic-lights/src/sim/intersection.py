from dataclasses import dataclass, field
import numpy as np

PHASE_NS = 0  # N/S go, E/W stop
PHASE_EW = 1  # E/W go, N/S stop

@dataclass
class Intersection:
    rng: np.random.Generator
    lam: dict  # {"N":λN,"E":λE,"S":λS,"W":λW}
    saturation_flow: int
    phase: int = PHASE_NS
    phase_timer: int = 0
    amber_timer: int = 0
    allred_timer: int = 0
    queues: dict = field(default_factory=lambda: {"N":0,"E":0,"S":0,"W":0})
    departures_last_tick: int = 0

    def arrivals(self):
        for a in self.queues.keys():
            inc = self.rng.poisson(self.lam[a])
            self.queues[a] += inc

    def green_approaches(self, phase:int):
        return ["N","S"] if phase == PHASE_NS else ["E","W"]

    def serve(self):
        # count how many departed this step
        self.departures_last_tick = 0
        if self.amber_timer > 0 or self.allred_timer > 0:
            return
        for a in self.green_approaches(self.phase):
            d = min(self.queues[a], self.saturation_flow)
            self.queues[a] -= d
            self.departures_last_tick += d

    def step_timers(self):
        if self.amber_timer > 0:
            self.amber_timer -= 1
            return
        if self.allred_timer > 0:
            self.allred_timer -= 1
            # switch phase when all-red finishes
            if self.allred_timer == 0:
                self.phase = PHASE_EW if self.phase == PHASE_NS else PHASE_NS
            return
        # normal running
        self.phase_timer += 1

    def can_switch(self):
        return self.amber_timer == 0 and self.allred_timer == 0

    def request_switch(self, amber:int, all_red:int):
        if self.can_switch():
            self.amber_timer = amber
            self.phase_timer = 0
            # we set allred after amber finishes (handled in step_timers)

    def finalize_switch_if_due(self, all_red:int):
        # if amber just finished this tick and we were in amber, move to allred
        if self.amber_timer == 0 and self.allred_timer == 0 and self.phase_timer == 0:
            # entering all-red
            self.allred_timer = all_red
