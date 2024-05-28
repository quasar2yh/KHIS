import React, { useEffect } from 'react';
import { Container, Row, Col, Card, ListGroup, Badge } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import { getPatientInfoAction } from '../redux/modules/registerActions';
import Account from '../components/Account';

function Profile() {
    const AccountInfo = useSelector(state => state.userReducer.AccountInfo);
    const patientInfo = useSelector(state => state.userReducer.patientInfo);
    const dispatch = useDispatch();

    useEffect(() => {
        if (AccountInfo) {
            dispatch(getPatientInfoAction(AccountInfo.patient));
        }
    }, [dispatch, AccountInfo]);

    if (!patientInfo) {
        return <div>Loading...</div>;
    }

    const { name, telecom, address, gender, marital_status, allergies } = patientInfo;

    return (
        <>
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
                                        <Col md={4} className="text-right font-weight-bold">address:</Col>
                                        <Col md={8}>{address || 'N/A'}</Col>
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
                                        <Col md={4} className="text-right font-weight-bold">Marital Status:</Col>
                                        <Col md={8}>
                                            <Badge variant={marital_status ? "success" : "secondary"}>
                                                {marital_status ? "Married" : "Single"}
                                            </Badge>
                                        </Col>
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
                                            {telecom ? `${telecom.system} - ${telecom.value} (${telecom.use})` : 'N/A'}
                                        </Col>
                                    </Row>
                                </ListGroup.Item>
                            </ListGroup>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>

        <Account />
        </>
    );
}

export default Profile;
