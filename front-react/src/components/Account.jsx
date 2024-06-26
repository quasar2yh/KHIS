import React, { useState } from 'react';
import { Container, Row, Col, Card, ListGroup, Button } from 'react-bootstrap';
import { useSelector } from 'react-redux';
import PasswordChange from './PasswordChange';


// 프로필 페이지에 계정 정보 랜더링하는 컴포넌트
function Account() {
    const accountInfo = useSelector(state => state.userReducer.accountInfo);

    const [showPasswordChange, setShowPasswordChange] = useState(false);

    const onClick = () => {
        setShowPasswordChange(true);
    }

    const onClose = () => {
        setShowPasswordChange(false);
    }

    if (!accountInfo) {
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
                                            <Col md={8}>{accountInfo.username}</Col>
                                        </Row>
                                    </ListGroup.Item>

                                    <ListGroup.Item>
                                        <Row>
                                            <Col md={4} className="text-right font-weight-bold">Subject:</Col>
                                            <Col md={8}>{accountInfo.subject}</Col>
                                        </Row>
                                    </ListGroup.Item>

                                    {accountInfo.patient ?
                                        <ListGroup.Item>
                                            <Row>
                                                <Col md={4} className="text-right font-weight-bold">Patient ID:</Col>
                                                <Col md={8}>{accountInfo.patient}</Col>
                                            </Row>
                                        </ListGroup.Item>

                                        : <ListGroup.Item>
                                            <Row>
                                                <Col md={4} className="text-right font-weight-bold">Practitioner ID:</Col>
                                                <Col md={8}>{accountInfo.practitioner || "N/A"}</Col>
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
