import { useEffect, useState } from "react";
import { disableAdminProduct, fetchAdminProducts } from "../../api/admin/products";

export default function ProductList() {
    const [product, setProducts] = useState([]);

    useEffect(()=>{
        fetchAdminProducts().then(setProducts);
    },[])

    const handleDisable = async (id) => {
            await disableAdminProduct(id);
            setProducts((prev) => 
            prev.map((p)=> (p.id === id ? {...p, is_active:false}:p))
        );
    }

    return (
        <div>
            <h2>Products</h2>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Category</th>
                        <th>Name</th>
                        <th>Gender</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {product.map((p)=>(
                        <tr key={p.id}>
                            <td>{p.name}</td>
                            <td>{p.category}</td>
                            <td>{p.gender}</td>
                            <td>{p.is_active ? "Active" : "Inactive"}</td>
                            <td>
                                {p.is_active && (
                                    <button onClick={() => handleDisable(p.id)}>Disable</button>
                                )}
                            </td>

                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}