import React, { useState, useEffect } from 'react'
import { Table, Button, Modal, Form } from 'react-bootstrap';
import { getProcedureRecordList, updateProcedureRecord } from '../apis/procedure_apis';
import { useSelector } from 'react-redux';

function ConsultationList({ consultations }) {
    const accountInfo = useSelector(state => state.userReducer.accountInfo)
    const [showConsultationModal, setShowConsultationModal] = useState(false);
    const [selectConsultation, setSelectConsultation] = useState([]);
    const [showProcedureRecordUpdateModal, setShowProcedureRecordUpdateModal] = useState(false);
    const [selectedProcedureRecord, setSelectedProcedureRecord] = useState(null);

    const handleShow = (consultationId) => {
        setShowConsultationModal(true);

        const getAndSetProcedureRecordList = async (consultationId) => {
            try {
                const res = await getProcedureRecordList(consultationId);
                setSelectConsultation(res);
            } catch (err) {
                console.log("error", err);
            }
        };
        getAndSetProcedureRecordList(consultationId);
    };

    const handleClose = () => {
        setShowConsultationModal(false);
    };

    const handleProcedureRecordUpdate = (record) => {
        setSelectedProcedureRecord(record);
        setShowProcedureRecordUpdateModal(true);
    };

    return (
        <div className="container mt-5">
            <h2>진단 기록</h2>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>진단 번호</th>
                        <th>담당 의사 ID</th>
                        <th>내용</th>
                        <th>결과</th>
                        <th>수술 요청</th>
                        <th>수술 결과</th>
                    </tr>
                </thead>
                <tbody>
                    {consultations ? (
                        consultations.detail ? (
                            <tr>
                                <td colSpan="7" className="text-center">{consultations.detail}</td>
                            </tr>
                        ) : (
                            consultations.map(consultation => (
                                <tr key={consultation.id}>
                                    <td>{consultation.id}</td>
                                    <td>{consultation.patient}</td>
                                    <td>{consultation.diagnosis}</td>
                                    <td>{consultation.diagnostic_results}</td>
                                    <td>{consultation.surgical_request_record}</td>
                                    <td>{consultation.surgical_result}</td>
                                    <td>
                                        <Button variant="primary" onClick={() => handleShow(consultation.id)}>
                                            상세보기
                                        </Button>
                                    </td>
                                </tr>
                            ))
                        )
                    ) : (
                        <tr>
                            <td colSpan="7" className="text-center">Loading...</td>
                        </tr>
                    )}
                </tbody>
            </Table>

            <Modal show={showConsultationModal} onHide={handleClose} size="lg">
                <Modal.Header closeButton>
                    <Modal.Title>상세보기</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {selectConsultation && (
                        <div style={{ overflowX: 'auto' }}>
                            <Table striped bordered hover>
                                <thead>
                                    <tr>
                                        <th>수술기록 번호</th>
                                        <th>담당 의사 ID</th>
                                        <th>수술 번호</th>
                                        <th>수술 코드</th>
                                        <th>수술 이름</th>
                                        <th>상세 설명</th>
                                        <th>시작 시간</th>
                                        <th>종료 시간</th>
                                        <th>수술 결과</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {selectConsultation.length ? (
                                        selectConsultation.map(procedureRecord => (
                                            <tr key={procedureRecord.id}>
                                                <td>{procedureRecord.id}</td>
                                                <td>{procedureRecord.practitioner}</td>
                                                <td>{procedureRecord.procedure.id}</td>
                                                <td>{procedureRecord.procedure.procedure_code}</td>
                                                <td>{procedureRecord.procedure.procedure_name}</td>
                                                <td>{procedureRecord.procedure.description}</td>
                                                <td>{procedureRecord.start}</td>
                                                <td>{procedureRecord.end}</td>
                                                <td>{procedureRecord.procedure_result}</td>
                                            {accountInfo && accountInfo.subject==='Practitioner' && (
                                                <td>
                                                    <Button variant="primary" onClick={() => handleProcedureRecordUpdate(procedureRecord)}>
                                                        수정
                                                    </Button>
                                                </td>
                                                )}
                                            </tr>
                                        ))
                                    ) : (
                                        <tr>
                                            <td colSpan="9" className="text-center">Loading...</td>
                                        </tr>
                                    )}
                                </tbody>
                            </Table>
                        </div>
                    )}
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>

            {selectedProcedureRecord && (
                <ProcedureRecordUpdateModal
                    show={showProcedureRecordUpdateModal}
                    handleClose={() => setShowProcedureRecordUpdateModal(false)}
                    procedureRecord={selectedProcedureRecord}
                />
            )}
        </div>
    );
}

function ProcedureRecordUpdateModal({ show, handleClose, procedureRecord }) {
    const [updatedRecord, setUpdatedRecord] = useState(procedureRecord);

    useEffect(() => {
        setUpdatedRecord(procedureRecord);
    }, [procedureRecord]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        const keys = name.split('.');
        if (keys.length === 2) {
            setUpdatedRecord({
                ...updatedRecord,
                [keys[0]]: {
                    ...updatedRecord[keys[0]],
                    [keys[1]]: value,
                },
            });
        } else {
            setUpdatedRecord({
                ...updatedRecord,
                [name]: value,
            });
        }
    };

    const handleSubmit = () => {
        updateProcedureRecord(procedureRecord.id, updatedRecord);
        handleClose();
    };

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>수술 기록 수정</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group>
                        <Form.Label>수술 코드</Form.Label>
                        <Form.Control
                            type="text"
                            name="procedure.procedure_code"
                            value={updatedRecord.procedure?.procedure_code || ''}
                            onChange={handleChange}
                        />
                    </Form.Group>
                    <Form.Group>
                        <Form.Label>수술 이름</Form.Label>
                        <Form.Control
                            type="text"
                            name="procedure.procedure_name"
                            value={updatedRecord.procedure?.procedure_name || ''}
                            onChange={handleChange}
                        />
                    </Form.Group>
                    <Form.Group>
                        <Form.Label>상세 설명</Form.Label>
                        <Form.Control
                            type="text"
                            name="procedure.description"
                            value={updatedRecord.procedure?.description || ''}
                            onChange={handleChange}
                        />
                    </Form.Group>
                    <Form.Group>
                        <Form.Label>시작 시간</Form.Label>
                        <Form.Control
                            type="text"
                            name="start"
                            value={updatedRecord.start || ''}
                            onChange={handleChange}
                        />
                    </Form.Group>
                    <Form.Group>
                        <Form.Label>종료 시간</Form.Label>
                        <Form.Control
                            type="text"
                            name="end"
                            value={updatedRecord.end || ''}
                            onChange={handleChange}
                        />
                    </Form.Group>
                    <Form.Group>
                        <Form.Label>수술 결과</Form.Label>
                        <Form.Control
                            type="text"
                            name="procedure_result"
                            value={updatedRecord.procedure_result || ''}
                            onChange={handleChange}
                        />
                    </Form.Group>
                    <Button variant="primary" onClick={handleSubmit}>
                        완료
                    </Button>
                </Form>
            </Modal.Body>
        </Modal>
    );
};

export default ConsultationList