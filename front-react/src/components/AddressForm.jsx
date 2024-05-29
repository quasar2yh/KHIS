import React from 'react';
import { Form, Row, Col } from 'react-bootstrap';
import Postcode from './PostCode';

const AddressForm = ({ formData, setFormData }) => {

    const handleAddressChange = (e) => {
        setFormData({
            ...formData,
            address: {
                ...formData.address,
                [e.target.name]: e.target.value
            }
        });
    };

    return (
        <Form.Group className="mt-3">
            <Form.Label>Address</Form.Label>
            <Row className="align-items-center">
                <Col xs={12} md={6} className="mb-2">
                    <Postcode formData={formData} setFormData={setFormData} />
                </Col>
                <Col xs={12} md={12} className="mb-2">
                    <Form.Control
                        type="text"
                        name="city"
                        value={formData.address.city}
                        onChange={handleAddressChange}
                        placeholder="City"
                    />
                </Col>
                <Col xs={12} md={6} className="mb-2">
                    <Form.Control
                        type="text"
                        name="postal_code"
                        value={formData.address.postal_code}
                        onChange={handleAddressChange}
                        placeholder="Postal Code"
                    />
                </Col>
                <Col xs={12} md={6} className="mb-2">
                    <Form.Control
                        type="text"
                        name="text"
                        value={formData.address.text}
                        onChange={handleAddressChange}
                        placeholder="Enter detailed address"
                    />
                </Col>
            </Row>
        </Form.Group>
    );
};

export default AddressForm;