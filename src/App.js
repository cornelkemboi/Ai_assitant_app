// import React from 'react';
// import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
// import Register from './components/Register';
// import Login from './components/Login';
// import FileUpload from './components/FileUpload';
// import DocumentViewer from './components/DocumentViewer';

// function App() {
//     return (
//         <Router>
//             <Routes>
//                 <Route path="/" element={<Navigate to="/login" />} />
//                 <Route path="/login" element={<Login />} />
//                 <Route path="/register" element={<Register />} />
//                 <Route path="/upload/" element={<FileUpload />} />
//                 <Route path="/documents/:id" element={<DocumentViewer />} />
//             </Routes>
//         </Router>
//     );
// }

// export default App;
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import FileUpload from './components/FileUpload';
import DocumentViewer from './components/DocumentViewer';
import Register from './components/Register';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';


const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));

  const handleLogin = (token) => {
    localStorage.setItem('token', token);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
  };

  return (
    <Router>
      <nav>
        <Link to="/">Home</Link>
        {isLoggedIn && (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <button onClick={handleLogout}>Logout</button>
          </>
        )}
      </nav>
      <div className="container">
        <Routes>
          <Route path="/" element={isLoggedIn ? <Navigate to="/dashboard" /> : <Login onLogin={handleLogin} />} />
          <Route path="/dashboard" element={isLoggedIn ? <Dashboard onLogout={handleLogout} /> : <Navigate to="/" />} />
          <Route path="/upload" element={isLoggedIn ? <FileUpload /> : <Navigate to="/" />} />
          <Route path="/documents/:id" element={isLoggedIn ? <DocumentViewer /> : <Navigate to="/" />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;

