# backend/background_tasks.py

import time
from fraud_detection import detect
from audit_chain import add
from cache import cache
import fraud_detection
import gnn_model
import explainability
import neo4j_graph
import time

# shared progress tracker
progress = {
    "status": "idle",      
    "percent": 0,
    "message": "Waiting"
}

def run_fraud_pipeline():
    progress["status"] = "running"
    progress["step"] = "Running fraud detection"
    cache["fraud"] = fraud_detection.detect()
    time.sleep(1)

    progress["step"] = "Running GNN analysis"
    cache["gnn"] = gnn_model.predict()
    time.sleep(1)

    progress["step"] = "Generating explanations"
    cache["explain"] = explainability.explain()
    time.sleep(1)

    progress["step"] = "Analyzing collusion graph"
    neo4j_graph.load_graph()
    cache["collusion"] = neo4j_graph.detect_collusion()
    time.sleep(1)

    progress["status"] = "completed"
    progress["step"] = "All analysis complete"

