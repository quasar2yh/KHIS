import Form from 'react-bootstrap/Form';

function SelectPatientPractitioner() {
    return (
        <Form.Select aria-label="Default select example">
            <option>옵션을 선택하세요</option>
            <option value="patient">환자</option>
            <option value="practitioner">의료 관계자</option>
        </Form.Select>
    );
}

export default SelectPatientPractitioner;