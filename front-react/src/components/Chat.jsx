import React, { useState, useEffect } from 'react';
import { getChatMessages, sendMessage, getAllUser } from '../apis/apis';
import { useSelector } from 'react-redux';
import './Chat.css';

const Chat = () => {
    const accountInfo = useSelector(state => state.userReducer.accountInfo);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [selectedUser, setSelectedUser] = useState(null);
    const [userMap, setUserMap] = useState({});
    const [users, setUsers] = useState([]);
    

    useEffect(() => {
        async function fetchAllUsers() {
            try {
                const data = await getAllUser();
                setUsers(data);
                const userMap = data.reduce((acc, user) => {
                    acc[user.id] = `${user.last_name} ${user.first_name}`;
                    return acc;
                }, {});
                setUserMap(userMap);
            } catch (error) {
                console.error("Error fetching users:", error);
            }
        }
        fetchAllUsers();
    }, []);

    useEffect(() => {
        if (selectedUser && accountInfo) {
            async function fetchMessages() {
                try {
                    const allMessages = await getChatMessages();
                    const filteredMessages = allMessages.filter(msg =>
                        (msg.sender === accountInfo.id && msg.receiver === selectedUser.id) ||
                        (msg.sender === selectedUser.id && msg.receiver === accountInfo.id)
                    );
                    setMessages(filteredMessages);
                } catch (error) {
                    console.error("Error fetching messages:", error);
                }
            }
            fetchMessages();
        }
    }, [selectedUser, accountInfo]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (input.trim() === '' || !selectedUser) return;

        try {
            const newMessage = await sendMessage(selectedUser.id, input);
            setMessages([...messages, newMessage]);
            setInput('');
        } catch (error) {
            console.error("Error sending message:", error);
        }
    };

    const escapeHTML = (str) => {
        if (typeof str !== 'string') {
            return '';
        }
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    };

    // accountInfo가 없으면 로딩 중 표시
    if (!accountInfo) {
        return <div>Loading chat...</div>;
    }

    return (
        <div className="chat-container">
            <div className="user-list">
                <h3>전체 유저</h3>
                <ul>
                    {users.map((user) => (
                        <li 
                            key={user.id} 
                            className={selectedUser?.id === user.id ? 'selected-user' : ''}
                            onClick={() => {
                                setSelectedUser(user);
                                setInput('');
                            }}
                        >
                            {user.last_name} {user.first_name}
                        </li>
                    ))}
                </ul>
            </div>
            {selectedUser ? (
                <div className="message-section">
                    <h3>메시지 창 - {userMap[selectedUser.id]}</h3>
                    <div className="chat-box">
                        {messages.length > 0 ? (
                            messages.map((msg, index) => (
                                <p key={index}>
                                    {userMap[msg.sender]} &rarr; {userMap[msg.receiver]}: {escapeHTML(msg.message)}
                                </p>
                            ))
                        ) : (
                            <p>No messages to show</p>
                        )}
                    </div>
                    <form className="message-form" onSubmit={handleSubmit}>
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="메세지를 입력하세요"
                        />
                        <button type="submit">Send</button>
                    </form>
                </div>
            ) : (
                <div className="message-section">
                    <p>유저를 선택하세요</p>
                </div>
            )}
        </div>
    );
};

export default Chat;
