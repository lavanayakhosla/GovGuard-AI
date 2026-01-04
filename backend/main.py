from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from background_init import initialize_services

from background_tasks import run_fraud_pipeline, progress

from cache import cache

# import fraud_detection
# import explainability
# import neo4j_graph
# import gnn_model
# import audit_chain

APP_STATUS = {
    "state": "starting",
    "message": "Booting services..."
}

app = FastAPI(title="GovGuard AI")

@app.on_event("startup")
def startup_event():
    from threading import Thread
    Thread(
        target=initialize_services,
        args=(APP_STATUS,),
        daemon=True
    ).start()
# ------------------- CORS -------------------
origins = [
    "http://localhost:3000",                      # local dev
    "https://gov-guard-ai.vercel.app",           # deployed frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # frontend URLs allowed
    allow_credentials=True,
    allow_methods=["*"],    # GET, POST, etc.
    allow_headers=["*"],    # headers like Content-Type
)

# ------------------- ROUTES -------------------

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/status")
def status():
    return APP_STATUS


@app.get("/fraud")
def fraud():
    if cache["fraud"] is None:
        return {"message": "Analysis not ready"}
    return cache["fraud"].to_dict(orient="records")

@app.get("/explain")
def explain():
    return cache["explain"] or {"message": "Analysis not ready"}

# @app.get("/graph/load")
# def load_graph():
#     neo4j_graph.load_graph()
#     return {"status": "graph loaded"}

@app.get("/collusion")
def collusion():
    return cache["collusion"] or []


@app.get("/gnn")
def gnn():
    return cache["gnn"] or []

@app.get("/fraud/statewise")
def fraud_statewise():
    if cache["fraud"] is None:
        return {"message": "Analysis not ready"}
    return cache["fraud"].groupby("state").size().to_dict()


# @app.get("/audit")
# def audit():
#     return audit_chain.chain

@app.post("/start-fraud-analysis")
def start_fraud(background_tasks: BackgroundTasks):
    if progress["status"] == "running":
        return {"message": "Analysis already running"}

    background_tasks.add_task(run_fraud_pipeline)
    return {"message": "Fraud analysis started"}

@app.get("/progress")
def get_progress():
    return progress

