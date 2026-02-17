'use client';
import { useState } from 'react';
import { useLanguage } from '@/lib/LanguageContext';

export default function AISupportButton() {
    const { t } = useLanguage();
    const [isOpen, setIsOpen] = useState(false);
    const [issue, setIssue] = useState('');
    const [response, setResponse] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        setLoading(true);

        try {
            const res = await fetch('/api/support/analyze-issue', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ issue_description: issue })
            });

            const data = await res.json();
            setResponse(data);
        } catch (error) {
            console.error('Error:', error);
            alert('Помилка при аналізі проблеми');
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            {/* Floating help button */}
            <button
                onClick={() => setIsOpen(true)}
                className="fixed bottom-6 right-6 bg-blue-600 text-white rounded-full p-4 shadow-lg hover:bg-blue-700 transition-all z-50 hover:scale-110"
                title={t('aiSupport.title')}
            >
                <div className="relative flex items-center justify-center w-6 h-6">
                    {/* Wrench emoji */}
                    <span className="text-2xl">🔧</span>
                    {/* Small question mark badge */}
                    <div className="absolute -top-1 -right-1 bg-white text-blue-600 rounded-full w-3 h-3 flex items-center justify-center text-[10px] font-bold shadow-sm">
                        ?
                    </div>
                </div>
            </button>

            {/* Modal */}
            {isOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto">
                        <div className="p-6">
                            <div className="flex justify-between items-center mb-4">
                                <h2 className="text-2xl font-bold">🤖 {t('aiSupport.title')}</h2>
                                <button
                                    onClick={() => {
                                        setIsOpen(false);
                                        setResponse(null);
                                        setIssue('');
                                    }}
                                    className="text-gray-500 hover:text-gray-700 text-2xl"
                                >
                                    ✕
                                </button>
                            </div>

                            {!response ? (
                                <>
                                    <p className="text-gray-600 mb-4">
                                        {t('aiSupport.description')}
                                    </p>

                                    <textarea
                                        value={issue}
                                        onChange={(e) => setIssue(e.target.value)}
                                        placeholder={t('aiSupport.placeholder')}
                                        className="w-full border rounded-lg p-3 mb-4 h-32 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    />

                                    <button
                                        onClick={handleSubmit}
                                        disabled={loading || !issue.trim()}
                                        className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                                    >
                                        {loading ? `🔍 ${t('aiSupport.analyzing')}` : `🚀 ${t('aiSupport.analyze')}`}
                                    </button>
                                </>
                            ) : (
                                <>
                                    <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-4">
                                        <p className="text-sm text-gray-600 mb-2">
                                            📊 {t('aiSupport.analyzed').replace('{count}', response.logs_analyzed)}
                                            {response.errors_found > 0 && ` • ${t('aiSupport.errorsFound').replace('{count}', response.errors_found)}`}
                                        </p>
                                    </div>

                                    <div className="prose max-w-none mb-4 bg-gray-50 p-4 rounded-lg">
                                        <div className="whitespace-pre-wrap">{response.response}</div>
                                    </div>

                                    {response.needs_human_support && (
                                        <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 mb-4">
                                            <p className="font-semibold">⚠️ {t('aiSupport.needsHuman')}</p>
                                            <p className="text-sm mt-1">
                                                {t('aiSupport.needsHumanDesc')}
                                            </p>
                                        </div>
                                    )}

                                    <div className="flex gap-3">
                                        <button
                                            onClick={() => {
                                                setResponse(null);
                                                setIssue('');
                                            }}
                                            className="flex-1 bg-gray-200 text-gray-800 py-2 rounded-lg hover:bg-gray-300 transition-colors"
                                        >
                                            {t('aiSupport.anotherIssue')}
                                        </button>
                                        <button
                                            onClick={() => setIsOpen(false)}
                                            className="flex-1 bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition-colors"
                                        >
                                            ✅ {t('aiSupport.helped')}
                                        </button>
                                    </div>

                                    <p className="text-xs text-gray-500 text-center mt-4">
                                        Ticket ID: #{response.ticket_id}
                                    </p>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}
