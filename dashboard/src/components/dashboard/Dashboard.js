import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import { styled } from '@mui/material/styles';
import CoachingTable from './CoachingTable'; // You can add other components like Nutrition and Home
import NutriTable from './NutriTable';
import HomeStatistics from './HomeStatistics';

// Dashboard Container styled component
const DashboardContainer = styled('div')({
  backgroundColor: '#f4f6f9', // Light gray background for a clean look
  minHeight: '100vh',
  padding: '20px',
  marginLeft: '200px', // Align with the sidebar
  paddingTop: '60px', // Space for the header
});

const Dashboard = () => {
  const [activeSection, setActiveSection] = useState('home');  // Initial section is 'home'

  const handleSelectItem = (item) => {
    setActiveSection(item);  // Set the active section based on the clicked item
  };

  return (
    <div>
      <Header />
      <Sidebar onSelectItem={handleSelectItem} activeSection={activeSection} />
      <DashboardContainer>
        {/* Home Section */}
        {activeSection === 'home' && <HomeStatistics />}

        {/* Coaching Section */}
        {activeSection === 'coaching' && <CoachingTable />}

        {/* Nutrition Section */}
        {activeSection === 'nutrition' && <NutriTable />}
      </DashboardContainer>
    </div>
  );
};

export default Dashboard;
