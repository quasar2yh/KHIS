import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button } from 'react-bootstrap';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { passwordChange } from '../apis/apis';

function PasswordChange({ onClose }) {
    const accountInfo = useSelector(state => state.userReducer.AccountInfo)
    const navigator = useNavigate()

    const [formData, setFormData] = useState({
        old_password: '',
        new_password: '',
        confirm_password: '',
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        console.log("formData", formData)
        passwordChange(accountInfo.id, formData).then(() => {
            alert("비밀번호 변경 성공")
            navigator("/");
        });
    };

    return (
        <Container className="mt-5">
            <Row className="justify-content-center">
                <Col md={8}>
                    <Card>
                        <Card.Header as="h4" className="bg-primary text-white text-center">
                            Password Change
                        </Card.Header>
                        <Card.Body>
                            <Form onSubmit={handleSubmit}>
                                <Form.Group>
                                    <Form.Label>Password</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="old_password"
                                        value={formData.old_password}
                                        onChange={handleChange}
                                    />
                                </Form.Group>

                                <Form.Group>
                                    <Form.Label>New Password</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="new_password"
                                        value={formData.new_password}
                                        onChange={handleChange}
                                    />
                                </Form.Group>

                                <Form.Group>
                                    <Form.Label>Confirm Password</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="confirm_password"
                                        value={formData.confirm_password}
                                        onChange={handleChange}
                                    />
                                </Form.Group>

                                <Button variant="primary" type="submit" className="mt-3">
                                    Update
                                </Button>
                                <Button variant="secondary" className="mt-3 ms-2" onClick={onClose}>
                                    Cancel
                                </Button>
                            </Form>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    );
}

export default PasswordChange;
