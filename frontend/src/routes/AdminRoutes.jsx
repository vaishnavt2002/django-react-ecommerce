import { Routes, Route } from "react-router-dom";
import ProductList from "../pages/admin/ProductList";
import ProductCreate from "../pages/admin/ProductCreate";
import AdminCategoryPage from "../pages/admin/AdminCategoryPage";
import { AdminLayout } from "../components/admin/AdminLayout";

export default function AdminRoutes() {
  return (
    <Routes>
      <Route element={<AdminLayout />}>
        {/* Product Routes */}
        <Route path="products" element={<ProductList />} />
        <Route path="products/create" element={<ProductCreate />} />

        {/* Category Routes */}
        <Route path="categories" element={<AdminCategoryPage />} />
      </Route>
    </Routes>
  );
}