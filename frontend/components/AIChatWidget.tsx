'use client';

import { useState } from 'react';

interface Citation {
    law_name: string;
    paragraph: string;
    article: string | null;
    formatted: string;
}

interface AIResponse {
    answer: string;
    citations: Citation[];
    has_citations: boolean;
}

interface AIChatWidgetProps {
    caseId?: string;
}

export default function AIChatWidget({ caseId }: AIChatWidgetProps) {
    const [message, setMessage] = useState('');
    const [chatHistory, setChatHistory] = useState<Array<{ role: string, content: string, citations?: Citation[] }>>([]);
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!message.trim()) return;

        // Add user message to history
        setChatHistory(prev => [...prev, { role: 'user', content: message }]);
        setLoading(true);

        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/ai/cases/chat', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message,
                    case_id: caseId || null
                }),
            });

            if (response.ok) {
                const data: AIResponse = await response.json();

                // Add AI response with citations
                setChatHistory(prev => [...prev, {
                    role: 'assistant',
                    content: data.answer,
                    citations: data.citations
                }]);
            }
        } catch (error) {
            console.error('Failed to send message:', error);
            setChatHistory(prev => [...prev, {
                role: 'error',
                content: 'Помилка з'єднання з AI асистентом'
      }]);
        } finally {
            setLoading(false);
            setMessage('');
        }
    };

    const renderContentWithLinks = (text: string) => {
        const urlRegex = /(https?:\/\/[^\s]+|www\.[^\s]+)/g;
        const parts = text.split(urlRegex);

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
                            className="underline hover:text-blue-800 font-medium break-all text-blue-700"
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

    return (
        <div className="bg-white rounded-lg shadow-lg flex flex-col h-[600px]">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-4 rounded-t-lg">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                        🤖
                    </div>
                    <div>
                        <h3 className="font-semibold">AI Юридичний Асистент</h3>
                        <p className="text-xs text-blue-100">З посиланнями на закони</p>
                    </div>
                </div>
            </div>

            {/* Chat History */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {chatHistory.length === 0 && (
                    <div className="text-center text-gray-500 py-12">
                        <div className="text-4xl mb-4">⚖️</div>
                        <p className="text-lg font-medium mb-2">Вітаю! Я ваш AI юридичний асистент</p>
                        <p className="text-sm">Задайте питання про ваш випадок, і я надам відповідь з посиланнями на закони</p>
                    </div>
                )}

                {chatHistory.map((msg, index) => (
                    <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] rounded-lg p-4 ${msg.role === 'user'
                            ? 'bg-blue-600 text-white'
                            : msg.role === 'error'
                                ? 'bg-red-100 text-red-800'
                                : 'bg-gray-100 text-gray-900'
                            }`}>
                            <div className="whitespace-pre-wrap">
                                {renderContentWithLinks(msg.content)}
                            </div>

                            {/* Citations */}
                            {msg.citations && msg.citations.length > 0 && (
                                <div className="mt-3 pt-3 border-t border-gray-300">
                                    <div className="text-xs font-semibold mb-2 text-gray-700">📚 Правові посилання:</div>
                                    <div className="space-y-1">
                                        {msg.citations.map((citation, idx) => (
                                            <div key={idx} className="text-xs bg-white/50 rounded px-2 py-1">
                                                <span className="font-medium">{citation.law_name}</span>
                                                {citation.paragraph && <span className="text-gray-600">, § {citation.paragraph}</span>}
                                                {citation.article && <span className="text-gray-600">, čl. {citation.article}</span>}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                ))}

                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-gray-100 rounded-lg p-4">
                            <div className="flex items-center gap-2">
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                                <span className="text-sm text-gray-600">AI аналізує закони...</span>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Input */}
            <div className="border-t p-4">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                        placeholder="Задайте юридичне питання..."
                        className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        disabled={loading}
                    />
                    <button
                        onClick={sendMessage}
                        disabled={loading || !message.trim()}
                        className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white px-6 py-2 rounded-lg font-medium transition-colors"
                    >
                        Надіслати
                    </button>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                    ⚠️ Всі відповіді містять посилання на конкретні закони та параграфи
                </p>
            </div>
        </div>
    );
}
