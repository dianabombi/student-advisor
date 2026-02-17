'use client';

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Filter, X } from 'lucide-react';
import { useLanguage } from '@/lib/LanguageContext';

interface FilterState {
    jurisdiction: string;
    specialization: string;
    minRating: number;
    language: string;
    availableOnly: boolean;
}

interface LawyerSearchFiltersProps {
    filters: FilterState;
    onFilterChange: (filters: FilterState) => void;
    onClear: () => void;
}

// Active jurisdictions (currently supported)
const ACTIVE_JURISDICTIONS = [
    'SK', // Slovakia
    'CZ', // Czech Republic
    'PL'  // Poland
];

// Inactive jurisdictions (EU countries not yet supported)
const INACTIVE_JURISDICTIONS = [
    'AT', // Austria
    'BE', // Belgium
    'BG', // Bulgaria
    'HR', // Croatia
    'CY', // Cyprus
    'DK', // Denmark
    'EE', // Estonia
    'FI', // Finland
    'FR', // France
    'DE', // Germany
    'GR', // Greece
    'HU', // Hungary
    'IE', // Ireland
    'IT', // Italy
    'LV', // Latvia
    'LT', // Lithuania
    'LU', // Luxembourg
    'MT', // Malta
    'NL', // Netherlands
    'PT', // Portugal
    'RO', // Romania
    'SI', // Slovenia
    'ES', // Spain
    'SE'  // Sweden
];

const SPECIALIZATIONS = [
    'civil_law',
    'criminal_law',
    'labor_law',
    'family_law',
    'commercial_law',
    'real_estate_law',
    'tax_law',
    'intellectual_property',
    'administrative_law',
    'corporate_law'
];

const LANGUAGES = [
    { code: 'sk', name: 'Slovenčina' },
    { code: 'cs', name: 'Čeština' },
    { code: 'pl', name: 'Polski' },
    { code: 'en', name: 'English' },
    { code: 'de', name: 'Deutsch' },
    { code: 'uk', name: 'Українська' },
    { code: 'ru', name: 'Русский' },
    { code: 'fr', name: 'Français' },
    { code: 'es', name: 'Español' },
    { code: 'it', name: 'Italiano' }
];

const RATINGS = [3, 4, 5];

export default function LawyerSearchFilters({ filters, onFilterChange, onClear }: LawyerSearchFiltersProps) {
    const { t } = useTranslation();
    const { language, setLanguage } = useLanguage();
    const [isExpanded, setIsExpanded] = useState(false);

    const handleFilterChange = (key: keyof FilterState, value: any) => {
        onFilterChange({
            ...filters,
            [key]: value
        });
    };

    const handleLanguageChange = (langCode: string) => {
        // Change the global interface language
        setLanguage(langCode as any);
        // Also update the filter
        handleFilterChange('language', langCode);
    };

    const hasActiveFilters =
        filters.jurisdiction !== '' ||
        filters.specialization !== '' ||
        filters.minRating > 0 ||
        filters.language !== '' ||
        filters.availableOnly;

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                    <Filter className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                        {t('marketplace.filters.title')}
                    </h3>
                    {hasActiveFilters && (
                        <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded-full">
                            {Object.values(filters).filter(v => v !== '' && v !== false && v !== 0).length}
                        </span>
                    )}
                </div>
                <div className="flex items-center gap-2">
                    {hasActiveFilters && (
                        <button
                            onClick={onClear}
                            className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white flex items-center gap-1"
                        >
                            <X className="w-4 h-4" />
                            {t('marketplace.filters.clear')}
                        </button>
                    )}
                    <button
                        onClick={() => setIsExpanded(!isExpanded)}
                        className="lg:hidden px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm"
                    >
                        {isExpanded ? t('common.close') : t('marketplace.filters.apply')}
                    </button>
                </div>
            </div>

            {/* Filters */}
            <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 ${isExpanded ? 'block' : 'hidden lg:grid'}`}>
                {/* Jurisdiction */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        {t('marketplace.filters.jurisdiction')}
                    </label>
                    <select
                        value={filters.jurisdiction}
                        onChange={(e) => handleFilterChange('jurisdiction', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                        <option value="">{t('common.all') || 'All'}</option>

                        {/* Active jurisdictions */}
                        <optgroup label="✓ Active">
                            {ACTIVE_JURISDICTIONS.map((jur) => (
                                <option key={jur} value={jur}>
                                    {jur}
                                </option>
                            ))}
                        </optgroup>

                        {/* Inactive jurisdictions */}
                        <optgroup label="⏳ Coming Soon">
                            {INACTIVE_JURISDICTIONS.map((jur) => (
                                <option key={jur} value={jur} disabled>
                                    {jur} (not available yet)
                                </option>
                            ))}
                        </optgroup>
                    </select>
                </div>

                {/* Specialization */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        {t('marketplace.filters.specialization')}
                    </label>
                    <select
                        value={filters.specialization}
                        onChange={(e) => handleFilterChange('specialization', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                        <option value="">{t('common.all') || 'All'}</option>
                        {SPECIALIZATIONS.map((spec) => (
                            <option key={spec} value={spec}>
                                {t(`marketplace.specializations.${spec}`)}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Minimum Rating */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        {t('marketplace.filters.rating')}
                    </label>
                    <select
                        value={filters.minRating}
                        onChange={(e) => handleFilterChange('minRating', parseFloat(e.target.value))}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                        {RATINGS.map((rating) => (
                            <option key={rating} value={rating}>
                                {`${rating} ⭐`}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Language */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        {t('marketplace.filters.language')}
                    </label>
                    <select
                        value={language}
                        onChange={(e) => handleLanguageChange(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                        {LANGUAGES.map((lang) => (
                            <option key={lang.code} value={lang.code}>
                                {lang.name}
                            </option>
                        ))}
                    </select>
                </div>
            </div>

            {/* Available Only Checkbox */}
            <div className={`mt-4 ${isExpanded ? 'block' : 'hidden lg:block'}`}>
                <label className="flex items-center gap-2 cursor-pointer">
                    <input
                        type="checkbox"
                        checked={filters.availableOnly}
                        onChange={(e) => handleFilterChange('availableOnly', e.target.checked)}
                        className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <span className="text-sm text-gray-700 dark:text-gray-300">
                        {t('marketplace.filters.available')}
                    </span>
                </label>
            </div>
        </div>
    );
}
