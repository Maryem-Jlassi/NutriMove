import React, { useState } from 'react';
import 'mdb-react-ui-kit/dist/css/mdb.min.css';
import { MDBContainer, MDBInput, MDBBtn } from 'mdb-react-ui-kit';
import { Dialog, DialogActions, DialogContent, DialogTitle, CircularProgress, Fade } from '@mui/material';
import axiosInstance from '../../axiosInstance';

const ForgotPassword = () => {
  const [identifier, setIdentifier] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);

  const handleRequestReset = async () => {
    setLoading(true);
    try {
      const response = await axiosInstance.post('request-password-reset/', {
        identifier: identifier,
      });

      setLoading(false);
      if (response.status === 200) {
        setMessage('A password reset link has been sent to your email.');
        setError('');
      } else {
        setError('Unable to process request. Please try again.');
        setMessage('');
      }
    } catch (error) {
      setLoading(false);
      setError('An error occurred. Please try again later.');
      setMessage('');
    }
  };

  const handleClose = () => {
    setOpen(false);
  };

  // CSS styles
  const styles = {
    dialogTitle: {
      fontSize: '1.5rem',
      fontWeight: 'bold',
      textAlign: 'center',
      color: '#00000',
    },
    dialogContent: {
      textAlign: 'center',
    },
    inputWrapper: {
      marginBottom: '1rem',
    },
    btnSendLink: {
      fontSize: '0.9rem',
      padding: '8px 20px',
      borderRadius: '5px',
      textTransform: 'none',
    },
    messageBox: {
      margin: '1rem 0',
      padding: '0.5rem',
      borderRadius: '5px',
      fontSize: '0.9rem',
    },
    successMessage: {
      backgroundColor: '#d4edda',
      color: '#155724',
      border: '1px solid #c3e6cb',
    },
    errorMessage: {
      backgroundColor: '#f8d7da',
      color: '#721c24',
      border: '1px solid #f5c6cb',
    },
    actionButtons: {
      display: 'flex',
      justifyContent: 'space-between',
    },
    btnClose: {
      textTransform: 'none',
    },
  };

  return (
    <MDBContainer className="my-5 text-center">
      <MDBBtn color="link" className="text-decoration-underline" onClick={() => setOpen(true)}>
        Forgot Password?
      </MDBBtn>

      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle style={styles.dialogTitle}>Reset Your Password</DialogTitle>
        <DialogContent style={styles.dialogContent}>
          <p className="text-muted">Enter your email or username to reset your password.</p>

          <Fade in={!!message}>
            <div style={{ ...styles.messageBox, ...styles.successMessage }}>{message}</div>
          </Fade>
          <Fade in={!!error}>
            <div style={{ ...styles.messageBox, ...styles.errorMessage }}>{error}</div>
          </Fade>

          <MDBInput
            wrapperClass="mb-4"
            style={styles.inputWrapper}
            label="Email or Username"
            id="identifier"
            type="text"
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
            required
          />

          <div>
            <MDBBtn
              style={styles.btnSendLink}
              color="primary"
              type="button"
              onClick={handleRequestReset}
              disabled={loading || !identifier.trim()}
            >
              {loading ? <CircularProgress size={16} color="inherit" /> : 'Send Reset Link'}
            </MDBBtn>
          </div>
        </DialogContent>

        <DialogActions style={styles.actionButtons}>
          <MDBBtn outline color="secondary" style={styles.btnClose} onClick={handleClose}>
            Close
          </MDBBtn>
          <MDBBtn outline color="danger" style={styles.btnClose} onClick={handleClose}>
            Back to Login
          </MDBBtn>
        </DialogActions>
      </Dialog>
    </MDBContainer>
  );
};

export default ForgotPassword;
