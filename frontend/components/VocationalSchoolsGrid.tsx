'use client';

import { useState, useEffect } from 'react';
import { useLanguage } from '@/lib/LanguageContext';
import { useJurisdiction } from '@/contexts/JurisdictionContext';
import UniversityChatModal from './UniversityChatModal';

interface VocationalSchool {
    id: number;
    name: string;
    name_local: string;
    city: string;
    country: string;
    website_url: string;
    student_count: number;
    programs_count: number;
}

export default function VocationalSchoolsGrid() {
    const [schools, setSchools] = useState<VocationalSchool[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedSchool, setSelectedSchool] = useState<VocationalSchool | null>(null);
    const [isChatModalOpen, setIsChatModalOpen] = useState(false);
    const { language, t } = useLanguage();
    const { jurisdiction } = useJurisdiction();

    useEffect(() => {
        async function fetchSchools() {
            try {
                const response = await fetch(`/api/universities?jurisdiction_code=${jurisdiction}&type=vocational_school`);
                const data = await response.json();
                setSchools(data.universities || []);
            } catch (error) {
                console.error('Failed to fetch vocational schools:', error);
            } finally {
                setLoading(false);
            }
        }

        fetchSchools();
    }, [jurisdiction]);

    const handleChatOpen = (school: VocationalSchool) => {
        setSelectedSchool(school);
        setIsChatModalOpen(true);
    };

    if (loading) {
        return (
            <div className="grid-courses">
                {[1, 2, 3].map((i) => (
                    <div key={i} className="card-course animate-pulse">
                        <div className="h-40 bg-gray-200"></div>
                        <div className="p-4">
                            <div className="h-4 bg-gray-200 rounded mb-2"></div>
                            <div className="h-6 bg-gray-200 rounded mb-2"></div>
                            <div className="h-4 bg-gray-200 rounded w-2/3"></div>
                        </div>
                    </div>
                ))}
            </div>
        );
    }

    const colors = [
        'from-amber-500 to-amber-600',
        'from-yellow-500 to-yellow-600',
        'from-orange-500 to-orange-600',
    ];

    return (
        <>
            <div className="grid-courses">
                {schools.map((school, index) => (
                    <div
                        key={school.id}
                        className="card-course hover:shadow-xl transition-shadow duration-300 relative"
                    >
                        <div
                            className={`h-40 bg-gradient-to-br ${colors[index % colors.length]} flex items-center justify-center cursor-pointer`}
                            onClick={() => window.open(school.website_url, '_blank')}
                        >
                            <div className="text-white text-center p-4">
                                <div className="text-5xl mb-2">🏫</div>
                                <h3 className="font-bold text-xl">
                                    {language === 'sk' ? school.name_local : school.name}
                                </h3>
                            </div>
                        </div>
                        <div className="p-4">
                            <p className="text-sm text-gray-600 mb-2">📍 {school.city}, {school.country}</p>
                            <p className="text-gray-700 mb-3 line-clamp-2">
                                {t(`vocationalSchools.${school.id}.description`)}
                            </p>
                            <div className="flex items-center justify-between text-sm mb-3">
                                <span className="text-gray-600">
                                    👥 {school.student_count?.toLocaleString()} {t('common.students')}
                                </span>
                                <span className="text-amber-600 font-semibold">
                                    {school.programs_count} {t('common.programs')}
                                </span>
                            </div>
                            <button
                                className="w-full bg-amber-600 hover:bg-amber-700 text-white px-4 py-2 rounded-lg font-semibold transition-colors duration-300 flex items-center justify-center gap-2"
                                onClick={(e) => {
                                    e.stopPropagation();
                                    handleChatOpen(school);
                                }}
                            >
                                <span>🤖</span>
                                <span>{t('university.aiConsultant')}</span>
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {selectedSchool && (
                <UniversityChatModal
                    isOpen={isChatModalOpen}
                    onClose={() => setIsChatModalOpen(false)}
                    universityId={selectedSchool.id}
                    universityName={language === 'sk' ? selectedSchool.name_local : selectedSchool.name}
                />
            )}
        </>
    );
}
