import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './components/dashboard/Dashboard';
import Login from './components/login/Login';
import Register from './components/login/Register';
import CoachingTable from './components/dashboard/CoachingTable';
import NutriTable from './components/dashboard/NutriTable';
import PrivateRoute from './components/dashboard/PrivateRoute';
import ForgotPassword from './components/login/ForgotPassword';
import ResetPassword from './components/login/ResetPassword';
import FaceRecognition from './components/login/FaceRecognitionLogin'

const App = () => {
  return (
    <Router
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <Routes>
        {/*<Route path="/FaceRecognition" element={<FaceRecognition />} />*/}
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* Use PrivateRoute to protect access to the Dashboard */}
        <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        
        {/* Other routes */}
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/users/reset-password/:token" element={<ResetPassword />} />
        <Route path="/coach" element={<CoachingTable />} />
        <Route path="/nutrition" element={<NutriTable />} />
      </Routes>
    </Router>
  );
};

export default App;