'use client';

import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { CheckCircle, XCircle, Eye, FileText, Clock, User } from 'lucide-react';
import {
    getPendingLawyers,
    verifyLawyer,
    rejectLawyer
} from '@/lib/marketplaceService';

export default function AdminVerificationPanel() {
    const { t } = useTranslation();
    const [activeTab, setActiveTab] = useState<'pending' | 'verified' | 'rejected'>('pending');
    const [lawyers, setLawyers] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedLawyer, setSelectedLawyer] = useState<any>(null);
    const [rejectReason, setRejectReason] = useState('');
    const [processing, setProcessing] = useState(false);

    useEffect(() => {
        fetchLawyers();
    }, [activeTab]);

    const fetchLawyers = async () => {
        setLoading(true);
        try {
            const data = await getPendingLawyers(activeTab);
            setLawyers(data);
        } catch (err) {
            console.error('Error fetching lawyers:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleVerify = async (lawyerId: number) => {
        if (!confirm(t('marketplace.admin.confirmVerify'))) return;

        setProcessing(true);
        try {
            await verifyLawyer(lawyerId);
            setLawyers(prev => prev.filter(l => l.id !== lawyerId));
            setSelectedLawyer(null);
            alert(t('marketplace.admin.verifySuccess'));
        } catch (err: any) {
            alert(err.message || t('marketplace.admin.error'));
        } finally {
            setProcessing(false);
        }
    };

    const handleReject = async (lawyerId: number) => {
        if (!rejectReason || rejectReason.length < 10) {
            alert(t('marketplace.admin.rejectReasonPlaceholder'));
            return;
        }

        if (!confirm(t('marketplace.admin.confirmReject'))) return;

        setProcessing(true);
        try {
            await rejectLawyer(lawyerId, rejectReason);
            setLawyers(prev => prev.filter(l => l.id !== lawyerId));
            setSelectedLawyer(null);
            setRejectReason('');
            alert(t('marketplace.admin.rejectSuccess'));
        } catch (err: any) {
            alert(err.message || t('marketplace.admin.error'));
        } finally {
            setProcessing(false);
        }
    };

    const renderLawyerCard = (lawyer: any) => (
        <div
            key={lawyer.id}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-lg transition cursor-pointer"
            onClick={() => setSelectedLawyer(lawyer)}
        >
            <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-lg">
                        {lawyer.full_name.charAt(0).toUpperCase()}
                    </div>
                    <div>
                        <h3 className="font-semibold text-gray-900 dark:text-white">
                            {lawyer.full_name}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                            {lawyer.license_number}
                        </p>
                    </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${activeTab === 'pending'
                        ? 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
                        : activeTab === 'verified'
                            ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                            : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                    }`}>
                    {t(`marketplace.admin.${activeTab}`)}
                </span>
            </div>

            <div className="grid grid-cols-2 gap-4 text-sm mb-4">
                <div>
                    <span className="text-gray-600 dark:text-gray-400">Experience:</span>
                    <p className="font-medium text-gray-900 dark:text-white">
                        {lawyer.experience_years} years
                    </p>
                </div>
                <div>
                    <span className="text-gray-600 dark:text-gray-400">Bar:</span>
                    <p className="font-medium text-gray-900 dark:text-white">
                        {lawyer.bar_association}
                    </p>
                </div>
            </div>

            <div className="flex flex-wrap gap-2 mb-4">
                {lawyer.specializations?.slice(0, 3).map((spec: string, index: number) => (
                    <span
                        key={index}
                        className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded-full"
                    >
                        {t(`marketplace.specializations.${spec}`)}
                    </span>
                ))}
                {lawyer.specializations?.length > 3 && (
                    <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 text-xs rounded-full">
                        +{lawyer.specializations.length - 3}
                    </span>
                )}
            </div>

            <div className="text-xs text-gray-500 dark:text-gray-400">
                {t('marketplace.admin.registeredAt')}: {new Date(lawyer.created_at).toLocaleDateString()}
            </div>
        </div>
    );

    const renderDetailModal = () => {
        if (!selectedLawyer) return null;

        return (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                <div className="bg-white dark:bg-gray-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
                    <div className="sticky top-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 p-6">
                        <div className="flex items-center justify-between">
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                                {selectedLawyer.full_name}
                            </h2>
                            <button
                                onClick={() => setSelectedLawyer(null)}
                                className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                            >
                                <XCircle className="w-6 h-6" />
                            </button>
                        </div>
                    </div>

                    <div className="p-6 space-y-6">
                        {/* Personal Info */}
                        <div>
                            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                                Personal Information
                            </h3>
                            <dl className="grid grid-cols-2 gap-4 text-sm">
                                <div>
                                    <dt className="text-gray-600 dark:text-gray-400">Full Name:</dt>
                                    <dd className="font-medium text-gray-900 dark:text-white">{selectedLawyer.full_name}</dd>
                                </div>
                                <div>
                                    <dt className="text-gray-600 dark:text-gray-400">Title:</dt>
                                    <dd className="font-medium text-gray-900 dark:text-white">{selectedLawyer.title || 'N/A'}</dd>
                                </div>
                                <div>
                                    <dt className="text-gray-600 dark:text-gray-400">License Number:</dt>
                                    <dd className="font-medium text-gray-900 dark:text-white">{selectedLawyer.license_number}</dd>
                                </div>
                                <div>
                                    <dt className="text-gray-600 dark:text-gray-400">Bar Association:</dt>
                                    <dd className="font-medium text-gray-900 dark:text-white">{selectedLawyer.bar_association}</dd>
                                </div>
                                <div>
                                    <dt className="text-gray-600 dark:text-gray-400">Experience:</dt>
                                    <dd className="font-medium text-gray-900 dark:text-white">{selectedLawyer.experience_years} years</dd>
                                </div>
                                <div>
                                    <dt className="text-gray-600 dark:text-gray-400">Hourly Rate:</dt>
                                    <dd className="font-medium text-gray-900 dark:text-white">
                                        {selectedLawyer.hourly_rate ? `€${selectedLawyer.hourly_rate}` : 'N/A'}
                                    </dd>
                                </div>
                            </dl>
                        </div>

                        {/* Bio */}
                        {selectedLawyer.bio && (
                            <div>
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                                    Biography
                                </h3>
                                <p className="text-gray-700 dark:text-gray-300">{selectedLawyer.bio}</p>
                            </div>
                        )}

                        {/* Education */}
                        {selectedLawyer.education && (
                            <div>
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                                    Education
                                </h3>
                                <p className="text-gray-700 dark:text-gray-300">{selectedLawyer.education}</p>
                            </div>
                        )}

                        {/* Specializations & Jurisdictions */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                                    Specializations
                                </h3>
                                <div className="flex flex-wrap gap-2">
                                    {selectedLawyer.specializations?.map((spec: string, index: number) => (
                                        <span
                                            key={index}
                                            className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded-full"
                                        >
                                            {t(`marketplace.specializations.${spec}`)}
                                        </span>
                                    ))}
                                </div>
                            </div>
                            <div>
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                                    Jurisdictions
                                </h3>
                                <p className="text-gray-700 dark:text-gray-300">
                                    {selectedLawyer.jurisdictions?.join(', ')}
                                </p>
                            </div>
                        </div>

                        {/* Documents */}
                        <div>
                            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                                {t('marketplace.admin.viewDocuments')}
                            </h3>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                                {['diploma', 'license', 'idDocument'].map((docType) => (
                                    <a
                                        key={docType}
                                        href={selectedLawyer[`${docType}_url`]}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex items-center gap-2 p-3 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition"
                                    >
                                        <FileText className="w-5 h-5 text-blue-600" />
                                        <span className="text-sm text-gray-700 dark:text-gray-300">
                                            {t(`marketplace.admin.${docType}`)}
                                        </span>
                                    </a>
                                ))}
                            </div>
                        </div>

                        {/* Actions */}
                        {activeTab === 'pending' && (
                            <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
                                <div className="flex flex-col gap-4">
                                    <div className="flex gap-3">
                                        <button
                                            onClick={() => handleVerify(selectedLawyer.id)}
                                            disabled={processing}
                                            className="flex-1 px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium disabled:opacity-50 flex items-center justify-center gap-2"
                                        >
                                            <CheckCircle className="w-5 h-5" />
                                            {processing ? t('marketplace.admin.verifying') : t('marketplace.admin.verify')}
                                        </button>
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                            {t('marketplace.admin.rejectReason')}
                                        </label>
                                        <textarea
                                            value={rejectReason}
                                            onChange={(e) => setRejectReason(e.target.value)}
                                            placeholder={t('marketplace.admin.rejectReasonPlaceholder')}
                                            rows={3}
                                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                                        />
                                        <button
                                            onClick={() => handleReject(selectedLawyer.id)}
                                            disabled={processing || !rejectReason}
                                            className="mt-2 w-full px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium disabled:opacity-50 flex items-center justify-center gap-2"
                                        >
                                            <XCircle className="w-5 h-5" />
                                            {processing ? t('marketplace.admin.rejecting') : t('marketplace.admin.reject')}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                        {t('marketplace.admin.title')}
                    </h1>
                    <p className="text-gray-600 dark:text-gray-400">
                        Review and verify lawyer registration applications
                    </p>
                </div>

                {/* Tabs */}
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md mb-6">
                    <div className="border-b border-gray-200 dark:border-gray-700">
                        <nav className="flex -mb-px">
                            <button
                                onClick={() => setActiveTab('pending')}
                                className={`px-6 py-4 text-sm font-medium border-b-2 transition flex items-center gap-2 ${activeTab === 'pending'
                                        ? 'border-orange-500 text-orange-600 dark:text-orange-400'
                                        : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                                    }`}
                            >
                                <Clock className="w-4 h-4" />
                                {t('marketplace.admin.pending')}
                            </button>
                            <button
                                onClick={() => setActiveTab('verified')}
                                className={`px-6 py-4 text-sm font-medium border-b-2 transition flex items-center gap-2 ${activeTab === 'verified'
                                        ? 'border-green-500 text-green-600 dark:text-green-400'
                                        : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                                    }`}
                            >
                                <CheckCircle className="w-4 h-4" />
                                {t('marketplace.admin.verified')}
                            </button>
                            <button
                                onClick={() => setActiveTab('rejected')}
                                className={`px-6 py-4 text-sm font-medium border-b-2 transition flex items-center gap-2 ${activeTab === 'rejected'
                                        ? 'border-red-500 text-red-600 dark:text-red-400'
                                        : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                                    }`}
                            >
                                <XCircle className="w-4 h-4" />
                                {t('marketplace.admin.rejected')}
                            </button>
                        </nav>
                    </div>
                </div>

                {/* Content */}
                {loading ? (
                    <div className="text-center py-12">
                        <div className="text-gray-600 dark:text-gray-400">Loading...</div>
                    </div>
                ) : lawyers.length === 0 ? (
                    <div className="text-center py-12">
                        <p className="text-gray-600 dark:text-gray-400">
                            {t('marketplace.admin.noPending')}
                        </p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {lawyers.map(renderLawyerCard)}
                    </div>
                )}

                {/* Detail Modal */}
                {renderDetailModal()}
            </div>
        </div>
    );
}
