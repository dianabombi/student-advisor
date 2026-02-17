'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, FileText, Sparkles } from 'lucide-react';
import { useLanguage } from '@/lib/LanguageContext';

interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
    sources?: ChatSource[];
}

interface ChatSource {
    document_id: number;
    filename: string;
    chunk_index: number;
    content: string;
    similarity: number;
}

interface ChatInterfaceProps {
    sessionId?: number;
    onSessionCreated?: (sessionId: number) => void;
}

export default function ChatInterface({ sessionId, onSessionCreated }: ChatInterfaceProps) {
    const { t } = useLanguage();
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [currentSessionId, setCurrentSessionId] = useState<number | undefined>(sessionId);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLTextAreaElement>(null);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Load session messages if sessionId provided
    useEffect(() => {
        if (sessionId) {
            loadSessionMessages(sessionId);
        }
    }, [sessionId]);

    const loadSessionMessages = async (sid: number) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`/api/chat/sessions/${sid}/messages`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                const formattedMessages = data.messages.map((msg: any) => ({
                    role: msg.role,
                    content: msg.content,
                    sources: msg.sources
                }));
                setMessages(formattedMessages);
            }
        } catch (error) {
            console.error('Failed to load session messages:', error);
        }
    };

    const handleSendMessage = async () => {
        if (!inputMessage.trim() || isLoading) return;

        const userMessage = inputMessage.trim();
        setInputMessage('');
        setIsLoading(true);

        // Add user message to UI
        const newUserMessage: ChatMessage = {
            role: 'user',
            content: userMessage
        };
        setMessages(prev => [...prev, newUserMessage]);

        try {
            const token = localStorage.getItem('token');

            // Prepare history for RAG API
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
                    k: 5,  // Retrieve top 5 chunks
                    include_context: false
                })
            });

            if (!response.ok) {
                // Handle rate limiting
                if (response.status === 429) {
                    const errorMessage: ChatMessage = {
                        role: 'assistant',
                        content: t('chat.rateLimitError') || 'You have made too many requests. Please wait a minute and try again.'
                    };
                    setMessages(prev => [...prev, errorMessage]);
                    setIsLoading(false);
                    return;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Add assistant message to UI with sources
            const assistantMessage: ChatMessage = {
                role: 'assistant',
                content: data.reply,
                sources: data.sources?.map((source: any) => ({
                    document_id: 0,  // Not provided by new API
                    filename: source.filename,
                    chunk_index: source.chunk_index,
                    content: '',  // Not provided by new API
                    similarity: 1 - source.distance  // Convert distance to similarity
                }))
            };
            setMessages(prev => [...prev, assistantMessage]);

        } catch (error) {
            console.error('Error sending message:', error);
            // Add error message
            const errorMessage: ChatMessage = {
                role: 'assistant',
                content: t('chat.error') || 'Sorry, something went wrong. Please try again.'
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

    return (
        <div className="flex flex-col h-full bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-full text-center">
                        <Sparkles className="w-16 h-16 text-purple-400 mb-4" />
                        <h2 className="text-2xl font-bold text-white mb-2">
                            {t('chat.welcome') || 'Welcome to CODEX Legal AI'}
                        </h2>
                        <p className="text-gray-400 max-w-md">
                            {t('chat.welcomeDesc') || 'Ask me anything about your legal documents or Slovak law.'}
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
                                        <span>{t('chat.sources') || 'Sources'}:</span>
                                    </div>
                                    <div className="space-y-2">
                                        {message.sources.map((source, idx) => (
                                            <div
                                                key={idx}
                                                className="text-sm bg-white/5 rounded-lg p-3 hover:bg-white/10 transition-colors"
                                            >
                                                <div className="font-semibold text-purple-300 mb-1">
                                                    {source.filename}
                                                </div>
                                                <div className="text-gray-400 text-xs line-clamp-2">
                                                    {source.content}
                                                </div>
                                                <div className="text-xs text-gray-500 mt-1">
                                                    {t('chat.similarity') || 'Relevance'}: {(source.similarity * 100).toFixed(0)}%
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
                                <span>{t('chat.thinking') || 'Thinking...'}</span>
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="border-t border-white/10 bg-slate-900/50 backdrop-blur-lg p-4">
                <div className="max-w-4xl mx-auto">
                    <div className="flex gap-3">
                        <textarea
                            ref={inputRef}
                            value={inputMessage}
                            onChange={(e) => setInputMessage(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder={t('chat.placeholder') || 'Ask a legal question...'}
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
                                    <span className="hidden sm:inline">{t('chat.send') || 'Send'}</span>
                                </>
                            )}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
