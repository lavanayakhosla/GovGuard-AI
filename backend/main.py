from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import fraud_detection
import explainability
import neo4j_graph
import gnn_model
import audit_chain

app = FastAPI(title="GovGuard AI")

# ✅ CORRECT CORS CONFIG (NO NETWORK ERROR)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- ROUTES -------------------

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/fraud")
def fraud():
    audit_chain.add("Fraud detection run")
    return fraud_detection.detect().to_dict(orient="records")

@app.get("/explain")
def explain():
    return explainability.explain()

@app.get("/graph/load")
def load_graph():
    neo4j_graph.load_graph()
    return {"status": "graph loaded"}

@app.get("/collusion")
def collusion():
    return neo4j_graph.detect_collusion()

@app.get("/gnn")
def gnn():
    return gnn_model.predict()

@app.get("/fraud/statewise")
def fraud_statewise():
    df = fraud_detection.detect()
    return df.groupby("state").size().to_dict()

@app.get("/audit")
def audit():
    return audit_chain.chain


