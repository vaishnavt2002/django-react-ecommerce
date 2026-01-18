import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Register from './pages/Register'
import VerifyOtp from './pages/VerifyOtp'
import Login from './pages/Login'
import AuthRoutes from './routes/AuthRoutes'
import AdminRoutes from './routes/AdminRoutes'

function App() {

  return (
    <BrowserRouter>
      <AuthRoutes/>
      <AdminRoutes/>
    </BrowserRouter>
  )
}

export default App
