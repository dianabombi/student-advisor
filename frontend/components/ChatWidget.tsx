'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, FileText, Sparkles, AlertCircle } from 'lucide-react';

interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
    sources?: ChatSource[];
}

interface ChatSource {
    filename: string;
    chunk_index: number;
    distance: number;
}

export default function ChatWidget() {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLTextAreaElement>(null);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSendMessage = async () => {
        if (!inputMessage.trim() || isLoading) return;

        const userMessage = inputMessage.trim();
        setInputMessage('');
        setIsLoading(true);
        setError(null);

        // Add user message to UI
        const newUserMessage: ChatMessage = {
            role: 'user',
            content: userMessage
        };
        setMessages(prev => [...prev, newUserMessage]);

        try {
            const token = localStorage.getItem('token');

            // Prepare history
            const history = messages.map(msg => ({
                role: msg.role,
                content: msg.content
            }));

            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    message: userMessage,
                    history: history,
                    k: 5
                })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Add assistant message to UI
            const assistantMessage: ChatMessage = {
                role: 'assistant',
                content: data.reply,
                sources: data.sources
            };
            setMessages(prev => [...prev, assistantMessage]);

        } catch (error: any) {
            console.error('Error sending message:', error);
            setError(error.message || 'Failed to send message');

            // Add error message to chat
            const errorMessage: ChatMessage = {
                role: 'assistant',
                content: 'Prepáčte, vyskytla sa chyba. Skúste to prosím znova.'
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
            inputRef.current?.focus();
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
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

                // Remove trailing punctuation (greedy)
                const cleanHref = href.replace(/[.,;!?)]+$/, '');
                const cleanPart = part.replace(/[.,;!?)]+$/, '');
                const punctuation = part.slice(cleanPart.length);

                return (
                    <span key={index}>
                        <a
                            href={cleanHref}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="underline hover:text-purple-300 font-medium break-all text-purple-200"
                            onClick={(e: any) => e.stopPropagation()}
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
        <div className="flex flex-col h-full bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 rounded-2xl overflow-hidden">
            {/* Header */}
            <div className="bg-white/5 backdrop-blur-lg border-b border-white/10 p-4">
                <div className="flex items-center gap-2">
                    <Sparkles className="w-6 h-6 text-purple-400" />
                    <h2 className="text-xl font-bold text-white">CODEX Legal AI</h2>
                </div>
            </div>

            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-full text-center">
                        <Sparkles className="w-16 h-16 text-purple-400 mb-4" />
                        <h3 className="text-2xl font-bold text-white mb-2">
                            Vitajte v CODEX Legal AI
                        </h3>
                        <p className="text-gray-400 max-w-md">
                            Opýtajte sa ma na čokoľvek o slovenskom práve alebo vašich právnych dokumentoch.
                        </p>
                    </div>
                )}

                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div
                            className={`max-w-3xl rounded-2xl p-4 ${message.role === 'user'
                                ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                                : 'bg-white/10 backdrop-blur-lg border border-white/20 text-white'
                                }`}
                        >
                            <div className="whitespace-pre-wrap">
                                {renderContentWithLinks(message.content)}
                            </div>

                            {/* Sources */}
                            {message.sources && message.sources.length > 0 && (
                                <div className="mt-4 pt-4 border-t border-white/20">
                                    <div className="flex items-center gap-2 text-sm text-gray-300 mb-2">
                                        <FileText className="w-4 h-4" />
                                        <span>Zdroje:</span>
                                    </div>
                                    <div className="space-y-2">
                                        {message.sources.map((source, idx) => (
                                            <div
                                                key={idx}
                                                className="text-sm bg-white/5 rounded-lg p-3 hover:bg-white/10 transition-colors"
                                            >
                                                <div className="font-semibold text-purple-300">
                                                    {source.filename}
                                                </div>
                                                <div className="text-xs text-gray-500 mt-1">
                                                    Chunk {source.chunk_index} • Vzdialenosť: {source.distance.toFixed(3)}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-4">
                            <div className="flex items-center gap-2 text-white">
                                <Loader2 className="w-5 h-5 animate-spin" />
                                <span>Premýšľam...</span>
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Error Display */}
            {error && (
                <div className="mx-6 mb-2 p-3 bg-red-500/20 border border-red-500/50 rounded-lg flex items-center gap-2 text-red-200">
                    <AlertCircle className="w-4 h-4" />
                    <span className="text-sm">{error}</span>
                </div>
            )}

            {/* Input Area */}
            <div className="border-t border-white/10 bg-slate-900/50 backdrop-blur-lg p-4">
                <div className="flex gap-3">
                    <textarea
                        ref={inputRef}
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Položte právnu otázku..."
                        className="flex-1 bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
                        rows={2}
                        disabled={isLoading}
                    />
                    <button
                        onClick={handleSendMessage}
                        disabled={!inputMessage.trim() || isLoading}
                        className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center gap-2"
                    >
                        {isLoading ? (
                            <Loader2 className="w-5 h-5 animate-spin" />
                        ) : (
                            <>
                                <Send className="w-5 h-5" />
                                <span className="hidden sm:inline">Odoslať</span>
                            </>
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}
