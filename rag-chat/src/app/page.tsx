'use client';

import { useState, useRef, useEffect, FormEvent } from 'react';

// Define the structure of a message in our chat
interface Message {
  text: string;
  isUser: boolean;
}

export default function Home() {
  // State to hold all chat messages
  const [messages, setMessages] = useState<Message[]>([]);
  // State for the user's current input
  const [input, setInput] = useState('');
  // State to show a loading indicator while the backend is thinking
  const [isLoading, setIsLoading] = useState(false);

  // Ref to the chat container to auto-scroll to the latest message
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Effect to scroll down whenever a new message is added
  useEffect(() => {
    chatContainerRef.current?.scrollTo({
      top: chatContainerRef.current.scrollHeight,
      behavior: 'smooth',
    });
  }, [messages]);
  
  // This function is called when the user submits the form (sends a message)
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user's message to the chat
    const userMessage: Message = { text: input, isUser: true };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // THE MOST IMPORTANT PART: Calling the Python Backend!
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // Send the user's query in the request body
        body: JSON.stringify({ query: input }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }
      
      const data = await response.json();

      // Add the backend's response to the chat
      const botMessage: Message = { text: data.answer, isUser: false };
      setMessages((prevMessages) => [...prevMessages, botMessage]);

    } catch (error) {
      console.error("Failed to fetch from backend:", error);
      // Add an error message to the chat
      const errorMessage: Message = { text: 'Sorry, I ran into an error. Please check the console.', isUser: false };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      // Stop the loading indicator
      setIsLoading(false);
    }
  };
  
  return (
    <main className="flex flex-col h-screen bg-gray-900 text-white">
      <header className="bg-gray-800 p-4 shadow-md">
        <h1 className="text-2xl font-bold text-center">RAG Chat with Amazon Bedrock</h1>
      </header>
      
      {/* Chat messages container */}
      <div ref={chatContainerRef} className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-xl p-3 rounded-lg ${msg.isUser ? 'bg-blue-600' : 'bg-gray-700'}`}>
              <p className="text-sm" style={{ whiteSpace: 'pre-wrap' }}>{msg.text}</p>
            </div>
          </div>
        ))}
        {/* Show loading indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-lg p-3 rounded-lg bg-gray-700">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse [animation-delay:-0.3s]"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse [animation-delay:-0.15s]"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input form */}
      <div className="border-t border-gray-700 p-4 bg-gray-800">
        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask anything about human nutrition..."
            className="flex-1 p-2 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 rounded-md hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed"
            disabled={isLoading}
          >
            Send
          </button>
        </form>
      </div>
    </main>
  );
}
