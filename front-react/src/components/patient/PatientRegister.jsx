import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import CommonInfoForm from '../CommonInfoForm';
import { registerAction } from '../../apis/apis';

function PatientRegister() {

    const [patientRegisterData, setPatientRegisterData] = useState({
        id: '',
        password: '',
        familyName: '',
        name: '',
        address: {
            city: '',
            postal_code: '',
            text: '',
            country: 'South Korea',
            use: 'Home',
        },
        gender: '',
        contact: '',
    })

    const navigate = useNavigate();

    const handleChange = (e) => {
        setPatientRegisterData({
            ...patientRegisterData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        const { id, password, familyName, name, address, gender, contact } = patientRegisterData;

        const body = {
            username: id,
            password,
            name: {
                family: familyName,
                name,
            },
            address,
            gender,
            telecom: {
                system: "Phone",
                value: contact,
                use: "Mobile"
            },
            subject: "Patient",
            marital_status: "0",
        };

        try {
            const response = await registerAction(body);
            
            if (response.id) {
                alert("회원가입 성공")
                navigate('/login')
            }
            else {
                alert("회원가입 실패")
            }
        } catch (error) {
            console.error('회원가입 에러', error)
            alert("회원가입 중 오류가 발생했습니다.")
        }
    };


    return (
        <>
            <Form noValidate onSubmit={handleSubmit}>
                <CommonInfoForm
                    registerData={patientRegisterData}
                    setRegisterData={setPatientRegisterData}
                    handleChange={handleChange}
                    />

                <Form.Group as={Col} xs={5}>
                    <Button type="submit" variant="primary">회원가입</Button>
                </Form.Group>
            </Form>
        </>
    );
}

export default PatientRegister;