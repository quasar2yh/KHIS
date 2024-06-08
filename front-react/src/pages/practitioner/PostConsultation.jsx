import React, { useEffect, useState } from 'react';
import { Modal, Button, Form, ListGroup } from 'react-bootstrap';
import { searchPatient } from '../../apis/apis';
import { postConsultation } from '../../apis/consultation_apis';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { getPractitionerInfoAction } from '../../redux/modules/userActions';

const PostConsultation = () => {
    const accountInfo = useSelector(state => state.userReducer.accountInfo)
    const practitionerInfo = useSelector(state => state.userReducer.practitionerInfo)
    const dispatch = useDispatch()
    const [showModal, setShowModal] = useState(false);
    const [patientName, setPatientName] = useState({ name: null});
    const [patientList, setPatientList] = useState([]);
    const [selectedPatient, setSelectedPatient] = useState({ name: '', id: 0 });
    const [consultationData, setConsultationData] = useState({
        patient: 0,
        practitioner : 0,
        department: 0,
        diagnosis: '',
        diagnostic_results: '',
        surgical_request_record: '',
        surgical_result: ''
    });

    useEffect(() => {
        if (!practitionerInfo && accountInfo?.practitioner) {
            dispatch(getPractitionerInfoAction(accountInfo.practitioner));
        }
    }, [dispatch, accountInfo, practitionerInfo]);

    const handleClose = () => setShowModal(false);

    const searchHandler = (e) => {
        setPatientName({
            ...patientName,
            [e.target.name]: e.target.value
        });
    }

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
        const body = {
            patient: selectedPatient.id,
            practitioner : practitionerInfo.id,
            department: practitionerInfo.department,
            diagnosis: consultationData.diagnosis,
            diagnostic_results: consultationData.diagnostic_results,
            surgical_request_record: consultationData.surgical_request_record,
            surgical_result: consultationData.surgical_result
        }
        postConsultation(body)
        alert("진단 기록 생성 완료")
        navigator("/")
    };

    console.log("selectedPatient", selectedPatient)
    return (
        <div className="container mt-5">
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
                            name="name"
                            value={patientName.name}
                            onChange = {searchHandler}
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
                                readOnly
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
        </div>
    );
};

export default PostConsultation;
