export default function AuthLayout({title, children}){
    return (
        <div style={{ maxWidth: 400, margin: "50px auto" }}>
            <h2>{title}</h2>
            {children}
        </div>
    )
}
