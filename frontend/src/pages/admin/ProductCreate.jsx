import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchAdminCatagories } from "../../api/admin/categories";
import { createAdminProduct } from "../../api/admin/products";
import ProductForm from "../../components/admin/ProductForm";

export default function ProductCreate(){
    const [categories, setCategories] = useState([]);
    const navigate = useNavigate();
    useEffect(()=>{
        fetchAdminCatagories().then(setCategories);
    },[]);
    
    const handleSubmit = async (data) => {
        await createAdminProduct(data);
        navigate('/admin/products');
    };

    return (
        <div>
            <h2>Create Product</h2>
            <ProductForm 
                categories={categories}
                onSubmit={handleSubmit}
                submitLabel="Create"
            />
        </div>
    )

}