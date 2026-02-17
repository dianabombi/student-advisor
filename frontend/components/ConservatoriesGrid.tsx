'use client';

import { useState, useEffect } from 'react';
import { useLanguage } from '@/lib/LanguageContext';
import { useJurisdiction } from '@/contexts/JurisdictionContext';
import UniversityChatModal from './UniversityChatModal';

interface Conservatory {
    id: number;
    name: string;
    name_local: string;
    city: string;
    country: string;
    website_url: string;
    student_count: number;
    programs_count: number;
}

export default function ConservatoriesGrid() {
    const [conservatories, setConservatories] = useState<Conservatory[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedConservatory, setSelectedConservatory] = useState<Conservatory | null>(null);
    const [isChatModalOpen, setIsChatModalOpen] = useState(false);
    const { language, t } = useLanguage();
    const { jurisdiction } = useJurisdiction();

    useEffect(() => {
        async function fetchConservatories() {
            try {
                const response = await fetch(`/api/universities?jurisdiction_code=${jurisdiction}&type=conservatory`);
                const data = await response.json();
                setConservatories(data.universities || []);
            } catch (error) {
                console.error('Failed to fetch conservatories:', error);
            } finally {
                setLoading(false);
            }
        }

        fetchConservatories();
    }, [jurisdiction]);

    const handleChatOpen = (conservatory: Conservatory) => {
        setSelectedConservatory(conservatory);
        setIsChatModalOpen(true);
    };

    if (loading) {
        return (
            <div className="grid-courses">
                {[1, 2].map((i) => (
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
        'from-pink-500 to-pink-600',
        'from-rose-500 to-rose-600',
    ];

    return (
        <>
            <div className="grid-courses">
                {conservatories.map((conservatory, index) => (
                    <div
                        key={conservatory.id}
                        className="card-course hover:shadow-xl transition-shadow duration-300 relative"
                    >
                        <div
                            className={`h-40 bg-gradient-to-br ${colors[index % colors.length]} flex items-center justify-center cursor-pointer`}
                            onClick={() => window.open(conservatory.website_url, '_blank')}
                        >
                            <div className="text-white text-center p-4">
                                <div className="text-5xl mb-2">🎨</div>
                                <h3 className="font-bold text-xl">
                                    {language === 'sk' ? conservatory.name_local : conservatory.name}
                                </h3>
                            </div>
                        </div>
                        <div className="p-4">
                            <p className="text-sm text-gray-600 mb-2">📍 {conservatory.city}, {conservatory.country}</p>
                            <p className="text-gray-700 mb-3 line-clamp-2">
                                {t(`conservatories.${conservatory.id}.description`)}
                            </p>
                            <div className="flex items-center justify-between text-sm mb-3">
                                <span className="text-gray-600">
                                    👥 {conservatory.student_count?.toLocaleString()} {t('common.students')}
                                </span>
                                <span className="text-pink-600 font-semibold">
                                    {conservatory.programs_count} {t('common.programs')}
                                </span>
                            </div>
                            <button
                                className="w-full bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg font-semibold transition-colors duration-300 flex items-center justify-center gap-2"
                                onClick={(e) => {
                                    e.stopPropagation();
                                    handleChatOpen(conservatory);
                                }}
                            >
                                <span>🤖</span>
                                <span>{t('university.aiConsultant')}</span>
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {selectedConservatory && (
                <UniversityChatModal
                    isOpen={isChatModalOpen}
                    onClose={() => setIsChatModalOpen(false)}
                    universityId={selectedConservatory.id}
                    universityName={language === 'sk' ? selectedConservatory.name_local : selectedConservatory.name}
                />
            )}
        </>
    );
}
