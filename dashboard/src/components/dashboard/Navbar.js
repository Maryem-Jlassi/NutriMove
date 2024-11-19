// src/components/Navbar.js
import React from 'react';
import { AppBar, Toolbar, Typography, IconButton, Menu, MenuItem } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { styled } from '@mui/material/styles';

// Styled AppBar with a gradient background
const CustomNavbar = styled(AppBar)(({ theme }) => ({
  background: 'linear-gradient(90deg, #000000, #1976D2)', // Dégradé noir à bleu
  borderBottom: '2px solid #1976D2',
  width: 'calc(100% - 250px)',
  marginLeft: '250px',
  boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
  position: 'fixed',
  top: 0,
  left: 0,
  zIndex: 1030,
  height: '60px',
}));

const Navbar = () => {
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <CustomNavbar position="static">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          {/* Title removed */}
        </Typography>
        <IconButton onClick={handleProfileMenuOpen} color="inherit">
          <AccountCircleIcon />
        </IconButton>
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
        >
          <MenuItem onClick={handleMenuClose}>Voir Profil</MenuItem>
          <MenuItem onClick={handleMenuClose}>Déconnexion</MenuItem>
        </Menu>
      </Toolbar>
    </CustomNavbar>
  );
};

export default Navbar;
