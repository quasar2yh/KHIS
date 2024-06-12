import React, { useState, useEffect } from 'react';
import { getChatMessages, sendMessage, getAllUser } from '../apis/apis';
import { useSelector } from 'react-redux';
import './Chat.css';

const Chat = ({loggedInUserId}) => {
    // const accountInfo = useSelector(state => state.userReducer.accountInfo);  
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [selectedUser, setSelectedUser] = useState(null);
    const [userMap, setUserMap] = useState({});
    const [users, setUsers] = useState([]);
    // console.log("dddddddddddddddddddddd",accountInfo)
// accountInfo에서 로그인한 유저 ID를 가져옴
 
    // // accountInfo가 로드될 때까지 로딩 상태 유지
    // if (!accountInfo) {
    //     return <div>Loading chat...</div>; // 로딩 상태 표시
    // }

    // const loggedInUserId = accountInfo.id; // accountInfo가 존재할 때만 id에 접근
  useEffect(() => {
    async function fetchAllUsers() {
      const data = await getAllUser();
      setUsers(data);
      console.log("전체 유저:", data);

      const userMap = data.reduce((acc, user) => {
        acc[user.id] = `${user.last_name} ${user.first_name}`;
        return acc;
      }, {});
      setUserMap(userMap);
      console.log("Mapped users:", userMap);
    }
    fetchAllUsers();
  }, []);

  useEffect(() => {
    if (selectedUser) {
      async function fetchMessages() {
        const allMessages = await getChatMessages();
        console.log("All Messages:", allMessages);

        console.log("loggedInUserId:", loggedInUserId); // 로그에 출력
        console.log("selectedUser.id:", selectedUser.id); // 로그에 출력

        // 선택된 유저와 로그인한 유저 간의 메시지 필터링
        const filteredMessages = allMessages.filter(msg =>
          (msg.sender === loggedInUserId && msg.receiver === selectedUser.id) ||
          (msg.sender === selectedUser.id && msg.receiver === loggedInUserId)
        );
        console.log("Filtered Messages:", filteredMessages); // 필터링된 메시지 콘솔에 출력
        setMessages(filteredMessages);
      }
      fetchMessages();
    }
  }, [selectedUser, loggedInUserId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim() === '' || !selectedUser) return;

    const newMessage = await sendMessage(selectedUser.id, input);
    setMessages([...messages, newMessage]);
    setInput('');
  };

  const escapeHTML = (str) => {
    if (typeof str !== 'string') {
      return '';
    }
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  };

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
