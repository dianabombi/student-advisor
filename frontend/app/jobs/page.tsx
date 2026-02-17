'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { useLanguage } from '@/lib/LanguageContext';
import { useJurisdiction } from '@/contexts/JurisdictionContext';

export default function JobsPage() {
    const router = useRouter();
    const { isAuthenticated, isLoading, user } = useAuth();
    const { t, language } = useLanguage();
    const { jurisdiction } = useJurisdiction();
    const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([]);
    const [inputMessage, setInputMessage] = useState('');
    const [contextCity, setContextCity] = useState<string | null>(null);
    const [contextUniversity, setContextUniversity] = useState<string | null>(null);
    const [isTyping, setIsTyping] = useState(false);

    useEffect(() => {
        const storedToken = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
        const storedUser = typeof window !== 'undefined' ? localStorage.getItem('user') : null;

        if (!isLoading && !isAuthenticated && !storedToken && !storedUser) {
            router.push('/register?redirect=/jobs');
        }
    }, [isAuthenticated, isLoading, router]);

    // Check for university context from localStorage
    useEffect(() => {
        const lastUniversity = localStorage.getItem('lastViewedUniversity');
        if (lastUniversity) {
            try {
                const uniData = JSON.parse(lastUniversity);
                // Only set context if the university belongs to the current jurisdiction
                if (uniData.country === jurisdiction) {
                    setContextCity(uniData.city);
                    setContextUniversity(uniData.name);
                } else {
                    // Clear context if it's from a different jurisdiction
                    setContextCity(null);
                    setContextUniversity(null);
                }
            } catch (e) {
                console.error('Error parsing university context:', e);
                setContextCity(null);
                setContextUniversity(null);
            }
        } else {
            setContextCity(null);
            setContextUniversity(null);
        }
    }, [jurisdiction]);

    useEffect(() => {
        const storedUser = typeof window !== 'undefined' ? localStorage.getItem('user') : null;
        const userName = user?.name || (storedUser ? JSON.parse(storedUser).name : 'Student');

        if ((isAuthenticated || storedUser) && messages.length === 0) {
            let greeting = `👋 ${t('jobs.greeting').replace('{name}', userName)}`;

            if (contextCity && contextUniversity) {
                greeting += `\n\n${t('jobs.greetingWithContext').replace('{university}', contextUniversity).replace('{city}', contextCity)}`;
            }

            greeting += `\n\n${t('jobs.howCanHelp')}`;

            setMessages([{ role: 'assistant', content: greeting }]);
        }
    }, [isAuthenticated, user, messages.length, contextCity, contextUniversity]);

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-white to-blue-50">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
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
            const response = await fetch('/api/jobs/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...(token && { 'Authorization': `Bearer ${token}` })
                },
                body: JSON.stringify({
                    message: inputMessage,
                    conversation_history: messages,
                    jurisdiction: jurisdiction,
                    language: language,
                    context: contextCity ? { city: contextCity, university: contextUniversity } : undefined
                })
            });

            if (response.ok) {
                const data = await response.json();
                setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
            } else {
                throw new Error(`Failed to get response: ${response.status}`);
            }
        } catch (error) {
            console.error('❌ Jobs chat error:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: t('jobs.error')
            }]);
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50">
            {/* Header */}
            <div className="bg-white border-b border-gray-200 shadow-sm">
                <div className="max-w-7xl mx-auto px-4 py-8">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-4xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
                                💼 {t('jobs.title')}
                            </h1>
                            <p className="text-gray-600 mt-2 text-lg">
                                {t('jobs.subtitle')}
                            </p>
                            {contextCity && contextUniversity && (
                                <p className="text-sm text-green-600 mt-1">
                                    📍 {t('jobs.searchIn')}: {contextCity} ({contextUniversity})
                                </p>
                            )}
                        </div>
                        <button
                            onClick={() => router.push('/')}
                            className="px-6 py-3 bg-gradient-to-r from-green-600 to-blue-600 text-white rounded-xl font-semibold hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                        >
                            {t('jobs.back')}
                        </button>
                    </div>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 py-8">
                {/* Chat Interface */}
                <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
                    <div className="bg-gradient-to-r from-green-600 to-blue-600 p-6">
                        <h2 className="text-2xl font-bold text-white">
                            💬 {t('jobs.chatTitle')}
                        </h2>
                        <p className="text-green-100 mt-2">
                            {t('jobs.chatSubtitle')}
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
                                        ? 'bg-gradient-to-r from-green-600 to-blue-600 text-white'
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
                                        <div className="w-3 h-3 bg-green-600 rounded-full animate-bounce"></div>
                                        <div className="w-3 h-3 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                                        <div className="w-3 h-3 bg-green-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
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
                                placeholder={t('jobs.placeholder')}
                                className="flex-1 px-6 py-4 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                            />
                            <button
                                onClick={handleSendMessage}
                                disabled={isTyping || !inputMessage.trim()}
                                className="px-8 py-4 bg-gradient-to-r from-green-600 to-blue-600 text-white rounded-xl font-semibold hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105"
                            >
                                {t('jobs.send')}
                            </button>
                        </div>
                    </div>
                </div>

                {/* Info Boxes */}
                <div className="grid md:grid-cols-2 gap-6 mt-8">
                    <div className="bg-gradient-to-r from-green-50 to-blue-50 border-2 border-green-200 rounded-2xl p-6">
                        <div className="flex items-start space-x-4">
                            <div className="text-3xl">💡</div>
                            <div>
                                <h3 className="font-bold text-gray-900 mb-2">{t('jobs.popularPortals')}</h3>
                                <ul className="text-gray-700 space-y-1">
                                    <li>• {t('jobs.portals.profesia')}</li>
                                    <li>• {t('jobs.portals.studentjob')}</li>
                                    <li>• {t('jobs.portals.brigada')}</li>
                                    <li>• {t('jobs.portals.kariera')}</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <div className="bg-gradient-to-r from-blue-50 to-green-50 border-2 border-blue-200 rounded-2xl p-6">
                        <div className="flex items-start space-x-4">
                            <div className="text-3xl">🎯</div>
                            <div>
                                <h3 className="font-bold text-gray-900 mb-2">{t('jobs.jobTypes')}</h3>
                                <ul className="text-gray-700 space-y-1">
                                    <li>• {t('jobs.types.parttime')}</li>
                                    <li>• {t('jobs.types.brigada')}</li>
                                    <li>• {t('jobs.types.seasonal')}</li>
                                    <li>• {t('jobs.types.homeoffice')}</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
