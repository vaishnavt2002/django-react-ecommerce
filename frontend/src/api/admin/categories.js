import apiClient  from "../client";

export const fetchAdminCatagories = async () => {
    const res = await apiClient.get("/api/catalog/admin/categories/");
    return res.data
};

