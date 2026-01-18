export default function categorySelect({categories, value, onChange}){
    return(
        <select value={value || ""} onChange={(e) => e.target.value}>
            <option value="">Select Catagory</option>
            {categories.map((cat)=>(
                <option key={cat.id}
                value={cat.id}
                disabled={cat.children && cat.children.length > 0}
                >
                    {cat.name}
                </option>
            ))}
        </select>
    );
}