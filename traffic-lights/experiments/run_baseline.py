from sim.config import ArrivalConfig, PhaseConfig, SimConfig
from sim.env_multi import MultiEnv
from sim.controller import RuleBasedController

def main():
    arrival = ArrivalConfig(lam_N=0.6, lam_E=0.8, lam_S=0.5, lam_W=0.4)
    phase   = PhaseConfig(min_green=12, amber=3, all_red=1, saturation_flow=2)
    simcfg  = SimConfig(horizon=1800, seed=7, dt=1)

    env = MultiEnv(arrival, phase, simcfg, RuleBasedController)
    metrics = env.run()
    df_total, df_per = metrics.to_dataframes()
    print(df_total.tail())
    print("Avg total queue:", df_total["total"].mean())

    # quick plot (headless-friendly; comment plt.show() if needed)
    import matplotlib.pyplot as plt
    plt.plot(df_total["t"], df_total["total"])
    plt.xlabel("time (s)"); plt.ylabel("total queued cars"); plt.title("Rule-based baseline (4 intersections)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
