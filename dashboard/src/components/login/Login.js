import React, { useState } from "react";
import axiosInstance from "../../axiosInstance";
import { useNavigate } from "react-router-dom";
import FaceRecognition from "./FaceRecognitionLogin";
import { motion } from "framer-motion";
import { Camera } from "lucide-react"; // Added face recognition icon
import {
  MDBBtn,
  MDBContainer,
  MDBCard,
  MDBCardBody,
  MDBCardImage,
  MDBRow,
  MDBCol,
  MDBInput,
} from "mdb-react-ui-kit";
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  CircularProgress,
} from "@mui/material";
import {
  LoginOutlined,
  EmailOutlined,
  LockOutlined,
  PersonOutlined,
  ResetTvOutlined,
} from "@mui/icons-material";
import Cookies from "js-cookie";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [openForgotPassword, setOpenForgotPassword] = useState(false);
  const [resetEmail, setResetEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [isFaceRecognitionOpen, setIsFaceRecognitionOpen] = useState(false);

  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await axiosInstance.post("login-coach/", {
        username,
        password,
      });

      const { token, user } = response.data;

      localStorage.setItem("token", token.access);
      localStorage.setItem("refresh_token", token.refresh);
      localStorage.setItem("isAuthenticated", true);

      if (user.is_client) {
        Cookies.set("access_token", token.access, {
          secure: true,
          sameSite: "strict",
        });
        Cookies.set("refresh_token", token.refresh, {
          secure: true,
          sameSite: "strict",
        });
        Cookies.set("isAuthenticated", true, {
          secure: true,
          sameSite: "strict",
        });
        Cookies.set("user_info", JSON.stringify(user), {
          secure: true,
          sameSite: "strict",
        });
        window.location.href = "http://localhost:8000";
      } else {
        navigate("/dashboard");
      }
    } catch (err) {
      setError(
        err.response?.data?.detail || "Login failed. Please try again later."
      );
    }
  };

  const handlePasswordReset = async () => {
    setLoading(true);
    try {
      const response = await axiosInstance.post("request-password-reset/", {
        identifier: resetEmail,
      });

      if (response.status === 200) {
        alert("Password reset link sent to your email.");
        setOpenForgotPassword(false);
      } else {
        setError("Unable to process your request. Please try again.");
      }
    } catch {
      setError("An error occurred. Please try again later.");
    }
    setLoading(false);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        backgroundColor: "#121212", // Dark Gray Background
      }}
    >
      <MDBContainer>
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{
            type: "spring",
            stiffness: 120,
            damping: 10,
          }}
        >
          <MDBCard
            style={{
              width: "900px",
              margin: "auto",
              boxShadow: "0 4px 6px rgba(0,0,0,0.3)",
              backgroundColor: "#1e1e1e", // Card Background
              color: "#ffffff", // Text Color
            }}
          >
            <MDBRow className="g-0">
              <MDBCol md="6">
                <MDBCardImage
                  src="https://i0.wp.com/weightlosscny.com/wp-content/uploads/2020/09/exercise-nutrition-medical-weight-loss-1.png?w=1080&ssl=1"
                  alt="login form"
                  className="rounded-start w-100 h-100"
                  style={{ objectFit: "cover" }}
                />
              </MDBCol>

              <MDBCol md="6" className="d-flex align-items-center">
                <MDBCardBody className="p-4 w-100">
                  <motion.div
                    initial={{ y: -50, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="text-center mb-4"
                  >
                    <motion.div
                      animate={{
                        rotate: [0, 10, -10, 0],
                        scale: [1, 1.1, 1],
                      }}
                      transition={{
                        duration: 0.5,
                        repeat: 1,
                        repeatType: "mirror",
                      }}
                    >
                      <PersonOutlined
                        style={{ fontSize: "4rem", color: "#f36100" }} // Orange
                      />
                    </motion.div>
                    <h2 className="mt-2" style={{ color: "#f36100" }}>
                      Welcome Back!
                    </h2>
                  </motion.div>

                  {error && (
                    <motion.p
                      initial={{ x: -20 }}
                      animate={{ x: 0 }}
                      transition={{ type: "spring", stiffness: 300 }}
                      style={{
                        color: "#ff3d00", // Bright Red for errors
                        textAlign: "center",
                        marginBottom: "15px",
                      }}
                    >
                      {error}
                    </motion.p>
                  )}

                  <motion.div
                    initial={{ x: -50, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.3 }}
                  >
                    <MDBInput
                      className="mb-3"
                      label="Username"
                      type="text"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      style={{ color: "white" }} // Input text white
                      labelStyle={{ color: "white" }} // Label text white
                      leftIcon={
                        <motion.div
                          whileHover={{ scale: 1.2, rotate: 360 }}
                          transition={{ type: "spring", stiffness: 300 }}
                        >
                          <PersonOutlined style={{ color: "#f36100" }} />
                        </motion.div>
                      }
                    />

                    <MDBInput
                      className="mb-3"
                      label="Password"
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      style={{ color: "white" }} // Input text white
                      labelStyle={{ color: "white" }} // Label text white
                      leftIcon={
                        <motion.div
                          whileHover={{ scale: 1.2, rotate: 360 }}
                          transition={{ type: "spring", stiffness: 300 }}
                        >
                          <LockOutlined style={{ color: "#f36100" }} />
                        </motion.div>
                      }
                    />
                  </motion.div>

                  <motion.div
                    initial={{ y: 50, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.4 }}
                  >
                    <div className="d-flex align-items-center justify-content-between">
                      <MDBBtn
                        style={{
                          backgroundColor: "#f36100",
                          borderColor: "#f36100",
                          color: "#fff",
                        }}
                        className="w-100 mb-3"
                        onClick={handleLogin}
                      >
                        <LoginOutlined
                          style={{ marginRight: "10px", color: "#ffffff" }}
                        />
                        Login
                      </MDBBtn>

                      {/* New Face Recognition Icon */}
                      <motion.div
                        whileHover={{ scale: 1.2 }}
                        whileTap={{ scale: 0.9 }}
                        style={{
                          marginLeft: "10px",
                          cursor: "pointer",
                          color: "#f36100",
                        }}
                        onClick={() => setIsFaceRecognitionOpen(true)} // Add this line
                      >
                        <Camera size={30} />
                      </motion.div>

                      <FaceRecognition
                        open={isFaceRecognitionOpen}
                        onClose={() => setIsFaceRecognitionOpen(false)}
                        onLoginSuccess={(userData) => {
                          // Add the same login success logic as in handleLogin
                          localStorage.setItem("token", userData.token.access);
                          localStorage.setItem(
                            "refresh_token",
                            userData.token.refresh
                          );
                          localStorage.setItem("isAuthenticated", true);

                          Cookies.set("access_token", userData.token.access, {
                            secure: true,
                            sameSite: "strict",
                          });
                          Cookies.set("refresh_token", userData.token.refresh, {
                            secure: true,
                            sameSite: "strict",
                          });
                          Cookies.set("isAuthenticated", true, {
                            secure: true,
                            sameSite: "strict",
                          });
                          Cookies.set(
                            "user_info",
                            JSON.stringify(userData.user),
                            {
                              secure: true,
                              sameSite: "strict",
                            }
                          );

                          if (userData.user.is_client) {
                            window.location.href = "http://localhost:8000"; // Or navigate to the client home page
                          } else {
                            navigate("/dashboard");
                          }
                        }}
                      />
                    </div>
                    <div className="text-center">
                      <motion.a
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setOpenForgotPassword(true)}
                        style={{
                          color: "#f36100",
                          textDecoration: "underline",
                          cursor: "pointer",
                        }}
                      >
                        Forgot Password?
                      </motion.a>

                      <p className="mt-3">
                        Don't have an account?{" "}
                        <motion.a
                          href="/register"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                          style={{ color: "#f36100" }}
                        >
                          Register
                        </motion.a>
                      </p>
                    </div>
                  </motion.div>
                </MDBCardBody>
              </MDBCol>
            </MDBRow>
          </MDBCard>
        </motion.div>

        {/* Forgot Password Dialog */}
        <Dialog
          open={openForgotPassword}
          onClose={() => setOpenForgotPassword(false)}
          maxWidth="sm"
          fullWidth
        >
          <DialogTitle style={{ color: "#f36100", fontWeight: "bold" }}>
            Reset Your Password
          </DialogTitle>
          <DialogContent>
            <p
              className="text-muted mb-3"
              style={{ color: "#f36100", fontSize: "16px" }}
            >
              Enter your email to receive a reset link.
            </p>
            <MDBInput
              label="Email"
              value={resetEmail}
              onChange={(e) => setResetEmail(e.target.value)}
              style={{ color: "#f36100" }} // Makes the input text color match the theme
              labelStyle={{ color: "#000000" }} // Ensures the label is black
              leftIcon={<EmailOutlined style={{ color: "#f36100" }} />}
            />
            <div className="text-center mt-4">
              <MDBBtn
                size="sm" // Makes the button smaller
                style={{
                  backgroundColor: "#f36100",
                  borderColor: "#f36100",
                  color: "#ffffff",
                  width: "auto", // Adjusts the width to the content size
                  padding: "10px 20px", // Adjusts padding for a better fit if needed
                }}
                onClick={handlePasswordReset}
                disabled={loading}
              >
                {loading ? (
                  <CircularProgress size={20} style={{ color: "#ffffff" }} />
                ) : (
                  <>
                    <ResetTvOutlined
                      style={{ marginRight: "10px", color: "#ffffff" }}
                    />
                    Send Reset Link
                  </>
                )}
              </MDBBtn>
            </div>
          </DialogContent>

          <DialogActions>
            <MDBBtn
              outline
              color="secondary"
              onClick={() => setOpenForgotPassword(false)}
            >
              Close
            </MDBBtn>
          </DialogActions>
        </Dialog>
      </MDBContainer>
    </motion.div>
  );
};

export default Login;
