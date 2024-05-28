import React, { useState } from 'react';
import { Container, Form, Button, Card } from 'react-bootstrap';
import { sendChatMessage } from '../apis/apis';

function Chatbot() {
    const [message, setMessage] = useState('');
    const [chatMessages, setChatMessages] = useState(["증상을 말씀해주세요. 진료과를 추천해드릴게요!"]);

    const handleChange = (e) => {
        setMessage(e.target.value);
    };

    const addMessageToChat = (message) => {
        setChatMessages([...chatMessages, message]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const body = { message };
        try {
            const response = await sendChatMessage(body);
            addMessageToChat(response.response);
            setMessage('');
        } catch (error) {
            console.error('채팅 메시지 전송 오류:', error);
        }
    };

    return (
        <Container className="mt-5">
            <Card>
                <Card.Header as="h5">Chatbot</Card.Header>
                <Card.Body>
                    <div style={{ height: '200px', overflowY: 'auto' }}>
                        {chatMessages.map((message, index) => (
                            <p key={index}>{message}</p>
                        ))}
                    </div>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group controlId="chatInput">
                            <Form.Control
                                type="text"
                                placeholder="증상을 말씀해주세요."
                                value={message}
                                onChange={handleChange}
                            />
                        </Form.Group>
                        <Button variant="primary" type="submit">
                            전송
                        </Button>
                    </Form>
                </Card.Body>
            </Card>
        </Container>
    );
}

export default Chatbot;
