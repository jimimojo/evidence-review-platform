import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Container, AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import Dashboard from './components/Dashboard';
import ReviewForm from './components/ReviewForm';
import Login from './components/Login';
import Register from './components/Register';

function App() {
  const [isAuthenticated, setIsAuthenticated] = React.useState(false);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Evidence Review Platform
            </Typography>
            {isAuthenticated ? (
              <Button color="inherit" onClick={handleLogout}>Logout</Button>
            ) : (
              <>
                <Button color="inherit" href="/login">Login</Button>
                <Button color="inherit" href="/register">Register</Button>
              </>
            )}
          </Toolbar>
        </AppBar>
        <Container maxWidth="lg" sx={{ mt: 4 }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/review/new" element={<ReviewForm />} />
            <Route path="/login" element={<Login setAuth={setIsAuthenticated} />} />
            <Route path="/register" element={<Register />} />
          </Routes>
        </Container>
      </Box>
    </Router>
  );
}

export default App;
