import React, { useState } from 'react';
import { Table, Button, Form, Modal, ListGroup } from 'react-bootstrap';
import { getClaim } from '../../apis/claim_apis';
import { searchPatient } from '../../apis/apis';

function GetClaim() {
    const [patientName, setPatientName] = useState({ name: '' });
    const [patientList, setPatientList] = useState([]);
    const [selectedPatient, setSelectedPatient] = useState({ name: '', id: 0 });
    const [showSearchPatientModal, setShowSearchPatientModal] = useState(false);
    const [claims, setClaims] = useState(null);

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
                console.log("error", e);
            }
        };
        searchAndSetPatient();
    };

    const handlePatientClick = (id, family, given) => {
        const name = `${family} ${given}`;
        setSelectedPatient({ id, name });
        setShowSearchPatientModal(false);

        const getAndSetClaims = async () => {
            try {
                const res = await getClaim(id);
                setClaims(res);
            } catch (e) {
                console.log("error", e);
            }
        };
        getAndSetClaims();
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
            
            <h2>청구서 조회</h2>
            {claims ? (
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>청구서 번호</th>
                            <th>청구 내역</th>
                        </tr>
                    </thead>
                    <tbody>
                        {claims.claims.map((claim) => (
                            <React.Fragment key={claim.id}>
                                <tr>
                                    <td>{claim.id}</td>
                                    <td>
                                        <Table striped bordered hover>
                                            <thead>
                                                <tr>
                                                    <th>수술 번호</th>
                                                    <th>수량</th>
                                                    <th>금액</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {claim.charge_items.map((item) => (
                                                    <tr key={item.id}>
                                                        <td>{item.procedure}</td>
                                                        <td>{item.quantity}</td>
                                                        <td>{item.total}</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </Table>
                                    </td>
                                </tr>
                            </React.Fragment>
                        ))}
                    </tbody>
                </Table>
            ) : (
                <div className="text-center mt-3">
                    청구서가 없습니다.
                </div>
            )}
            <Button variant="primary" onClick={() => window.history.back()}>뒤로</Button>
        </div>
    );
}

export default GetClaim;
