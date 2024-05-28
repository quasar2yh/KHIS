import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import CommonInfoForm from './CommonInfoForm';
import { registerAction } from '../apis/apis';

function PractitionerRegister() {

    const [practitionerRegisterData, setPractitionerRegisterData] = useState({
        id: '',
        password: '',
        familyName: '',
        name: '',
        gender: '',
        contact: '',
        licenseType: '',
        licenseNumber: 0,
        role: '',
        rank: 0,
    })

    const roleList = ['Physician', 'Assistant']
    const navigate = useNavigate();

    const handleChange = (e) => {
        setPractitionerRegisterData({
            ...practitionerRegisterData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const { id, password, familyName, name, gender, contact, licenseType, licenseNumber, role, rank } = practitionerRegisterData;

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
                value: contact,
                use: "Mobile"
            },
            subject: "Practitioner",
            marital_status: "0",
            license_type: licenseType,
            license_number: licenseNumber,
            role,
            rank,
        };

        try {
            const response = await registerAction(body);
            console.log(response);
            if (response.id) {
                alert("회원가입 성공")
                navigate('/login')
            }
            else {
                alert("회원가입 실패")
            }
        } catch (error) {
            alert("회원가입 중 오류가 발생했습니다.")
            console.error(error)
        }
    };


    return (
        <Form noValidate onSubmit={handleSubmit}>
            <CommonInfoForm
                registerData={practitionerRegisterData}
                handleChange={handleChange} />

            <Row className="mb-3">
                <Col xs={2}>
                    <Form.Select aria-label="Default select example" name="role" onChange={handleChange}>
                        <option>역할을 선택하세요.</option>
                        {roleList.map((item, index) => {
                            return <option key={index} value={item}>{item}</option>;
                        })}
                    </Form.Select>
                </Col>
            </Row>

            <Row className="mb-3">
                <Form.Group as={Col} xs={2}>
                    <Form.Label>자격 종류</Form.Label>
                    <Form.Control type="text" id='licenseType' name="licenseType" value={practitionerRegisterData.licenseType} onChange={handleChange} />
                </Form.Group>

                <Form.Group as={Col} xs={3}>
                    <Form.Label>자격 번호</Form.Label>
                    <Form.Control type="text" id='licenseNumber' name="licenseNumber" value={practitionerRegisterData.licenseNumber} onChange={handleChange} />
                </Form.Group>
            </Row>

            <Row className="mb-3">
                <Col xs={2}>
                    <Form.Group>
                        <Form.Label>권한</Form.Label>
                        <Form.Control type="text" id='rank' name="rank" value={practitionerRegisterData.rank} onChange={handleChange} />
                    </Form.Group>
                </Col>
            </Row>

            <Row className="mb-">
                <Form.Group as={Col} xs={5}>
                    <Button type="submit" variant="primary">회원가입</Button>
                </Form.Group>
            </Row>
        </Form>
    );
}

export default PractitionerRegister;