'use client';

import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useRouter } from 'next/navigation';
import { Search, Loader2, ArrowLeft } from 'lucide-react';
import Navigation from '@/components/Navigation';
import LawyerCard from '@/components/marketplace/LawyerCard';
import LawyerSearchFilters from '@/components/marketplace/LawyerSearchFilters';
import { searchLawyers } from '@/lib/marketplaceService';
import '@/lib/i18n'; // Initialize i18next

interface FilterState {
    jurisdiction: string;
    specialization: string;
    minRating: number;
    language: string;
    availableOnly: boolean;
}

export default function MarketplaceSearchPage() {
    const { t } = useTranslation('common');
    const router = useRouter();
    const [searchQuery, setSearchQuery] = useState('');
    const [filters, setFilters] = useState<FilterState>({
        jurisdiction: '',
        specialization: '',
        minRating: 0,
        language: '',
        availableOnly: false
    });
    const [lawyers, setLawyers] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Fetch lawyers on mount and when filters change
    useEffect(() => {
        fetchLawyers();
    }, [filters]);

    const fetchLawyers = async () => {
        setLoading(true);
        setError(null);

        try {
            const params: any = {};

            if (filters.jurisdiction) params.jurisdiction = filters.jurisdiction;
            if (filters.specialization) params.specialization = filters.specialization;
            if (filters.minRating > 0) params.min_rating = filters.minRating;
            if (filters.language) params.language = filters.language;
            if (filters.availableOnly) params.available_only = true;
            if (searchQuery) params.search = searchQuery;

            const data = await searchLawyers(params);
            setLawyers(data);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch lawyers');
            console.error('Error fetching lawyers:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        fetchLawyers();
    };

    const handleFilterChange = (newFilters: FilterState) => {
        setFilters(newFilters);
    };

    const handleClearFilters = () => {
        setFilters({
            jurisdiction: '',
            specialization: '',
            minRating: 0,
            language: '',
            availableOnly: false
        });
        setSearchQuery('');
    };

    return (
        <>
            <Navigation />
            <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    {/* Back Button */}
                    <button
                        onClick={() => router.push('/dashboard')}
                        className="mb-6 flex items-center gap-3 px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-bold text-lg rounded-xl hover:shadow-lg hover:shadow-green-500/50 transform hover:scale-105 transition-all duration-200"
                    >
                        <ArrowLeft className="w-8 h-8" />
                        <span>{t('common.backToDashboard')}</span>
                    </button>

                    {/* Header */}
                    <div className="mb-8">
                        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-4">
                            <div>
                                <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                                    {t('marketplace.title')}
                                </h1>
                                <p className="text-gray-600 dark:text-gray-400">
                                    {t('marketplace.findLawyer')}
                                </p>
                            </div>
                            <button
                                onClick={() => router.push('/marketplace/register')}
                                className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-blue-500/50 transform hover:scale-105 transition-all duration-200 whitespace-nowrap"
                            >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                                </svg>
                                <span>{t('marketplace.registerAsLawyer')}</span>
                            </button>
                        </div>
                    </div>

                    {/* Search Bar */}
                    <form onSubmit={handleSearch} className="mb-6">
                        <div className="relative">
                            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                            <input
                                type="text"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                placeholder={t('marketplace.searchLawyers')}
                                className="w-full pl-12 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                            <button
                                type="submit"
                                className="absolute right-2 top-1/2 transform -translate-y-1/2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                            >
                                {t('marketplace.filters.apply')}
                            </button>
                        </div>
                    </form>

                    {/* Filters */}
                    <LawyerSearchFilters
                        filters={filters}
                        onFilterChange={handleFilterChange}
                        onClear={handleClearFilters}
                    />

                    {/* Results */}
                    <div className="mt-6">
                        {loading ? (
                            <div className="flex items-center justify-center py-12">
                                <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
                            </div>
                        ) : error ? (
                            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 text-red-800 dark:text-red-200">
                                {error}
                            </div>
                        ) : lawyers.length === 0 ? (
                            <div className="text-center py-12">
                                <p className="text-gray-600 dark:text-gray-400 text-lg">
                                    {t('marketplace.noLawyers')}
                                </p>
                            </div>
                        ) : (
                            <>
                                <div className="mb-4 text-sm text-gray-600 dark:text-gray-400">
                                    {lawyers.length === 1
                                        ? t('marketplace.lawyerFound', { count: lawyers.length })
                                        : lawyers.length >= 2 && lawyers.length <= 4
                                            ? t('marketplace.lawyersFew', { count: lawyers.length })
                                            : t('marketplace.lawyersFound', { count: lawyers.length })
                                    }
                                </div>
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {lawyers.map((lawyer) => (
                                        <LawyerCard key={lawyer.id} lawyer={lawyer} />
                                    ))}
                                </div>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </>
    );
}
