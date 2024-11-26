import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axiosInstance from '../../axiosInstance';
import { FaLock, FaCheckCircle, FaExclamationCircle } from 'react-icons/fa';

const ResetPassword = () => {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();
  const { token } = useParams();

  const handleResetPassword = async () => {
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      const response = await axiosInstance.post('reset-password/', {
        token,
        new_password: newPassword,
      });

      if (response.status === 200) {
        setSuccess('Password has been reset successfully.');
        setTimeout(() => navigate('/login'), 2000);
      }
    } catch (error) {
      setError('An error occurred. Please try again later.');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.box}>
        <h2 style={styles.title}>Reset Password</h2>
        {error && (
          <div style={{ ...styles.message, ...styles.error }}>
            <FaExclamationCircle style={styles.icon} />
            {error}
          </div>
        )}
        {success && (
          <div style={{ ...styles.message, ...styles.success }}>
            <FaCheckCircle style={styles.icon} />
            {success}
          </div>
        )}
        <div style={styles.inputContainer}>
          <FaLock style={styles.inputIcon} />
          <input
            type="password"
            placeholder="New Password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            style={styles.input}
          />
        </div>
        <div style={styles.inputContainer}>
          <FaLock style={styles.inputIcon} />
          <input
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            style={styles.input}
          />
        </div>
        <button onClick={handleResetPassword} style={styles.button}>
          Reset Password
        </button>
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    background: 'linear-gradient(135deg, #000, #ff5733)',
    fontFamily: 'Arial, sans-serif',
  },
  box: {
    width: '100%',
    maxWidth: '400px',
    padding: '30px',
    background: '#fff',
    boxShadow: '0 8px 20px rgba(0, 0, 0, 0.2)',
    borderRadius: '10px',
    textAlign: 'center',
    animation: 'fadeIn 0.8s ease-in-out',
  },
  title: {
    fontSize: '24px',
    marginBottom: '20px',
    color: '#333',
  },
  inputContainer: {
    position: 'relative',
    marginBottom: '20px',
  },
  input: {
    width: '100%',
    padding: '12px 12px 12px 40px',
    fontSize: '16px',
    border: '1px solid #ddd',
    borderRadius: '5px',
    outline: 'none',
    transition: 'border 0.3s',
  },
  inputFocus: {
    borderColor: '#6a11cb',
    boxShadow: '0 0 8px rgba(106, 17, 203, 0.5)',
  },
  inputIcon: {
    position: 'absolute',
    top: '50%',
    left: '12px',
    transform: 'translateY(-50%)',
    color: '#aaa',
    fontSize: '18px',
  },
  button: {
    width: '100%',
    padding: '12px',
    background: 'linear-gradient(135deg, #ff5733, #000)',
    color: '#fff',
    fontSize: '16px',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  message: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '10px',
    marginBottom: '20px',
    borderRadius: '5px',
    fontSize: '14px',
  },
  success: {
    background: '#d4edda',
    color: '#155724',
  },
  error: {
    background: '#f8d7da',
    color: '#721c24',
  },
  icon: {
    marginRight: '8px',
    fontSize: '18px',
  },
};

export default ResetPassword;
