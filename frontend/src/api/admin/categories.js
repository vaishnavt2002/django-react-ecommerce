import apiClient from "../client";

export const fetchCatagoryTree = async () => {
    const res = await apiClient.get("/api/admin/categories/");
    return res.data
};

export const createCategory = async (data) => {
    const res = await apiClient.post("/api/admin/categories/", data);
    return res.data;
};

export const updateCategory = async (id, data) => {
    const res = await apiClient.put(`/api/admin/categories/${id}/`, data)
    return res.data;

};

export const deactivateCategory = async (id) => {
    const res = await apiClient.patch(`/api/admin/categories/${id}/deactivate/`)
    return res.data;
}





