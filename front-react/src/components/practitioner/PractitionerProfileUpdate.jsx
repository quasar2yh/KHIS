import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button } from 'react-bootstrap';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { updatePractitionerInfo } from '../../apis/apis';
import AddressForm from '../AddressForm';

function PractitionerProfileUpdate({ onClose }) {
    const practitionerInfo = useSelector(state => state.userReducer.practitionerInfo);
    const navigator = useNavigate()
    console.log("practitionerInfo", practitionerInfo)

    const [formData, setFormData] = useState({
        familyName: practitionerInfo.name.family,
        name: practitionerInfo.name.name,
        address: practitionerInfo.address,
        gender: practitionerInfo.gender,
        telecom: practitionerInfo.telecom.value,
        department: practitionerInfo.department
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        const body = {
            name: {
                family: formData.familyName,
                name: formData.name
            },
            address: formData.address,
            gender: formData.gender,
            department:formData.department,
        };

        if (formData.telecom !== practitionerInfo.telecom.value) {
            body.telecom = { value: formData.telecom };
        }
        if (formData.gender === '성별') {
            body.gender = practitionerInfo.gender;
        }

        updatePractitionerInfo(practitionerInfo.id, body).then(() => {
            alert("정보 수정 성공")
            navigator("/");
        });
    };

    return (
        <Container className="mt-5">
            <Row className="justify-content-center">
                <Col md={8}>
                    <Card>
                        <Card.Header as="h4" className="bg-primary text-white text-center">
                            Update Profile
                        </Card.Header>
                        <Card.Body>
                            <Form onSubmit={handleSubmit}>
                                <Form.Group>
                                    <Form.Label>Family Name</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="familyName"
                                        value={formData.familyName}
                                        onChange={handleChange}
                                        placeholder="Enter family name"
                                    />
                                </Form.Group>

                                <Form.Group>
                                    <Form.Label>Name</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="name"
                                        value={formData.name}
                                        onChange={handleChange}
                                        placeholder="Enter name"
                                    />
                                </Form.Group>

                                <AddressForm
                                    formData={formData}
                                    setFormData={setFormData}
                                />

                                <Form.Group className="mt-3">
                                    <Form.Label>Gender</Form.Label>
                                    <Form.Control
                                        as="select"
                                        name="gender"
                                        value={formData.gender}
                                        onChange={handleChange}
                                    >
                                        <option>성별</option>
                                        <option value="Male">Male</option>
                                        <option value="Female">Female</option>
                                    </Form.Control>
                                </Form.Group>

                                <Form.Group className="mt-3">
                                    <Form.Label>Telecom</Form.Label>
                                    <Form.Control
                                        required
                                        type="text"
                                        name="telecom"
                                        value={formData.telecom}
                                        onChange={handleChange}
                                        placeholder="Enter telecom"
                                    />
                                </Form.Group>
                                
                                <Form.Group>
                                    <Form.Label>Department</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="department"
                                        value={formData.department}
                                        onChange={handleChange}
                                        placeholder="Enter department"
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

export default PractitionerProfileUpdate;
