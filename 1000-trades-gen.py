from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# Create fake data
np.random.seed(42)
dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(10000)]
outcomes = np.random.choice(["WIN", "LOSS"], 10000, p=[0.6, 0.4])
pl_percent = np.random.uniform(-10, 15, 10000)  # P/L between -10% and 15%
risk_percent = np.random.uniform(0.5, 2, 10000)  # Risk between 0.5% and 2%
entry_times = [f"{h:02d}:{m:02d}" for h in np.random.randint(0, 24, 10000) for m in np.random.randint(0, 60, 1)]
pl_by_rr = pl_percent / risk_percent  # Risk-reward ratio

df = pd.DataFrame(
    {
        "date": dates,
        "outcome": outcomes,
        "pl_by_percentage": pl_percent,
        "risk_by_percentage": risk_percent,
        "entry_time": entry_times[:10000],
        "pl_by_rr": pl_by_rr,
    }
)

# Save as CSV
df.to_csv("test_trades_10000.csv", index=False)
