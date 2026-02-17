'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ChatInterface from '@/components/ChatInterface';
import UsageIndicator from '@/components/UsageIndicator';
import { MessageSquare, Plus, Trash2, Clock } from 'lucide-react';
import { useLanguage } from '@/lib/LanguageContext';
import LanguageSwitcher from '@/components/LanguageSwitcher';

interface ChatSession {
    id: number;
    title: string;
    created_at: string;
    updated_at: string;
    message_count: number;
}

export default function ChatPage() {
    const { t } = useLanguage();
    const router = useRouter();
    const [sessions, setSessions] = useState<ChatSession[]>([]);
    const [currentSessionId, setCurrentSessionId] = useState<number | undefined>();
    const [isLoadingSessions, setIsLoadingSessions] = useState(true);

    useEffect(() => {
        // Check authentication
        const token = localStorage.getItem('token');
        if (!token) {
            router.push('/login');
            return;
        }

        loadSessions();
    }, []);

    const loadSessions = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/chat/sessions', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                setSessions(data);
            }
        } catch (error) {
            console.error('Failed to load sessions:', error);
        } finally {
            setIsLoadingSessions(false);
        }
    };

    const createNewSession = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/chat/sessions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ title: 'New Conversation' })
            });

            if (response.ok) {
                const newSession = await response.json();
                setSessions(prev => [newSession, ...prev]);
                setCurrentSessionId(newSession.id);
            }
        } catch (error) {
            console.error('Failed to create session:', error);
        }
    };

    const deleteSession = async (sessionId: number) => {
        if (!confirm(t('chat.confirmDelete') || 'Are you sure you want to delete this conversation?')) {
            return;
        }

        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`/api/chat/sessions/${sessionId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                setSessions(prev => prev.filter(s => s.id !== sessionId));
                if (currentSessionId === sessionId) {
                    setCurrentSessionId(undefined);
                }
            }
        } catch (error) {
            console.error('Failed to delete session:', error);
        }
    };

    const handleSessionCreated = (sessionId: number) => {
        setCurrentSessionId(sessionId);
        loadSessions();
    };

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);

        if (diffMins < 1) return t('chat.justNow') || 'Just now';
        if (diffMins < 60) return `${diffMins}${t('chat.minsAgo') || 'm ago'}`;
        if (diffHours < 24) return `${diffHours}${t('chat.hoursAgo') || 'h ago'}`;
        if (diffDays < 7) return `${diffDays}${t('chat.daysAgo') || 'd ago'}`;
        return date.toLocaleDateString();
    };

    return (
        <div className="flex h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
            {/* Sidebar */}
            <div className="w-80 bg-slate-900/50 backdrop-blur-lg border-r border-white/10 flex flex-col">
                {/* Header */}
                <div className="p-4 border-b border-white/10">
                    <div className="flex items-center justify-between mb-4">
                        <h1 className="text-xl font-bold text-white flex items-center gap-2">
                            <MessageSquare className="w-6 h-6 text-purple-400" />
                            {t('chat.title') || 'Legal Chat'}
                        </h1>
                        <LanguageSwitcher />
                    </div>
                    <button
                        onClick={createNewSession}
                        className="w-full px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all flex items-center justify-center gap-2"
                    >
                        <Plus className="w-5 h-5" />
                        {t('chat.newSession') || 'New Conversation'}
                    </button>

                    {/* Usage Indicator */}
                    <div className="mt-4">
                        <UsageIndicator />
                    </div>
                </div>

                {/* Sessions List */}
                <div className="flex-1 overflow-y-auto p-4 space-y-2">
                    {isLoadingSessions ? (
                        <div className="text-center text-gray-400 py-8">
                            {t('common.loading') || 'Loading...'}
                        </div>
                    ) : sessions.length === 0 ? (
                        <div className="text-center text-gray-400 py-8">
                            <MessageSquare className="w-12 h-12 mx-auto mb-2 opacity-50" />
                            <p>{t('chat.noSessions') || 'No conversations yet'}</p>
                        </div>
                    ) : (
                        sessions.map(session => (
                            <div
                                key={session.id}
                                onClick={() => setCurrentSessionId(session.id)}
                                className={`p-3 rounded-lg cursor-pointer transition-all group ${currentSessionId === session.id
                                    ? 'bg-purple-500/20 border border-purple-500/50'
                                    : 'bg-white/5 hover:bg-white/10 border border-transparent'
                                    }`}
                            >
                                <div className="flex items-start justify-between gap-2">
                                    <div className="flex-1 min-w-0">
                                        <div className="text-white font-medium truncate">
                                            {session.title}
                                        </div>
                                        <div className="flex items-center gap-2 text-xs text-gray-400 mt-1">
                                            <Clock className="w-3 h-3" />
                                            {formatDate(session.updated_at)}
                                            <span>•</span>
                                            <span>{session.message_count} {t('chat.messages') || 'messages'}</span>
                                        </div>
                                    </div>
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            deleteSession(session.id);
                                        }}
                                        className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-500/20 rounded transition-all"
                                    >
                                        <Trash2 className="w-4 h-4 text-red-400" />
                                    </button>
                                </div>
                            </div>
                        ))
                    )}
                </div>

                {/* Footer */}
                <div className="p-4 border-t border-white/10">
                    <button
                        onClick={() => router.push('/dashboard')}
                        className="w-full px-4 py-2 text-white hover:bg-white/10 rounded-lg transition-all"
                    >
                        ← {t('common.backToDashboard') || 'Back to Dashboard'}
                    </button>
                </div>
            </div>

            {/* Chat Area */}
            <div className="flex-1 flex flex-col">
                <ChatInterface
                    sessionId={currentSessionId}
                    onSessionCreated={handleSessionCreated}
                />
            </div>
        </div>
    );
}
