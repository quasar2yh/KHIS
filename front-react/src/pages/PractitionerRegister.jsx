import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import CommonInfoForm from '../components/CommonInfoForm';
import { registerAction } from '../redux/modules/registerActions';

function PractitionerRegister() {

    const [practitionerRegisterData, setPractitionerRegisterData] = useState({
        id: '',
        password: '',
        familyName: '',
        name: '',
        gender: '',
        telecom: '',
        licenseType: '',
        licenseNumber: 0,
        role: '',
        rank: 0,
    })

    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleChange = (e) => {
        setPractitionerRegisterData({
            ...practitionerRegisterData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = (event) => {
        event.preventDefault();

        const { id, password, familyName, name, gender, telecom, licenseType, licenseNumber, role, rank } = practitionerRegisterData;

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
            subject: "Practitioner",
            marital_status: "0",
            license_type: licenseType,
            license_number: licenseNumber,
            role,
            rank,
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
                registerData={practitionerRegisterData}
                handleChange={handleChange} />

            <Row>
                <Form.Group as={Col} xs={2}>
                    <Form.Label>자격 종류</Form.Label>
                    <Form.Control type="text" id='id' name="licenseType" value={practitionerRegisterData.licenseType} onChange={handleChange} />
                </Form.Group>
                <Form.Group as={Col} xs={3}>
                    <Form.Label>자격 번호</Form.Label>
                    <Form.Control type="text" id='id' name="licenseNumber" value={practitionerRegisterData.licenseNumber} onChange={handleChange} />
                </Form.Group>
            </Row>

            <Row>
                <Form.Group as={Col} xs={2}>
                    <Form.Label>역할</Form.Label>
                    <Form.Control type="text" id='id' name="role" value={practitionerRegisterData.role} onChange={handleChange} />
                </Form.Group>
                <Form.Group as={Col} xs={3}>
                    <Form.Label>권한</Form.Label>
                    <Form.Control type="text" id='id' name="rank" value={practitionerRegisterData.rank} onChange={handleChange} />
                </Form.Group>
            </Row>


            <Form.Group as={Col} xs={5}>
                <Button type="submit" variant="primary">회원가입</Button>
            </Form.Group>
        </Form>
    );
}

export default PractitionerRegister;