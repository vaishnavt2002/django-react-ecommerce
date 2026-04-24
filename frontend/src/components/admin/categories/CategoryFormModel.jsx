import { useState } from "react";

export default function CategoryFormModal({ state, errors, onClose, onSubmit }) {
    const [name, setName] = useState(state.node?.name || "");

    return (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center">
            <div className="bg-white rounded-xl w-96 p-6 shadow-lg">
                <h2 className="text-lg font-semibold mb-4">
                    {state.type === "create" ? "Add Category" : "Edit Category"}
                </h2>

                <div className="space-y-4">
                    <div>
                        <input
                            className={`w-full border rounded-md px-3 py-2 ${errors?.name ? "border-red-500" : "border-gray-300"
                                }`}
                            placeholder="Category Name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                        {errors?.name && (
                            <p className="text-red-500 text-sm mt-1">
                                {errors.name}
                            </p>
                        )}
                    </div>

                    {errors?.error && (
                        <p className="text-red-500 text-sm">{errors.error}</p>
                    )}
                </div>

                <div className="flex justify-end gap-3 mt-6">
                    <button onClick={onClose} className="text-gray-500">
                        Cancel
                    </button>
                    <button
                        onClick={() => onSubmit({ name })}
                        className="bg-black text-white px-4 py-2 rounded-lg"
                    >
                        Save
                    </button>
                </div>
            </div>
        </div>
    );
}