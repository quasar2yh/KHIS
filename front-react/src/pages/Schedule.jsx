import React, { useState } from 'react';
import { Table, Button, Modal, Form } from 'react-bootstrap';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function Schedule() {
    const departments = ["외과", "내과", "치과"];
    const initialSlots = ["09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00", "13:00 - 14:00", "14:00 - 15:00", "15:00 - 16:00", "16:00 - 17:00"];
    
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [selectedDepartment, setSelectedDepartment] = useState(departments[0]);
    const [availability, setAvailability] = useState({});
    const [showModal, setShowModal] = useState(false);
    const [currentSlot, setCurrentSlot] = useState('');

    const handleDateChange = date => setSelectedDate(date);

    const handleDepartmentChange = e => setSelectedDepartment(e.target.value);

    const checkAvailability = () => {
        const formattedDate = selectedDate.toISOString().split('T')[0];
        setAvailability({
            ...availability,
            [formattedDate]: {
                ...availability[formattedDate],
                [selectedDepartment]: initialSlots.reduce((acc, slot) => {
                    acc[slot] = Math.random() > 0.5;
                    return acc;
                }, {})
            }
        });
    };

    const handleSlotClick = slot => {
        setCurrentSlot(slot);
        setShowModal(true);
    };

    const handleModalClose = () => setShowModal(false);

    const formattedDate = selectedDate.toISOString().split('T')[0];
    const slots = availability[formattedDate]?.[selectedDepartment] || {};

    return (
        <div className="container mt-5">
            <h2>병원 스케줄</h2>
            <Form.Group controlId="formDepartment">
                <Form.Label>부서 선택</Form.Label>
                <Form.Control as="select" value={selectedDepartment} onChange={handleDepartmentChange}>
                    {departments.map(department => (
                        <option key={department} value={department}>{department}</option>
                    ))}
                </Form.Control>
            </Form.Group>
            <Form.Group controlId="formDate" className="mt-3">
                <Form.Label>날짜 선택</Form.Label>
                <DatePicker
                    selected={selectedDate}
                    onChange={handleDateChange}
                    dateFormat="yyyy-MM-dd"
                    className="form-control"
                />
            </Form.Group>
            <Button className="mt-3" onClick={checkAvailability}>시간대 확인</Button>
            
            <h3 className="mt-5">{selectedDepartment} 스케줄 ({formattedDate})</h3>
            <Table striped bordered hover className="mt-3">
                <thead>
                    <tr>
                        <th>시간대</th>
                        <th>상태</th>
                    </tr>
                </thead>
                <tbody>
                    {initialSlots.map(slot => (
                        <tr key={slot} onClick={() => handleSlotClick(slot)} style={{ cursor: 'pointer' }}>
                            <td>{slot}</td>
                            <td>{slots[slot] ? "비어있음" : "예약됨"}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>

            <Modal show={showModal} onHide={handleModalClose}>
                <Modal.Header closeButton>
                    <Modal.Title>시간대 상세 정보</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p>{currentSlot} 시간대의 상세 정보입니다.</p>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleModalClose}>닫기</Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
}

export default Schedule;
