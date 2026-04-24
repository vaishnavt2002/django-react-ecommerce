import { useState } from "react";
import { useCategoryTree } from "../../hooks/admin/useCategoryTree";
import CategoryTree from "../../components/admin/categories/CategoryTree";
import CategoryFormModal from "../../components/admin/categories/CategoryFormModel";

export default function AdminCategoryPage() {
    const {
        tree,
        loading,
        refresh,
        createCategory,
        updateCategory,
        deactivateCategory,
    } = useCategoryTree();

    const [modalState, setModalState] = useState(null);
    const [modalErrors, setModalErrors] = useState(null);

    const openModal = (state) => {
        setModalErrors(null);
        setModalState(state);
    };

    const closeModal = () => {
        setModalState(null);
        setModalErrors(null);
    };

    const handleCreate = async (data) => {
        const result = await createCategory(data);
        if (!result.success) {
            setModalErrors(result.errors);
            return;
        }
        closeModal();
        refresh();
    };

    const handleUpdate = async (id, data) => {
        const result = await updateCategory(id, data);
        if (!result.success) {
            setModalErrors(result.errors);
            return;
        }
        closeModal();
        refresh();
    };

    const handleDeactivate = async (id) => {
        const result = await deactivateCategory(id);
        if (!result.success) {
            // no modal open here, just log for now
            // later: show a toast
            console.error("Deactivate failed", result.errors);
            return;
        }
        refresh();
    };

    return (
        <div className="p-8 bg-gray-50 min-h-screen">
            <div className="flex justify-between mb-6">
                <h1 className="text-2xl font-semibold">Category Management</h1>
                <button
                    onClick={() => openModal({ type: "create", parent: null })}
                    className="bg-black text-white px-4 py-2 rounded-lg"
                >
                    + Add Root Category
                </button>
            </div>

            <div className="bg-white rounded-xl shadow-sm border p-4">
                {loading ? (
                    <p className="text-gray-400 text-sm">Loading...</p>
                ) : (
                    <CategoryTree
                        nodes={tree}
                        onAdd={(parent) => openModal({ type: "create", parent })}
                        onEdit={(node) => openModal({ type: "edit", node })}
                        onDeactivate={handleDeactivate}
                    />
                )}
            </div>

            {modalState && (
                <CategoryFormModal
                    state={modalState}
                    errors={modalErrors}
                    onClose={closeModal}
                    onSubmit={async (data) => {
                        if (modalState.type === "create") {
                            await handleCreate({
                                ...data,
                                parent: modalState.parent?.id || null,
                            });
                        } else {
                            await handleUpdate(modalState.node.id, data);
                        }
                    }}
                />
            )}
        </div>
    );
}