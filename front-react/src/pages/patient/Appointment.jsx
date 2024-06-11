
import React, { useState, useEffect } from 'react';
import { Form, Button, Col, Row } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { postAppointment, getAbleAppointmentPractitioner } from '../../apis/appointment_apis';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { getDepartmentListAction } from '../../redux/modules/departmentActions';

function Appointment() {
    // userReducer의 userId
    const accountInfo = useSelector(state => state.userReducer.accountInfo);

    // departmentReducer의 departmentList
    const departmentList = useSelector(state => state.departmentReducer.departmentList);

    // 예약 가능한 의사 : 초기값 null
    const [ablePractitioner, setAblePractitioner] = useState([]);

    // 예약 요청 보낼 데이터
    const [appointmentData, setAppointmentData] = useState({
        date: '',
        time: '',
        reason: '',
        practitioner: 0,
        department: 0,
        appointmentType: 'checkup',
        status: 'booked',
    });
    const dispatch = useDispatch();
    const navigate = useNavigate();

    useEffect(() => {
        if (departmentList === null) {
            dispatch(getDepartmentListAction());
        }
    }, [departmentList, dispatch]);


    // 예약 요청 데이터가 변경 될 때 날짜, 시간, 부서가 모두 선택됐으면
    // 해당 조건에 예약 가능한 의사 리스트 set
    useEffect(() => {
        const fetchAblePractitioner = async () => {
            if (appointmentData.date && appointmentData.time && appointmentData.department) {
                    const res = await getAbleAppointmentPractitioner(appointmentData);
                    setAblePractitioner(res);
            }
        };
        fetchAblePractitioner();
    }, [appointmentData]);

    const handleChange = (e) => {
        setAppointmentData({
            ...appointmentData,
            [e.target.name]: e.target.value
        });
    };


    const handleSubmit = async (e) => {
        e.preventDefault();

        const { date, time, reason, practitioner, department, appointmentType, status } = appointmentData;
        const body = {
            start: `${date}T${time}:00`,
            reason,
            practitioner,
            department,
            appointmentType,
            status,
            active: true,
        };

        try {
            const response = await postAppointment(body, accountInfo.patient);

            if (response.active) {
                alert("예약 성공");
                navigate('/');
            } else {
                alert("예약 실패");
            }
        } catch (error) {
            console.error('예약 에러', error);
            alert(error);
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
        <>
            <div className="container mt-5">
                <h2>병원 예약</h2>
                <Form onSubmit={handleSubmit}>

                    <Form.Group as={Row} className="mb-3">
                        <Form.Label column sm="2">부서</Form.Label>
                        <Col sm="10">
                            <Form.Control
                                as="select"
                                name="department"
                                value={appointmentData.department}
                                onChange={handleChange}
                                required
                            >
                                <option>부서를 선택하세요.</option>
                                {departmentList && departmentList.map((department) => (
                                    <option key={department.id} value={department.id}>{department.department_name}</option>
                                ))}
                            </Form.Control>
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} className="mb-3">
                        <Form.Label column sm="2">날짜</Form.Label>
                        <Col sm="10">
                            <Form.Control
                                type="date"
                                name="date"
                                value={appointmentData.date}
                                onChange={handleChange}
                            />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} className="mb-3">
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
                                {timeOption().map((time, index) => (
                                    <option key={index} value={time}>{time}</option>
                                ))}
                            </Form.Control>
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} className="mb-3">
                        <Form.Label column sm="2">의사</Form.Label>
                        <Col sm="10">
                            <Form.Control
                                as="select"
                                name="practitioner"
                                value={appointmentData.practitioner}
                                onChange={handleChange}
                                required
                            >
                                <option>의사를 선택하세요.</option>
                                {ablePractitioner && ablePractitioner.map((practitioner) => (
                                    <option key={practitioner.id} value={practitioner.id}>{practitioner.name.family} {practitioner.name.name}</option>
                                ))}
                            </Form.Control>
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} className="mb-3">
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
        </>
    );
}

export default Appointment;
