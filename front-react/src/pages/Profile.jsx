import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card, ListGroup, Button } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import { getPatientInfoAction } from '../redux/modules/userActions';
import Account from '../components/Account';
import ProfileUpdate from '../components/ProfileUpdate';

function Profile() {
    const AccountInfo = useSelector(state => state.userReducer.AccountInfo);
    const patientInfo = useSelector(state => state.userReducer.patientInfo);
    const dispatch = useDispatch();
    const [showProfileUpdate, setShowProfileUpdate] = useState(false);

    useEffect(() => {
        if (AccountInfo && AccountInfo.subject==='Patient' && patientInfo === null) {
            dispatch(getPatientInfoAction(AccountInfo.patient));
        }
    }, [dispatch, AccountInfo, patientInfo]);

    if (!patientInfo || !AccountInfo) {
        return <div>Loading...</div>;
    }

    const { name, telecom, address, gender, allergies } = patientInfo;

    const onClose = () => {
        setShowProfileUpdate(false);
    };
    return (
        <>
            {showProfileUpdate ? (
                <ProfileUpdate onClose={onClose}/>
            ) : (
                <Container className="mt-5">
                    <Row className="justify-content-center">
                        <Col md={8}>
                            <Card>
                                <Card.Header as="h4" className="bg-primary text-white text-center">
                                    Profile
                                </Card.Header>
                                <Card.Body>
                                    <ListGroup variant="flush">
                                        <ListGroup.Item>
                                            <Row>
                                                <Col md={4} className="text-right font-weight-bold">Name:</Col>
                                                <Col md={8}>{`${name.family} ${name.name}`}</Col>
                                            </Row>
                                        </ListGroup.Item>
                                        <ListGroup.Item>
                                            <Row>
                                                <Col md={4} className="text-right font-weight-bold">Gender:</Col>
                                                <Col md={8}>{gender || 'N/A'}</Col>
                                            </Row>
                                        </ListGroup.Item>
                                        <ListGroup.Item>
                                            <Row>
                                                <Col md={4} className="text-right font-weight-bold">Allergies:</Col>
                                                <Col md={8}>{allergies || "None"}</Col>
                                            </Row>
                                        </ListGroup.Item>
                                        <ListGroup.Item>
                                            <Row>
                                                <Col md={4} className="text-right font-weight-bold">Telecom:</Col>
                                                <Col md={8}>
                                                    {telecom ? telecom.value : 'N/A'}
                                                </Col>
                                            </Row>
                                        </ListGroup.Item>
                                        <ListGroup.Item>
                                            <Row>
                                                <Col md={4} className="text-right font-weight-bold">Address:</Col>
                                                <Col md={8}>
                                                    {telecom ? `${address.city}  ${address.text}` : 'N/A'}
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
                </Container >
            )
            }
            <Account />
        </>
    );
}

export default Profile;
