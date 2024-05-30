import React, { useState, useEffect } from 'react';
import { Form, Button, Table, Container, Row, Col } from 'react-bootstrap';
import { annualAction, getAnnual } from '../../apis/apis';

const Annual = () => {
    const [annualList, setAnnualList] = useState(null);
    const [annual, setAnnual] = useState({
        start_date: '',
        end_date: '',
        reason: ''
    });

    useEffect(() => {
        getAnnual().then(res => {
            setAnnualList(res);
        });
    }, []);

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
        <Container>
            <Row>
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
                <Col>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group>
                            <Form.Label>시작 날짜</Form.Label>
                            <Form.Control
                                type="date"
                                name="start_date"
                                value={annual.start_date}
                                onChange={handleChange}
                                required
                            />
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>종료 날짜</Form.Label>
                            <Form.Control
                                type="date"
                                name="end_date"
                                value={annual.end_date}
                                onChange={handleChange}
                                required
                            />
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>신청 사유</Form.Label>
                            <Form.Control
                                as="textarea"
                                name="reason"
                                value={annual.reason}
                                onChange={handleChange}
                                required
                            />
                        </Form.Group>
                        <Button variant="primary" type="submit">
                            신청
                        </Button>
                    </Form>
                </Col>
            </Row>
        </Container>
    );
};

export default Annual;
