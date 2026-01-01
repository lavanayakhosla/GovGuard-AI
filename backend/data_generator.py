import pandas as pd
import numpy as np
import random
from state_mapper import assign_state
from indian_schemes import SCHEMES

def generate():
    rows = []
    for i in range(1500):
        amount = abs(np.random.normal(50000,12000))
        if random.random() < 0.07:
            amount *= 6

        rows.append({
            "transaction_id": i,
            "vendor": f"VENDOR_{random.randint(1,50)}",
            "scheme": random.choice(list(SCHEMES.keys())),
            "amount": round(amount,2),
            "state": assign_state()
        })

    df = pd.DataFrame(rows)
    df.to_csv("data/transactions.csv", index=False)

if __name__ == "__main__":
    generate()
