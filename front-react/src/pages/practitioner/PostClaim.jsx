import React, { useState } from 'react';
import { Modal, Button, Form, ListGroup, Table } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { searchPatient } from '../../apis/apis';
import { getUnchargedProcedure } from '../../apis/procedure_apis';
import { postClaim, postChargeItem } from '../../apis/claim_apis';

function PostClaim() {
    const navigate = useNavigate()

    const [patientName, setPatientName] = useState({ name: '' });
    const [patientList, setPatientList] = useState([]);
    const [selectedPatient, setSelectedPatient] = useState({ name: '', id: 0 });
    const [showSearchPatientModal, setShowSearchPatientModal] = useState(false);
    const [procedureList, setProcedureList] = useState(null);
    const [showChargeModal, setShowChargeModal] = useState(false);
    const [chargeItems, setChargeItems] = useState([]);
    const [chargeItem, setChargeItem] = useState({
        quantity: 1,
        total: 0,
        claim: 0,
        patient: 0,
        procedure: 0,
    });

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

        const getAndSetProcedures = async () => {
            try {
                const res = await getUnchargedProcedure(id);
                setProcedureList(res);
            } catch (e) {
                console.log("error", e);
            }
        };
        getAndSetProcedures();
    };

    const handleChargeClick = (procedureId) => () => {
        setChargeItem({
            ...chargeItem,
            procedure: procedureId,
            patient: selectedPatient.id
        });
        setShowChargeModal(true);
    };

    const handleCloseChargeModal = () => {
        setShowChargeModal(false);
    };

    const handleChargeSubmit = () => {
        setChargeItems([...chargeItems, chargeItem]);
        handleCloseChargeModal();
    };

    const handleClaimSubmit = async () => {
        try {
            const claim = await postClaim({ patient: selectedPatient.id, status: "active" });
            console.log("claim", claim);
            for (const item of chargeItems) {
                await postChargeItem({ ...item, claim: claim.id });
            }
            navigate("/")
            alert("청구서 저장 성공")
        } catch (error) {
            console.error("error:", error);
        }
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

        {selectedPatient.id !== 0 && procedureList && procedureList.length > 0 && (
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
                        {procedureList.map(procedure => (
                            <tr key={procedure.id}>
                                <td>{procedure.id}</td>
                                <td>{procedure.procedure_code}</td>
                                <td>{procedure.procedure_name}</td>
                                <td>{procedure.description}</td>
                                <td>
                                    <Button variant="primary" onClick={handleChargeClick(procedure.id)}>
                                        청구
                                    </Button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            </div>
        )}

        {selectedPatient.id !== 0 && procedureList && (
            <div className="text-center mt-3">
                청구할 수술 기록이 없습니다.
            </div>
        )}


        <Modal show={showChargeModal} onHide={handleCloseChargeModal}>
            <Modal.Header closeButton>
                <Modal.Title>청구서 작성</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form.Group controlId="quantity">
                    <Form.Label>수량</Form.Label>
                    <Form.Control
                        type="number"
                        placeholder="수량을 입력하세요."
                        value={chargeItem.quantity}
                        onChange={(e) => setChargeItem({ ...chargeItem, quantity: e.target.value })}
                    />
                </Form.Group>
                <Form.Group controlId="total">
                    <Form.Label>금액</Form.Label>
                    <Form.Control
                        type="number"
                        placeholder="금액을 입력하세요."
                        value={chargeItem.total}
                        onChange={(e) => setChargeItem({ ...chargeItem, total: e.target.value })}
                    />
                </Form.Group>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleCloseChargeModal}>
                    취소
                </Button>
                <Button variant="primary" onClick={handleChargeSubmit}>
                    저장
                </Button>
            </Modal.Footer>
        </Modal>


        <div className="container mt-5">
            <h2>청구서</h2>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>환자</th>
                        <th>수술 번호</th>
                        <th>수량</th>
                        <th>금액</th>
                    </tr>
                </thead>
                <tbody>
                    {chargeItems.map((item, index) => (
                        <tr key={index}>
                            <td>{item.patient}</td>
                            <td>{item.procedure}</td>
                            <td>{item.quantity}</td>
                            <td>{item.total}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
            <Button variant="primary" onClick={handleClaimSubmit}>저장</Button>
        </div>

    </div>
);
}

export default PostClaim;
