import React from 'react';
import { Form, Col, Row } from 'react-bootstrap';
import AddressForm from './AddressForm';


// 회원가입 할 때 사용하는 CommonInfoForm
function CommonInfoForm({ registerData, setRegisterData, handleChange }) {

    return (
        <>
            <Form.Group as={Col} xs={5}>
                <Form.Label>Id</Form.Label>
                <Form.Control type="text" id='id' name="id" value={registerData.id} onChange={handleChange} />
            </Form.Group>

            <Form.Group as={Col} xs={5}>
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" name="password" value={registerData.password} onChange={handleChange} />
            </Form.Group>

            <Form.Group as={Col} xs={5}>
                <Form.Label>Password 확인</Form.Label>
                <Form.Control type="password" />
            </Form.Group>

            <Row className="mb-3">
                <Col>
                <Form.Group as={Col} xs={5}>
                    <Form.Label>연락처</Form.Label>
                    <Form.Control
                        required
                        type="text"
                        name="contact"
                        value={registerData.contact}
                        onChange={handleChange}
                    />
                    <Form.Control.Feedback type="invalid">
                        유효한 연락처를 입력하세요.
                    </Form.Control.Feedback>
                </Form.Group>
                </Col>
            </Row>

            {/* AddressForm 컴포넌트 */}
            <AddressForm 
                formData={registerData}
                setFormData={setRegisterData}
            />

            <Form.Group as={Col}>
                <Form.Label>성별</Form.Label>
                <div>
                    <Form.Check
                        inline
                        label="남성"
                        name="gender"
                        type="radio"
                        id="inline-radio-1"
                        value="Male"
                        onChange={handleChange}
                    />
                    <Form.Check
                        inline
                        label="여성"
                        name="gender"
                        type="radio"
                        id="inline-radio-2"
                        value="Female"
                        onChange={handleChange}
                    />
                </div>
            </Form.Group>

            <Row as={Col} className="mb-3">
                <Form.Group as={Col} xs={2}>
                    <Form.Label>성</Form.Label>
                    <Form.Control
                        required
                        type="text"
                        name="familyName"
                        value={registerData.familyName}
                        onChange={handleChange}
                    />
                    <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                </Form.Group>
                <Form.Group as={Col} xs={3}>
                    <Form.Label>이름</Form.Label>
                    <Form.Control
                        required
                        type="text"
                        name="name"
                        value={registerData.name}
                        onChange={handleChange}
                    />
                    <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                </Form.Group>
            </Row>
        </>
    )
}

export default CommonInfoForm;
