import React from 'react'
import { Table, Button, Modal } from 'react-bootstrap';
import { useSelector } from 'react-redux';

function ConsultationList({ consultations, selectConsultation, show, handleClose, handleShow }) {
    const accountInfo = useSelector(state => state.userReducer.accountInfo)

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
                                        <Button variant="primary" onClick={() => handleShow(consultation)}>
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

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>상세보기</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {selectConsultation && (
                        <div>
                            <p><strong>Date:</strong> </p>
                            <p><strong>Doctor:</strong> </p>
                            <p><strong>Summary:</strong> </p>
                            <p><strong>Details:</strong> </p>
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