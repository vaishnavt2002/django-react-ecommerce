import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/auth";
import AuthLayout from "../components/AuthLayout";


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
            await login(email, password);
            navigate("/")
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false)
        }
    };

    return (
    <AuthLayout 
                title="Login"
                subtitle="Login and start shopping with us"
            >

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label>Email</label>
          <input
            type="email"
            className="w-full rounded border px-4 py-2 focus:outline-none focus:ring"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div style={{ marginTop: 12 }}>
          <label>Password</label>
          <input
            type="password"
            className="w-full rounded border px-4 py-2 focus:outline-none focus:ring"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && (
                    <p className="text-sm text-red-600">
                        {error}
                    </p>
                    )}

        <button
          type="submit"
          disabled={loading}
          style={{ marginTop: 16 }}
          className="w-full rounded bg-black py-2 text-white hover:bg-gray-900 disabled:opacity-50"
        >
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
      </AuthLayout>
  );



}