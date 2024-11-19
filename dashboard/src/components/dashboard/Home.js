import React from 'react';

const Home = () => {
  return (
    <div style={styles.homeContainer}>
      <h1 style={styles.welcomeText}>Welcome to the Dashboard!</h1>
      <p style={styles.descriptionText}>This is the home page for coaches and nutritionists.</p>
    </div>
  );
};

const styles = {
  homeContainer: {
    padding: '20px',
    marginTop: '60px',
    transition: '0.5s',
    color: '#FFFFFF', // White text for contrast
  },
  welcomeText: {
    fontSize: '2rem',
    marginBottom: '10px',
  },
  descriptionText: {
    fontSize: '1.2rem',
    color: '#B0BEC5', // Light gray for description
  },
};

export default Home;
