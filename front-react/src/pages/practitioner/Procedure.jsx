import React, { useState } from 'react';
import { Modal, Form, Button, Container, Row, Col, ListGroup } from 'react-bootstrap';
import { searchPatient, getMedicalRecord, postProcedureRecord } from '../../apis/apis';
import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

const Procedure = () => {
    const navigate = useNavigate()
    const accountInfo = useSelector(state => state.userReducer.accountInfo);

    const [showModal, setShowModal] = useState(false);
    const [showRecords, setShowRecords] = useState(false);
    const [patientName, setPatientName] = useState({ name: '' });
    const [patientList, setPatientList] = useState([]);
    const [selectedPatient, setSelectedPatient] = useState({ name: '', id: null });
    const [medicalRecords, setMedicalRecords] = useState([]);
    const [selectedMedicalRecord, setSelectedMedicalRecord] = useState(0);
    const [procedure, setProcedure] = useState({
        patient: 0,
        practitioner: 0,
        medical_record: 0,
        procedure_code: '',
        procedure_name: '',
        description: '',
        procedure_result: '',
        start: '',
        end: '',
    });

    const searchHandler = (e) => {
        setPatientName({
            ...patientName,
            [e.target.name]: e.target.value
        });
    };

    const handleSearch = () => {
        searchPatient(patientName).then(res => {
            setPatientList(res);
        });
    };

    const handlePatientClick = (id, family, name) => {
        const patientName = `${family} ${name}`;
        setSelectedPatient({ id, patientName });
        getMedicalRecord(id).then(res => {
            setMedicalRecords(res);
            setShowRecords(true);
        });
    };

    const handleChange = (e) => {
        setProcedure({
            ...procedure,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const body = {
            patient: selectedPatient.id,
            practitioner: accountInfo.practitioner,
            medical_record: selectedMedicalRecord,
            procedure: {
                procedure_code: procedure.procedure_code,
                procedure_name: procedure.procedure_name,
                description: procedure.description,
            },
            procedure_result: procedure.procedure_result,
            start: procedure.start,
            end: procedure.end,
        };
        postProcedureRecord(body)
        console.log(body);
        alert("수술 기록 작성 완료")
        navigate('/');
    };

    return (
        <>
            <Container className="mt-5">
                <Modal show={showModal} onHide={() => setShowModal(false)}>
                    <Modal.Header closeButton>
                        <Modal.Title>환자 정보</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form.Group>
                            <Form.Label>이름</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="이름을 입력하세요."
                                name="name"
                                value={patientName.name}
                                onChange={searchHandler}
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
                        <Button variant="secondary" onClick={() => setShowModal(false)}>
                            닫기
                        </Button>
                    </Modal.Footer>
                </Modal>
                
                <Modal show={showRecords} onHide={() => setShowRecords(false)}>
                    <Modal.Header closeButton>
                        <Modal.Title>수술 목록</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        {medicalRecords.length > 0 ? (
                            <ListGroup>
                                {medicalRecords.map(record => (
                                    <ListGroup.Item key={record.id} onClick={() => {
                                        setSelectedMedicalRecord(record.id);
                                        setShowRecords(false);
                                        setShowModal(false);
                                    }}
                                    action>
                                        ID : {record.id}
                                        <br />
                                        진단: {record.diagnosis}
                                        <br />
                                        진단 결과: {record.diagnostic_results}
                                        <br />
                                        수술 요청 기록: {record.surgical_request_record}
                                        <br />
                                        작성 날짜: {record.created_at}
                                        <br />
                                        업데이트 날짜: {record.updated_at}
                                    </ListGroup.Item>
                                ))}
                            </ListGroup>
                        ) : (
                            <p>기록이 없습니다.</p>
                        )}
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={() => setShowRecords(false)}>
                            닫기
                        </Button>
                    </Modal.Footer>
                </Modal>

                <h2 className="text-center mb-4">수술 기록 작성</h2>
                <Form onSubmit={handleSubmit}>
                    <Form.Group>
                        <Form.Label>환자</Form.Label>
                        <Button variant="primary" onClick={() => setShowModal(true)}>
                            검색
                        </Button>
                        <Form.Control
                            type="text"
                            name="diagnosis"
                            value={selectedPatient.patientName}
                            readOnly
                        />
                    </Form.Group>
                    <Row className="mb-3">
                        <Col>
                            <Form.Group controlId="procedure_code">
                                <Form.Label>수술 코드</Form.Label>
                                <Form.Control
                                    type="text"
                                    name="procedure_code"
                                    value={procedure.procedure_code}
                                    onChange={handleChange}
                                    required
                                />
                            </Form.Group>
                        </Col>
                    </Row>
                    <Row className="mb-3">
                        <Col>
                            <Form.Group controlId="procedure_name">
                                <Form.Label>수술 이름</Form.Label>
                                <Form.Control
                                    type="text"
                                    name="procedure_name"
                                    value={procedure.procedure_name}
                                    onChange={handleChange}
                                    required
                                />
                            </Form.Group>
                        </Col>
                    </Row>
                    <Row className="mb-3">
                        <Col>
                            <Form.Group controlId="description">
                                <Form.Label>수술 상세 설명</Form.Label>
                                <Form.Control
                                    as="textarea"
                                    name="description"
                                    value={procedure.description}
                                    onChange={handleChange}
                                    required
                                />
                            </Form.Group>
                        </Col>
                    </Row>
                    <Row className="mb-3">
                        <Col>
                            <Form.Group controlId="procedure_result">
                                <Form.Label>수술 결과</Form.Label>
                                <Form.Control
                                    as="textarea"
                                    name="procedure_result"
                                    value={procedure.procedure_result}
                                    onChange={handleChange}
                                    required
                                />
                            </Form.Group>
                        </Col>
                    </Row>
                    <Row className="mb-3">
                        <Col md="6">
                            <Form.Group controlId="start">
                                <Form.Label>시작 시간</Form.Label>
                                <Form.Control
                                    type="datetime-local"
                                    name="start"
                                    value={procedure.start}
                                    onChange={handleChange}
                                    required
                                />
                            </Form.Group>
                        </Col>
                        <Col md="6">
                            <Form.Group controlId="end">
                                <Form.Label>종료 시간</Form.Label>
                                <Form.Control
                                    type="datetime-local"
                                    name="end"
                                    value={procedure.end}
                                    onChange={handleChange}
                                    required
                                />
                            </Form.Group>
                        </Col>
                    </Row>
                    <Button variant="primary" type="submit">
                        제출
                    </Button>
                </Form>
            </Container>
        </>
    );
};

export default Procedure;
