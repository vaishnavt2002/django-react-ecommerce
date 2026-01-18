import { Route, Routes } from "react-router-dom";
import ProductCreate from "../pages/admin/ProductCreate";
import ProductList from "../pages/admin/ProductList";

export default function AuthRoutes() {
    return (
        <Routes>
            <Route path="admin/products" element={<ProductList/>}/>
            <Route path="admin/products/create" element={<ProductCreate/>}/>
        </Routes>
    )
}