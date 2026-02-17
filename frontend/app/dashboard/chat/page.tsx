'use client';

import { useState, useRef, useEffect } from 'react';
import { ArrowLeft, Send, Bot, User as UserIcon } from 'lucide-react';
import Link from 'next/link';
import { useLanguage } from '@/lib/LanguageContext';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { UPLDisclaimer } from '@/components/UPLDisclaimer';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

export default function ChatPage() {
    return (
        <ErrorBoundary>
            <ChatPageContent />
        </ErrorBoundary>
    );
}

function ChatPageContent() {
    const { t } = useLanguage();
    const [messages, setMessages] = useState<Message[]>([
        {
            role: 'assistant',
            content: t('ai.welcome')
        }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setLoading(true);

        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ message: userMessage })
            });

            if (response.ok) {
                const data = await response.json();
                setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
            } else {
                setMessages(prev => [...prev, {
                    role: 'assistant',
                    content: t('ai.error_retry')
                }]);
            }
        } catch (err) {
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: t('ai.error_connection')
            }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col">
            {/* Header */}
            <div className="border-b border-white/10 bg-white/5 backdrop-blur-lg">
                <div className="container mx-auto px-6 py-4">
                    <Link href="/dashboard" className="inline-flex items-center space-x-2 text-gray-300 hover:text-white transition-colors">
                        <ArrowLeft className="w-5 h-5" />
                        <span>{t('dashboard.back_to_dashboard')}</span>
                    </Link>
                </div>
            </div>

            {/* Chat Container */}
            <div className="flex-1 container mx-auto px-6 py-8 flex flex-col max-w-4xl">
                <h1 className="text-3xl font-bold text-white mb-6">{t('ai.title')}</h1>

                {/* UPL Disclaimer */}
                <UPLDisclaimer />

                {/* Messages */}
                <div className="flex-1 bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-6 overflow-y-auto mb-6 space-y-4">
                    {messages.map((message, idx) => (
                        <div
                            key={idx}
                            className={`flex items-start space-x-3 ${message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                                }`}
                        >
                            <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${message.role === 'user'
                                ? 'bg-gradient-to-br from-purple-500 to-pink-500'
                                : 'bg-gradient-to-br from-blue-500 to-cyan-500'
                                }`}>
                                {message.role === 'user' ? (
                                    <UserIcon className="w-5 h-5 text-white" />
                                ) : (
                                    <Bot className="w-5 h-5 text-white" />
                                )}
                            </div>
                            <div className={`flex-1 ${message.role === 'user' ? 'text-right' : ''}`}>
                                <div className={`inline-block max-w-[80%] px-4 py-3 rounded-2xl ${message.role === 'user'
                                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                                    : 'bg-white/10 text-gray-100'
                                    }`}>
                                    <p className="whitespace-pre-wrap">{message.content}</p>
                                </div>
                            </div>
                        </div>
                    ))}
                    {loading && (
                        <div className="flex items-start space-x-3">
                            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
                                <Bot className="w-5 h-5 text-white" />
                            </div>
                            <div className="bg-white/10 px-4 py-3 rounded-2xl">
                                <div className="flex space-x-2">
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input */}
                <form onSubmit={handleSubmit} className="flex space-x-3">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder={t('ai.placeholder')}
                        className="flex-1 px-6 py-4 bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        disabled={loading || !input.trim()}
                        className="px-6 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </form>

                {/* Suggestions */}
                <div className="mt-4 flex flex-wrap gap-2">
                    {[t('ai.suggestions.1'), t('ai.suggestions.2'), t('ai.suggestions.3')].map((suggestion, idx) => (
                        <button
                            key={idx}
                            onClick={() => setInput(suggestion)}
                            className="px-4 py-2 bg-white/5 hover:bg-white/10 text-gray-300 text-sm rounded-lg border border-white/10 transition-all"
                        >
                            {suggestion}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}
