import matplotlib.pyplot as plt
import matplotlib.animation as anim
from sim.config import ArrivalConfig, PhaseConfig, SimConfig
from sim.env_multi import MultiEnv
from sim.controller import RuleBasedController
from sim.intersection import PHASE_NS, PHASE_EW

# live-stepping animation for 4 intersections (A,B,C,D)
arrival = ArrivalConfig(lam_N=0.6, lam_E=0.8, lam_S=0.5, lam_W=0.4)
phase   = PhaseConfig(min_green=12, amber=3, all_red=1, saturation_flow=2)
simcfg  = SimConfig(horizon=3600, seed=7, dt=1)

env = MultiEnv(arrival, phase, simcfg, RuleBasedController)

fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.axis('off')
ax.set_title("Traffic Lights – 4 Intersections (live)\nNS=green, EW=red (and vice versa)", pad=12)

# positions for 2x2 grid
centers = {
    "A": (-1.5,  1.5),
    "B": ( 1.5,  1.5),
    "C": (-1.5, -1.5),
    "D": ( 1.5, -1.5),
}

# artists per intersection
artists = {}
for k,(cx,cy) in centers.items():
    # draw roads (simple cross)
    ax.plot([cx-1.0, cx+1.0], [cy, cy], linewidth=4, alpha=0.3)
    ax.plot([cx, cx], [cy-1.0, cy+1.0], linewidth=4, alpha=0.3)
    # lights (two small circles to show current phase)
    ns_light = plt.Circle((cx, cy+0.9), 0.08, fc='grey', ec='black')
    ew_light = plt.Circle((cx+0.9, cy), 0.08, fc='grey', ec='black')
    ax.add_patch(ns_light); ax.add_patch(ew_light)

    # scatter placeholders for cars on each approach
    n_sc = ax.plot([], [], 'o', markersize=5)[0]
    s_sc = ax.plot([], [], 'o', markersize=5)[0]
    e_sc = ax.plot([], [], 'o', markersize=5)[0]
    w_sc = ax.plot([], [], 'o', markersize=5)[0]

    label = ax.text(cx-0.25, cy+1.15, k, fontsize=10, weight='bold')

    artists[k] = dict(ns=ns_light, ew=ew_light, N=n_sc, S=s_sc, E=e_sc, W=w_sc, label=label)

def update_frame(frame):
    t = frame
    env.step(t)
    snap = env.snapshot()

    for k,(cx,cy) in centers.items():
        d = snap[k]
        phase = d['phase']
        amber = d['amber']; allr = d['allred']

        # set light colors
        # simple scheme: active phase green, opposing red; amber/all-red override
        if amber > 0:
            ns_color = 'orange'
            ew_color = 'orange'
        elif allr > 0:
            ns_color = 'red'
            ew_color = 'red'
        else:
            if phase == PHASE_NS:
                ns_color = 'green'; ew_color = 'red'
            else:
                ns_color = 'red'; ew_color = 'green'

        artists[k]['ns'].set_facecolor(ns_color)
        artists[k]['ew'].set_facecolor(ew_color)

        # place cars as dots stacked along approaches
        # spacing between cars
        sp = 0.12
        # North (cars above moving southwards)
        qN = d['N']
        xN = [cx]*qN
        yN = [cy+0.8 - i*sp for i in range(qN)]
        artists[k]['N'].set_data(xN, yN)

        # South (below moving northwards)
        qS = d['S']
        xS = [cx]*qS
        yS = [cy-0.8 + i*sp for i in range(qS)]
        artists[k]['S'].set_data(xS, yS)

        # East (right moving westwards)
        qE = d['E']
        xE = [cx+0.8 - i*sp for i in range(qE)]
        yE = [cy]*qE
        artists[k]['E'].set_data(xE, yE)

        # West (left moving eastwards)
        qW = d['W']
        xW = [cx-0.8 + i*sp for i in range(qW)]
        yW = [cy]*qW
        artists[k]['W'].set_data(xW, yW)

    return [a for d in artists.values() for a in (d['ns'], d['ew'], d['N'], d['S'], d['E'], d['W'])]

ani = anim.FuncAnimation(fig, update_frame, frames=simcfg.horizon, interval=50, blit=True)
plt.show()
