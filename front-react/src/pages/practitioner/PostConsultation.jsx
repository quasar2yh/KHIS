import React, { useState } from 'react';
import { Modal, Button, Form, ListGroup } from 'react-bootstrap';
import { searchPatient } from '../../apis/apis';
import { consultationAction } from '../../apis/apis';
import { useNavigate } from 'react-router-dom';

const PostConsultation = () => {
    const [showModal, setShowModal] = useState(false);
    const [patientName, setPatientName] = useState('');
    const [patientList, setPatientList] = useState([]);
    const [selectedPatient, setSelectedPatient] = useState({ name: '', id: null });
    const [consultationData, setConsultationData] = useState({
        diagnosis: '',
        diagnostic_results: '',
        surgical_request_record: '',
        surgical_result: ''
    });

    const handleClose = () => setShowModal(false);

    const handleSearch = () => {
        searchPatient(patientName).then(res => {
            setPatientList(res);
        });
    };

    const handlePatientClick = (id, family, given) => {
        const name = `${family} ${given}`;
        setSelectedPatient({ id, name });
        setShowModal(false);
    };

    const handleConsultationChange = (e) => {
        const { name, value } = e.target;
        setConsultationData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const navigator = useNavigate()
    const handleSubmit = () => {
        consultationAction(selectedPatient.id, consultationData)
        alert("진단 기록 생성 완료")
        navigator("/")
    };


    return (
        <>
            <Modal show={showModal} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>환자 정보</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form.Group>
                        <Form.Label>이름</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="이름을 입력하세요."
                            value={patientName}
                            onChange={(e) => setPatientName(e.target.value)}
                        />
                    </Form.Group>
                    <Button variant="primary" onClick={handleSearch} className="mt-3">
                        검색
                    </Button>

                    {patientList.length > 0 && (
                        <ListGroup className="mt-3">
                            {patientList.map(patient => (
                                <ListGroup.Item
                                    key={patient.id}
                                    onClick={() => handlePatientClick(patient.id, patient.name.family, patient.name.name)}
                                    action
                                >
                                    {patient.name.family} {patient.name.name} ({patient.gender})
                                    <br />
                                    전화: {patient.telecom.value}
                                </ListGroup.Item>
                            ))}
                        </ListGroup>
                    )}
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        닫기
                    </Button>
                </Modal.Footer>
            </Modal>

            {selectedPatient && (
                <div>
                    <h2>진단 기록 작성</h2>
                    <Form>
                        <Form.Group>
                            <Form.Label>환자</Form.Label>
                            <Button variant="primary" onClick={() => setShowModal(true)}>
                                검색
                            </Button>
                            <Form.Control
                                type="text"
                                name="diagnosis"
                                value={selectedPatient.name}
                            />
                        </Form.Group>

                        <Form.Group>
                            <Form.Label>진단</Form.Label>
                            <Form.Control
                                type="text"
                                name="diagnosis"
                                value={consultationData.diagnosis}
                                onChange={handleConsultationChange}
                            />
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>진단 결과</Form.Label>
                            <Form.Control
                                type="text"
                                name="diagnostic_results"
                                value={consultationData.diagnostic_results}
                                onChange={handleConsultationChange}
                            />
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>수술 요청 기록</Form.Label>
                            <Form.Control
                                type="text"
                                name="surgical_request_record"
                                value={consultationData.surgical_request_record}
                                onChange={handleConsultationChange}
                            />
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>수술 결과</Form.Label>
                            <Form.Control
                                type="text"
                                name="surgical_result"
                                value={consultationData.surgical_result}
                                onChange={handleConsultationChange}
                            />
                        </Form.Group>
                        <Button variant="primary" onClick={handleSubmit} className="mt-3">
                            저장
                        </Button>
                    </Form>
                </div>
            )}
        </>
    );
};

export default PostConsultation;
