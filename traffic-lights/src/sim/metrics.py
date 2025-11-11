from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Metrics:
    time: List[int] = field(default_factory=list)
    totals: List[int] = field(default_factory=list)
    per_itx: List[Dict[str, Any]] = field(default_factory=list)  # [{itx_id: {N,E,S,W,phase,...}}, ...]

    def log(self, t:int, snapshots: Dict[str, Dict[str, int]]):
        self.time.append(t)
        total = 0
        rec = {}
        for k, v in snapshots.items():
            total += v.get("N",0)+v.get("E",0)+v.get("S",0)+v.get("W",0)
            rec[k] = dict(v)
        self.totals.append(total)
        self.per_itx.append(rec)

    def to_dataframes(self):
        import pandas as pd
        # overall totals
        df_total = pd.DataFrame({"t": self.time, "total": self.totals})
        # per-intersection queues (flattened wide format for convenience)
        rows = []
        for t, per in zip(self.time, self.per_itx):
            row = {"t": t}
            for itx_id, q in per.items():
                for k,v in q.items():
                    row[f"{itx_id}_{k}"] = v
            rows.append(row)
        df_per = pd.DataFrame(rows)
        return df_total, df_per
