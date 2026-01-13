import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/auth";


export default function Login(){
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e)=>{
        e.preventDefault();
        setError(null);
        setLoading(true);

        try{
            response = await login(email, password)
            navigate("/")
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false)
        }
    };

    return (
    <div style={{ maxWidth: 400, margin: "2rem auto" }}>
      <h2>Login</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <div>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div style={{ marginTop: 12 }}>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{ marginTop: 16 }}
        >
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
    </div>
  );



}