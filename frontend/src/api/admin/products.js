import apiClient from "../client";

export const fetchAdminProducts = async ()=> {
    const res = await apiClient.get("api/catalog/admin/products/");
    return res.data;
};

export const createAdminProduct = async (data) => {
    const res = await apiClient.post("api/catalog/admin/products/", data);
    return res.data
};

export const updateAdminProduct = async (id, data) => {
    const res = await apiClient.put(`api/catalog/admin/products/${id}/`, data);
    return res.data
}

export const disableAdminProduct = async (id) => {
    const res = await apiClient.patch(
        `api/catalog/admin/products/${id}/`,
        {is_active: false}
    );
    return res.data
}