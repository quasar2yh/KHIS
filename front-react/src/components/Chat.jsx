import React, { useState, useEffect } from 'react';
import { getChatMessages, sendMessage,getAccountInfo } from '../apis/apis';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [receiver, setReceiver] = useState('');
  const [user ,setUser]= useState([]);


  useEffect(() => {
    async function fetchMessages() {
        const data = await getChatMessages();
        setMessages(data);
        console.log("data",data)

      // 사용자 ID 목록 추출
      // 사용자 ID 목록 추출
      const senderIds = data.map(msg => msg.sender);
      const receiverIds = data.map(msg => msg.receiver);

    // 중복 제거된 사용자 ID 목록 생성
      const userIds = [...new Set([...senderIds, ...receiverIds])];
    
    // 사용자 정보 가져오기
        const userPromises = userIds.map(id => getAccountInfo(id));
        const userData = await Promise.all(userPromises);
        console.log(userData,"sssssssssssssssssssss")

    // 사용자 정보를 ID를 키로, name을 값으로 저장
        const userMap = userData.reduce((acc, user) => {
        acc[user.id] = user.name.first_name + ' ' + user.name.last_name; // 이름 조합
        return acc;
        }, {});
        setUser(userMap);
        console.log("Fetched users:", userMap);
    }
    fetchMessages();
  }, []); 


  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim() === '' || receiver.trim() === '') return;

    const newMessage = await sendMessage(receiver, input);
    setMessages([...messages, newMessage]);
    setInput('');
    
  };
  const escapeHTML = (str) => {
    if (typeof str !== 'string') {
      return ''; // 문자열이 아닐 경우 빈 문자열 반환
    }
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  };
  

  return (
    <div>
      <h2>Chat</h2>
      <div className="chat-box">
    
        {messages.map((msg, index) => {
            console.log("Message object:", msg); // 여기에서 msg 객체를 출력
            return (
              <p key={index}>
                {user[msg.sender]} &rarr; 
                {user[msg.receiver]}: 
                {escapeHTML(msg.message)}
              </p>
            );
          })}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="메세지를 입력하세요"
        />
        <input
          type="text"
          value={receiver}
          onChange={(e) => setReceiver(e.target.value)}
          placeholder="받는이"
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default Chat;
