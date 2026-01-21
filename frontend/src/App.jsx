import { BrowserRouter, Routes, Route } from "react-router-dom";
import AuthRoutes from "./routes/AuthRoutes";
import AdminRoutes from "./routes/AdminRoutes";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Auth routes */}
        <Route path="/auth/*" element={<AuthRoutes />} />

        {/* Admin routes */}
        <Route path="/admin/*" element={<AdminRoutes />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
