import React, { useState } from 'react';
import { Modal, Button, Form, ListGroup } from 'react-bootstrap';
import { searchPatient, getConsultations } from '../../apis/apis';
import ConsultationList from '../../components/ConsultationList';

function GetConsultations() {
    const [patientName, setPatientName] = useState({ name: '' });
    const [patientList, setPatientList] = useState([]);
    const [selectedPatient, setSelectedPatient] = useState({ name: '', id: 0 });
    const [showSearchPatientModal, setShowSearchPatientModal] = useState(false);
    const [consultations, setConsultations] = useState([]);
    const [selectConsultation] = useState(null);
    const [showConsultationModal, setShowConsultationModal] = useState(false);

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
                console.log("PatientList", res);
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
        console.log("selectedPatient", selectedPatient)

        const getAndSetConsultations = async () => {
            try {
                const res = await getConsultations(id);
                setConsultations(res);
            } catch (e) {
                console.log("error", e)
            };
        }
        getAndSetConsultations();
        console.log("consultations", consultations);
    };

    const handleShowConsultationModal = () => {
        setShowConsultationModal(true);
    };

    const handleCloseConsultationModal = () => {
        setShowConsultationModal(false);
    };

    return (
        <>
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
                    selectConsultation={selectConsultation}
                    show={showConsultationModal}
                    handleClose={handleCloseConsultationModal}
                    handleShow={handleShowConsultationModal}
                />
            )}
        </>
    );
}

export default GetConsultations;
