'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useTranslation } from 'react-i18next';
import {
    Star, MapPin, Briefcase, Languages, GraduationCap,
    CheckCircle, Shield, Clock, Euro, ArrowLeft
} from 'lucide-react';
import '@/lib/i18n'; // Initialize i18next
import Navigation from '@/components/Navigation';
import ReviewCard from '@/components/marketplace/ReviewCard';
import { getLawyerProfile } from '@/lib/marketplaceService';

export default function LawyerProfilePage() {
    const params = useParams();
    const router = useRouter();
    const { t } = useTranslation('common');
    const [lawyer, setLawyer] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState<'about' | 'reviews'>('about');

    useEffect(() => {
        if (params.id) {
            fetchLawyerProfile();
        }
    }, [params.id]);

    const fetchLawyerProfile = async () => {
        try {
            const data = await getLawyerProfile(Number(params.id));
            setLawyer(data);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch lawyer profile');
        } finally {
            setLoading(false);
        }
    };

    const handleBookConsultation = () => {
        router.push(`/marketplace/lawyers/${params.id}/book`);
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
                <div className="text-gray-600 dark:text-gray-400">Loading...</div>
            </div>
        );
    }

    if (error || !lawyer) {
        return (
            <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
                <div className="text-red-600 dark:text-red-400">{error || 'Lawyer not found'}</div>
            </div>
        );
    }

    return (
        <>
            <Navigation />
            <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    {/* Back Button */}
                    <button
                        onClick={() => router.back()}
                        className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white mb-6"
                    >
                        <ArrowLeft className="w-5 h-5" />
                        {t('common.back')}
                    </button>

                    {/* Header Card */}
                    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8 mb-6">
                        <div className="flex flex-col md:flex-row gap-6">
                            {/* Avatar */}
                            <div className="flex-shrink-0">
                                <div className="w-32 h-32 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-4xl font-bold">
                                    {lawyer.full_name.charAt(0).toUpperCase()}
                                </div>
                            </div>

                            {/* Info */}
                            <div className="flex-1">
                                <div className="flex items-center gap-3 mb-2">
                                    <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                                        {lawyer.full_name}
                                    </h1>
                                    {lawyer.is_verified && (
                                        <CheckCircle className="w-6 h-6 text-green-500" />
                                    )}
                                </div>

                                {lawyer.title && (
                                    <p className="text-lg text-gray-600 dark:text-gray-400 mb-4">
                                        {lawyer.title}
                                    </p>
                                )}

                                {/* Stats */}
                                <div className="flex flex-wrap gap-6 mb-4">
                                    <div className="flex items-center gap-2">
                                        <Briefcase className="w-5 h-5 text-gray-500" />
                                        <span className="text-gray-700 dark:text-gray-300">
                                            {t('marketplace.lawyerProfile.yearsExperience', { years: lawyer.experience_years })}
                                        </span>
                                    </div>
                                    {lawyer.rating && lawyer.total_reviews > 0 && (
                                        <div className="flex items-center gap-2">
                                            <Star className="w-5 h-5 fill-yellow-400 text-yellow-400" />
                                            <span className="font-medium text-gray-900 dark:text-white">
                                                {lawyer.rating.toFixed(1)}
                                            </span>
                                            <span className="text-gray-600 dark:text-gray-400">
                                                ({lawyer.total_reviews} {t('marketplace.lawyerProfile.reviews')})
                                            </span>
                                        </div>
                                    )}
                                </div>

                                {/* Specializations */}
                                <div className="flex flex-wrap gap-2 mb-4">
                                    {lawyer.specializations.map((spec: string, index: number) => (
                                        <span
                                            key={index}
                                            className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-sm rounded-full"
                                        >
                                            {t(`marketplace.specializations.${spec}`)}
                                        </span>
                                    ))}
                                </div>

                                {/* Pricing */}
                                <div className="flex flex-wrap gap-6 mb-6">
                                    {lawyer.hourly_rate && (
                                        <div>
                                            <span className="text-sm text-gray-600 dark:text-gray-400">
                                                {t('marketplace.lawyerProfile.hourlyRate')}:{' '}
                                            </span>
                                            <span className="text-lg font-bold text-gray-900 dark:text-white">
                                                €{lawyer.hourly_rate}/hr
                                            </span>
                                        </div>
                                    )}
                                    {lawyer.consultation_fee && (
                                        <div>
                                            <span className="text-sm text-gray-600 dark:text-gray-400">
                                                {t('marketplace.lawyerProfile.consultationFee')}:{' '}
                                            </span>
                                            <span className="text-lg font-bold text-gray-900 dark:text-white">
                                                €{lawyer.consultation_fee}
                                            </span>
                                        </div>
                                    )}
                                </div>

                                {/* Book Button */}
                                {lawyer.is_available && (
                                    <button
                                        onClick={handleBookConsultation}
                                        className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
                                    >
                                        {t('marketplace.lawyerProfile.orderConsultation')}
                                    </button>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Tabs */}
                    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md mb-6">
                        <div className="border-b border-gray-200 dark:border-gray-700">
                            <nav className="flex -mb-px">
                                <button
                                    onClick={() => setActiveTab('about')}
                                    className={`px-6 py-4 text-sm font-medium border-b-2 transition ${activeTab === 'about'
                                        ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                                        : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                                        }`}
                                >
                                    {t('marketplace.lawyerProfile.about')}
                                </button>
                                <button
                                    onClick={() => setActiveTab('reviews')}
                                    className={`px-6 py-4 text-sm font-medium border-b-2 transition ${activeTab === 'reviews'
                                        ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                                        : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                                        }`}
                                >
                                    {t('marketplace.lawyerProfile.reviews')} ({lawyer.total_reviews || 0})
                                </button>
                            </nav>
                        </div>

                        <div className="p-6">
                            {activeTab === 'about' ? (
                                <div className="space-y-6">
                                    {/* Bio */}
                                    {lawyer.bio && (
                                        <div>
                                            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                                                {t('marketplace.lawyerProfile.about')}
                                            </h3>
                                            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                                                {lawyer.bio}
                                            </p>
                                        </div>
                                    )}

                                    {/* Education */}
                                    {lawyer.education && (
                                        <div>
                                            <div className="flex items-center gap-2 mb-2">
                                                <GraduationCap className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                                                    {t('marketplace.lawyerProfile.education')}
                                                </h3>
                                            </div>
                                            <p className="text-gray-700 dark:text-gray-300">
                                                {lawyer.education}
                                            </p>
                                        </div>
                                    )}

                                    {/* Jurisdictions */}
                                    <div>
                                        <div className="flex items-center gap-2 mb-2">
                                            <MapPin className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                                            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                                                {t('marketplace.lawyerProfile.jurisdictions')}
                                            </h3>
                                        </div>
                                        <div className="flex flex-wrap gap-2">
                                            {lawyer.jurisdictions.map((jur: string, index: number) => (
                                                <span
                                                    key={index}
                                                    className="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-full"
                                                >
                                                    {jur}
                                                </span>
                                            ))}
                                        </div>
                                    </div>

                                    {/* Languages */}
                                    <div>
                                        <div className="flex items-center gap-2 mb-2">
                                            <Languages className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                                            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                                                {t('marketplace.lawyerProfile.languages')}
                                            </h3>
                                        </div>
                                        <div className="flex flex-wrap gap-2">
                                            {lawyer.languages.map((lang: string, index: number) => (
                                                <span
                                                    key={index}
                                                    className="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-full"
                                                >
                                                    {lang.toUpperCase()}
                                                </span>
                                            ))}
                                        </div>
                                    </div>

                                    {/* License Info */}
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                                        <div>
                                            <span className="text-sm text-gray-600 dark:text-gray-400">
                                                {t('marketplace.lawyerProfile.licenseNumber')}:
                                            </span>
                                            <p className="font-medium text-gray-900 dark:text-white">
                                                {lawyer.license_number}
                                            </p>
                                        </div>
                                        <div>
                                            <span className="text-sm text-gray-600 dark:text-gray-400">
                                                {t('marketplace.lawyerProfile.barAssociation')}:
                                            </span>
                                            <p className="font-medium text-gray-900 dark:text-white">
                                                {lawyer.bar_association}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    {lawyer.reviews && lawyer.reviews.length > 0 ? (
                                        lawyer.reviews.map((review: any) => (
                                            <ReviewCard key={review.id} review={review} />
                                        ))
                                    ) : (
                                        <p className="text-center text-gray-600 dark:text-gray-400 py-8">
                                            {t('marketplace.lawyerProfile.noReviews')}
                                        </p>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}
