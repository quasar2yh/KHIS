import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card, ListGroup, Button } from 'react-bootstrap';
import { useSelector } from 'react-redux';
import { getAppointmentStatus, deleteAppointment } from '../../apis/appointment_apis';

function AppointmentStatus() {
    const accountInfo = useSelector(state => state.userReducer.accountInfo);
    const [appointmentStatus, setAppointmentStatus] = useState([]);

    useEffect(() => {
        if (accountInfo && accountInfo.patient) {
            getAppointmentStatus(accountInfo.patient).then(res => {
                setAppointmentStatus(res);
            });
        }
    }, [accountInfo]);

    const handleDelete = (appointmentId) => {
        deleteAppointment(appointmentId).then(() => {
            setAppointmentStatus(prevStatus => prevStatus.filter(appointment => appointment.id !== appointmentId));
        });
    };

    return (
        <>
            {appointmentStatus.length > 0 ? (
                appointmentStatus.map(appointment => (
                    <Container key={appointment.id} className="mt-5">
                        <Row className="justify-content-center">
                            <Col md={8}>
                                <Card>
                                    <Card.Header as="h4" className="bg-primary text-white text-center">
                                        예약 내용
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
                                            <ListGroup.Item className="d-flex justify-content-between align-items-center">
                                                <span></span> {/* 빈 공간 확보 */}
                                                <Button variant="danger" onClick={() => handleDelete(appointment.id)}>
                                                    삭제
                                                </Button>
                                            </ListGroup.Item>
                                        </ListGroup>
                                    </Card.Body>
                                </Card>
                            </Col>
                        </Row>
                    </Container>
                ))
            ) : (
                <Container className="mt-5">
                    <Row className="justify-content-center">
                        <Col md={8}>
                            <Card>
                                <Card.Header as="h4" className="bg-primary text-white text-center">
                                    예약 내용
                                </Card.Header>
                                <Card.Body>
                                    <ListGroup variant="flush">
                                        <ListGroup.Item>
                                            <Row>
                                                <Col md={12} className="text-center font-weight-bold">예약 현황이 없습니다.</Col>
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
