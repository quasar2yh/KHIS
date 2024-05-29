import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';

const MedicalRecord = () => {
    const [showModal, setShowModal] = useState(false);
    const [patientInfo, setPatientInfo] = useState({
        name: ''
    });
    const [consultationData, setConsultationData] = useState({
        diagnosis: '',
        diagnostic_results: '',
        surgical_request_record: '',
        surgical_result: ''
    });

    const handleClose = () => setShowModal(false);

    const handleSearch = () => {
        // 여기서 환자 정보를 검색하고 결과를 설정합니다.
        // 예를 들어, API 호출로 환자 정보를 가져올 수 있습니다.
        // 결과를 받아와서 setPatientInfo 함수를 사용하여 설정합니다.
    };

    const handleSubmit = () => {
        // 여기서 진료 기록을 저장하고 처리합니다.
        // 예를 들어, API 호출로 진료 기록을 서버에 저장할 수 있습니다.
        // 저장이 완료되면 모달을 닫습니다.
        handleClose();
    };

    return (
        <>
            <Button variant="primary" onClick={() => setShowModal(true)}>
                환자 검색
            </Button>

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
                            value={patientInfo.name}
                            onChange={(e) => setPatientInfo({ ...patientInfo, name: e.target.value })}
                        />
                    </Form.Group>
                    <Button variant="primary" onClick={handleSearch}>
                        검색
                    </Button>
                </Modal.Body>
            </Modal>

            <Modal show={showModal} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>환자 정보</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {/* 여기에 환자 정보 표시 */}
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        닫기
                    </Button>
                </Modal.Footer>
            </Modal>

            <Modal show={showModal} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>진료 기록 작성</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form.Group controlId="formDiagnosis">
                        <Form.Label>진단 내용</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="진단 내용을 입력하세요."
                            value={consultationData.diagnosis}
                            onChange={(e) => setConsultationData({ ...consultationData, diagnosis: e.target.value })}
                        />
                    </Form.Group>
                    <Form.Group controlId="formDiagnosticResults">
                        <Form.Label>진단 결과</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="진단 결과를 입력하세요."
                            value={consultationData.diagnostic_results}
                            onChange={(e) => setConsultationData({ ...consultationData, diagnostic_results: e.target.value })}
                        />
                    </Form.Group>
                    <Form.Group controlId="formSurgicalRequestRecord">
                        <Form.Label>수술 요청 기록</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="수술 요청 기록을 입력하세요."
                            value={consultationData.surgical_request_record}
                            onChange={(e) => setConsultationData({ ...consultationData, surgical_request_record: e.target.value })}
                        />
                    </Form.Group>
                    <Form.Group controlId="formSurgicalResult">
                        <Form.Label>Test 수술 결과</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Test 수술 결과를 입력하세요."
                            value={consultationData.surgical_result}
                            onChange={(e) => setConsultationData({ ...consultationData, surgical_result: e.target.value })}
                        />
                    </Form.Group>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        취소
                    </Button>
                    <Button variant="primary" onClick={handleSubmit}>
                        저장
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
};

export default MedicalRecord;
