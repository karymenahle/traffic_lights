from sim.config import ArrivalConfig, PhaseConfig, SimConfig
from sim.env_multi import MultiEnv
from sim.controller import RuleBasedController

def test_basic_run():
    env = MultiEnv(ArrivalConfig(), PhaseConfig(), SimConfig(horizon=10, seed=1, dt=1), RuleBasedController)
    m = env.run()
    df_total, df_per = m.to_dataframes()
    assert len(df_total) == 10
    assert (df_total['total'] >= 0).all()
