import React from 'react';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import IdPwForm from './IdPwForm';
import '../styles.css';


function CommonInfoForm() {
    return (
        <>
            <IdPwForm />

            <Form.Group as={Col} xs={5} controlId="formBasicPassword">
                <Form.Label>Password 확인</Form.Label>
                <Form.Control type="password" />
            </Form.Group>

            <Form.Group as={Col} controlId="gender">
                <Form.Label>성별</Form.Label>
                <div>
                    <Form.Check
                        inline
                        label="남성"
                        name="gender"
                        type="radio"
                        id="inline-radio-1"
                    />
                    <Form.Check
                        inline
                        label="여성"
                        name="gender"
                        type="radio"
                        id="inline-radio-2"
                    />
                </div>
            </Form.Group>

            <Row as={Col} className="mb-3 indented" >
                <Form.Group as={Col} xs={2} controlId="validationCustom01">
                    <Form.Label>성</Form.Label>
                    <Form.Control
                        required
                        type="text"
                    />
                    <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                </Form.Group>
                <Form.Group as={Col} xs={3} controlId="validationCustom02">
                    <Form.Label>이름</Form.Label>
                    <Form.Control
                        required
                        type="text"
                    />
                    <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                </Form.Group>
            </Row>

            <Row className="mb-3 indented">
                <Form.Group as={Col} xs={5} controlId="validationCustom03">
                    <Form.Label>연락처</Form.Label>
                    <Form.Control
                        required
                        type="text"
                    />
                    <Form.Control.Feedback type="invalid">
                        유효한 연락처를 입력하세요.
                    </Form.Control.Feedback>
                </Form.Group>
            </Row>
        </>
    )
}

export default CommonInfoForm