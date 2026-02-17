'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';

interface CaseDetail {
    id: string;
    title: string;
    description: string;
    status: string;
    priority: string;
    deadline: string | null;
    claim_amount: number | null;
    client_name: string | null;
    client_email: string | null;
    client_phone: string | null;
    assigned_to: number | null;
    created_at: string;
    updated_at: string;
    logs: CaseLog[];
    documents: CaseDocument[];
}

interface CaseLog {
    id: string;
    event_type: string;
    event_time: string;
    old_value: string | null;
    new_value: string | null;
    comment: string | null;
    created_by: number;
}

interface CaseDocument {
    id: string;
    file_name: string;
    file_key: string;
    uploaded_at: string;
    uploaded_by: number | null;
}

const statusColors = {
    draft: 'bg-gray-100 text-gray-800',
    submitted: 'bg-blue-100 text-blue-800',
    under_review: 'bg-yellow-100 text-yellow-800',
    hearing_scheduled: 'bg-purple-100 text-purple-800',
    resolved: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800',
};

const statusLabels = {
    draft: 'Чернетка',
    submitted: 'Подано',
    under_review: 'На розгляді',
    hearing_scheduled: 'Призначено слухання',
    resolved: 'Вирішено',
    cancelled: 'Скасовано',
};

const eventTypeLabels = {
    created: '📝 Створено',
    updated: '✏️ Оновлено',
    status_change: '🔄 Зміна статусу',
    assignment: '👤 Призначення',
    note: '💬 Нотатка',
    document_uploaded: '📎 Завантажено документ',
    document_deleted: '🗑️ Видалено документ',
};

