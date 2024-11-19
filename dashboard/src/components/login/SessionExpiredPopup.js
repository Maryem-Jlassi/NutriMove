import React from 'react';
import styled from 'styled-components';
import { FaExclamationCircle } from 'react-icons/fa';

// Overlay avec animation
const Overlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.5s forwards;

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }
`;

// Popup avec animation
const Popup = styled.div`
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
  width: 320px;
  transform: scale(0.9);
  animation: popupAnimation 0.3s forwards;

  @keyframes popupAnimation {
    from {
      transform: scale(0.9);
    }
    to {
      transform: scale(1);
    }
  }
`;

const PopupHeader = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
`;

const PopupTitle = styled.h2`
  font-size: 22px;
  color: #333;
  font-weight: bold;
  margin: 0;
`;

const PopupMessage = styled.p`
  margin-bottom: 20px;
  color: #555;
  font-size: 16px;
`;

const PopupButton = styled.button`
  background-color: #ff5733;
  color: #fff;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background-color: #ff4500;
    transform: scale(1.05);
  }

  &:focus {
    outline: none;
  }
`;

const SessionExpiredPopup = ({ onClose }) => {
  return (
    <Overlay>
      <Popup>
        <PopupHeader>
          <FaExclamationCircle style={{ fontSize: '40px', color: '#ff5733', marginRight: '10px' }} />
          <PopupTitle>Session Expirée</PopupTitle>
        </PopupHeader>
        <PopupMessage>
          Oh non! Votre session a expiré. <br />
          Veuillez vous reconnecter pour continuer votre parcours.
        </PopupMessage>
        <PopupButton onClick={onClose}>Reconnectez-vous</PopupButton>
      </Popup>
    </Overlay>
  );
};

export default SessionExpiredPopup;
