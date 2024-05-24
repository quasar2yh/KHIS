import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import CommonInfoForm from '../components/CommonInfoForm';

function SigninPatient() {

    const handleSubmit = (event) => {
        const form = event.currentTarget;
        if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
        }}

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
