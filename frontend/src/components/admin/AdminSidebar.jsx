import { Link, useLocation } from "react-router-dom";

export default function AdminSidebar(){
    const location = useLocation();

    const navItem = (path) =>
        `block rounded-lg px-4 py-2 text-sm font-medium transition ${
            location.pathname.startsWith(path)
                ? "bg-black text-white"
                : "text-gray-600 hover:bg-gray-100"
        }`;
    return (
        <aside className="w-64 bg-white border-r p-6">
            <h1 className="text-xl font-semibold mb-8">
                Admin Panel
            </h1>

            <nav className="space-y-2">
                <Link to="/admin/products" className={navItem("/admin/products")}>
                    Products
                </Link>

                <Link to="/admin/categories" className={navItem("/admin/categories")}>
                    Categories
                </Link>
            </nav>
        </aside>
    );
}