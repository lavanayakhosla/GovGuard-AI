import time

def initialize_services(status):
    status["message"] = "Loading ML models..."
    time.sleep(2)

    import fraud_detection
    import explainability
    import neo4j_graph
    import gnn_model
    import audit_chain

    status["message"] = "All services ready"
    status["state"] = "ready"
