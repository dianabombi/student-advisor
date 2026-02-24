'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';

interface CaseFormData {
    title: string;
    description: string;
    deadline: string;
    priority: string;
    claim_amount: string;
    client_name: string;
    client_email: string;
    client_phone: string;
}

export default function CaseFormPage() {
    const router = useRouter();
    const params = useParams();
    const caseId = params?.id as string | undefined;
    const isEdit = !!caseId;

    const [formData, setFormData] = useState<CaseFormData>({
        title: '',
        description: '',
        deadline: '',
        priority: 'medium',
        claim_amount: '',
        client_name: '',
        client_email: '',
        client_phone: '',
    });

    const [files, setFiles] = useState<File[]>([]);
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        if (isEdit) {
            fetchCase();
        }
    }, [caseId]);

    const fetchCase = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
            const response = await fetch(`/api/cases/${caseId}`, {
                headers: { 'Authorization': `Bearer ${token}` },
            });

            if (response.ok) {
                const data = await response.json();
                setFormData({
                    title: data.title || '',
                    description: data.description || '',
                    deadline: data.deadline ? data.deadline.split('T')[0] : '',
                    priority: data.priority || 'medium',
                    claim_amount: data.claim_amount?.toString() || '',
                    client_name: data.client_name || '',
                    client_email: data.client_email || '',
                    client_phone: data.client_phone || '',
                });
            }
        } catch (error) {
            console.error('Failed to fetch case:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (submitStatus: 'draft' | 'submitted') => {
        try {
            setSaving(true);
            const token = localStorage.getItem('token');

            // Create or update case
            const casePayload = {
                ...formData,
                deadline: formData.deadline || null,
                claim_amount: formData.claim_amount ? parseFloat(formData.claim_amount) : null,
            };

            let createdCaseId = caseId;

            if (isEdit) {
                // Update existing case
                const response = await fetch(`/api/cases/${caseId}`, {
                    method: 'PATCH',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(casePayload),
                });

                if (!response.ok) throw new Error('Failed to update case');
            } else {
                // Create new case
                const response = await fetch('/api/cases', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(casePayload),
                });

                if (!response.ok) throw new Error('Failed to create case');
                const data = await response.json();
                createdCaseId = data.id;
            }

            // Upload files if any
            if (files.length > 0 && createdCaseId) {
                await uploadFiles(createdCaseId, token!);
            }

            // Change status if submitting
            if (submitStatus === 'submitted' && createdCaseId) {
                await fetch(`/api/cases/${createdCaseId}/status`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ new_status: 'submitted' }),
                });
            }

            // Redirect to cases list
            router.push('/cases');
        } catch (error) {
            console.error('Failed to save case:', error);
            alert('Помилка при збереженні справи');
        } finally {
            setSaving(false);
        }
    };

    const uploadFiles = async (caseId: string, token: string) => {
        for (const file of files) {
            const formData = new FormData();
            formData.append('file', file);

            await fetch(`/api/cases/${caseId}/documents`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData,
            });
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFiles(Array.from(e.target.files));
        }
    };

    const removeFile = (index: number) => {
        setFiles(files.filter((_, i) => i !== index));
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
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <button
                        onClick={() => router.push('/cases')}
                        className="text-blue-600 hover:text-blue-800 mb-4 flex items-center gap-2"
                    >
                        ← Назад до списку справ
                    </button>
                    <h1 className="text-3xl font-bold text-gray-900">
                        {isEdit ? 'Редагувати справу' : 'Створити нову справу'}
                    </h1>
                </div>

                {/* Form */}
                <div className="bg-white rounded-lg shadow-lg p-8">
                    <form className="space-y-6">
                        {/* Title */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Назва справи <span className="text-red-500">*</span>
                            </label>
                            <input
                                type="text"
                                required
                                value={formData.title}
                                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Наприклад: Позов про стягнення заборгованості"
                            />
                        </div>

                        {/* Description */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Опис справи
                            </label>
                            <textarea
                                value={formData.description}
                                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                rows={6}
                                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Детальний опис справи, обставини, вимоги..."
                            />
                        </div>

                        {/* Deadline and Priority */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Дедлайн
                                </label>
                                <input
                                    type="date"
                                    value={formData.deadline}
                                    onChange={(e) => setFormData({ ...formData, deadline: e.target.value })}
                                    className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Пріоритет
                                </label>
                                <select
                                    value={formData.priority}
                                    onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                                    className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                >
                                    <option value="low">Низький</option>
                                    <option value="medium">Середній</option>
                                    <option value="high">Високий</option>
                                    <option value="urgent">Терміновий</option>
                                </select>
                            </div>
                        </div>

                        {/* Claim Amount */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Сума претензії (EUR)
                            </label>
                            <input
                                type="number"
                                step="0.01"
                                value={formData.claim_amount}
                                onChange={(e) => setFormData({ ...formData, claim_amount: e.target.value })}
                                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="0.00"
                            />
                        </div>

                        {/* Client Information */}
                        <div className="border-t pt-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">Інформація про клієнта</h3>

                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Ім'я клієнта
                                    </label>
                                    <input
                                        type="text"
                                        value={formData.client_name}
                                        onChange={(e) => setFormData({ ...formData, client_name: e.target.value })}
                                        className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    />
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">
                                            Email
                                        </label>
                                        <input
                                            type="email"
                                            value={formData.client_email}
                                            onChange={(e) => setFormData({ ...formData, client_email: e.target.value })}
                                            className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">
                                            Телефон
                                        </label>
                                        <input
                                            type="tel"
                                            value={formData.client_phone}
                                            onChange={(e) => setFormData({ ...formData, client_phone: e.target.value })}
                                            className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* File Upload */}
                        <div className="border-t pt-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">Документи</h3>

                            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
                                <input
                                    type="file"
                                    multiple
                                    onChange={handleFileChange}
                                    className="hidden"
                                    id="file-upload"
                                />
                                <label
                                    htmlFor="file-upload"
                                    className="cursor-pointer flex flex-col items-center"
                                >
                                    <svg className="w-12 h-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                    </svg>
                                    <span className="text-sm text-gray-600">
                                        Клікніть для вибору файлів або перетягніть сюди
                                    </span>
                                    <span className="text-xs text-gray-500 mt-1">
                                        PDF, DOC, DOCX, JPG, PNG (макс. 10MB)
                                    </span>
                                </label>
                            </div>

                            {/* Selected Files */}
                            {files.length > 0 && (
                                <div className="mt-4 space-y-2">
                                    {files.map((file, index) => (
                                        <div key={index} className="flex items-center justify-between bg-gray-50 p-3 rounded-lg">
                                            <div className="flex items-center gap-3">
                                                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                                </svg>
                                                <span className="text-sm text-gray-700">{file.name}</span>
                                                <span className="text-xs text-gray-500">
                                                    ({(file.size / 1024).toFixed(1)} KB)
                                                </span>
                                            </div>
                                            <button
                                                type="button"
                                                onClick={() => removeFile(index)}
                                                className="text-red-600 hover:text-red-800"
                                            >
                                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                                </svg>
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>

                        {/* Action Buttons */}
                        <div className="flex gap-4 pt-6 border-t">
                            <button
                                type="button"
                                onClick={() => handleSubmit('draft')}
                                disabled={saving || !formData.title}
                                className="flex-1 bg-gray-600 hover:bg-gray-700 disabled:bg-gray-300 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                            >
                                {saving ? 'Збереження...' : 'Зберегти як чернетку'}
                            </button>

                            <button
                                type="button"
                                onClick={() => handleSubmit('submitted')}
                                disabled={saving || !formData.title}
                                className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                            >
                                {saving ? 'Збереження...' : 'Зберегти та подати'}
                            </button>

                            <button
                                type="button"
                                onClick={() => router.push('/cases')}
                                disabled={saving}
                                className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50 transition-colors"
                            >
                                Скасувати
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}
