import { useState } from "react";

export default function ProductForm({
    initialData = {},
    categories,
    onSubmit,
    submitLabel,
}){
    const [form, setForm] = useState({
        name: initialData.name || "",
        slug: initialData.slug || "",
        description: initialData.description || "",
        gender: initialData.gender || "",
        category: initialData.category || "",
    });

    const handleChange = (e) => {
        setForm({...form, [e.target.name]: e.target.value});
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(form);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                name="name"
                placeholder="Product Name"
                value={form.name}
                onChange={handleChange}
                required
            />

            <input 
                name="slug"
                placeholder="Slug"
                value={form.slug}
                onChange={handleChange}
                required
            />
            <textarea
                name="description"
                placeholder="Description"
                value={form.description}
                onChange={handleChange}
            />

            <select
                name="gender"
                value={form.gender}
                onChange={handleChange}
                required
            >
                <option value="">Select Gender</option>
                <option value="men">Men</option>
                <option value="woman">Women</option>
                <option value="unisex">Unisex</option>
            </select>

            <CategorySelect categories={categories}
                value={form.category}
                onChange={(val) => setForm({...form, category:val})}
            />

            <button>{submitLabel}</button>

        </form>
    )
}