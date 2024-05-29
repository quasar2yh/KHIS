import React, { useState } from 'react';
import { Container, Row, Col, Card, ListGroup, Button } from 'react-bootstrap';
import { useSelector } from 'react-redux';
import PasswordChange from './PasswordChange';

function Account() {
    const AccountInfo = useSelector(state => state.userReducer.AccountInfo);

    const [showPasswordChange, setShowPasswordChange] = useState(false);

    const onClick = () => {
        setShowPasswordChange(true);
    }

    const onClose = () => {
        setShowPasswordChange(false);
    }

    if (!AccountInfo) {
        return <div>Loading...</div>;
    }

    return (
        <>
            <Container className="mt-5">
                <Row className="justify-content-center">
                    <Col md={8}>
                        <Card>
                            <Card.Header as="h4" className="bg-primary text-white text-center">
                                Account
                            </Card.Header>
                            <Card.Body>
                                <ListGroup variant="flush">
                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">ID:</Col>
                                            <Col md={8}>{AccountInfo.username}</Col>
                                        </Row>
                                    </ListGroup.Item>

                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">Subject:</Col>
                                            <Col md={8}>{AccountInfo.subject}</Col>
                                        </Row>
                                    </ListGroup.Item>

                                    {AccountInfo.patient ?
                                        <ListGroup.Item>
                                            <Row>
                                                <Col md={4} className="text-right font-weight-bold">Patient ID:</Col>
                                                <Col md={8}>{AccountInfo.patient}</Col>
                                            </Row>
                                        </ListGroup.Item>

                                        : <ListGroup.Item>
                                            <Row>
                                                <Col md={4} className="text-right font-weight-bold">Practitioner ID:</Col>
                                                <Col md={8}>{AccountInfo.practitioner || "N/A"}</Col>
                                            </Row>
                                        </ListGroup.Item>
                                    }
                                </ListGroup>
                                <Button variant="primary" className="mt-3 mr-2" onClick={onClick}>
                                    Password Change
                                </Button>
                                {showPasswordChange && <PasswordChange onClose={onClose} />}
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </>
    );
}

export default Account;
