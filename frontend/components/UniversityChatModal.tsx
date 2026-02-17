'use client';

import { useState, useEffect, useRef } from 'react';
import { X, Send, Bot } from 'lucide-react';
import { useLanguage } from '@/lib/LanguageContext';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
}

interface UniversityChatModalProps {
    isOpen: boolean;
    onClose: () => void;
    universityId: number;
    universityName: string;
}

export default function UniversityChatModal({
    isOpen,
    onClose,
    universityId,
    universityName
}: UniversityChatModalProps) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId, setSessionId] = useState<string>('');
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const { t } = useLanguage();

    // Clear messages and reset session when university changes
    useEffect(() => {
        if (isOpen) {
            setMessages([]);
            setSessionId(`session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
        }
    }, [universityId, isOpen]);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Add welcome message when modal opens
    useEffect(() => {
        if (isOpen && messages.length === 0) {
            setMessages([{
                role: 'assistant',
                content: t('university.chat.welcome').replace('{university}', universityName),
                timestamp: new Date()
            }]);
        }
    }, [isOpen, universityName, t, messages.length]);

    const handleSendMessage = async () => {
        if (!inputMessage.trim() || isLoading) return;

        const userMessage: Message = {
            role: 'user',
            content: inputMessage,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputMessage('');
        setIsLoading(true);

        try {
            const url = `/api/universities/${universityId}/chat`;

            // Prepare conversation history
            const conversationHistory = messages
                .filter(msg => msg.role === 'user' || msg.role === 'assistant')
                .map(msg => ({
                    role: msg.role,
                    content: msg.content
                }));

            // Get current platform language
            const currentLanguage = t('language.code');

            const requestBody = {
                message: inputMessage,
                session_id: sessionId,
                conversation_history: conversationHistory,
                language: currentLanguage
            };

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            const data = await response.json();

            const assistantMessage: Message = {
                role: 'assistant',
                content: data.response,
                timestamp: new Date()
            };

            setMessages(prev => [...prev, assistantMessage]);

        } catch (error) {
            console.error('Chat error:', error);
            const errorMessage: Message = {
                role: 'assistant',
                content: t('university.chat.error'),
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    const renderContentWithLinks = (text: string) => {
        // First, convert markdown links [text](url) to just the URL
        let processedText = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '$2');

        // Then parse URLs
        const urlRegex = /(https?:\/\/[^\s]+|www\.[^\s]+)/g;
        const parts = processedText.split(urlRegex);

        return parts.map((part, index) => {
            if (part.match(urlRegex)) {
                let href = part;
                if (part.startsWith('www.')) {
                    href = `https://${part}`;
                }

                const cleanHref = href.replace(/[.,;!?)]+$/, '');
                const cleanPart = part.replace(/[.,;!?)]+$/, '');
                const punctuation = part.slice(cleanPart.length);

                return (
                    <span key={index}>
                        <a
                            href={cleanHref}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="underline hover:text-blue-200 font-medium break-all"
                            onClick={(e) => e.stopPropagation()}
                        >
                            {cleanPart}
                        </a>
                        {punctuation}
                    </span>
                );
            }
            return part;
        });
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
            <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl h-[600px] flex flex-col">
                <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-blue-600 text-white rounded-t-lg">
                    <div className="flex items-center gap-3">
                        <Bot className="w-6 h-6" />
                        <div>
                            <h3 className="font-bold text-lg">{t('university.chat.title')}</h3>
                            <p className="text-sm text-blue-100">{universityName}</p>
                        </div>
                    </div>
                    <button
                        onClick={onClose}
                        className="text-white hover:bg-blue-700 rounded-full p-2 transition-colors"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            {message.role === 'assistant' && (
                                <div className="flex-shrink-0">
                                    <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
                                        <Bot className="w-5 h-5 text-white" />
                                    </div>
                                </div>
                            )}
                            <div
                                className={`max-w-[70%] rounded-lg p-3 ${message.role === 'user'
                                        ? 'bg-blue-600 text-white'
                                        : 'bg-white border border-gray-200'
                                    }`}
                            >
                                <div className="whitespace-pre-wrap break-words">
                                    {renderContentWithLinks(message.content)}
                                </div>
                            </div>
                        </div>
                    ))}
                    {isLoading && (
                        <div className="flex justify-start gap-3">
                            <div className="flex-shrink-0">
                                <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
                                    <Bot className="w-5 h-5 text-white" />
                                </div>
                            </div>
                            <div className="bg-white border border-gray-200 rounded-lg p-3">
                                <div className="flex gap-1">
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                <div className="border-t border-gray-200 p-4 bg-white rounded-b-lg">
                    <div className="flex gap-2">
                        <input
                            type="text"
                            value={inputMessage}
                            onChange={(e) => setInputMessage(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder={t('university.chat.placeholder')}
                            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            disabled={isLoading}
                        />
                        <button
                            onClick={handleSendMessage}
                            disabled={!inputMessage.trim() || isLoading}
                            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                        >
                            <Send className="w-4 h-4" />
                            <span className="hidden sm:inline">{t('university.chat.send')}</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
