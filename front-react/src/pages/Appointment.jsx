import React, { useState } from 'react';
import { Form, Button, Col, Row } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { API_ENDPOINT } from '../shared/server';
import instance from '../apis/accountControl';
import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

function Appointment() {
    const userId = useSelector(state => state.userReducer.userId);
    const navigate = useNavigate();

    const [appointmentData, setAppointmentData] = useState({
        date: '',
        time: '',
        reason: '',
        practitioner: '',
        department: '',
        appointmentype: 'checkup',
        status: 'booked',
    });

    const appointmentAction = async (data) => {
        const response = await instance.post(API_ENDPOINT + '/khis/appointment/patient/' + userId, data);
        return response.data;
    };

    const handleChange = (e) => {
        setAppointmentData({
            ...appointmentData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const { date, time, reason, practitioner, department, appointmentype, status } = appointmentData
        const body = {
            date,
            time,
            reason,
            practitioner,
            department,
            appointmentype,
            status,
        };

        try {
            const response = await appointmentAction(body);

            if (response.id) {
                alert("예약 성공")
                navigate('/')
            }
            else {
                alert("예약 실패")
            }
        } catch (error) {
            console.error('예약 에러', error)
            alert("예약 중 오류가 발생했습니다.")
        }

    };
    const timeOption = () => {
        const options = [];
        for (let hour = 8; hour < 18; hour++) {
            for (let minute = 0; minute < 60; minute += 20) {
                const formattedHour = hour.toString().padStart(2, '0');
                const formattedMinute = minute.toString().padStart(2, '0');
                options.push(`${formattedHour}:${formattedMinute}`);
            }
        }
        return options;
    };

    return (
        <div className="container mt-5">
            <h2>병원 예약</h2>
            <Form onSubmit={handleSubmit}>

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
                            as="select"
                            name="time"
                            value={appointmentData.time}
                            onChange={handleChange}
                            required
                        >
                            <option>시간을 선택하세요.</option>
                            {timeOption().map((time, index) => {
                                return (
                                    <option key={index} value={time}>{time}</option>
                                );
                            })}
                        </Form.Control>
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
