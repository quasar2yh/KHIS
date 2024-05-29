import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card, ListGroup } from 'react-bootstrap';
import { useSelector } from 'react-redux';
import { getAppointmentStatus } from '../apis/apis';

function AppointmentStatus() {
    const AccountInfo = useSelector(state => state.userReducer.AccountInfo);
    const [appointmentStatus, setAppointmentStatus] = useState([]);

    useEffect(() => {
        if (AccountInfo && AccountInfo.patient) {
            getAppointmentStatus(AccountInfo.patient).then(appointmentInfo => {
                setAppointmentStatus(appointmentInfo);
            });
        }
    }, [AccountInfo]);

    return (
        <>
            {appointmentStatus && appointmentStatus.map(appointment => {
                return (
                    <Container className="mt-5">
                        <Row className="justify-content-center">
                            <Col md={8}>
                                <Card>
                                    <Card.Header as="h4" className="bg-primary text-white text-center">
                                        Appointment Status
                                    </Card.Header>
                                    <Card.Body>
                                        <ListGroup variant="flush">
                                            <ListGroup.Item>
                                                <Row>
                                                    <Col md={4} className="text-right font-weight-bold">Department:</Col>
                                                    <Col md={8}>{appointment.department}</Col>
                                                </Row>
                                            </ListGroup.Item>
                                            <ListGroup.Item>
                                                <Row>
                                                    <Col md={4} className="text-right font-weight-bold">Start Time:</Col>
                                                    <Col md={8}>{appointment.start}</Col>
                                                </Row>
                                            </ListGroup.Item>
                                            <ListGroup.Item>
                                                <Row>
                                                    <Col md={4} className="text-right font-weight-bold">End Time:</Col>
                                                    <Col md={8}>{appointment.end}</Col>
                                                </Row>
                                            </ListGroup.Item>
                                            <ListGroup.Item>
                                                <Row>
                                                    <Col md={4} className="text-right font-weight-bold">Reason:</Col>
                                                    <Col md={8}>{appointment.reason}</Col>
                                                </Row>
                                            </ListGroup.Item>

                                            <ListGroup.Item>
                                                <Row>
                                                    <Col md={4} className="text-right font-weight-bold">Created:</Col>
                                                    <Col md={8}>{appointment.created}</Col>
                                                </Row>
                                            </ListGroup.Item>
                                        </ListGroup>
                                    </Card.Body>
                                </Card>
                            </Col>
                        </Row>
                    </Container>
                );
            })}
            {appointmentStatus.length === 0 && (
                <Container className="mt-5">
                    <Row className="justify-content-center">
                        <Col md={8}>
                            <Card>
                                <Card.Header as="h4" className="bg-primary text-white text-center">
                                    Appointment Status
                                </Card.Header>
                                <Card.Body>
                                    <ListGroup variant="flush">
                                        <ListGroup.Item>
                                            <Row>
                                                <Col md={8} className="text-right font-weight-bold">예약 현황이 없습니다.</Col>
                                            </Row>
                                        </ListGroup.Item>
                                    </ListGroup>
                                </Card.Body>
                            </Card>
                        </Col>
                    </Row>
                </Container>
            )}
        </>
    );
}

export default AppointmentStatus;
