import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card, ListGroup, Button } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import { getPatientInfoAction, getPractitionerInfoAction } from '../redux/modules/userActions';
import Account from '../components/Account';
import ProfileUpdate from '../components/ProfileUpdate';

function Profile() {
    const AccountInfo = useSelector(state => state.userReducer.AccountInfo);
    const patientInfo = useSelector(state => state.userReducer.patientInfo);
    const practitionerInfo = useSelector(state => state.userReducer.practitionerInfo);
    const dispatch = useDispatch();
    const [showProfileUpdate, setShowProfileUpdate] = useState(false);

    useEffect(() => {
        if (AccountInfo && AccountInfo.subject === 'Patient' && patientInfo === null) {
            dispatch(getPatientInfoAction(AccountInfo.patient));
        }
    }, [dispatch, AccountInfo, patientInfo]);

    useEffect(() => {
        if (AccountInfo && AccountInfo.subject === 'Practitioner' && practitionerInfo === null) {
            dispatch(getPractitionerInfoAction(AccountInfo.practitioner));
        }
    })



    if (!patientInfo && !practitionerInfo) {
        return <div>Loading...</div>;
    }

    const onClose = () => {
        setShowProfileUpdate(false);
    };

    const renderPatientProfile = () => {

        return (
            <Container className="mt-5">
                <Row className="justify-content-center">
                    <Col md={8}>
                        <Card>
                            <Card.Header as="h4" className="bg-primary text-white text-center">
                                Patient Profile
                            </Card.Header>
                            <Card.Body>
                                <ListGroup variant="flush">
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">Name:</Col>
                                            <Col md={8}>{patientInfo.name ? `${patientInfo.name.family} ${patientInfo.name.name}` : 'N/A'}</Col>
                                        </Row>
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">Gender:</Col>
                                            <Col md={8}>{patientInfo.gender || 'N/A'}</Col>
                                        </Row>
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">Allergies:</Col>
                                            <Col md={8}>{patientInfo.allergies || "None"}</Col>
                                        </Row>
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">Telecom:</Col>
                                            <Col md={8}>
                                                {patientInfo.telecom ? patientInfo.telecom.value : 'N/A'}
                                            </Col>
                                        </Row>
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">Address:</Col>
                                            <Col md={8}>
                                                {patientInfo.address ? `${patientInfo.address.city} ${patientInfo.address.text}` : 'N/A'}
                                            </Col>
                                        </Row>
                                    </ListGroup.Item>
                                </ListGroup>
                                <Button variant="primary" className="mt-3" onClick={() => {
                                    setShowProfileUpdate(true);
                                }}>
                                    Update
                                </Button>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        );
    };

    const renderPractitionerProfile = () => {

        return (
            <Container className="mt-5">
                <Row className="justify-content-center">
                    <Col md={8}>
                        <Card>
                            <Card.Header as="h4" className="bg-primary text-white text-center">
                                Practitioner Profile
                            </Card.Header>
                            <Card.Body>
                                <ListGroup variant="flush">
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">Name:</Col>
                                            <Col md={8}>{practitionerInfo.name ? `${practitionerInfo.name.family} ${practitionerInfo.name.name}` : 'N/A'}</Col>
                                        </Row>
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">Gender:</Col>
                                            <Col md={8}>{practitionerInfo.gender || 'N/A'}</Col>
                                        </Row>
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">Birth Date:</Col>
                                            <Col md={8}>{practitionerInfo.birth_date || 'N/A'}</Col>
                                        </Row>
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">License Type:</Col>
                                            <Col md={8}>{practitionerInfo.license_type || 'N/A'}</Col>
                                        </Row>
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">License Number:</Col>
                                            <Col md={8}>{practitionerInfo.license_number || 'N/A'}</Col>
                                        </Row>
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">Role:</Col>
                                            <Col md={8}>{practitionerInfo.role || 'N/A'}</Col>
                                        </Row>
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">Rank:</Col>
                                            <Col md={8}>{practitionerInfo.rank || 'N/A'}</Col>
                                        </Row>
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">Telecom:</Col>
                                            <Col md={8}>
                                                {practitionerInfo.telecom ? practitionerInfo.telecom.value : 'N/A'}
                                            </Col>
                                        </Row>
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">Address:</Col>
                                            <Col md={8}>
                                                {practitionerInfo.address ? `${practitionerInfo.address.city} ${practitionerInfo.address.text}` : 'N/A'}
                                            </Col>
                                        </Row>
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">Department:</Col>
                                            <Col md={8}>{practitionerInfo.department || 'N/A'}</Col>
                                        </Row>
                                    </ListGroup.Item>
                                </ListGroup>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        );
    };

    return (
        <>
            {showProfileUpdate ? (
                <ProfileUpdate onClose={onClose} />
            ) : (
                <>
                    {patientInfo ? renderPatientProfile() : renderPractitionerProfile()}
                </>
            )}
            <Account />
        </>
    );
}

export default Profile;
