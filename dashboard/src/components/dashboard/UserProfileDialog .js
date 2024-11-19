import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button } from '@mui/material';
import { MDBCol, MDBRow, MDBCard, MDBCardText, MDBCardBody, MDBCardImage, MDBTypography, MDBIcon } from 'mdb-react-ui-kit';

const UserProfileDialog = ({ open, onClose, userData }) => {
    if (!userData) {
        return (
            <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
                <DialogTitle>User Profile</DialogTitle>
                <DialogContent>
                    <p>Loading user data...</p>
                </DialogContent>
                <DialogActions>
                    <Button onClick={onClose} color="primary">Close</Button>
                </DialogActions>
            </Dialog>
        );
    }

    return (
        <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
            <DialogTitle>User Profile</DialogTitle>
            <DialogContent>
                <MDBCol lg="12">
                    <MDBCard className="mb-3" style={{ borderRadius: '.5rem' }}>
                        <MDBRow className="g-0">
                            <MDBCol md="3" className="text-center text-white"
                                style={{
                                    borderTopLeftRadius: '.5rem',
                                    borderBottomLeftRadius: '.5rem',
                                    background: 'linear-gradient(to right bottom, rgba(246, 211, 101, 1), rgba(253, 160, 133, 1))'
                                }}>
                                <MDBCardImage
                                    src={userData.photo}
                                    alt="Avatar" className="my-5" style={{ width: '80px' }} fluid />
                                <MDBTypography tag="h5">{userData?.username}</MDBTypography>
                                <MDBCardText>{userData?.specialization || 'Fitness'}</MDBCardText>
                                <MDBIcon far icon="edit mb-5" onClick={onClose} style={{ cursor: 'pointer' }} />
                            </MDBCol>
                            <MDBCol md="9">
                                <MDBCardBody className="p-4">
                                    <MDBTypography tag="h6">User Information</MDBTypography>
                                    <hr className="mt-0 mb-4" />
                                    <MDBRow>
                                        <MDBCol size="6" className="mb-3">
                                            <MDBTypography tag="h6">Email</MDBTypography>
                                            <MDBCardText className="text-muted">{userData?.email}</MDBCardText>
                                        </MDBCol>
                
                                        <MDBCol size="6" className="mb-3">
                                            <MDBTypography tag="h6">Certifications</MDBTypography>
                                            <MDBCardText className="text-muted">{userData?.certifications || 'None'}</MDBCardText>
                                        </MDBCol>
                                    </MDBRow>
                                    <MDBTypography tag="h6">Bio</MDBTypography>
                                    <MDBCardText className="text-muted">{userData?.bio || 'No bio available.'}</MDBCardText>
                                </MDBCardBody>
                            </MDBCol>
                        </MDBRow>
                    </MDBCard>
                </MDBCol>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} color="primary">Close</Button>
            </DialogActions>
        </Dialog>
    );
};

export default UserProfileDialog;
