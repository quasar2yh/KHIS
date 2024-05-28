import React from 'react';
import { Container, Row, Col, Card, ListGroup } from 'react-bootstrap';
import { useSelector } from 'react-redux';

function Account() {
    const AccountInfo = useSelector(state => state.userReducer.AccountInfo);

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
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
        </>
    );
}

export default Account;
