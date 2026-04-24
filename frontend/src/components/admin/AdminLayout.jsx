import React from 'react'
import AdminSidebar from './AdminSidebar'
import { Outlet } from 'react-router-dom'

export const AdminLayout = () => {
  return (
    <div className='flex min-h-screen bg-gray-100'>
        <AdminSidebar/>
        <main className='flex-1 p-10'>
            <div className="max-w-6xl mx-auto">
                <Outlet/>
            </div>
        </main>
    </div>
  )
}
