import { Routes, Route, Navigate } from "react-router-dom";
import Register from "../pages/Register";
import VerifyOtp from "../pages/VerifyOtp";
import Login from "../pages/Login";

export default function AuthRoutes() {
  return (
    <Routes>
      <Route path="register" element={<Register />} />
      <Route path="verify-otp" element={<VerifyOtp />} />
      <Route path="login" element={<Login />} />
      <Route path="*" element={<Navigate to="register" replace />} />
    </Routes>
  );
}
