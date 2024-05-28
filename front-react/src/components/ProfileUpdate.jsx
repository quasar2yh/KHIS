import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import { updatePatientInfo } from '../apis/apis';

function ProfileUpdate({ onClose }) {
    const patientInfo = useSelector(state => state.userReducer.patientInfo);
    console.log('patientInfo', patientInfo)

    const [formData, setFormData] = useState({
        familyName: patientInfo.name.family,
        name: patientInfo.name.name,
        address: patientInfo.address,
        gender: patientInfo.gender,
        maritalStatus: patientInfo.marital_status,
        allergies: patientInfo.allergies,
        telecom: patientInfo.telecom
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
            address: formData.address || null,
            gender: formData.gender,
            marital_status: formData.maritalStatus,
            allergies: formData.allergies,
            telecom: {
                value: formData.telecom
            }
        }

        updatePatientInfo(patientInfo.id, body).then(() => {
            onClose();
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
                                        name="familName"
                                        value={formData.familyName}
                                        onChange={handleChange}
                                        placeholder="Enter name"
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

                                <Form.Group className="mt-3">
                                    <Form.Label>Address</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="address"
                                        value={formData.address}
                                        onChange={handleChange}
                                        placeholder="Enter address"
                                    />
                                </Form.Group>
                                <Form.Group className="mt-3">
                                    <Form.Label>Gender</Form.Label>
                                    <Form.Control
                                        as="select"
                                        name="gender"
                                        value={formData.gender}
                                        onChange={handleChange}
                                    >
                                        <option>Select gender</option>
                                        <option value="male">Male</option>
                                        <option value="female">Female</option>
                                    </Form.Control>
                                </Form.Group>
                                <Form.Group className="mt-3">
                                    <Form.Label>Marital Status</Form.Label>
                                    <Form.Control
                                        as="select"
                                        name="maritalStatus"
                                        value={formData.maritalStatus}
                                        onChange={handleChange}
                                    >
                                        <option>Select marital status</option>
                                        <option value={false}>Single</option>
                                        <option value={true}>Married</option>
                                    </Form.Control>
                                </Form.Group>
                                <Form.Group className="mt-3">
                                    <Form.Label>Allergies</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="allergies"
                                        value={formData.allergies}
                                        onChange={handleChange}
                                        placeholder="Enter allergies"
                                    />
                                </Form.Group>

                                <Form.Group className="mt-3">
                                    <Form.Label>Telecom</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="telecom"
                                        value={formData.telecom.value}
                                        onChange={handleChange}
                                        placeholder="Enter telecom"
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

export default ProfileUpdate;
