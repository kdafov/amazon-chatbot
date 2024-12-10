import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import ChatIcon from '../public/logo.png';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

const App: React.FC = () => {
  const [isChatOpen, setIsChatOpen] = useState<boolean>(false);
  const [messages, setMessages] = useState<Message[]>([{sender: 'bot', text: 'Hello! How can we help you today?'}]);
  const [input, setInput] = useState<string>("");
  const chatWindowRef = useRef<HTMLDivElement | null>(null);

  const toggleChat = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsChatOpen(!isChatOpen);
  };

  const handleSendMessage = async () => {
    if (input.trim()) {
      setMessages([...messages, { sender: 'user', text: input }]);
      setInput("");

      // Query the Dialogflow CX
      try {
        const response = await fetch('http://localhost:5000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: input }),
        });
        const data = await response.json();
        const botMessage: Message = { sender: 'bot', text: data.response };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
      } catch (error) {
        console.error('Error fetching from server:', error);
        const errorMessage: Message = { sender: 'bot', text: 'Sorry, there was an error. Please try again.' };
        setMessages((prevMessages) => [...prevMessages, errorMessage]);
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  const handleClickOutside = (e: MouseEvent) => {
    if (chatWindowRef.current && !chatWindowRef.current.contains(e.target as Node)) {
      setIsChatOpen(false);
    }
  };

  useEffect(() => {
    if (isChatOpen) {
      document.addEventListener('click', handleClickOutside);
    } else {
      document.removeEventListener('click', handleClickOutside);
    }
    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, [isChatOpen]);

  return (
    <div className="App">
      {/* Chat Pop-up Button */}
      {!isChatOpen && (
        <div className="chat-popup-button" onClick={toggleChat}>
          <img src={ChatIcon} alt="Chat Icon" className="chat-icon" />
        </div>
      )}

      {/* Chat Window */}
      {isChatOpen && (
        <div className="chat-window" ref={chatWindowRef} onClick={(e) => e.stopPropagation()}>
          <div className="chat-header">
            <span>Customer support chat</span>
            <button onClick={toggleChat}>X</button>
          </div>
          <div className="chat-body">
            {messages.map((message, index) => (
              <div key={index} className={`chat-message ${message.sender}`}>
                {message.text}
              </div>
            ))}
          </div>
          <div className="chat-input">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="I need help with..."
            />
            <button onClick={handleSendMessage}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;