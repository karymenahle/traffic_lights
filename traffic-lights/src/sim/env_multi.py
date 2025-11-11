import numpy as np
from .intersection import Intersection
from .metrics import Metrics

class MultiEnv:
    """A 2x2 grid of intersections: IDs A,B,C,D arranged as
        A | B
        -----
        C | D
    For simplicity, intersections are independent controllers (no global sync).
    """
    def __init__(self, arrival_cfg, phase_cfg, sim_cfg, controller_cls):
        self.rng = np.random.default_rng(sim_cfg.seed)
        lam_base = {"N":arrival_cfg.lam_N, "E":arrival_cfg.lam_E,
                    "S":arrival_cfg.lam_S, "W":arrival_cfg.lam_W}

        # create 4 intersections with slightly perturbed arrivals to vary load
        def lam_jitter(scale):
            return {d: max(0.0, lam_base[d] * scale) for d in lam_base}

        self.itx = {
            "A": Intersection(rng=self.rng, lam=lam_jitter(1.00), saturation_flow=phase_cfg.saturation_flow),
            "B": Intersection(rng=self.rng, lam=lam_jitter(1.10), saturation_flow=phase_cfg.saturation_flow),
            "C": Intersection(rng=self.rng, lam=lam_jitter(0.90), saturation_flow=phase_cfg.saturation_flow),
            "D": Intersection(rng=self.rng, lam=lam_jitter(1.20), saturation_flow=phase_cfg.saturation_flow),
        }

        self.ctrl = {k: controller_cls(min_green=phase_cfg.min_green,
                                       amber=phase_cfg.amber,
                                       all_red=phase_cfg.all_red)
                     for k in self.itx.keys()}

        self.horizon = sim_cfg.horizon
        self.dt = sim_cfg.dt
        self.phase_cfg = phase_cfg
        self.metrics = Metrics()

    def snapshot(self):
        snap = {}
        for k, itx in self.itx.items():
            snap[k] = {
                "N": itx.queues["N"], "E": itx.queues["E"],
                "S": itx.queues["S"], "W": itx.queues["W"],
                "phase": itx.phase,
                "amber": itx.amber_timer,
                "allred": itx.allred_timer,
                "phase_t": itx.phase_timer,
                "departed": itx.departures_last_tick,
            }
        return snap

    def step(self, t:int):
        # arrivals everywhere
        for itx in self.itx.values():
            itx.arrivals()

        # decisions
        for k, itx in self.itx.items():
            self.ctrl[k].decide(itx)

        # service
        for itx in self.itx.values():
            itx.serve()

        # finalize switch transitions & timers
        for itx in self.itx.values():
            itx.finalize_switch_if_due(self.phase_cfg.all_red)
            itx.step_timers()

        # log
        self.metrics.log(t, self.snapshot())

    def run(self):
        for t in range(0, self.horizon, self.dt):
            self.step(t)
        return self.metrics
