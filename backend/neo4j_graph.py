import os
from neo4j import GraphDatabase
import pandas as pd

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    auth=(os.getenv("NEO4J_USER","neo4j"), os.getenv("NEO4J_PASS","password"))
)

def load_graph():
    df = pd.read_csv("data/transactions.csv")
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        for _, r in df.iterrows():
            session.run("""
                MERGE (v:Vendor {name:$vendor})
                MERGE (s:Scheme {name:$scheme})
                MERGE (v)-[:PAID {amount:$amount}]->(s)
            """, vendor=r.vendor, scheme=r.scheme, amount=r.amount)

def detect_collusion():
    with driver.session() as session:
        res = session.run("""
            MATCH (v:Vendor)-[r]->()
            WITH v, COUNT(r) as c
            WHERE c > 8
            RETURN v.name AS vendor, c
        """)
        return [dict(r) for r in res]