export default function CaseDetailPage() {
    const params = useParams();
    const router = useRouter();
    const caseId = params?.id as string;

    const [caseData, setCaseData] = useState<CaseDetail | null>(null);
    const [loading, setLoading] = useState(true);
    const [noteText, setNoteText] = useState('');
    const [uploadingFile, setUploadingFile] = useState(false);

    useEffect(() => {
        fetchCaseDetail();
    }, [caseId]);

    const fetchCaseDetail = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`/api/cases/${caseId}`, {
                headers: { 'Authorization': `Bearer ${token}` },
            });

            if (response.ok) {
                const data = await response.json();
                setCaseData(data);
            }
        } catch (error) {
            console.error('Failed to fetch case:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleAddNote = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!noteText.trim()) return;

        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`/api/cases/${caseId}/notes`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ comment: noteText }),
            });

            if (response.ok) {
                setNoteText('');
                fetchCaseDetail();
            }
        } catch (error) {
            console.error('Failed to add note:', error);
        }
    };

    const handleStatusChange = async (newStatus: string) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`/api/cases/${caseId}/status`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ new_status: newStatus }),
            });

            if (response.ok) {
                fetchCaseDetail();
            } else {
                const error = await response.json();
                alert(error.detail || 'Помилка зміни статусу');
            }
        } catch (error) {
            console.error('Failed to change status:', error);
        }
    };

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files || e.target.files.length === 0) return;

        try {
            setUploadingFile(true);
            const token = localStorage.getItem('token');
            const file = e.target.files[0];
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`/api/cases/${caseId}/documents`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData,
            });

            if (response.ok) {
                fetchCaseDetail();
            }
        } catch (error) {
            console.error('Failed to upload file:', error);
        } finally {
            setUploadingFile(false);
        }
    };

    const formatDate = (dateString: string | null) => {
        if (!dateString) return '-';
        return new Date(dateString).toLocaleString('uk-UA');
    };

    const formatDateShort = (dateString: string | null) => {
        if (!dateString) return '-';
        return new Date(dateString).toLocaleDateString('uk-UA');
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-xl">Завантаження...</div>
            </div>
        );
    }

    if (!caseData) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-xl text-red-600">Справу не знайдено</div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-6">
                    <button
                        onClick={() => router.push('/cases')}
                        className="text-blue-600 hover:text-blue-800 mb-4 flex items-center gap-2"
                    >
                        ← Назад до списку справ
                    </button>

                    <div className="flex items-start justify-between">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">{caseData.title}</h1>
                            <div className="mt-2 flex items-center gap-4">
                                <span className={`px-3 py-1 text-sm font-medium rounded-full ${statusColors[caseData.status as keyof typeof statusColors]}`}>
                                    {statusLabels[caseData.status as keyof typeof statusLabels]}
                                </span>
                                <span className="text-sm text-gray-500">
                                    Створено: {formatDateShort(caseData.created_at)}
                                </span>
                            </div>
                        </div>

                        <button
                            onClick={() => router.push(`/cases/${caseId}/edit`)}
                            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium"
                        >
                            Редагувати
                        </button>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Main Content */}
                    <div className="lg:col-span-2 space-y-6">
                        {/* Case Information */}
                        <div className="bg-white rounded-lg shadow p-6">
                            <h2 className="text-xl font-semibold mb-4">Інформація про справу</h2>

                            <div className="space-y-4">
                                {caseData.description && (
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">Опис</label>
                                        <p className="text-gray-900 whitespace-pre-wrap">{caseData.description}</p>
                                    </div>
                                )}

                                <div className="grid grid-cols-2 gap-4">
                                    {caseData.deadline && (
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-1">Дедлайн</label>
                                            <p className="text-gray-900">{formatDateShort(caseData.deadline)}</p>
                                        </div>
                                    )}

                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">Пріоритет</label>
                                        <p className="text-gray-900 capitalize">{caseData.priority}</p>
                                    </div>
                                </div>

                                {caseData.claim_amount && (
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">Сума претензії</label>
                                        <p className="text-gray-900">{caseData.claim_amount.toFixed(2)} EUR</p>
                                    </div>
                                )}

                                {caseData.client_name && (
                                    <div className="border-t pt-4">
                                        <h3 className="font-medium text-gray-900 mb-2">Клієнт</h3>
                                        <div className="space-y-1 text-sm">
                                            <p className="text-gray-900">{caseData.client_name}</p>
                                            {caseData.client_email && <p className="text-gray-600">{caseData.client_email}</p>}
                                            {caseData.client_phone && <p className="text-gray-600">{caseData.client_phone}</p>}
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Documents */}
                        <div className="bg-white rounded-lg shadow p-6">
                            <div className="flex items-center justify-between mb-4">
                                <h2 className="text-xl font-semibold">Документи ({caseData.documents.length})</h2>
                                <label className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium cursor-pointer">
                                    {uploadingFile ? 'Завантаження...' : '+ Додати файл'}
                                    <input
                                        type="file"
                                        onChange={handleFileUpload}
                                        className="hidden"
                                        disabled={uploadingFile}
                                    />
                                </label>
                            </div>

                            {caseData.documents.length === 0 ? (
                                <p className="text-gray-500 text-center py-8">Документів ще немає</p>
                            ) : (
                                <div className="space-y-2">
                                    {caseData.documents.map((doc) => (
                                        <div key={doc.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100">
                                            <div className="flex items-center gap-3">
                                                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                                </svg>
                                                <div>
                                                    <p className="text-sm font-medium text-gray-900">{doc.file_name}</p>
                                                    <p className="text-xs text-gray-500">{formatDate(doc.uploaded_at)}</p>
                                                </div>
                                            </div>
                                            <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                                                Завантажити
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>

                        {/* Add Note */}
                        <div className="bg-white rounded-lg shadow p-6">
                            <h2 className="text-xl font-semibold mb-4">Додати нотатку</h2>
                            <form onSubmit={handleAddNote}>
                                <textarea
                                    value={noteText}
                                    onChange={(e) => setNoteText(e.target.value)}
                                    rows={3}
                                    className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    placeholder="Введіть вашу нотатку..."
                                />
                                <button
                                    type="submit"
                                    disabled={!noteText.trim()}
                                    className="mt-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white px-6 py-2 rounded-md font-medium"
                                >
                                    Додати нотатку
                                </button>
                            </form>
                        </div>
                    </div>

                    {/* Sidebar */}
                    <div className="space-y-6">
                        {/* Status Actions */}
                        <div className="bg-white rounded-lg shadow p-6">
                            <h2 className="text-lg font-semibold mb-4">Дії</h2>
                            <div className="space-y-2">
                                {caseData.status === 'draft' && (
                                    <button
                                        onClick={() => handleStatusChange('submitted')}
                                        className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium"
                                    >
                                        Подати на розгляд
                                    </button>
                                )}
                                {caseData.status === 'submitted' && (
                                    <button
                                        onClick={() => handleStatusChange('under_review')}
                                        className="w-full bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-md font-medium"
                                    >
                                        Взяти на розгляд
                                    </button>
                                )}
                                {caseData.status === 'under_review' && (
                                    <>
                                        <button
                                            onClick={() => handleStatusChange('hearing_scheduled')}
                                            className="w-full bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md font-medium"
                                        >
                                            Призначити слухання
                                        </button>
                                        <button
                                            onClick={() => handleStatusChange('resolved')}
                                            className="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md font-medium"
                                        >
                                            Вирішити справу
                                        </button>
                                    </>
                                )}
                                {caseData.status === 'hearing_scheduled' && (
                                    <button
                                        onClick={() => handleStatusChange('resolved')}
                                        className="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md font-medium"
                                    >
                                        Вирішити справу
                                    </button>
                                )}
                                {!['resolved', 'cancelled'].includes(caseData.status) && (
                                    <button
                                        onClick={() => handleStatusChange('cancelled')}
                                        className="w-full bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md font-medium"
                                    >
                                        Скасувати справу
                                    </button>
                                )}
                            </div>
                        </div>

                        {/* Timeline */}
                        <div className="bg-white rounded-lg shadow p-6">
                            <h2 className="text-lg font-semibold mb-4">Таймлайн подій</h2>
                            <div className="space-y-4">
                                {caseData.logs.length === 0 ? (
                                    <p className="text-gray-500 text-sm">Подій ще немає</p>
                                ) : (
                                    caseData.logs.map((log) => (
                                        <div key={log.id} className="border-l-2 border-blue-500 pl-4 pb-4">
                                            <div className="flex items-start justify-between">
                                                <div className="flex-1">
                                                    <p className="text-sm font-medium text-gray-900">
                                                        {eventTypeLabels[log.event_type as keyof typeof eventTypeLabels] || log.event_type}
                                                    </p>
                                                    {log.comment && (
                                                        <p className="text-sm text-gray-600 mt-1">{log.comment}</p>
                                                    )}
                                                    {log.old_value && log.new_value && (
                                                        <p className="text-xs text-gray-500 mt-1">
                                                            {log.old_value} → {log.new_value}
                                                        </p>
                                                    )}
                                                </div>
                                            </div>
                                            <p className="text-xs text-gray-400 mt-1">{formatDate(log.event_time)}</p>
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
