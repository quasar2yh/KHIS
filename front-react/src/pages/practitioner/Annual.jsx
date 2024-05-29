import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import { annualAction } from '../../apis/apis';

const Annual = () => {
    const [annual, setAnnual] = useState({
        start_date: '',
        end_date: '',
        reason: ''
    });

    const handleChange = (e) => {
        setAnnual({
            ...annual,
            [e.target.name]: e.target.value
        })
    };

    const handleSubmit = () => {
        annualAction(annual)
    };

    console.log("annual", annual)
    return (
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
    );
};

export default Annual;
