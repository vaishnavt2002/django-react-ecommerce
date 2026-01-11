import { useNavigate } from "react-router-dom";
import { clearVerificationId, getVerificationId } from "../utils/storage";
import { useEffect, useState } from "react";
import { verifyOtp } from "../api/auth";
import AuthLayout from "../components/AuthLayout";

export default function VerifyOtp() {
    const navigate = useNavigate();
    const verificationId = getVerificationId();

    const [otp, setOtp] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(()=>{
        if (!verificationId){
            navigate("/auth/register");
        }
    }, [verificationId, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setLoading(true);
        
        try {
            await verifyOtp(verificationId, otp);
            clearVerificationId()
            navigate("/login")
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <AuthLayout title="Verify Otp">
            <form onSubmit={handleSubmit}> 
                <input 
                    type="text"
                    placeholder="Enter OTP"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value)}
                    maxLength={6}
                    required
                />

                {error && <p style={{ color: "red" }}>{error}</p>}

                <button>
                    {loading ? "Verifying...." : "Verify" }
                </button>
            </form>
        </AuthLayout>
    )



}