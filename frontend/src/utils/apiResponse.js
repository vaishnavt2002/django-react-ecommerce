export const ok = (data) => ({ success: true, data })
export const fail = (err) => (
    {
        success: false,
        errors: err.response?.data || { error: "Something went wrong" }
    }
)