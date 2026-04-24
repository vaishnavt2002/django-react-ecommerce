import { useEffect, useState } from "react";
import { disableAdminProduct, fetchAdminProducts } from "../../api/admin/products";
import { Link } from "react-router-dom";

export default function ProductList() {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        fetchAdminProducts().then(setProducts);
    }, []);

    const handleDisable = async (id) => {
        await disableAdminProduct(id);
        setProducts((prev) =>
            prev.map((p) =>
                p.id === id ? { ...p, is_active: false } : p
            )
        );
    };

    return (
        <div>
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-2xl font-semibold">Products</h1>
                    <p className="text-sm text-gray-500">
                        Manage your product catalog
                    </p>
                </div>

                <Link
                    to="/admin/products/create"
                    className="rounded-lg bg-black px-4 py-2 text-sm text-white hover:bg-gray-900"
                >
                    + Add Product
                </Link>
            </div>

            {/* Card */}
            <div className="bg-white rounded-xl shadow-sm border">
                <table className="w-full text-sm">
                    <thead className="bg-gray-50 border-b text-gray-600">
                        <tr>
                            <th className="text-left px-6 py-3">Name</th>
                            <th className="text-left px-6 py-3">Category</th>
                            <th className="text-left px-6 py-3">Gender</th>
                            <th className="text-left px-6 py-3">Status</th>
                            <th className="text-left px-6 py-3">Action</th>
                        </tr>
                    </thead>

                    <tbody>
                        {products.map((p) => (
                            <tr
                                key={p.id}
                                className="border-b last:border-none hover:bg-gray-50"
                            >
                                <td className="px-6 py-4 font-medium">
                                    {p.name}
                                </td>

                                <td className="px-6 py-4 text-gray-600">
                                    {p.category}
                                </td>

                                <td className="px-6 py-4 text-gray-600 capitalize">
                                    {p.gender}
                                </td>

                                <td className="px-6 py-4">
                                    <span
                                        className={`px-2 py-1 text-xs rounded-full ${
                                            p.is_active
                                                ? "bg-green-100 text-green-700"
                                                : "bg-gray-200 text-gray-600"
                                        }`}
                                    >
                                        {p.is_active ? "Active" : "Inactive"}
                                    </span>
                                </td>

                                <td className="px-6 py-4">
                                    {p.is_active && (
                                        <button
                                            onClick={() => handleDisable(p.id)}
                                            className="text-sm text-red-600 hover:underline"
                                        >
                                            Disable
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
