import React, { useState } from 'react'
import { Table, Button, Modal } from 'react-bootstrap';
import { getProcedureRecordList } from '../apis/apis';

function ConsultationList({ consultations }) {
    const [showConsultationModal, setShowConsultationModal] = useState(false);
    const [selectConsultation, setSelectConsultation] = useState([]);

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

    console.log("consultations", consultations);
    console.log("ConsultationList-selectConsultation", selectConsultation)
    return (
        <div className="container mt-5">
            <h2>Consultations</h2>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>진단 번호</th>
                        <th>담당 의사</th>
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
                                        <th>담당 의사</th>
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
        </div>
    )
}

export default ConsultationList