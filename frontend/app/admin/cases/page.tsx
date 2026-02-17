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

interface User {
    id: number;
    name: string;
    email: string;
    role: string;
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

export default function AdminCasesPage() {
    const router = useRouter();
    const [cases, setCases] = useState<Case[]>([]);
    const [lawyers, setLawyers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);

    // Filters
    const [statusFilter, setStatusFilter] = useState<string>('');
    const [userFilter, setUserFilter] = useState<string>('');
    const [assignedFilter, setAssignedFilter] = useState<string>('');

    // Assignment modal
    const [showAssignModal, setShowAssignModal] = useState(false);
    const [selectedCase, setSelectedCase] = useState<Case | null>(null);
    const [selectedLawyer, setSelectedLawyer] = useState<string>('');

    useEffect(() => {
        fetchCases();
        fetchLawyers();
    }, [statusFilter]);

    const fetchCases = async () => {
        try {
            const token = localStorage.getItem('token');
            const params = new URLSearchParams();
            if (statusFilter) params.append('status', statusFilter);

            const response = await fetch(`http://localhost:8002/api/cases?${params}`, {
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

    const fetchLawyers = async () => {
        try {
            const token = localStorage.getItem('token');
            // Assuming there's an endpoint to get lawyers
            // For now, we'll use a placeholder
            setLawyers([]);
        } catch (error) {
            console.error('Failed to fetch lawyers:', error);
        }
    };

    const handleAssignLawyer = async () => {
        if (!selectedCase || !selectedLawyer) return;

        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:8002/api/cases/${selectedCase.id}/assign`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ lawyer_id: parseInt(selectedLawyer) }),
            });

            if (response.ok) {
                setShowAssignModal(false);
                setSelectedCase(null);
                setSelectedLawyer('');
                fetchCases();
            }
        } catch (error) {
            console.error('Failed to assign lawyer:', error);
        }
    };

    const handleStatusChange = async (caseId: string, newStatus: string) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:8002/api/cases/${caseId}/status`, {
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

    const filteredCases = cases.filter(c => {
        if (userFilter && c.user_id.toString() !== userFilter) return false;
        if (assignedFilter && (!c.assigned_to || c.assigned_to.toString() !== assignedFilter)) return false;
        return true;
    });

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
                    <h1 className="text-3xl font-bold text-gray-900">Адміністрування справ</h1>
                    <p className="mt-2 text-gray-600">Керування всіма справами платформи</p>
                </div>

                {/* Filters */}
                <div className="bg-white rounded-lg shadow p-6 mb-6">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Статус
                            </label>
                            <select
                                value={statusFilter}
                                onChange={(e) => setStatusFilter(e.target.value)}
                                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="">Всі статуси</option>
                                <option value="draft">Чернетка</option>
                                <option value="submitted">Подано</option>
                                <option value="under_review">На розгляді</option>
                                <option value="hearing_scheduled">Призначено слухання</option>
                                <option value="resolved">Вирішено</option>
                                <option value="cancelled">Скасовано</option>
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Користувач
                            </label>
                            <input
                                type="number"
                                value={userFilter}
                                onChange={(e) => setUserFilter(e.target.value)}
                                placeholder="ID користувача"
                                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Призначено юристу
                            </label>
                            <input
                                type="number"
                                value={assignedFilter}
                                onChange={(e) => setAssignedFilter(e.target.value)}
                                placeholder="ID юриста"
                                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500"
                            />
                        </div>
                    </div>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div className="bg-white rounded-lg shadow p-4">
                        <div className="text-sm text-gray-600">Всього справ</div>
                        <div className="text-2xl font-bold text-gray-900">{filteredCases.length}</div>
                    </div>
                    <div className="bg-white rounded-lg shadow p-4">
                        <div className="text-sm text-gray-600">Подано</div>
                        <div className="text-2xl font-bold text-blue-600">
                            {filteredCases.filter(c => c.status === 'submitted').length}
                        </div>
                    </div>
                    <div className="bg-white rounded-lg shadow p-4">
                        <div className="text-sm text-gray-600">На розгляді</div>
                        <div className="text-2xl font-bold text-yellow-600">
                            {filteredCases.filter(c => c.status === 'under_review').length}
                        </div>
                    </div>
                    <div className="bg-white rounded-lg shadow p-4">
                        <div className="text-sm text-gray-600">Не призначено</div>
                        <div className="text-2xl font-bold text-red-600">
                            {filteredCases.filter(c => !c.assigned_to).length}
                        </div>
                    </div>
                </div>

                {/* Cases Table */}
                <div className="bg-white rounded-lg shadow overflow-hidden">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Назва</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Клієнт</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Статус</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Юрист</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Дедлайн</th>
                                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Дії</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {filteredCases.length === 0 ? (
                                <tr>
                                    <td colSpan={7} className="px-6 py-12 text-center text-gray-500">
                                        Справ не знайдено
                                    </td>
                                </tr>
                            ) : (
                                filteredCases.map((caseItem) => (
                                    <tr key={caseItem.id} className="hover:bg-gray-50">
                                        <td className="px-6 py-4 text-sm text-gray-500">
                                            {caseItem.id.substring(0, 8)}...
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="text-sm font-medium text-gray-900">{caseItem.title}</div>
                                            <div className="text-sm text-gray-500">User ID: {caseItem.user_id}</div>
                                        </td>
                                        <td className="px-6 py-4 text-sm text-gray-900">
                                            {caseItem.client_name || '-'}
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusColors[caseItem.status as keyof typeof statusColors]}`}>
                                                {statusLabels[caseItem.status as keyof typeof statusLabels]}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-sm">
                                            {caseItem.assigned_to ? (
                                                <span className="text-gray-900">ID: {caseItem.assigned_to}</span>
                                            ) : (
                                                <span className="text-red-600">Не призначено</span>
                                            )}
                                        </td>
                                        <td className="px-6 py-4 text-sm text-gray-500">
                                            {formatDate(caseItem.deadline)}
                                        </td>
                                        <td className="px-6 py-4 text-right text-sm space-x-2">
                                            <button
                                                onClick={() => router.push(`/cases/${caseItem.id}`)}
                                                className="text-blue-600 hover:text-blue-900"
                                            >
                                                Переглянути
                                            </button>
                                            <button
                                                onClick={() => {
                                                    setSelectedCase(caseItem);
                                                    setShowAssignModal(true);
                                                }}
                                                className="text-green-600 hover:text-green-900"
                                            >
                                                Призначити
                                            </button>
                                            {caseItem.status === 'submitted' && (
                                                <button
                                                    onClick={() => handleStatusChange(caseItem.id, 'under_review')}
                                                    className="text-yellow-600 hover:text-yellow-900"
                                                >
                                                    На розгляд
                                                </button>
                                            )}
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Assignment Modal */}
            {showAssignModal && selectedCase && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-lg max-w-md w-full p-6">
                        <h2 className="text-xl font-bold mb-4">Призначити юриста</h2>
                        <p className="text-gray-600 mb-4">Справа: {selectedCase.title}</p>

                        <div className="mb-4">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                ID Юриста
                            </label>
                            <input
                                type="number"
                                value={selectedLawyer}
                                onChange={(e) => setSelectedLawyer(e.target.value)}
                                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500"
                                placeholder="Введіть ID юриста"
                            />
                        </div>

                        <div className="flex gap-3">
                            <button
                                onClick={handleAssignLawyer}
                                disabled={!selectedLawyer}
                                className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white px-4 py-2 rounded-md font-medium"
                            >
                                Призначити
                            </button>
                            <button
                                onClick={() => {
                                    setShowAssignModal(false);
                                    setSelectedCase(null);
                                    setSelectedLawyer('');
                                }}
                                className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-md font-medium"
                            >
                                Скасувати
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
