import hashlib, time

chain = []

def add(event):
    prev = chain[-1]["hash"] if chain else "GENESIS"
    payload = f"{event}{prev}{time.time()}"
    h = hashlib.sha256(payload.encode()).hexdigest()
    chain.append({"event":event,"hash":h})
