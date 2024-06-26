import React, { useState } from 'react';
import { Modal, Button, Form, ListGroup } from 'react-bootstrap';
import { searchPatient } from '../../apis/apis';
import { getConsultations } from '../../apis/consultation_apis';
import ConsultationList from '../../components/ConsultationList';

function GetConsultations() {
    const [patientName, setPatientName] = useState({ name: '' });
    const [patientList, setPatientList] = useState([]);
    const [selectedPatient, setSelectedPatient] = useState({ name: '', id: 0 });
    const [showSearchPatientModal, setShowSearchPatientModal] = useState(false);
    const [consultations, setConsultations] = useState([]);

    const searchHandler = (e) => {
        setPatientName({
            ...patientName,
            [e.target.name]: e.target.value
        });
    };

    const handleSearch = () => {
        const searchAndSetPatient = async () => {
            try {
                const res = await searchPatient(patientName);
                setPatientList(res);
            } catch (e) {
                console.log("error", e)
            };
        };
        searchAndSetPatient();
    }

    const handlePatientClick = (id, family, given) => {
        const name = `${family} ${given}`;
        setSelectedPatient({ id, name });
        setShowSearchPatientModal(false);

        const getAndSetConsultations = async () => {
            try {
                const res = await getConsultations(id);
                setConsultations(res);
            } catch (e) {
                console.log("error", e)
            };
        }
        getAndSetConsultations();
    };
    
    return (
        <div className="container mt-5">
                    <Modal show={showSearchPatientModal} onHide={() => setShowSearchPatientModal(false)}>
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
                    <Button variant="secondary" onClick={() => setShowSearchPatientModal(false)}>
                        닫기
                    </Button>
                </Modal.Footer>
            </Modal>

            <Form>
                <Form.Group>
                    <Form.Label>환자</Form.Label>
                    <Button variant="primary" onClick={() => setShowSearchPatientModal(true)}>
                        검색
                    </Button>
                    <Form.Control
                        type="text"
                        name="diagnosis"
                        value={selectedPatient.name}
                        readOnly
                    />
                </Form.Group>
            </Form>

            {selectedPatient.id !== 0 && (
                <ConsultationList
                    consultations={consultations}
                />
            )}
        </div>
    );
}

export default GetConsultations;
