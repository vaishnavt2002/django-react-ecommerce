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
        <AuthLayout 
            title="Get started"
            subtitle="Sign up and start shopping with us"
        >
            <form onSubmit={handleSubmit} className="space-y-4">
                <input
                    type="email"
                    placeholder="Email"
                    className="w-full rounded border px-4 py-2 focus:outline-none focus:ring"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />

                <input 
                    type="password"
                    placeholder="Password"
                    className="w-full rounded border px-4 py-2 focus:outline-none focus:ring"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                {error && (
                    <p className="text-sm text-red-600">
                        {error}
                    </p>
                    )}

                <button 
                type="submit" 
                disabled={loading}
                className="w-full rounded bg-black py-2 text-white hover:bg-gray-900 disabled:opacity-50"
                >
                    {loading ? "Registering....": "Register"}
                </button>
            </form>

        </AuthLayout>
    )
}