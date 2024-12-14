import React, { useState, useRef, useCallback } from "react";
import Webcam from "react-webcam";
import axiosInstance from "../../axiosInstance";
import { motion } from "framer-motion";
import { Dialog, DialogContent, DialogTitle } from "@mui/material";
import { MDBBtn, MDBSpinner } from "mdb-react-ui-kit";

const FaceRecognitionLogin = ({ open, onClose, onLoginSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const webcamRef = useRef(null);

  const captureAndSubmit = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const imageSrc = webcamRef.current.getScreenshot();
      const blob = await (await fetch(imageSrc)).blob();

      const formData = new FormData();
      formData.append("image", blob, "face.jpg");

      const response = await axiosInstance.post("coach-face-login/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      onLoginSuccess(response.data);
      onClose();
    } catch (err) {
      setError(
        err.response?.data?.detail || "Face recognition failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }, [onLoginSuccess, onClose]);

  const videoConstraints = {
    width: 420,
    height: 420,
    facingMode: "user",
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      PaperProps={{ style: { backgroundColor: "#1e1e1e", color: "#ffffff" } }}
    >
      <DialogTitle style={{ color: "#f36100", textAlign: "center", fontWeight: "bold" }}>
        Face Recognition Login
      </DialogTitle>
      <DialogContent>
        {error && (
          <motion.p
            initial={{ x: -20 }}
            animate={{ x: 0 }}
            transition={{ type: "spring", stiffness: 300 }}
            style={{ color: "#ff3d00", textAlign: "center", marginBottom: "15px" }}
          >
            {error}
          </motion.p>
        )}
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          videoConstraints={videoConstraints}
          style={{
            width: "100%",
            height: "auto",
            borderRadius: "10px",
            marginBottom: "20px",
          }}
        />
        <div style={{ display: "flex", justifyContent: "center" }}>
          <MDBBtn
            style={{ backgroundColor: "#f36100", borderColor: "#f36100", color: "#fff" }}
            onClick={captureAndSubmit}
            disabled={loading}
          >
            {loading ? <MDBSpinner size="sm" role="status" /> : "Recognize Face"}
          </MDBBtn>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default FaceRecognitionLogin;
