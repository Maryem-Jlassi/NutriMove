import React, { useEffect, useState } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Menu,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from "@mui/material";
import { styled } from "@mui/material/styles";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import axiosInstance from "../../axiosInstance"; // Import your axios instance
import axios from "axios";
import UserProfileDialog from "./UserProfileDialog ";
import { Navigate } from "react-router-dom";

const CustomNavbar = styled(AppBar)(({ theme }) => ({
  background: "linear-gradient(90deg, #000000, #F36100)",
  borderBottom: "2px solid #F36100",
  width: "calc(100% - 200px)",
  marginLeft: "200px",
  position: "fixed",
  top: 0,
  left: 0,
  zIndex: 1030,
  height: "60px",
}));

const Header = () => {
  const [anchorEl, setAnchorEl] = useState(null);
  const [userProfile, setUserProfile] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    const fetchUserProfile = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("No token found.");
        return; // Handle redirect to login
      }

      try {
        const response = await axiosInstance.get("profile-coach/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUserProfile(response.data); // Store the profile data
      } catch (error) {
        console.error("Error fetching user profile:", error.message);
        if (error.response && error.response.status === 401) {
          console.error("Unauthorized access.");
        }
      }
    };

    fetchUserProfile(); // Fetch profile on component mount
  }, []); // Empty dependency array to run once

  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleViewProfile = () => {
    setDialogOpen(true); // Open the dialog to view profile
    handleMenuClose(); // Close the menu when viewing the profile
  };

  const handleLogout = async () => {
    const refreshToken = localStorage.getItem("refresh_token"); // Correctly retrieve the refresh token
    if (!refreshToken) {
      console.error("No refresh token found.");
      return;
    }

    try {
      // Pass both the access and refresh tokens if needed
      await axiosInstance.post(
        "logout-coach/",
        { refresh: refreshToken },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`, // Include access token in headers
          },
        }
      );
      console.log("Logout successful");

      // Clear the tokens from local storage
      localStorage.removeItem("token");
      localStorage.removeItem("refresh_token");

      // Redirect to login page after logout
      window.location.href="/login";
    } catch (error) {
      console.error("Error logging out:", error.message);
    } finally {
      handleMenuClose(); // Close the menu after logout
    }
  };

  const handleDialogClose = () => {
    setDialogOpen(false); // Close the dialog
  };

  return (
    <CustomNavbar>
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}></Typography>
        <IconButton onClick={handleProfileMenuOpen} color="inherit">
          <AccountCircleIcon />
        </IconButton>
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
          sx={{
            '& .MuiPaper-root': {
              backgroundColor: 'black', // Set dropdown background color to black
              color: 'white', // Set text color to white
            }
          }}
        >
          <MenuItem onClick={handleViewProfile} sx={{ color: 'white' }}>Voir Profil</MenuItem>
          <MenuItem onClick={handleLogout} sx={{ color: 'white' }}>Déconnexion</MenuItem>
        </Menu>
      </Toolbar>

      <UserProfileDialog
        open={dialogOpen}
        onClose={handleDialogClose}
        userData={userProfile}
      />
    </CustomNavbar>
  );
};

export default Header;
