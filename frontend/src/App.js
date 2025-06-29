import React, { useState } from "react";
import axios from "axios";
import AdminPanel from "./AdminPanel";

function App() {
  const [token, setToken] = useState("");
  const [loginForm, setLoginForm] = useState({ username: "", password: "" });
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState("");
  const [variant, setVariant] = useState("");
  const [feedback, setFeedback] = useState(null);
  const [isAdmin, setIsAdmin] = useState(false);

  function decodeJWT(token) {
    try {
      const payload = token.split(".")[1];
      const decoded = JSON.parse(window.atob(payload));
      return decoded;
    } catch {
      return {};
    }
  }

  const handleLogin = async () => {
    const params = new URLSearchParams();
    params.append('username', loginForm.username);
    params.append('password', loginForm.password);

    const res = await axios.post("http://localhost:8000/token", params, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    setToken(res.data.access_token);

    const decoded = decodeJWT(res.data.access_token);
    setIsAdmin(decoded.is_admin === true);
  };

  const generate = async () => {
    setResult("");
    setFeedback(null);
    const res = await axios.post("http://localhost:8000/generate",
      { prompt },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    setResult(res.data.content);
    setVariant(res.data.variant);
  };

  const sendFeedback = async (value) => {
    await axios.post("http://localhost:8000/feedback",
      { feedback: value, variant, prompt },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    setFeedback(value);
  };

  if (!token) {
    return (
      <div style={{maxWidth: 600, margin: "auto"}}>
        <h2>Login</h2>
        <input placeholder="Username" value={loginForm.username}
          onChange={e => setLoginForm({...loginForm, username: e.target.value})} />
        <input placeholder="Password" type="password" value={loginForm.password}
          onChange={e => setLoginForm({...loginForm, password: e.target.value})} />
        <button onClick={handleLogin}>Login</button>
      </div>
    );
  }

  return (
    <div style={{maxWidth: 700, margin: "auto"}}>
      <h2>Content Generator</h2>
      <textarea rows={4} value={prompt}
        onChange={e => setPrompt(e.target.value)}
        style={{width: "100%"}} />
      <button onClick={generate}>Generate</button>
      <div style={{marginTop: 20, whiteSpace: "pre-line"}}>
        {result && <p>{result}</p>}
        {variant && <span>Variant: {variant}</span>}
      </div>
      {result && (
        <div>
          <button onClick={() => sendFeedback(1)}>👍</button>
          <button onClick={() => sendFeedback(0)}>👎</button>
          {feedback !== null && <span> Thanks for your feedback!</span>}
        </div>
      )}
      {isAdmin && (
        <div style={{marginTop: 40}}>
          <AdminPanel token={token} />
        </div>
      )}
    </div>
  );
}

export default App;