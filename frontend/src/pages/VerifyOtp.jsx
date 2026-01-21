import { useNavigate } from "react-router-dom";
import { clearVerificationId, getVerificationId } from "../utils/storage";
import { useEffect, useRef, useState } from "react";
import { verifyOtp } from "../api/auth";
import AuthLayout from "../components/AuthLayout";

export default function VerifyOtp() {
  const navigate = useNavigate();
  const verificationId = getVerificationId();

  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // refs to control focus
  const inputRefs = useRef([]);

  useEffect(() => {
    if (!verificationId) {
      navigate("/auth/register");
    }
  }, [verificationId, navigate]);

  const handleChange = (index, value) => {
    if (!/^\d?$/.test(value)) return; // allow only single digit

    const newOtp = [...otp];
    newOtp[index] = value;
    setOtp(newOtp);

    // move to next input automatically
    if (value && index < 5) {
      inputRefs.current[index + 1].focus();
    }
  };

  const handleKeyDown = (index, e) => {
    if (e.key === "Backspace" && !otp[index] && index > 0) {
      inputRefs.current[index - 1].focus();
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const otpValue = otp.join("");

    try {
        await verifyOtp(verificationId, otpValue);
        navigate("/auth/login");
    } catch (err) {
        setError(err.message);
    } finally {
        clearVerificationId();
        setLoading(false);
    }
  };

  return (
    <AuthLayout
      title="Verify your email"
      subtitle="A confirmation code was sent to your email"
    >
      <form onSubmit={handleSubmit} className="space-y-6">

        {/* OTP inputs */}
        <div className="flex justify-between gap-2">
          {otp.map((digit, index) => (
            <input
              key={index}
              ref={(el) => (inputRefs.current[index] = el)}
              type="text"
              inputMode="numeric"
              maxLength={1}
              value={digit}
              onChange={(e) => handleChange(index, e.target.value)}
              onKeyDown={(e) => handleKeyDown(index, e)}
              className="
                h-12 w-12 
                rounded border 
                text-center text-lg 
                focus:outline-none focus:ring
              "
            />
          ))}
        </div>

        {error && (
          <p className="text-sm text-red-600">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="
            w-full rounded 
            bg-black py-2 
            text-white 
            hover:bg-gray-900 
            disabled:opacity-50
          "
        >
          {loading ? "Verifying..." : "Next"}
        </button>

        <p className="text-sm text-center text-gray-500">
          Didn’t receive an email?{" "}
          <button type="button" className="text-black underline">
            Resend
          </button>
        </p>

      </form>
    </AuthLayout>
  );
}
