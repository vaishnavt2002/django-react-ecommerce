export default function AuthLayout({title, subtitle, children}){
    return (
        <div className="min-h-screen flex">
            <div className="hidden lg:block lg:w-1/2 bg-gray-200">

            </div>
            <div className="flex w-full lg:w-1/2 items-center justify-center">
                <div className="w-full max-w-md px-6 py-10">
                    <h1 className="text-2xl font-semibold mb-2">{title}</h1>
                    {subtitle && (
                        <p className="text-gray-500 mb-6">
                            {subtitle}
                        </p>
                    )}
                    {children}
                </div>
            </div>
            
        </div>
    )
}
