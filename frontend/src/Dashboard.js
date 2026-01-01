import { useEffect, useState } from "react";
import api from "./api";
import IndiaMap from "./IndiaMap";
import D3Network from "./D3Network";

export default function Dashboard() {
  const [fraudTxns, setFraudTxns] = useState([]);
  const [stateData, setStateData] = useState({});
  const [collusion, setCollusion] = useState([]);

  useEffect(() => {
    api.get("/fraud").then(res => setFraudTxns(res.data));
    api.get("/fraud/statewise").then(res => setStateData(res.data));
    api.get("/collusion").then(res => setCollusion(res.data));
  }, []);

  const totalTxns = 1500; // generated
  const fraudCount = fraudTxns.length;
  const fraudRate = ((fraudCount / totalTxns) * 100).toFixed(2);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>GovGuard AI – Public Fraud Analytics</h1>

      {/* KPI CARDS */}
      <div style={{ display: "flex", gap: "20px", marginBottom: "20px" }}>
        <KPI title="Total Transactions" value={totalTxns} />
        <KPI title="Flagged Frauds" value={fraudCount} />
        <KPI title="Fraud Rate (%)" value={fraudRate} />
      </div>

      {/* MAP */}
      <h2>Fraud Heatmap (State-wise)</h2>
      <IndiaMap data={stateData} />

      <h2>Vendor Network </h2>
      <D3Network />

      {/* FRAUD TABLE */}
      <h2>Flagged Transactions</h2>
      <FraudTable data={fraudTxns} />

      {/* COLLUSION */}
      <h2>Potential Vendor Collusion</h2>
      <CollusionList data={collusion} />
    </div>
  );
}

function KPI({ title, value }) {
  return (
    <div style={{
      padding: "15px",
      border: "1px solid #ccc",
      borderRadius: "8px",
      width: "200px",
      textAlign: "center",
      background: "#f9f9f9"
    }}>
      <h3>{title}</h3>
      <h2>{value}</h2>
    </div>
  );
}

function FraudTable({ data }) {
  return (
    <table border="1" width="100%" cellPadding="6">
      <thead>
        <tr>
          <th>Vendor</th>
          <th>Scheme</th>
          <th>Amount</th>
          <th>State</th>
          <th>Risk Score</th>
        </tr>
      </thead>
      <tbody>
        {data.map((d, i) => (
          <tr key={i} style={{ background: d.risk_score > 80 ? "#ffd6d6" : "" }}>
            <td>{d.vendor}</td>
            <td>{d.scheme}</td>
            <td>₹{d.amount}</td>
            <td>{d.state}</td>
            <td>{d.risk_score.toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function CollusionList({ data }) {
  if (!data.length) return <p>No major collusion detected.</p>;

  return (
    <ul>
      {data.map((d, i) => (
        <li key={i}>
          <b>{d.vendor}</b> – {d.c} linked contracts ⚠
        </li>
      ))}
    </ul>
  );
}