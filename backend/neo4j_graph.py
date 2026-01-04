import os
import pandas as pd

def get_driver():
    try:
        from neo4j import GraphDatabase
    except ImportError:
        return None

    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASS")

    if not uri or not user or not password:
        return None

    return GraphDatabase.driver(uri, auth=(user, password))


def load_graph():
    driver = get_driver()
    if driver is None:
        return {"status": "neo4j disabled"}

    df = pd.read_csv("data/transactions.csv")

    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        for _, r in df.iterrows():
            session.run(
                """
                MERGE (v:Vendor {name:$vendor})
                MERGE (s:Scheme {name:$scheme})
                MERGE (v)-[:PAID {amount:$amount}]->(s)
                """,
                vendor=r.vendor,
                scheme=r.scheme,
                amount=r.amount,
            )

    return {"status": "graph loaded"}


def detect_collusion():
    driver = get_driver()
    if driver is None:
        return {"status": "neo4j disabled"}

    with driver.session() as session:
        res = session.run(
            """
            MATCH (v:Vendor)-[r]->()
            WITH v, COUNT(r) as c
            WHERE c > 8
            RETURN v.name AS vendor, c
            """
        )
        return [dict(r) for r in res]
