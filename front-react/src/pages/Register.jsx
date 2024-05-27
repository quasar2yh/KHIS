import React, { useState } from 'react';
import PatientRegister from '../components/PatientRegister';
import PractitionerRegister from '../components/PractitionerRegister';
import Form from 'react-bootstrap/Form';

function SelectRegisterForm() {
    const [selectForm, setSelectForm] = useState("");

    return (
        <>
            <Form.Select aria-label="Default select example" onChange={(e) => {
                setSelectForm(e.target.value);
            }}>
                <option>회원가입 폼을 선택하세요.</option>
                <option value="patient">환자</option>
                <option value="practitioner">의료 관계자</option>
            </Form.Select>

            {selectForm === 'patient' ?  <PractitionerRegister /> : <PatientRegister />}
        </>
    );
}

export default SelectRegisterForm;
