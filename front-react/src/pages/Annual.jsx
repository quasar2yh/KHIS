import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import { annualAction } from '../apis/apis';
import { useSelector } from 'react-redux';

const Annual = () => {
    const practitioner = useSelector(state => state.userReducer.practitionerInfo)

    const [annal, setAnnal] = useState({
        start_date: '',
        end_date: '',
        reason: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setAnnal(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = () => {
        annualAction()
    };

    return (
        <Form onSubmit={handleSubmit}>
            <Form.Group>
                <Form.Label>시작 날짜</Form.Label>
                <Form.Control
                    type="date"
                    name="start_date"
                    value={annal.start_date}
                    onChange={handleChange}
                    required
                />
            </Form.Group>
            <Form.Group>
                <Form.Label>종료 날짜</Form.Label>
                <Form.Control
                    type="date"
                    name="end_date"
                    value={annal.end_date}
                    onChange={handleChange}
                    required
                />
            </Form.Group>
            <Form.Group>
                <Form.Label>신청 사유</Form.Label>
                <Form.Control
                    as="textarea"
                    name="reason"
                    value={annal.reason}
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
