'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { useTranslation } from 'react-i18next';
import { Star, MapPin, Briefcase, CheckCircle, Clock } from 'lucide-react';

interface LawyerCardProps {
    lawyer: {
        id: number;
        user_id: number;
        full_name: string;
        title?: string;
        bio?: string;
        specializations: string[];
        jurisdictions: string[];
        languages: string[];
        experience_years: number;
        hourly_rate?: number;
        consultation_fee?: number;
        rating?: number;
        total_reviews?: number;
        is_verified: boolean;
        is_available: boolean;
    };
}

export default function LawyerCard({ lawyer }: LawyerCardProps) {
    const router = useRouter();
    const { t } = useTranslation();

    const handleViewProfile = () => {
        router.push(`/marketplace/lawyers/${lawyer.id}`);
    };

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 p-6 cursor-pointer"
            onClick={handleViewProfile}>
            <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                        <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                            {lawyer.full_name}
                        </h3>
                        {lawyer.is_verified && (
                            <CheckCircle className="w-5 h-5 text-green-500" />
                        )}
                    </div>
                    {lawyer.title && (
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                            {lawyer.title}
                        </p>
                    )}
                </div>
                <div className={`px-3 py-1 rounded-full text-xs font-medium ${lawyer.is_available
                    ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                    : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
                    }`}>
                    {lawyer.is_available ? t('marketplace.lawyerCard.available') : t('marketplace.lawyerCard.unavailable')}
                </div>
            </div>

            {/* Bio */}
            {lawyer.bio && (
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
                    {lawyer.bio}
                </p>
            )}

            {/* Specializations */}
            <div className="mb-4">
                <div className="flex flex-wrap gap-2">
                    {lawyer.specializations.slice(0, 3).map((spec, index) => (
                        <span
                            key={index}
                            className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded-full"
                        >
                            {t(`marketplace.specializations.${spec}`)}
                        </span>
                    ))}
                    {lawyer.specializations.length > 3 && (
                        <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 text-xs rounded-full">
                            +{lawyer.specializations.length - 3}
                        </span>
                    )}
                </div>
            </div>

            {/* Info Row */}
            <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
                <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                    <Briefcase className="w-4 h-4" />
                    <span>{t('marketplace.lawyerCard.experience', { years: lawyer.experience_years })}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                    <MapPin className="w-4 h-4" />
                    <span>{lawyer.jurisdictions.join(', ')}</span>
                </div>
            </div>

            {/* Rating and Reviews */}
            {lawyer.rating && lawyer.total_reviews && lawyer.total_reviews > 0 && (
                <div className="flex items-center gap-2 mb-4">
                    <div className="flex items-center gap-1">
                        <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                        <span className="font-medium text-gray-900 dark:text-white">
                            {lawyer.rating.toFixed(1)}
                        </span>
                    </div>
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                        ({t('marketplace.lawyerCard.reviews', { count: lawyer.total_reviews })})
                    </span>
                </div>
            )}

            {/* Pricing */}
            <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
                <div className="flex gap-4 text-sm">
                    {lawyer.hourly_rate && (
                        <div>
                            <span className="text-gray-600 dark:text-gray-400">{t('marketplace.lawyerProfile.hourlyRate')}: </span>
                            <span className="font-semibold text-gray-900 dark:text-white">
                                {t('marketplace.lawyerCard.hourlyRate', { rate: lawyer.hourly_rate })}
                            </span>
                        </div>
                    )}
                    {lawyer.consultation_fee && (
                        <div>
                            <span className="font-semibold text-gray-900 dark:text-white">
                                {t('marketplace.lawyerCard.consultationFee', { fee: lawyer.consultation_fee })}
                            </span>
                        </div>
                    )}
                </div>
                <button
                    onClick={(e) => {
                        e.stopPropagation();
                        handleViewProfile();
                    }}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors"
                >
                    {t('marketplace.lawyerCard.viewProfile')}
                </button>
            </div>
        </div>
    );
}
