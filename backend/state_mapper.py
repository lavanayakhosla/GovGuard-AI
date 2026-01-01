import random

STATES = [
    "Delhi","Uttar Pradesh","Bihar","Maharashtra",
    "Karnataka","Tamil Nadu","Rajasthan","West Bengal"
]

def assign_state():
    return random.choice(STATES)
