'use client';

import { useState, useRef, useEffect } from 'react';
import Message from './Message';

const SUGGESTED_QUESTIONS = [
  "What departments are available in ANITS?",
  "Where is the placement cell?",
  "What are the library timings?",
  "How do I join a club?",
  "What is the highest placement package?",
];

export default function ChatBox({ activeCategory = "general" }) {

  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content:
        'Hi! 👋 I am your ANITS Campus Assistant. Ask me anything about departments, facilities, placements, events, and more!',
      media: null,
      recommendations: [],
      timestamp: new Date().toLocaleTimeString()
    }
  ]);

  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef(null);

  // Auto scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (question) => {

    const userQuestion = question || input.trim();
    if (!userQuestion) return;

    const userMsg = {
      role: 'user',
      content: userQuestion,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('https://campusinfo.onrender.com/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: userQuestion,
          category: activeCategory === "general" ? null : activeCategory,
          session_id: "default"
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const assistantMsg = {
        role: 'assistant',
        content: data.answer || "No response received.",
        media: data.media || null,
        recommendations: data.recommendations || [],
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, assistantMsg]);

    } catch (error) {

      console.error("Error:", error);

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `❌ Error: ${error.message}. Make sure FastAPI is running.`,
        media: null,
        recommendations: [],
        timestamp: new Date().toLocaleTimeString()
      }]);

    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col flex-1 overflow-hidden">

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">

        {/* Suggested questions */}
        {messages.length === 1 && (
          <div className="max-w-2xl mx-auto">
            <p className="text-gray-400 text-sm mb-3 text-center">
              Try asking:
            </p>

            <div className="flex flex-wrap gap-2 justify-center">
              {SUGGESTED_QUESTIONS.map((q, i) => (
                <button
                  key={i}
                  onClick={() => sendMessage(q)}
                  className="px-3 py-2 bg-gray-800 hover:bg-gray-700 rounded-full text-sm text-gray-300 hover:text-white transition border border-gray-600 hover:border-gray-400"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Chat messages */}
        {messages.map((msg, i) => (
          <Message key={i} message={msg} onSuggestionClick={sendMessage}/>
        ))}

        {/* Thinking animation */}
        {isLoading && (
          <div className="flex items-center gap-2 text-gray-400 px-4">

            <div className="flex gap-1">
              <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
              <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
              <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>

            <span className="text-sm">Thinking...</span>

          </div>
        )}

        <div ref={bottomRef} />

      </div>

      {/* Input box */}
      <div className="px-4 py-4 bg-gray-900 border-t border-gray-700">

        <div className="max-w-3xl mx-auto flex gap-3 items-end">

          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Ask anything about ANITS..."
            rows={1}
            className="flex-1 bg-gray-800 text-white rounded-xl px-4 py-3 resize-none outline-none border border-gray-600 focus:border-blue-500 transition placeholder-gray-500"
          />

          <button
            onClick={() => sendMessage()}
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-xl px-5 py-3 transition font-medium"
          >
            Send →
          </button>

        </div>

        <p className="text-center text-xs text-gray-600 mt-2">
          Press Enter to send • Shift+Enter for new line
        </p>

      </div>

    </div>
  );
}