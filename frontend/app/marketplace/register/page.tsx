'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useTranslation } from 'react-i18next';
import '@/lib/i18n'; // Initialize i18next
import { useAuth } from '@/contexts/AuthContext';
import { Upload, CheckCircle, ArrowLeft, ArrowRight, Check, X } from 'lucide-react';
import Navigation from '@/components/Navigation';
import { registerLawyer } from '@/lib/marketplaceService';

// Only SK, CZ, PL jurisdictions allowed for lawyer registration
const ALLOWED_JURISDICTIONS = ['SK', 'CZ', 'PL'];
const JURISDICTION_TO_LANGUAGE: { [key: string]: string } = {
    'SK': 'sk',
    'CZ': 'cs',
    'PL': 'pl'
};

const SPECIALIZATIONS = [
    'civil_law', 'criminal_law', 'labor_law', 'family_law', 'commercial_law',
    'real_estate_law', 'tax_law', 'intellectual_property', 'administrative_law', 'corporate_law'
];

export default function LawyerRegistrationPage() {
    const router = useRouter();
    const { t, i18n } = useTranslation('common');
    const { user } = useAuth();
    const [currentStep, setCurrentStep] = useState(0); // Start at step 0 for jurisdiction selection
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [selectedJurisdiction, setSelectedJurisdiction] = useState<string | null>(null);

    const [formData, setFormData] = useState({
        full_name: user?.name || '',
        title: '',
        license_number: '',
        bar_association: '',
        experience_years: 0,
        bio: '',
        education: '',
        hourly_rate: 0,
        consultation_fee: 0,
        specializations: [] as string[],
        languages: [] as string[],
    });

    const [files, setFiles] = useState({
        diploma: null as File | null,
        license: null as File | null,
        id_document: null as File | null,
    });

    // When jurisdiction is selected, change language automatically
    const handleJurisdictionSelect = (jurisdiction: string) => {
        setSelectedJurisdiction(jurisdiction);
        const language = JURISDICTION_TO_LANGUAGE[jurisdiction];
        if (language) {
            i18n.changeLanguage(language);
        }
    };

    const handleInputChange = (field: string, value: any) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    const handleArrayToggle = (field: 'specializations' | 'languages', value: string) => {
        setFormData(prev => ({
            ...prev,
            [field]: prev[field].includes(value)
                ? prev[field].filter(item => item !== value)
                : [...prev[field], value]
        }));
    };

    const handleFileChange = (field: 'diploma' | 'license' | 'id_document', file: File | null) => {
        setFiles(prev => ({ ...prev, [field]: file }));
    };

    const validateStep = (step: number): boolean => {
        switch (step) {
            case 0:
                return !!selectedJurisdiction;
            case 1:
                return !!(formData.full_name && formData.license_number && formData.bar_association && formData.experience_years > 0);
            case 2:
                return !!(files.diploma && files.license && files.id_document);
            case 3:
                return formData.specializations.length > 0 && formData.languages.length > 0;
            default:
                return true;
        }
    };

    const handleNext = () => {
        if (validateStep(currentStep)) {
            setCurrentStep(prev => Math.min(prev + 1, 4));
            setError(null);
        } else {
            setError(t('marketplace.registration.required'));
        }
    };

    const handlePrevious = () => {
        setCurrentStep(prev => Math.max(prev - 1, 0));
        setError(null);
    };

    const handleSubmit = async () => {
        setLoading(true);
        setError(null);

        try {
            const formDataToSend = new FormData();

            // Add jurisdiction (single value)
            if (selectedJurisdiction) {
                formDataToSend.append('jurisdictions', JSON.stringify([selectedJurisdiction]));
            }

            // Add all form fields
            Object.entries(formData).forEach(([key, value]) => {
                if (Array.isArray(value)) {
                    formDataToSend.append(key, JSON.stringify(value));
                } else {
                    formDataToSend.append(key, String(value));
                }
            });

            // Add files
            if (files.diploma) formDataToSend.append('diploma', files.diploma);
            if (files.license) formDataToSend.append('license', files.license);
            if (files.id_document) formDataToSend.append('id_document', files.id_document);

            await registerLawyer(formDataToSend);

            // Success - redirect to dashboard or show success message
            router.push('/marketplace?registered=true');
        } catch (err: any) {
            setError(err.message || t('marketplace.registration.error'));
        } finally {
            setLoading(false);
        }
    };

    // Step 0: Jurisdiction Selection
    const renderStep0 = () => (
        <div className="space-y-6">
            <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                    {t('marketplace.registration.selectYourJurisdiction')}
                </h2>
                <p className="text-gray-600 dark:text-gray-400">
                    {t('marketplace.registration.jurisdictionLanguageInfo')}
                </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {ALLOWED_JURISDICTIONS.map(jurisdiction => (
                    <button
                        key={jurisdiction}
                        onClick={() => handleJurisdictionSelect(jurisdiction)}
                        className={`p-8 rounded-xl border-4 transition-all transform hover:scale-105 ${selectedJurisdiction === jurisdiction
                            ? 'border-blue-600 bg-blue-50 dark:bg-blue-900/30 shadow-xl'
                            : 'border-gray-300 dark:border-gray-600 hover:border-blue-400'
                            }`}
                    >
                        <div className="text-6xl mb-4">
                            {jurisdiction === 'SK' && '🇸🇰'}
                            {jurisdiction === 'CZ' && '🇨🇿'}
                            {jurisdiction === 'PL' && '🇵🇱'}
                        </div>
                        <div className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                            {jurisdiction}
                        </div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">
                            {jurisdiction === 'SK' && 'Slovensko'}
                            {jurisdiction === 'CZ' && 'Česká republika'}
                            {jurisdiction === 'PL' && 'Polska'}
                        </div>
                        {selectedJurisdiction === jurisdiction && (
                            <div className="mt-4">
                                <CheckCircle className="w-8 h-8 text-blue-600 mx-auto" />
                            </div>
                        )}
                    </button>
                ))}
            </div>
        </div>
    );

    const renderStep1 = () => (
        <div className="space-y-4">
            <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    {t('marketplace.registration.fullName')} *
                </label>
                <input
                    type="text"
                    value={formData.full_name}
                    onChange={(e) => handleInputChange('full_name', e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    {t('marketplace.registration.lawyerTitle')}
                </label>
                <input
                    type="text"
                    value={formData.title}
                    onChange={(e) => handleInputChange('title', e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        {t('marketplace.registration.licenseNumber')} *
                    </label>
                    <input
                        type="text"
                        value={formData.license_number}
                        onChange={(e) => handleInputChange('license_number', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        {t('marketplace.registration.barAssociation')} *
                    </label>
                    <input
                        type="text"
                        value={formData.bar_association}
                        onChange={(e) => handleInputChange('bar_association', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                </div>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    {t('marketplace.registration.experienceYears')} *
                </label>
                <input
                    type="number"
                    min="0"
                    value={formData.experience_years}
                    onChange={(e) => handleInputChange('experience_years', parseInt(e.target.value) || 0)}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    {t('marketplace.registration.bio')}
                </label>
                <textarea
                    rows={4}
                    value={formData.bio}
                    onChange={(e) => handleInputChange('bio', e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    {t('marketplace.registration.education')}
                </label>
                <textarea
                    rows={3}
                    value={formData.education}
                    onChange={(e) => handleInputChange('education', e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        {t('marketplace.registration.hourlyRate')}
                    </label>
                    <input
                        type="number"
                        min="0"
                        value={formData.hourly_rate}
                        onChange={(e) => handleInputChange('hourly_rate', parseFloat(e.target.value) || 0)}
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        {t('marketplace.registration.consultationFee')}
                    </label>
                    <input
                        type="number"
                        min="0"
                        value={formData.consultation_fee}
                        onChange={(e) => handleInputChange('consultation_fee', parseFloat(e.target.value) || 0)}
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                </div>
            </div>
        </div>
    );

    const renderFileUpload = (
        field: 'diploma' | 'license' | 'id_document',
        label: string,
        required: boolean = true
    ) => (
        <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {label} {required && '*'}
            </label>
            <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6">
                {files[field] ? (
                    <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-700 dark:text-gray-300">{files[field]!.name}</span>
                        <button
                            onClick={() => handleFileChange(field, null)}
                            className="text-red-600 hover:text-red-700"
                        >
                            <X className="w-5 h-5" />
                        </button>
                    </div>
                ) : (
                    <label className="flex flex-col items-center cursor-pointer">
                        <Upload className="w-8 h-8 text-gray-400 mb-2" />
                        <span className="text-sm text-gray-600 dark:text-gray-400">Click to upload</span>
                        <input
                            type="file"
                            accept=".pdf,.jpg,.jpeg,.png"
                            onChange={(e) => handleFileChange(field, e.target.files?.[0] || null)}
                            className="hidden"
                        />
                    </label>
                )}
            </div>
        </div>
    );

    const renderStep2 = () => (
        <div className="space-y-4">
            {renderFileUpload('diploma', t('marketplace.registration.uploadDiploma'))}
            {renderFileUpload('license', t('marketplace.registration.uploadLicense'))}
            {renderFileUpload('id_document', t('marketplace.registration.uploadId'))}
            <p className="text-sm text-gray-600 dark:text-gray-400">
                {t('marketplace.registration.invalidFileType')}
            </p>
        </div>
    );

    const renderStep3 = () => (
        <div className="space-y-6">
            <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                    {t('marketplace.registration.selectSpecializations')} *
                </label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {SPECIALIZATIONS.map(spec => (
                        <button
                            key={spec}
                            onClick={() => handleArrayToggle('specializations', spec)}
                            className={`px-4 py-2 rounded-lg border-2 text-left transition ${formData.specializations.includes(spec)
                                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900 text-blue-700 dark:text-blue-200'
                                : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                                }`}
                        >
                            {t(`marketplace.specializations.${spec}`)}
                        </button>
                    ))}
                </div>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                    {t('marketplace.registration.selectLanguages')} *
                </label>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
                    {['sk', 'cs', 'pl', 'uk', 'ru', 'de', 'it', 'fr', 'es', 'en'].map(lang => (
                        <button
                            key={lang}
                            onClick={() => handleArrayToggle('languages', lang)}
                            className={`px-4 py-2 rounded-lg border-2 transition ${formData.languages.includes(lang)
                                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900 text-blue-700 dark:text-blue-200'
                                : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                                }`}
                        >
                            {lang.toUpperCase()}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );

    const renderStep4 = () => (
        <div className="space-y-6">
            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                <p className="text-sm text-blue-800 dark:text-blue-200">
                    {t('marketplace.registration.success')}
                </p>
            </div>

            <div className="space-y-4">
                <div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Personal Information</h4>
                    <dl className="grid grid-cols-2 gap-2 text-sm">
                        <dt className="text-gray-600 dark:text-gray-400">Name:</dt>
                        <dd className="text-gray-900 dark:text-white">{formData.full_name}</dd>
                        <dt className="text-gray-600 dark:text-gray-400">License:</dt>
                        <dd className="text-gray-900 dark:text-white">{formData.license_number}</dd>
                        <dt className="text-gray-600 dark:text-gray-400">Experience:</dt>
                        <dd className="text-gray-900 dark:text-white">{formData.experience_years} years</dd>
                    </dl>
                </div>

                <div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Documents</h4>
                    <ul className="text-sm space-y-1">
                        <li className="text-gray-700 dark:text-gray-300">✓ Diploma: {files.diploma?.name}</li>
                        <li className="text-gray-700 dark:text-gray-300">✓ License: {files.license?.name}</li>
                        <li className="text-gray-700 dark:text-gray-300">✓ ID: {files.id_document?.name}</li>
                    </ul>
                </div>

                <div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Specializations</h4>
                    <div className="flex flex-wrap gap-2">
                        {formData.specializations.map(spec => (
                            <span key={spec} className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded">
                                {t(`marketplace.specializations.${spec}`)}
                            </span>
                        ))}
                    </div>
                </div>

                <div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Jurisdiction & Languages</h4>
                    <p className="text-sm text-gray-700 dark:text-gray-300">
                        {selectedJurisdiction} | {formData.languages.map(l => l.toUpperCase()).join(', ')}
                    </p>
                </div>
            </div>
        </div>
    );

    return (
        <>
            <Navigation />
            <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
                <div className="max-w-3xl mx-auto px-4">
                    {/* Header */}
                    <div className="mb-8">
                        <button
                            onClick={() => router.back()}
                            className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white mb-4"
                        >
                            <ArrowLeft className="w-5 h-5" />
                            {t('common.back')}
                        </button>
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                            {t('marketplace.registration.title')}
                        </h1>
                        <p className="text-gray-600 dark:text-gray-400">
                            {t('marketplace.registration.subtitle')}
                        </p>
                    </div>

                    {/* Progress Steps */}
                    <div className="mb-8">
                        <div className="flex items-center justify-between">
                            {[0, 1, 2, 3, 4].map(step => (
                                <div key={step} className="flex items-center flex-1">
                                    <div className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold ${step < currentStep
                                        ? 'bg-green-500 text-white'
                                        : step === currentStep
                                            ? 'bg-blue-600 text-white'
                                            : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
                                        }`}>
                                        {step < currentStep ? <Check className="w-5 h-5" /> : step + 1}
                                    </div>
                                    {step < 4 && (
                                        <div className={`flex-1 h-1 mx-2 ${step < currentStep ? 'bg-green-500' : 'bg-gray-200 dark:bg-gray-700'
                                            }`} />
                                    )}
                                </div>
                            ))}
                        </div>
                        <div className="flex justify-between mt-2">
                            <span className="text-xs text-gray-600 dark:text-gray-400">{t('marketplace.registration.step0')}</span>
                            <span className="text-xs text-gray-600 dark:text-gray-400">{t('marketplace.registration.step1')}</span>
                            <span className="text-xs text-gray-600 dark:text-gray-400">{t('marketplace.registration.step2')}</span>
                            <span className="text-xs text-gray-600 dark:text-gray-400">{t('marketplace.registration.step3')}</span>
                            <span className="text-xs text-gray-600 dark:text-gray-400">{t('marketplace.registration.step4')}</span>
                        </div>
                    </div>

                    {/* Form */}
                    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
                        {currentStep === 0 && renderStep0()}
                        {currentStep === 1 && renderStep1()}
                        {currentStep === 2 && renderStep2()}
                        {currentStep === 3 && renderStep3()}
                        {currentStep === 4 && renderStep4()}

                        {error && (
                            <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-800 dark:text-red-200 text-sm">
                                {error}
                            </div>
                        )}
                    </div>

                    {/* Navigation Buttons */}
                    <div className="flex justify-between">
                        <button
                            onClick={handlePrevious}
                            disabled={currentStep === 0}
                            className="px-6 py-3 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                        >
                            <ArrowLeft className="w-5 h-5" />
                            {t('marketplace.registration.previous')}
                        </button>

                        {currentStep < 4 ? (
                            <button
                                onClick={handleNext}
                                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center gap-2"
                            >
                                {t('marketplace.registration.next')}
                                <ArrowRight className="w-5 h-5" />
                            </button>
                        ) : (
                            <button
                                onClick={handleSubmit}
                                disabled={loading}
                                className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {loading ? t('marketplace.registration.submitting') : t('marketplace.registration.submit')}
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </>
    );
}
