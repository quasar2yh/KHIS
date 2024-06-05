import React, { useState, useEffect } from 'react';
import { Form, Button, Table, Container, Row, Col } from 'react-bootstrap';
import { annualAction, getAnnual } from '../../apis/apis';

const Annual = () => {
    const [date, setDate] = useState({ start_date: '', end_date: '' });
    const [annualList, setAnnualList] = useState(null);
    const [annual, setAnnual] = useState({
        start_date: '',
        end_date: '',
        reason: ''
    });

    useEffect(() => {
        const getAnnualList = async () => {
        if (date.start_date && date.end_date) {
            console.log("date", date)
            const res = await getAnnual(date);
                setAnnualList(res);
                console.log("res", res)
            }}
            getAnnualList();
            console.log("annualList", annualList)
        }, [date, annualList])

    const datehandleChange = (e) => {
        setDate({
            ...date,
            [e.target.name]: e.target.value
        })
    }


    const handleChange = (e) => {
        setAnnual({
            ...annual,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = () => {
        annualAction(annual);
    };

    return (
        <div className="container mt-5">
            <Container>
                <Row className="mb-2">
                    <h4 className="mb-2">연차 조회</h4>
                    <Col md="6">
                        <Form.Group as={Row} className="mb-3">
                            <Form.Label column sm="4">시작 날짜</Form.Label>
                            <Col sm="8">
                                <Form.Control
                                    type="date"
                                    name="start_date"
                                    value={date.start_date}
                                    onChange={datehandleChange}
                                />
                            </Col>
                        </Form.Group>
                    </Col>
                    <Col md="6">
                        <Form.Group as={Row} className="mb-3">
                            <Form.Label column sm="4">종료 날짜</Form.Label>
                            <Col sm="8">
                                <Form.Control
                                    type="date"
                                    name="end_date"
                                    value={date.end_date}
                                    onChange={datehandleChange}
                                />
                            </Col>
                        </Form.Group>
                    </Col>
                </Row>
            </Container>
            <Container>
                <Row className="mb-4">
                    <Col>
                        <Table striped bordered hover>
                            <thead>
                                <tr>
                                    <th>시작 날짜</th>
                                    <th>종료 날짜</th>
                                    <th>신청 사유</th>
                                </tr>
                            </thead>
                            <tbody>
                                {annualList && annualList.length > 0 ? (
                                    annualList.map((annual, index) => (
                                        <tr key={index}>
                                            <td>{annual.start_date}</td>
                                            <td>{annual.end_date}</td>
                                            <td>{annual.reason}</td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan="3" className="text-center">연차 내역이 없습니다</td>
                                    </tr>
                                )}
                            </tbody>
                        </Table>
                    </Col>
                </Row>
            </Container>
            <Container>
                <Row>
                    <h4 className="mb-2">연차 신청</h4>
                    <Col>
                        <Form onSubmit={handleSubmit}>

                            <Row>
                                <Col md="3">
                                    <Form.Group className="mb-3">
                                        <Form.Label>시작 날짜</Form.Label>
                                        <Form.Control
                                            type="date"
                                            name="start_date"
                                            value={annual.start_date}
                                            onChange={handleChange}
                                            required
                                        />
                                    </Form.Group>
                                </Col>
                                <Col md="3">
                                    <Form.Group className="mb-3">
                                        <Form.Label>종료 날짜</Form.Label>
                                        <Form.Control
                                            type="date"
                                            name="end_date"
                                            value={annual.end_date}
                                            onChange={handleChange}
                                            required
                                        />
                                    </Form.Group>
                                </Col>
                            </Row>
                            <Row>
                                <Col md="7">
                                    <Form.Group className="mb-3">
                                        <Form.Label>신청 사유</Form.Label>
                                        <Form.Control
                                            as="textarea"
                                            name="reason"
                                            value={annual.reason}
                                            onChange={handleChange}
                                            required
                                        />
                                    </Form.Group>
                                </Col>
                            </Row>
                            <Button variant="primary" type="submit">
                                신청
                            </Button>
                        </Form>
                    </Col>
                </Row>
            </Container>
        </div>
    );
};

export default Annual;
