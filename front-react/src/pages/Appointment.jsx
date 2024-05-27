import React, { useState } from 'react';
import { Form, Button, Col, Row } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import { API_ENDPOINT } from '../shared/server';

function Appointment() {
    const [appointmentData, setAppointmentData] = useState({
        name: '',
        date: '',
        time: '',
        department: '',
        doctor: '',
        reason: '',
        contact: ''
    });

    const appointmentAction = async (data) => {
        const response = await axios.post(API_ENDPOINT + '/khis/appointment/patient/', data);
        return response.data;
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setAppointmentData({
            ...appointmentData,
            [name]: value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        
    };

    return (
        <div className="container mt-5">
            <h2>병원 예약</h2>
            <Form onSubmit={handleSubmit}>
                <Form.Group as={Row} className="mb-3" controlId="formName">
                    <Form.Label column sm="2">이름</Form.Label>
                    <Col sm="10">
                        <Form.Control
                            type="text"
                            name="name"
                            value={appointmentData.name}
                            onChange={handleChange}
                            placeholder="이름을 입력하세요"
                            required
                        />
                    </Col>
                </Form.Group>

                <Form.Group as={Row} className="mb-3" controlId="formContact">
                    <Form.Label column sm="2">연락처</Form.Label>
                    <Col sm="10">
                        <Form.Control
                            type="tel"
                            name="contact"
                            value={appointmentData.contact}
                            onChange={handleChange}
                            placeholder="연락처를 입력하세요"
                            required
                        />
                    </Col>
                </Form.Group>

                <Form.Group as={Row} className="mb-3" controlId="formDoctor">
                    <Form.Label column sm="2">부서</Form.Label>
                    <Col sm="10">
                        <Form.Control
                            as="select"
                            name="doctor"
                            value={appointmentData.department}
                            onChange={handleChange}
                            required
                        >
                            <option>부서를 선택하세요.</option>
                            <option value="1">외과</option>
                            <option value="2">내과</option>
                        </Form.Control>
                    </Col>
                </Form.Group>

                <Form.Group as={Row} className="mb-3" controlId="formDate">
                    <Form.Label column sm="2">날짜</Form.Label>
                    <Col sm="10">
                        <Form.Control
                            type="date"
                            name="date"
                            value={appointmentData.date}
                            onChange={handleChange}
                            required
                        />
                    </Col>
                </Form.Group>

                <Form.Group as={Row} className="mb-3" controlId="formTime">
                    <Form.Label column sm="2">시간</Form.Label>
                    <Col sm="10">
                        <Form.Control
                            type="time"
                            name="time"
                            value={appointmentData.time}
                            onChange={handleChange}
                            required
                        />
                    </Col>
                </Form.Group>

                <Form.Group as={Row} className="mb-3" controlId="formDoctor">
                    <Form.Label column sm="2">의사</Form.Label>
                    <Col sm="10">
                        <Form.Control
                            as="select"
                            name="doctor"
                            value={appointmentData.doctor}
                            onChange={handleChange}
                            required
                        >
                            <option>의사를 선택하세요.</option>
                            <option value="1">현효민</option>
                            <option value="2">이윤후</option>
                            <option value="3">안채연</option>
                            <option value="4">이훈희</option>
                        </Form.Control>
                    </Col>
                </Form.Group>

                <Form.Group as={Row} className="mb-3" controlId="formReason">
                    <Form.Label column sm="2">증상</Form.Label>
                    <Col sm="10">
                        <Form.Control
                            as="textarea"
                            name="reason"
                            value={appointmentData.reason}
                            onChange={handleChange}
                            rows={3}
                            placeholder="증상을 자세히 입력하세요"
                            required
                        />
                    </Col>
                </Form.Group>

                <Button variant="primary" type="submit">예약하기</Button>
            </Form>
        </div>
    );
}

export default Appointment;
