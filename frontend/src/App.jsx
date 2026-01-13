import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Register from './pages/Register'
import VerifyOtp from './pages/VerifyOtp'
import Login from './pages/Login'

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Navigate to="/auth/register" replace/>} />
        <Route path="/auth/register" element={<Register/>}/>
        <Route path="/auth/verify-otp" element={<VerifyOtp/>}/>
        <Route path="/auth/login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
