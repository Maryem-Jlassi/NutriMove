import React, { useState, useRef, useEffect } from "react";
import {
  Button,
  Box,
  Typography,
  Grid,
  Card,
  Table,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  Snackbar,
  Alert,
  CircularProgress,
} from "@mui/material";
import axiosInstance from "../../axiosInstance";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile"; // Import file icon

const NutriTable = () => {
  const [clients, setClients] = useState([]);
  const [coachId, setCoachId] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedClient, setSelectedClient] = useState(null);
  const [loading, setLoading] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarSeverity, setSnackbarSeverity] = useState("success");
  const fileInputRef = useRef(null);

  // Fetch coach profile
  const fetchCoachProfile = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      console.error("No token found.");
      return;
    }

    try {
      const response = await axiosInstance.get("profile-coach/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setCoachId(response.data.id);
    } catch (error) {
      console.error("Error fetching user profile:", error.message);
    }
  };

  // Fetch clients
  const fetchClients = () => {
    if (coachId) {
      axiosInstance
        .get(`${coachId}/clients/`)
        .then((response) => {
          setClients(response.data);
        })
        .catch((error) => {
          console.error("Error fetching clients:", error);
        });
    }
  };

  useEffect(() => {
    fetchCoachProfile();
  }, []);

  useEffect(() => {
    if (coachId) {
      fetchClients();
    }
  }, [coachId]);

  // Handle file input changes
  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  // Handle file upload
  const handleUploadProgram = (clientId) => {
    if (!selectedFile) {
      setSnackbarMessage("Please select an Excel file to upload.");
      setSnackbarSeverity("error");
      setSnackbarOpen(true);
      return;
    }

    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append("file", selectedFile);

    setLoading(true);

    axiosInstance
      .post(`assign-program/${clientId}/`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then(() => {
        setSnackbarMessage("Program assigned successfully!");
        setSnackbarSeverity("success");
        setSelectedFile(null);
        fetchClients(); // Refresh clients after upload
      })
      .catch((error) => {
        console.error("Error assigning program:", error);
        setSnackbarMessage("Error assigning program. Please try again.");
        setSnackbarSeverity("error");
      })
      .finally(() => {
        setLoading(false);
        setSnackbarOpen(true);
      });
  };

  // Handle program deletion
  const handleDeleteProgram = (clientId) => {
    const token = localStorage.getItem("token");
    axiosInstance
      .delete(`delete-program/${clientId}/`, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${token}`,
        },
      })
      .then(() => {
        setSnackbarMessage("Program deleted successfully.");
        setSnackbarSeverity("success");
        fetchClients(); // Refresh clients after deletion
      })
      .catch((error) => {
        console.error("Error deleting program:", error);
        setSnackbarMessage("Error deleting program. Please try again.");
        setSnackbarSeverity("error");
      })
      .finally(() => {
        setSnackbarOpen(true);
      });
  };

  // Close snackbar
  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };

  // Open file input dialog
  const openFileInput = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <Box sx={{ padding: 3 }}>
      <Grid container justifyContent="center" spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h4" color="primary" align="center" gutterBottom>
            Nutrition Clients Management
          </Typography>
        </Grid>

        <Grid item xs={12} md={10} lg={13}>
          <Card sx={{ padding: 2, boxShadow: 3, width: "100%" }}>
            <TableContainer component={Paper}>
              <Table sx={{ minWidth: 650 }}>
                <TableHead>
                  <TableRow>
                    <TableCell sx={{ fontWeight: "bold", fontSize: 14 }}>Photo</TableCell>
                    <TableCell sx={{ fontWeight: "bold", fontSize: 14 }}>Name</TableCell>
                    <TableCell sx={{ fontWeight: "bold", fontSize: 14 }}>Age</TableCell>
                    <TableCell sx={{ fontWeight: "bold", fontSize: 14 }}>Weight</TableCell>
                    <TableCell sx={{ fontWeight: "bold", fontSize: 14 }}>Height</TableCell>
                    <TableCell sx={{ fontWeight: "bold", fontSize: 14 }}>Activity</TableCell>
                    <TableCell sx={{ fontWeight: "bold", fontSize: 14 }}>Goal Weight</TableCell>
                    <TableCell sx={{ fontWeight: "bold", fontSize: 14 }}>Program</TableCell>
                    <TableCell sx={{ fontWeight: "bold", fontSize: 14 }}>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {clients.map((client) => (
                    <TableRow key={client.id}>
                      <TableCell>
                        <img
                          src={
                            client.photo ||
                            "https://e7.pngegg.com/pngimages/946/556/png-clipart-computer-icons-login-user-profile-client-smiley-%D0%B7%D0%BD%D0%B0%D1%87%D0%BA%D0%81.png"
                          }
                          alt={client.first_name}
                          style={{ width: 60, height: 30 }}
                          className="rounded-circle"
                        />
                      </TableCell>
                      <TableCell>{client.first_name} {client.last_name}</TableCell>
                      <TableCell>{client.age || "N/A"}</TableCell>
                      <TableCell>{client.weight} kg</TableCell>
                      <TableCell>{client.height} cm</TableCell>
                      <TableCell>{client.activity_level || "N/A"}</TableCell>
                      <TableCell>{client.goal_weight || "N/A"} kg</TableCell>

                      {/* Program Column */}
                      <TableCell>
                        {client.program_nutrition ? (
                          <>
                            <InsertDriveFileIcon fontSize="small" style={{ verticalAlign: "middle" }} />
                            <a
                              href={client.program_nutrition}
                              target="_blank"
                              rel="noopener noreferrer"
                              style={{ marginLeft: 5, fontSize: "14px" }}
                            >
                              {client.program_nutrition.split("/").pop()}
                            </a>

                          </>
                        ) : (
                          "No Program"
                        )}
                      </TableCell>

                      <TableCell>
                        <Button
                          variant="contained"
                          color="primary"
                          onClick={() => {
                            setSelectedClient(client);
                            openFileInput();
                          }}
                          startIcon={<UploadFileIcon />}
                          size="small"
                          sx={{ fontSize: "12px" }} // Reduces button font size
                        >
                          {client.program_nutrition 
                            ? "Update Program"
                            : "Upload Program"}
                        </Button>

                        {/* Hidden file input */}
                        <input
                          ref={fileInputRef}
                          type="file"
                          accept=".xlsx, .xls"
                          onChange={handleFileChange}
                          style={{ display: "none" }}
                        />

                        {/* Show the upload button when a file is selected */}
                        {selectedClient?.id === client.id && selectedFile && (
                          <Button
                            variant="contained"
                            color="secondary"
                            size="small"
                            onClick={() => handleUploadProgram(client.id)}
                            sx={{ fontSize: "12px", marginTop: 1 }}
                          >
                            {loading ? <CircularProgress size={24} /> : "Upload"}
                          </Button>
                        )}

                        {client.program_nutrition  ? (
                          <Button
                            variant="outlined"
                            color="error"
                            onClick={() => handleDeleteProgram(client.id)}
                            size="small"
                            sx={{ fontSize: "12px", marginTop: 1 }}
                          >
                            Delete
                          </Button>
                        ) : null}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Card>
        </Grid>
      </Grid>

      {/* Snackbar for error/success messages */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity={snackbarSeverity}
          sx={{ width: "100%" }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default NutriTable;
