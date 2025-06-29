import React, { useEffect, useState } from "react";
import axios from "axios";

function AdminPanel({ token }) {
  const [feedback, setFeedback] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/admin/feedback", {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => {
      const rows = res.data.split("\n").slice(1).filter(Boolean).map(line => {
        const [user_id, timestamp, metadata] = line.split(",");
        return { user_id, timestamp, metadata };
      });
      setFeedback(rows);
    });
  }, [token]);

  return (
    <div>
      <h2>Feedback Review</h2>
      <table>
        <thead>
          <tr><th>User</th><th>Timestamp</th><th>Metadata</th></tr>
        </thead>
        <tbody>
          {feedback.map((row, i) => (
            <tr key={i}>
              <td>{row.user_id}</td>
              <td>{row.timestamp}</td>
              <td>{row.metadata}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminPanel;
