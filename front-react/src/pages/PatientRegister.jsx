import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import CommonInfoForm from '../components/CommonInfoForm';
import { registerAction } from '../redux/modules/registerActions';

function PatientRegister() {

    const [patientRegisterData, setPatientRegisterData] = useState({
        id: '',
        password: '',
        familyName: '',
        name: '',
        gender: '',
        telecom: '',
    })

    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleChange = (e) => {
        setPatientRegisterData({
            ...patientRegisterData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = (event) => {
        event.preventDefault();

        const { id, password, familyName, name, gender, telecom } = patientRegisterData;

        const body = {
            username: id,
            password,
            name: {
                family: familyName,
                name,
            },
            gender,
            telecom: {
                system: "Phone",
                value: telecom,
                use: "Mobile"
            },
            subject: "Patient",
            marital_status: "0",
        };

        dispatch(registerAction(body))
        .then((res) => {
            console.log("콘솔 res", res); 
            if (res.id) {
                alert("회원가입 성공");
                navigate("/login");
            } else {
                alert("회원가입 실패");
            }
        })
        .catch((error) => {
            alert(error);
        });
};


    return (
        <Form noValidate onSubmit={handleSubmit}>
            <CommonInfoForm
                registerData={patientRegisterData}
                handleChange={handleChange} />

            <Form.Group as={Col} xs={5}>
                <Button type="submit" variant="primary">회원가입</Button>
            </Form.Group>
        </Form>
    );
}

export default PatientRegister;