import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../api/auth";
import { setVerificationId } from "../utils/storage";
import AuthLayout from "../components/AuthLayout";

export default function Register() {
    const navigate = useNavigate()
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("")
    const [loading, setLoading] = useState("")
    const [error, setError] = useState("")

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try{
            const data = await registerUser(email, password)
            setVerificationId(data.verification_id);
            navigate("/auth/verify-otp");

        } catch(err) {
            setError(err.message);
        } finally {
            setLoading(false)
        }
    };

    return(
        <AuthLayout title="Register">
            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />

                <input 
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                {error && <p style={{ color: "red"}}>{error}</p>}

                <button type="submit" disabled={loading}>
                    {loading ? "Registering....": "Register"}
                </button>
            </form>

        </AuthLayout>
    )
}