How to run
1. Have python , node and Neo4j installed
2. Create an instance on neo4j and make a password
3. clone this repo
4. Put following commands in terminal - cd backend ,
5.  python3.11 -m venv venv                                                 
6. source venv/bin/activate
7. pip install --upgrade pip
8. pip install \                                                           
fastapi \
uvicorn \
pandas \
"numpy<=2.3.3" \
scikit-learn \
neo4j \
networkx \
shap \
torch \
torch-geometric \
pdfplumber
9. python data_generator.py // This generates the demo data transactions.csv
10. export NEO4J_URI=bolt://localhost:7687                                  
export NEO4J_USER=neo4j
export NEO4J_PASS= put your password
11. python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
12. in frontend repo , do npm install and npm start 
