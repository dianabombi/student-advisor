// Lawyer interface - similar to admin but with different permissions
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface Case {
    id: string;
    title: string;
    description: string;
    status: string;
    priority: string;
    deadline: string | null;
    user_id: number;
    assigned_to: number | null;
    client_name: string | null;
    created_at: string;
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

export default function LawyerCasesPage() {
    const router = useRouter();
    const [cases, setCases] = useState<Case[]>([]);
    const [loading, setLoading] = useState(true);
    const [statusFilter, setStatusFilter] = useState<string>('');
    const [showOnlyMy, setShowOnlyMy] = useState(true);

    useEffect(() => {
        fetchCases();
    }, [statusFilter, showOnlyMy]);

    const fetchCases = async () => {
        try {
            const token = localStorage.getItem('token');
            const params = new URLSearchParams();
            if (statusFilter) params.append('status', statusFilter);
            if (showOnlyMy) params.append('assigned', 'true');

            const response = await fetch(`/api/cases?${params}`, {
                headers: { 'Authorization': `Bearer ${token}` },
            });

            if (response.ok) {
                const data = await response.json();
                setCases(data);
            }
        } catch (error) {
            console.error('Failed to fetch cases:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleStatusChange = async (caseId: string, newStatus: string) => {
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
                fetchCases();
            } else {
                const error = await response.json();
                alert(error.detail || 'Помилка зміни статусу');
            }
        } catch (error) {
            console.error('Failed to change status:', error);
        }
    };

    const formatDate = (dateString: string | null) => {
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

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Мої справи (Юрист)</h1>
                    <p className="mt-2 text-gray-600">Справи призначені вам для розгляду</p>
                </div>

                {/* Filters */}
                <div className="bg-white rounded-lg shadow p-6 mb-6">
                    <div className="flex flex-wrap gap-4 items-center">
                        <div className="flex-1">
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Статус
                            </label>
                            <select
                                value={statusFilter}
                                onChange={(e) => setStatusFilter(e.target.value)}
                                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="">Всі статуси</option>
                                <option value="submitted">Подано</option>
                                <option value="under_review">На розгляді</option>
                                <option value="hearing_scheduled">Призначено слухання</option>
                                <option value="resolved">Вирішено</option>
                            </select>
                        </div>

                        <div className="flex items-center pt-6">
                            <input
                                type="checkbox"
                                id="showOnlyMy"
                                checked={showOnlyMy}
                                onChange={(e) => setShowOnlyMy(e.target.checked)}
                                className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                            />
                            <label htmlFor="showOnlyMy" className="ml-2 text-sm text-gray-700">
                                Тільки мої справи
                            </label>
                        </div>
                    </div>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div className="bg-white rounded-lg shadow p-4">
                        <div className="text-sm text-gray-600">Всього справ</div>
                        <div className="text-2xl font-bold text-gray-900">{cases.length}</div>
                    </div>
                    <div className="bg-white rounded-lg shadow p-4">
                        <div className="text-sm text-gray-600">На розгляді</div>
                        <div className="text-2xl font-bold text-yellow-600">
                            {cases.filter(c => c.status === 'under_review').length}
                        </div>
                    </div>
                    <div className="bg-white rounded-lg shadow p-4">
                        <div className="text-sm text-gray-600">Слухання</div>
                        <div className="text-2xl font-bold text-purple-600">
                            {cases.filter(c => c.status === 'hearing_scheduled').length}
                        </div>
                    </div>
                    <div className="bg-white rounded-lg shadow p-4">
                        <div className="text-sm text-gray-600">Вирішено</div>
                        <div className="text-2xl font-bold text-green-600">
                            {cases.filter(c => c.status === 'resolved').length}
                        </div>
                    </div>
                </div>

                {/* Cases Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {cases.length === 0 ? (
                        <div className="col-span-full text-center py-12 text-gray-500">
                            Справ не знайдено
                        </div>
                    ) : (
                        cases.map((caseItem) => (
                            <div key={caseItem.id} className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow">
                                <div className="p-6">
                                    <div className="flex items-start justify-between mb-4">
                                        <h3 className="text-lg font-semibold text-gray-900 flex-1">
                                            {caseItem.title}
                                        </h3>
                                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusColors[caseItem.status as keyof typeof statusColors]}`}>
                                            {statusLabels[caseItem.status as keyof typeof statusLabels]}
                                        </span>
                                    </div>

                                    {caseItem.description && (
                                        <p className="text-sm text-gray-600 mb-4 line-clamp-2">
                                            {caseItem.description}
                                        </p>
                                    )}

                                    <div className="space-y-2 text-sm mb-4">
                                        {caseItem.client_name && (
                                            <div className="flex items-center gap-2">
                                                <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                                </svg>
                                                <span className="text-gray-700">{caseItem.client_name}</span>
                                            </div>
                                        )}
                                        {caseItem.deadline && (
                                            <div className="flex items-center gap-2">
                                                <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                                </svg>
                                                <span className="text-gray-700">{formatDate(caseItem.deadline)}</span>
                                            </div>
                                        )}
                                    </div>

                                    <div className="flex gap-2">
                                        <button
                                            onClick={() => router.push(`/cases/${caseItem.id}`)}
                                            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
                                        >
                                            Переглянути
                                        </button>
                                        {caseItem.status === 'submitted' && (
                                            <button
                                                onClick={() => handleStatusChange(caseItem.id, 'under_review')}
                                                className="flex-1 bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-md text-sm font-medium"
                                            >
                                                На розгляд
                                            </button>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}
