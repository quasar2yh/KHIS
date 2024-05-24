import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useState } from 'react';
import Col from 'react-bootstrap/Col';
import CommonInfoForm from '../components/CommonInfoForm';

function SigninPatient() {
    const [validated, setValidated] = useState(false);

    const handleSubmit = (event) => {
        const form = event.currentTarget;
        if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
        }

        setValidated(true);
    };

    return (
        <Form onSubmit={handleSubmit}>
            <CommonInfoForm />

            <Form.Group as={Col} xs={5}>
                <Button variant="primary">회원가입</Button>
            </Form.Group>
        </Form>
    );
}

export default SigninPatient;
