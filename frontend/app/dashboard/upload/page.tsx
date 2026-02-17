'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Sparkles, Upload as UploadIcon, X, FileText, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { useLanguage } from '@/lib/LanguageContext';
import { UPLDisclaimer } from '@/components/UPLDisclaimer';

export default function UploadPage() {
    const router = useRouter();
    const { t } = useLanguage();
    const [files, setFiles] = useState<File[]>([]);
    const [uploading, setUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            setFiles(Array.from(e.dataTransfer.files));
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFiles(Array.from(e.target.files));
        }
    };

    const handleUpload = async () => {
        if (files.length === 0) return;

        setUploading(true);
        const formData = new FormData();
        files.forEach(file => formData.append('files', file));

        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/documents/upload', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData
            });

            if (response.ok) {
                router.push('/dashboard');
            }
        } catch (err) {
            console.error('Upload error:', err);
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
            <div className="container mx-auto px-6 py-12">
                <Link href="/dashboard" className="inline-flex items-center space-x-2 text-gray-300 hover:text-white mb-8 transition-colors">
                    <ArrowLeft className="w-5 h-5" />
                    <span>{t('dashboard.back_to_dashboard')}</span>
                </Link>

                <div className="max-w-2xl mx-auto">
                    <h1 className="text-4xl font-bold text-white mb-4">{t('upload.title')}</h1>
                    <p className="text-gray-300 mb-8">{t('upload.description')}</p>

                    {/* UPL Disclaimer */}
                    <UPLDisclaimer />

                    {/* Upload Area */}
                    <div
                        onDragEnter={handleDrag}
                        onDragLeave={handleDrag}
                        onDragOver={handleDrag}
                        onDrop={handleDrop}
                        className={`border-2 border-dashed rounded-2xl p-12 text-center transition-all ${dragActive
                            ? 'border-purple-500 bg-purple-500/10'
                            : 'border-white/20 bg-white/5'
                            }`}
                    >
                        <UploadIcon className="w-16 h-16 text-purple-400 mx-auto mb-4" />
                        <h3 className="text-xl font-bold text-white mb-2">
                            {t('upload.drag_drop')}
                        </h3>
                        <p className="text-gray-300 mb-4">{t('upload.or')}</p>
                        <label className="inline-block px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all cursor-pointer">
                            <input
                                type="file"
                                multiple
                                onChange={handleFileChange}
                                className="hidden"
                                accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
                            />
                            {t('upload.button')}
                        </label>
                        <p className="text-sm text-gray-400 mt-4">
                            {t('upload.file_types')}
                        </p>
                    </div>

                    {/* Selected Files */}
                    {files.length > 0 && (
                        <div className="mt-8 bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
                            <h3 className="text-lg font-bold text-white mb-4">{t('upload.selected_files').replace('{{count}}', files.length.toString())}</h3>
                            <div className="space-y-3">
                                {files.map((file, idx) => (
                                    <div key={idx} className="flex items-center justify-between bg-white/5 rounded-lg p-3">
                                        <div className="flex items-center space-x-3">
                                            <FileText className="w-5 h-5 text-purple-400" />
                                            <div>
                                                <p className="text-white font-medium">{file.name}</p>
                                                <p className="text-sm text-gray-400">{(file.size / 1024).toFixed(2)} KB</p>
                                            </div>
                                        </div>
                                        <button
                                            onClick={() => setFiles(files.filter((_, i) => i !== idx))}
                                            className="p-1 text-gray-400 hover:text-red-400 transition-colors"
                                        >
                                            <X className="w-5 h-5" />
                                        </button>
                                    </div>
                                ))}
                            </div>

                            <button
                                onClick={handleUpload}
                                disabled={uploading}
                                className="w-full mt-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all disabled:opacity-50"
                            >
                                {uploading ? t('upload.uploading') : t('upload.upload_button')}
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
