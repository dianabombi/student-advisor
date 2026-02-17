'use client';

import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

interface ExtractedFields {
    [key: string]: any;
    _metadata?: {
        document_type: string;
        extracted_at: string;
        field_count: number;
    };
}

interface DocumentResult {
    document_id: string;
    filename: string;
    status: string;
    document_type?: string;
    confidence?: number;
    extracted_fields?: ExtractedFields;
    raw_document_url?: string;
    processed_document_url?: string;
    filled_template_url?: string;
    summary?: string;
    error?: string;
}

export default function DocumentUpload() {
    const { t } = useTranslation();
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [processing, setProcessing] = useState(false);
    const [documentId, setDocumentId] = useState<string | null>(null);
    const [progress, setProgress] = useState(0);
    const [status, setStatus] = useState('');
    const [result, setResult] = useState<DocumentResult | null>(null);
    const [error, setError] = useState('');

    // Poll for status updates
    useEffect(() => {
        if (!documentId || !processing) return;

        const interval = setInterval(async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch(
                    `/api/documents/${documentId}/status`,
                    {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    }
                );

                if (!response.ok) throw new Error('Failed to get status');

                const data = await response.json();
                setProgress(data.progress);
                setStatus(data.status);

                // If completed or failed, get full result
                if (data.status === 'completed' || data.status === 'failed') {
                    setProcessing(false);
                    await fetchResult(documentId);
                    clearInterval(interval);
                }
            } catch (err: any) {
                console.error('Error polling status:', err);
            }
        }, 2000); // Poll every 2 seconds

        return () => clearInterval(interval);
    }, [documentId, processing]);

    const fetchResult = async (docId: string) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(
                `/api/documents/${docId}`,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );

            if (!response.ok) throw new Error('Failed to get result');

            const data = await response.json();
            setResult(data);

            if (data.status === 'failed') {
                setError(data.error || 'Processing failed');
            }
        } catch (err: any) {
            setError(err.message);
        }
    };

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const allowedTypes = ['.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.tif'];
            const fileExt = '.' + file.name.split('.').pop()?.toLowerCase();

            if (!allowedTypes.includes(fileExt)) {
                setError(`Unsupported file type. Allowed: ${allowedTypes.join(', ')}`);
                return;
            }

            setSelectedFile(file);
            setError('');
            setResult(null);
            setProgress(0);
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
            setProgress(0);
            setStatus('uploading');

            const token = localStorage.getItem('token');
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('auto_process', 'true');

            const response = await fetch('/api/documents/upload', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Upload failed');
            }

            const data = await response.json();
            setDocumentId(data.document_id);
            setProcessing(true);
            setProgress(10);
            setStatus('processing');
        } catch (err: any) {
            setError(err.message);
        } finally {
            setUploading(false);
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

    const formatConfidence = (confidence?: number) => {
        if (!confidence) return 'N/A';
        return `${(confidence * 100).toFixed(1)}%`;
    };

    const renderExtractedFields = (fields?: ExtractedFields) => {
        if (!fields) return null;

        const entries = Object.entries(fields).filter(
            ([key]) => !key.startsWith('_')
        );

        if (entries.length === 0) return <p className="text-gray-500">No fields extracted</p>;

        return (
            <div className="overflow-x-auto">
                <table className="w-full border-collapse">
                    <thead>
                        <tr className="border-b border-gray-200">
                            <th className="text-left py-2 px-4 font-semibold text-gray-700">Field</th>
                            <th className="text-left py-2 px-4 font-semibold text-gray-700">Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        {entries.map(([key, value]) => (
                            <tr key={key} className="border-b border-gray-100">
                                <td className="py-2 px-4 font-medium text-gray-900">{key}</td>
                                <td className="py-2 px-4 text-gray-700">
                                    {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        );
    };

    return (
        <div className="max-w-4xl mx-auto p-6">
            <h1 className="text-3xl font-bold mb-6">Document Processing</h1>

            {/* Upload Section */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                <h2 className="text-xl font-semibold mb-4">Upload Document</h2>

                <div className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Select File (PDF, JPG, PNG, TIFF)
                        </label>
                        <input
                            type="file"
                            accept=".pdf,.jpg,.jpeg,.png,.tiff,.tif"
                            onChange={handleFileSelect}
                            disabled={uploading || processing}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                        />
                        {selectedFile && (
                            <p className="mt-2 text-sm text-gray-600">
                                Selected: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
                            </p>
                        )}
                    </div>

                    <button
                        onClick={handleUpload}
                        disabled={!selectedFile || uploading || processing}
                        className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                    >
                        {uploading ? 'Uploading...' : processing ? 'Processing...' : 'Upload and Process'}
                    </button>
                </div>
            </div>

            {/* Error Message */}
            {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
                    <strong>Error:</strong> {error}
                </div>
            )}

            {/* Progress Bar */}
            {processing && (
                <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                    <h2 className="text-xl font-semibold mb-4">Processing Status</h2>

                    <div className="space-y-4">
                        <div>
                            <div className="flex justify-between mb-2">
                                <span className="text-sm font-medium text-gray-700">
                                    {status === 'processing' ? 'Processing document...' : status}
                                </span>
                                <span className="text-sm font-medium text-gray-700">{progress}%</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-3">
                                <div
                                    className="bg-blue-600 h-3 rounded-full transition-all duration-300"
                                    style={{ width: `${progress}%` }}
                                />
                            </div>
                        </div>

                        <div className="text-sm text-gray-600">
                            {progress >= 10 && progress < 30 && '📄 Extracting text with OCR...'}
                            {progress >= 30 && progress < 50 && '🔍 Classifying document type...'}
                            {progress >= 50 && progress < 70 && '📋 Extracting key fields...'}
                            {progress >= 70 && progress < 90 && '💾 Saving processed data...'}
                            {progress >= 90 && progress < 100 && '✨ Generating summary...'}
                            {progress === 100 && '✅ Processing complete!'}
                        </div>
                    </div>
                </div>
            )}

            {/* Results Section */}
            {result && result.status === 'completed' && (
                <div className="space-y-6">
                    {/* Classification Result */}
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <h2 className="text-xl font-semibold mb-4">Classification Result</h2>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <p className="text-sm text-gray-600">Document Type</p>
                                <p className="text-lg font-semibold text-gray-900">
                                    {result.document_type?.replace(/_/g, ' ').toUpperCase() || 'Unknown'}
                                </p>
                            </div>
                            <div>
                                <p className="text-sm text-gray-600">Confidence</p>
                                <p className="text-lg font-semibold text-gray-900">
                                    {formatConfidence(result.confidence)}
                                </p>
                            </div>
                        </div>

                        {result.summary && (
                            <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                                <p className="text-sm font-medium text-blue-900 mb-2">Summary</p>
                                <p className="text-sm text-blue-800 whitespace-pre-line">{result.summary}</p>
                            </div>
                        )}
                    </div>

                    {/* Extracted Fields */}
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <h2 className="text-xl font-semibold mb-4">Extracted Fields</h2>
                        {renderExtractedFields(result.extracted_fields)}
                    </div>

                    {/* Download Buttons */}
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <h2 className="text-xl font-semibold mb-4">Downloads</h2>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {result.raw_document_url && (
                                <button
                                    onClick={() => handleDownload(result.raw_document_url!, result.filename)}
                                    className="px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center"
                                >
                                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                    Download Original
                                </button>
                            )}

                            {result.processed_document_url && (
                                <button
                                    onClick={() => handleDownload(result.processed_document_url!, `${result.filename}_processed.txt`)}
                                    className="px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center"
                                >
                                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                    Download Extracted Text
                                </button>
                            )}

                            {result.filled_template_url && (
                                <button
                                    onClick={() => handleDownload(result.filled_template_url!, 'filled_template.docx')}
                                    className="px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors flex items-center justify-center"
                                >
                                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                                    </svg>
                                    Download Filled Template
                                </button>
                            )}
                        </div>

                        {!result.raw_document_url && !result.processed_document_url && !result.filled_template_url && (
                            <p className="text-gray-500 text-center py-4">No downloads available</p>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}
