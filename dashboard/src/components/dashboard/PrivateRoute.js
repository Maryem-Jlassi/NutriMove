import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import SessionExpiredPopup from '../login/SessionExpiredPopup'; // Importer le popup

const PrivateRoute = ({ children }) => {
  const [isSessionExpired, setIsSessionExpired] = useState(false); // État pour afficher le popup

  // Vérification de la validité du token
  const checkTokenValidity = () => {
    const token = localStorage.getItem('token'); // Récupérer le token du localStorage
    if (!token) {
      setIsSessionExpired(true); // Si pas de token, session expirée
      return;
    }

    const tokenExpiry = JSON.parse(atob(token.split('.')[1])).exp;
    const currentTime = Math.floor(Date.now() / 1000);

    if (tokenExpiry < currentTime) {
      setIsSessionExpired(true); // Si le token est expiré
    }
  };

  useEffect(() => {
    checkTokenValidity(); // Vérification lors du montage du composant
  }, []);

  const handleSessionClose = () => {
    setIsSessionExpired(false);
    window.location.href = '/login'; // Rediriger vers la page de connexion
  };

  // Si la session est expirée, afficher le popup
  if (isSessionExpired) {
    return <SessionExpiredPopup onClose={handleSessionClose} />;
  }

  // Si le token est valide, afficher les enfants (le contenu de la route)
  return children;
};

export default PrivateRoute;
