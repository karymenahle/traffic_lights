from dataclasses import dataclass
from .intersection import PHASE_NS, PHASE_EW, Intersection

@dataclass
class BaseController:
    min_green:int
    amber:int
    all_red:int

    def decide(self, itx: Intersection):
        raise NotImplementedError

@dataclass
class RuleBasedController(BaseController):
    threshold:int = 3         # switch when opposing has >= threshold more cars than current
    max_green:int = 60        # optional: prevent starvation

    def decide(self, itx: Intersection):
        # if in intergreen, do nothing
        if itx.amber_timer > 0 or itx.allred_timer > 0:
            return

        # respect min_green
        if itx.phase_timer < self.min_green:
            return

        # if max_green reached, force a switch
        if self.max_green and itx.phase_timer >= self.max_green:
            itx.request_switch(self.amber, self.all_red)
            return

        if itx.phase == PHASE_NS:
            curr = itx.queues["N"] + itx.queues["S"]
            opp  = itx.queues["E"] + itx.queues["W"]
        else:
            curr = itx.queues["E"] + itx.queues["W"]
            opp  = itx.queues["N"] + itx.queues["S"]

        if opp - curr >= self.threshold:
            itx.request_switch(self.amber, self.all_red)
