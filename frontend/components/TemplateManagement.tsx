'use client';

import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

interface Template {
    name: string;
    type: string;
    size?: number;
    last_modified?: string;
    url?: string;
}

export default function TemplateManagement() {
    const { t } = useTranslation();
    const [templates, setTemplates] = useState<Template[]>([]);
    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [templateType, setTemplateType] = useState('general');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const templateTypes = [
        { value: 'contract', label: 'Zmluvy' },
        { value: 'legal', label: 'Právne dokumenty' },
        { value: 'administrative', label: 'Administratívne' },
        { value: 'correspondence', label: 'Korešpondencia' },
        { value: 'general', label: 'Všeobecné' }
    ];

    useEffect(() => {
        loadTemplates();
    }, []);

    const loadTemplates = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');

            const response = await fetch('/api/templates/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) throw new Error('Failed to load templates');

            const data = await response.json();
            setTemplates(data.templates);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            if (!file.name.endsWith('.docx')) {
                setError('Only DOCX files are supported');
                return;
            }
            setSelectedFile(file);
            setError('');
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setError('Please select a file');
            return;
        }

        try {
            setUploading(true);
            setError('');
            setSuccess('');

            const token = localStorage.getItem('token');
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('template_type', templateType);

            const response = await fetch('/api/templates/upload', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (!response.ok) throw new Error('Upload failed');

            const data = await response.json();
            setSuccess(data.message);
            setSelectedFile(null);

            // Reset file input
            const fileInput = document.getElementById('file-input') as HTMLInputElement;
            if (fileInput) fileInput.value = '';

            // Reload templates
            await loadTemplates();
        } catch (err: any) {
            setError(err.message);
        } finally {
            setUploading(false);
        }
    };

    const handleDelete = async (templateName: string) => {
        if (!confirm(`Are you sure you want to delete "${templateName}"?`)) {
            return;
        }

        try {
            const token = localStorage.getItem('token');

            const response = await fetch(`/api/templates/${encodeURIComponent(templateName)}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) throw new Error('Delete failed');

            const data = await response.json();
            setSuccess(data.message);

            // Reload templates
            await loadTemplates();
        } catch (err: any) {
            setError(err.message);
        }
    };

    const handleDownload = (url: string, filename: string) => {
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    };

    const formatFileSize = (bytes?: number) => {
        if (!bytes) return 'N/A';
        const kb = bytes / 1024;
        if (kb < 1024) return `${kb.toFixed(1)} KB`;
        return `${(kb / 1024).toFixed(1)} MB`;
    };

    return (
        <div className="max-w-6xl mx-auto p-6">
            <h1 className="text-3xl font-bold mb-6">Template Management</h1>

            {/* Upload Section */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                <h2 className="text-xl font-semibold mb-4">Upload New Template</h2>

                <div className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Template Type
                        </label>
                        <select
                            value={templateType}
                            onChange={(e) => setTemplateType(e.target.value)}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            {templateTypes.map(type => (
                                <option key={type.value} value={type.value}>
                                    {type.label}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Template File (DOCX)
                        </label>
                        <input
                            id="file-input"
                            type="file"
                            accept=".docx"
                            onChange={handleFileSelect}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        {selectedFile && (
                            <p className="mt-2 text-sm text-gray-600">
                                Selected: {selectedFile.name} ({formatFileSize(selectedFile.size)})
                            </p>
                        )}
                    </div>

                    <button
                        onClick={handleUpload}
                        disabled={!selectedFile || uploading}
                        className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                    >
                        {uploading ? 'Uploading...' : 'Upload Template'}
                    </button>
                </div>
            </div>

            {/* Messages */}
            {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
                    {error}
                </div>
            )}

            {success && (
                <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-4">
                    {success}
                </div>
            )}

            {/* Templates List */}
            <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-semibold mb-4">
                    Existing Templates ({templates.length})
                </h2>

                {loading ? (
                    <div className="text-center py-8">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                        <p className="mt-4 text-gray-600">Loading templates...</p>
                    </div>
                ) : templates.length === 0 ? (
                    <p className="text-gray-500 text-center py-8">
                        No templates found. Upload your first template above.
                    </p>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-gray-200">
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Name</th>
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Type</th>
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Size</th>
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Last Modified</th>
                                    <th className="text-right py-3 px-4 font-semibold text-gray-700">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {templates.map((template, index) => (
                                    <tr key={index} className="border-b border-gray-100 hover:bg-gray-50">
                                        <td className="py-3 px-4">
                                            <span className="font-medium text-gray-900">{template.name}</span>
                                        </td>
                                        <td className="py-3 px-4">
                                            <span className="inline-block px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded">
                                                {template.type}
                                            </span>
                                        </td>
                                        <td className="py-3 px-4 text-gray-600">
                                            {formatFileSize(template.size)}
                                        </td>
                                        <td className="py-3 px-4 text-gray-600">
                                            {template.last_modified ? new Date(template.last_modified).toLocaleDateString() : 'N/A'}
                                        </td>
                                        <td className="py-3 px-4 text-right">
                                            <div className="flex justify-end space-x-2">
                                                {template.url && (
                                                    <button
                                                        onClick={() => handleDownload(template.url!, template.name)}
                                                        className="px-3 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
                                                    >
                                                        Download
                                                    </button>
                                                )}
                                                <button
                                                    onClick={() => handleDelete(template.name)}
                                                    className="px-3 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
                                                >
                                                    Delete
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            {/* Template Format Help */}
            <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="font-semibold text-blue-900 mb-2">Template Format</h3>
                <p className="text-sm text-blue-800 mb-2">
                    Use <code className="bg-blue-100 px-1 rounded">{`{{placeholder}}`}</code> format in your DOCX templates:
                </p>
                <ul className="text-sm text-blue-800 list-disc list-inside space-y-1">
                    <li><code className="bg-blue-100 px-1 rounded">{`{{contract_number}}`}</code> - Contract number</li>
                    <li><code className="bg-blue-100 px-1 rounded">{`{{date}}`}</code> - Date</li>
                    <li><code className="bg-blue-100 px-1 rounded">{`{{employer}}`}</code> - Employer name</li>
                    <li><code className="bg-blue-100 px-1 rounded">{`{{employee}}`}</code> - Employee name</li>
                </ul>
            </div>
        </div>
    );
}
