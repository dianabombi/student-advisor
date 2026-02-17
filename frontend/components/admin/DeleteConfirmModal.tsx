'use client';

import { useState } from 'react';
import { X, AlertTriangle, Trash2 } from 'lucide-react';
import { useLanguage } from '@/lib/LanguageContext';

interface Administrator {
    id: number;
    name: string;
    email: string;
}

interface DeleteConfirmModalProps {
    isOpen: boolean;
    admin: Administrator;
    onClose: () => void;
    onConfirm: () => void;
}

export default function DeleteConfirmModal({
    isOpen,
    admin,
    onClose,
    onConfirm,
}: DeleteConfirmModalProps) {
    const { t } = useLanguage();
    const [loading, setLoading] = useState(false);

    if (!isOpen) return null;

    const handleConfirm = async () => {
        setLoading(true);

        // Simulate API call
        setTimeout(() => {
            onConfirm();
            setLoading(false);
        }, 500);
    };

    const handleBackdropClick = (e: React.MouseEvent) => {
        if (e.target === e.currentTarget) {
            onClose();
        }
    };

    return (
        <div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
            onClick={handleBackdropClick}
        >
            <div className="bg-gray-800 rounded-xl border border-red-900/50 w-full max-w-md shadow-2xl">
                {/* Header */}
                <div className="flex items-center justify-between p-6 border-b border-red-900/50">
                    <h2 className="text-xl font-bold text-red-400 flex items-center gap-2">
                        <AlertTriangle className="w-6 h-6" />
                        {t('admin.administrators.modals.delete.title')}
                    </h2>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-gray-700 rounded-lg transition-colors text-gray-400 hover:text-white"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Content */}
                <div className="p-6 space-y-4">
                    <p className="text-gray-300">
                        {t('admin.administrators.modals.delete.message')}
                    </p>

                    <div className="bg-gray-900 rounded-lg p-4 border border-gray-700">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-semibold">
                                {admin.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)}
                            </div>
                            <div>
                                <div className="text-white font-medium">{admin.name}</div>
                                <div className="text-gray-400 text-sm">{admin.email}</div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-red-900/20 border border-red-700 rounded-lg p-4">
                        <p className="text-sm text-red-400">
                            ⚠️ {t('admin.administrators.modals.delete.warning')}
                        </p>
                    </div>
                </div>

                {/* Actions */}
                <div className="flex items-center gap-3 p-6 border-t border-red-900/50">
                    <button
                        type="button"
                        onClick={onClose}
                        className="flex-1 px-4 py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
                    >
                        {t('admin.administrators.modals.delete.cancel')}
                    </button>
                    <button
                        type="button"
                        onClick={handleConfirm}
                        disabled={loading}
                        className="flex-1 px-4 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
                    >
                        {loading ? (
                            <>
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                {t('admin.administrators.modals.delete.deleting')}
                            </>
                        ) : (
                            <>
                                <Trash2 className="w-4 h-4" />
                                {t('admin.administrators.modals.delete.confirm')}
                            </>
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}
