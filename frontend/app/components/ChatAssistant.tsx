'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Button } from './ui/Button';
import { sendChatMessage } from '@/lib/api';
import { ChatMessage, QUICK_QUESTIONS } from '@/lib/types';

interface ChatAssistantProps {
  kundaliId: string;
  personName: string;
}

export function ChatAssistant({ kundaliId, personName }: ChatAssistantProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      type: 'bot',
      content: `<b>Namaste! Main aapka Kundali Assistant hoon.</b><br><br>
<b style="color:#ff6b35;">${personName}</b> ki kundali taiyaar ho gayi hai!<br><br>
Ab aap <b>${personName}</b> ke baare mein kuch bhi puch sakte hain:<br>
- Career ke baare mein batao<br>
- Shaadi kab hogi?<br>
- Health kaisi rahegi?<br>
- Shani ka prabhav kya hai?<br><br>
Neeche quick buttons click karein ya apna sawaal type karein!`,
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (question?: string) => {
    const messageText = question || inputValue.trim();
    if (!messageText || isLoading) return;

    // Add user message
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      type: 'user',
      content: messageText,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await sendChatMessage(kundaliId, messageText);
      const botMessage: ChatMessage = {
        id: `bot-${Date.now()}`,
        type: 'bot',
        content: response.answer,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        type: 'bot',
        content: 'क्षमा करें, कुछ त्रुटि हुई। कृपया पुनः प्रयास करें। / Sorry, something went wrong. Please try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-chat text-white p-5 text-center">
        <h3 className="text-xl font-bold flex items-center justify-center gap-2">
          <span className="text-2xl">🤖</span>
          AI कुंडली सहायक / AI Kundali Assistant
        </h3>
        <p className="text-white/80 text-sm mt-1">
          अपनी कुंडली के बारे में कुछ भी पूछिए! / Ask anything about your kundali!
        </p>
      </div>

      {/* Messages */}
      <div className="h-96 overflow-y-auto p-5 bg-gray-50">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`mb-4 flex flex-col ${
              message.type === 'user' ? 'items-end' : 'items-start'
            }`}
          >
            <div
              className={`max-w-[80%] p-4 rounded-2xl ${
                message.type === 'user'
                  ? 'bg-gradient-primary text-white rounded-br-sm'
                  : 'bg-white border border-gray-200 shadow-sm rounded-bl-sm'
              }`}
              dangerouslySetInnerHTML={{ __html: message.content }}
            />
          </div>
        ))}

        {/* Typing indicator */}
        {isLoading && (
          <div className="flex items-start mb-4">
            <div className="bg-white border border-gray-200 p-4 rounded-2xl rounded-bl-sm shadow-sm">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '200ms' }} />
                <span className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '400ms' }} />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Questions */}
      <div className="flex flex-wrap gap-2 p-4 bg-gray-100 border-t border-gray-200">
        {QUICK_QUESTIONS.map((q) => (
          <button
            key={q.question}
            onClick={() => handleSend(q.question)}
            disabled={isLoading}
            className="px-3 py-2 bg-white border border-gray-300 rounded-full text-sm font-medium hover:bg-indigo-500 hover:text-white hover:border-indigo-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {q.icon} {q.labelHindi}
          </button>
        ))}
      </div>

      {/* Input */}
      <div className="flex gap-3 p-4 bg-white border-t border-gray-200">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="अपना प्रश्न यहाँ लिखें... / Type your question here..."
          disabled={isLoading}
          className="flex-1 px-5 py-3 border-2 border-gray-300 rounded-full text-base focus:border-indigo-500 focus:outline-none disabled:bg-gray-100"
        />
        <Button
          variant="chat"
          onClick={() => handleSend()}
          disabled={isLoading || !inputValue.trim()}
          className="px-6 rounded-full"
        >
          भेजें / Send ➤
        </Button>
      </div>
    </div>
  );
}
