import React from 'react';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';

function IdPwForm() {
    return (
        <>
            <Form.Group as={Col} xs={5} controlId="formBasicEmail">
                <Form.Label>Id</Form.Label>
                <Form.Control type="text" id='id' />
            </Form.Group>

            <Form.Group as={Col} xs={5} controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" />
            </Form.Group>
        </>
    );
}

export default IdPwForm;
