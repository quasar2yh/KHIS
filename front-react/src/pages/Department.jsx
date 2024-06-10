import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Table, Container, Spinner, Row, Col } from 'react-bootstrap';
import { getPractitionerFromDepartment } from '../apis/apis';
import { useSelector } from 'react-redux';

const Department = () => {
    const departmentList = useSelector(state => state.departmentReducer.departmentList);
    const { id } = useParams();
    const [practitionerList, setPractitionerList] = useState(null);

    const department = Array.isArray(departmentList)
        ? departmentList.find(department => department.id === parseInt(id))
        : null;

    useEffect(() => {
        const fetchPractitionerList = async () => {
            const res = await getPractitionerFromDepartment(id);
            setPractitionerList(res);
        };

        fetchPractitionerList();
    }, [id]);

    if (!practitionerList) {
        return (
            <Container className="mt-5 text-center">
                <Spinner animation="border" role="status">
                    <span className="sr-only">Loading...</span>
                </Spinner>
            </Container>
        );
    }

    return (
        <Container className="mt-5">
            <Row className="mb-4">
                <Col>
                    <h2 className="text-center">
                        {department ? `${department.department_name} 의사 목록` : '의사 목록'}
                    </h2>
                </Col>
            </Row>
            <Table striped bordered hover responsive>
                <thead className="bg-primary text-white">
                    <tr>
                        <th>번호</th>
                        <th>이름</th>
                        <th>연락처</th>
                    </tr>
                </thead>
                <tbody>
                    {practitionerList.map(practitioner => (
                        <tr key={practitioner.id}>
                            <td>{practitioner.id}</td>
                            <td>{`${practitioner.name.family} ${practitioner.name.name}`}</td>
                            <td>{practitioner.telecom.value}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </Container>
    );
};

export default Department;
