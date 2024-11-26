import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Drawer, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import { styled } from '@mui/material/styles';
import HomeIcon from '@mui/icons-material/Home';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import LockIcon from '@mui/icons-material/Lock';

const drawerWidth = 200;

const CustomDrawer = styled(Drawer)(({ theme }) => ({
  width: drawerWidth,
  flexShrink: 0,
  '& .MuiDrawer-paper': {
    width: drawerWidth,
    boxSizing: 'border-box',
    backgroundColor: '#000000',
    color: '#f5f5f5',
    overflowY: 'auto',
    overflowX: 'hidden',
  },
}));

const CustomListItem = styled(ListItem)(({ theme, selected, disabled }) => ({
  transition: theme.transitions.create(['background-color', 'transform'], {
    easing: theme.transitions.easing.easeInOut,
    duration: theme.transitions.duration.short,
  }),
  backgroundColor: selected ? '#F36100' : 'transparent',
  color: disabled ? '#9e9e9e' : '#f5f5f5', // Couleur grise si désactivé
  borderRadius: '8px',
  margin: '20px 0',
  '&:hover': {
    backgroundColor: disabled ? 'transparent' : '#F36100', // Ne pas changer la couleur si désactivé
    transform: disabled ? 'none' : 'scale(1.05)',
  },
  '&.Mui-selected': {
    backgroundColor: disabled ? 'transparent' : '#F36100',
    transform: disabled ? 'none' : 'scale(1.02)',
  },
}));

const Sidebar = ({ activeSection, onSelectItem }) => {
  const navigate = useNavigate();
  const [isCoach, setIsCoach] = useState(false);
  const [isNutritionist, setIsNutritionist] = useState(false);

  useEffect(() => {
    const coachStatus = localStorage.getItem('is_coach') === 'true';
    const nutritionistStatus = localStorage.getItem('is_nutritionist') === 'true';

    setIsCoach(coachStatus);
    setIsNutritionist(nutritionistStatus);
  }, []);

  const menuItems = [
    { name: 'home', label: 'Home', icon: <HomeIcon sx={{ color: '#f5f5f5' }} />, accessible: true },
    {
      name: 'coaching',
      label: 'Coaching',
      icon: <FitnessCenterIcon sx={{ color: isCoach ? '#f5f5f5' : '#9e9e9e' }} />,
      accessible: isCoach,
    },
    {
      name: 'nutrition',
      label: 'Nutrition',
      icon: <RestaurantIcon sx={{ color: isNutritionist ? '#f5f5f5' : '#9e9e9e' }} />,
      accessible: isNutritionist,
    },
  ];

  return (
    <CustomDrawer variant="permanent">
      <List sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: '200px' }}>
        {menuItems.map((item) => (
          <CustomListItem
            key={item.name}
            selected={activeSection === item.name}
            onClick={() => {
              if (item.accessible) {
                onSelectItem(item.name);
              }
            }}
            disabled={!item.accessible} // Désactiver le bouton si l'accès n'est pas autorisé
          >
            <ListItemIcon>
              {item.accessible ? item.icon : <LockIcon sx={{ color: '#9e9e9e' }} />} {/* Cadenas si inactif */}
            </ListItemIcon>
            <ListItemText primary={item.label} />
          </CustomListItem>
        ))}
      </List>
    </CustomDrawer>
  );
};

export default Sidebar;
