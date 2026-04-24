import { useEffect, useState } from "react";
import {
    fetchCatagoryTree,
    createCategory as apiCreateCategory,
    updateCategory as apiUpdateCategory,
    deactivateCategory as apiDeactivateCategory
} from "../../api/admin/categories";
import { ok, fail } from "../../utils/apiResponse";

export function useCategoryTree() {
    const [tree, setTree] = useState([]);
    const [loading, setLoading] = useState(false);

    const load = async () => {
        setLoading(true);
        try {
            const data = await fetchCatagoryTree();
            setTree(data);
        } catch (err) {
            console.error("Failed to load category tree", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        load();
    }, []);

    const createCategory = async (data) => {
        try {
            const result = await apiCreateCategory(data);
            return ok(result);
        } catch (err) {
            return fail(err);
        }
    };

    const updateCategory = async (id, data) => {
        try {
            const result = await apiUpdateCategory(id, data);
            return ok(result);
        } catch (err) {
            return fail(err);
        }
    };

    const deactivateCategory = async (id) => {
        try {
            const result = await apiDeactivateCategory(id);
            return ok(result);
        } catch (err) {
            return fail(err);
        }
    };

    return {
        tree,
        loading,
        refresh: load,
        createCategory,
        updateCategory,
        deactivateCategory,
    };
}