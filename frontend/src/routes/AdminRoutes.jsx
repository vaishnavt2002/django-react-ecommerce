import { Routes, Route } from "react-router-dom";
import ProductList from "../pages/admin/ProductList";
import ProductCreate from "../pages/admin/ProductCreate";

export default function AdminRoutes() {
  return (
    <Routes>
      <Route path="/admin/products" element={<ProductList />} />
      <Route path="/admin/products/create" element={<ProductCreate />} />
    </Routes>
  );
}
