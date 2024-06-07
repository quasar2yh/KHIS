import React, { useState } from 'react';
import { Modal, Button, Form, ListGroup, Table } from 'react-bootstrap';
import { searchPatient } from '../../apis/apis';
import { getProcedure } from '../../apis/procedure_apis';

function Claim() {
    const [patientName, setPatientName] = useState({ name: '' });
    const [patientList, setPatientList] = useState([]);
    const [selectedPatient, setSelectedPatient] = useState({ name: '', id: 0 });
    const [showSearchPatientModal, setShowSearchPatientModal] = useState(false);
    const [procedureList, setProcedureList] = useState(null);

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
                console.log("error", e);
            }
        };
        searchAndSetPatient();
    };

    const handlePatientClick = (id, family, given) => {
        const name = `${family} ${given}`;
        setSelectedPatient({ id, name });
        setShowSearchPatientModal(false);
        console.log("selectedPatient", selectedPatient);

        const getAndSetProcedures = async () => {
            try {
                const res = await getProcedure(id);
                setProcedureList(res);
            } catch (e) {
                console.log("error", e);
            }
        };
        getAndSetProcedures();
    };

    console.log("procedureList", procedureList);

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

            {selectedPatient.id !== 0 && procedureList && procedureList.results && procedureList.results.length > 0 && (
                <div style={{ overflowX: 'auto' }}>
                    <Table striped bordered hover>
                        <thead>
                            <tr>
                                <th>수술 번호</th>
                                <th>수술 코드</th>
                                <th>수술 이름</th>
                                <th>상세 설명</th>
                            </tr>
                        </thead>
                        <tbody>
                            {procedureList.results.map(procedure => (
                                <tr key={procedure.id}>
                                    <td>{procedure.id}</td>
                                    <td>{procedure.procedure_code}</td>
                                    <td>{procedure.procedure_name}</td>
                                    <td>{procedure.description}</td>
                                    <td>
                                        <Button variant="primary">
                                            청구
                                        </Button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </Table>
                </div>
            )}

            {selectedPatient.id !== 0 && procedureList && !procedureList.results && (
                <div className="text-center mt-3">
                    수술 기록이 없습니다.
                </div>
            )}
        </div>
    );
}

export default Claim;
