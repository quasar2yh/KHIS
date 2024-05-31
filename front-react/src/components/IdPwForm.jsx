import React from 'react';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';

// 로그인 할 때 사용하는 IdPwForm 컴포넌트
function IdPwForm({ id, pw, idHandler, pwHandler }) {
    return (
        <>
            <Form.Group as={Col} xs={5}>
                <Form.Label>Id</Form.Label>
                <Form.Control type="text" id='id' name="id" value={id} onChange={idHandler} />
            </Form.Group>

            <Form.Group as={Col} xs={5}>
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" name="password" value={pw} onChange={pwHandler} />
            </Form.Group>
        </>
    );
}

export default IdPwForm;