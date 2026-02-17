'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { useLanguage } from '@/lib/LanguageContext';
import { useJurisdiction } from '@/contexts/JurisdictionContext';

export default function HousingSearchPage() {
    const router = useRouter();
    const { isAuthenticated, isLoading, user } = useAuth();
    const { t, language } = useLanguage();
    const { jurisdiction } = useJurisdiction();
    const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isTyping, setIsTyping] = useState(false);

    // Redirect to login if not authenticated
    useEffect(() => {
        const storedToken = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
        const storedUser = typeof window !== 'undefined' ? localStorage.getItem('user') : null;

        if (!isLoading && !isAuthenticated && !storedToken && !storedUser) {
            router.push('/register?redirect=/housing');
        }
    }, [isAuthenticated, isLoading, router]);

    // Initial greeting when page loads
    useEffect(() => {
        const storedUser = typeof window !== 'undefined' ? localStorage.getItem('user') : null;
        const userName = user?.name || (storedUser ? JSON.parse(storedUser).name : 'Student');

        if ((isAuthenticated || storedUser) && messages.length === 0) {
            const greeting = {
                role: 'assistant',
                content: t('housing.welcome').replace('{{name}}', userName)
            };
            setMessages([greeting]);
        }
    }, [isAuthenticated, user, t, messages.length]);

    // Show loading while checking authentication
    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    const storedToken = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    const storedUser = typeof window !== 'undefined' ? localStorage.getItem('user') : null;

    if (!isAuthenticated && !storedToken && !storedUser) {
        return null;
    }

    const renderMessageWithLinks = (text: string) => {
        // Regular expression to detect URLs
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        const parts = text.split(urlRegex);

        return parts.map((part, index) => {
            if (part.match(urlRegex)) {
                return (
                    <a
                        key={index}
                        href={part}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 underline font-medium"
                    >
                        {part}
                    </a>
                );
            }
            return part;
        });
    };

    const handleSendMessage = async () => {
        if (!inputMessage.trim()) return;

        const userMessage = { role: 'user', content: inputMessage };
        setMessages(prev => [...prev, userMessage]);
        setInputMessage('');
        setIsTyping(true);

        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/housing/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...(token && { 'Authorization': `Bearer ${token}` })
                },
                body: JSON.stringify({
                    message: inputMessage,
                    conversation_history: messages,
                    jurisdiction: jurisdiction,
                    language: language
                })
            });

            if (response.ok) {
                const data = await response.json();
                setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
            } else {
                throw new Error(`Failed to get response: ${response.status}`);
            }
        } catch (error) {
            console.error('❌ Housing chat error:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: t('housing.error')
            }]);
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
            {/* Header */}
            <div className="bg-white border-b border-gray-200 shadow-sm">
                <div className="max-w-7xl mx-auto px-4 py-8">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                                🏠 {t('housing.title')}
                            </h1>
                            <p className="text-gray-600 mt-2 text-lg">
                                {t('housing.subtitle')}
                            </p>
                        </div>
                        <button
                            onClick={() => router.push('/')}
                            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                        >
                            {t('common.back')}
                        </button>
                    </div>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 py-8">
                {/* Chat Interface */}
                <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
                    <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-6">
                        <h2 className="text-2xl font-bold text-white">
                            💬 {t('housing.chatTitle')}
                        </h2>
                        <p className="text-blue-100 mt-2">
                            {t('housing.chatDescription')}
                        </p>
                    </div>

                    {/* Messages */}
                    <div className="h-[500px] overflow-y-auto p-6 space-y-4 bg-gray-50">
                        {messages.map((message, index) => (
                            <div
                                key={index}
                                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div
                                    className={`max-w-[80%] rounded-2xl px-6 py-4 shadow-md ${message.role === 'user'
                                        ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                                        : 'bg-white text-gray-900 border border-gray-200'
                                        }`}
                                >
                                    <p className="whitespace-pre-wrap">{renderMessageWithLinks(message.content)}</p>
                                </div>
                            </div>
                        ))}

                        {isTyping && (
                            <div className="flex justify-start">
                                <div className="bg-white rounded-2xl px-6 py-4 shadow-md border border-gray-200">
                                    <div className="flex space-x-2">
                                        <div className="w-3 h-3 bg-blue-600 rounded-full animate-bounce"></div>
                                        <div className="w-3 h-3 bg-purple-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                                        <div className="w-3 h-3 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Input */}
                    <div className="border-t border-gray-200 p-6 bg-white">
                        <div className="flex space-x-4">
                            <input
                                type="text"
                                value={inputMessage}
                                onChange={(e) => setInputMessage(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                                placeholder={t('housing.placeholder')}
                                className="flex-1 px-6 py-4 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                            />
                            <button
                                onClick={handleSendMessage}
                                disabled={isTyping || !inputMessage.trim()}
                                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105"
                            >
                                {t('housing.send')}
                            </button>
                        </div>
                    </div>
                </div>

                {/* Info Box */}
                <div className="mt-8 bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-200 rounded-2xl p-6">
                    <div className="flex items-start space-x-4">
                        <div className="text-3xl">💡</div>
                        <div>
                            <h3 className="font-bold text-gray-900 mb-2">{t('housing.infoTitle')}</h3>
                            <p className="text-gray-700">{t('housing.info')}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
