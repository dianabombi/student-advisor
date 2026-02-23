'use client';

import { useState, useEffect } from 'react';
import { useLanguage } from '@/lib/LanguageContext';
import { useJurisdiction } from '@/contexts/JurisdictionContext';
import UniversityChatModal from './UniversityChatModal';

interface FoundationProgram {
    id: number;
    name: string;
    name_local: string;
    city: string;
    country: string;
    website_url: string;
    student_count: number;
    programs_count: number;
}

export default function FoundationProgramsGrid() {
    const [programs, setPrograms] = useState<FoundationProgram[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedProgram, setSelectedProgram] = useState<FoundationProgram | null>(null);
    const [isChatModalOpen, setIsChatModalOpen] = useState(false);
    const { language, t } = useLanguage();
    const { jurisdiction } = useJurisdiction();

    useEffect(() => {
        async function fetchPrograms() {
            try {
                const response = await fetch(`/api/universities?jurisdiction_code=${jurisdiction}&type=foundation_program`);
                const data = await response.json();
                setPrograms(data.universities || []);
            } catch (error) {
                console.error('Failed to fetch foundation programs:', error);
            } finally {
                setLoading(false);
            }
        }

        fetchPrograms();
    }, [jurisdiction]);

    const handleChatOpen = (program: FoundationProgram) => {
        setSelectedProgram(program);
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

    if (programs.length === 0) return null;

    const colors = [
        'from-indigo-500 to-indigo-600',
        'from-violet-500 to-violet-600',
        'from-purple-500 to-purple-600',
    ];

    return (
        <>
            <div className="grid-courses">
                {programs.map((program, index) => (
                    <div
                        key={program.id}
                        className="card-course hover:shadow-xl transition-shadow duration-300 relative"
                    >
                        <div
                            className={`h-40 bg-gradient-to-br ${colors[index % colors.length]} flex items-center justify-center cursor-pointer`}
                            onClick={() => window.open(program.website_url, '_blank')}
                        >
                            <div className="text-white text-center p-4">
                                <div className="text-5xl mb-2">📚</div>
                                <h3 className="font-bold text-xl">
                                    {language === 'sk' ? program.name_local : program.name}
                                </h3>
                            </div>
                        </div>
                        <div className="p-4">
                            <p className="text-sm text-gray-600 mb-2">📍 {program.city}, {program.country}</p>
                            <p className="text-gray-700 mb-3 line-clamp-2">
                                {t(`foundationPrograms.${program.id}.description`)}
                            </p>
                            <div className="flex items-center justify-between text-sm mb-3">
                                <span className="text-gray-600">
                                    👥 {program.student_count?.toLocaleString()} {t('common.students')}
                                </span>
                                <span className="text-indigo-600 font-semibold">
                                    {program.programs_count} {t('common.programs')}
                                </span>
                            </div>
                            <button
                                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg font-semibold transition-colors duration-300 flex items-center justify-center gap-2"
                                onClick={(e) => {
                                    e.stopPropagation();
                                    handleChatOpen(program);
                                }}
                            >
                                <span>🤖</span>
                                <span>{t('university.aiConsultant')}</span>
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {selectedProgram && (
                <UniversityChatModal
                    isOpen={isChatModalOpen}
                    onClose={() => setIsChatModalOpen(false)}
                    universityId={selectedProgram.id}
                    universityName={language === 'sk' ? selectedProgram.name_local : selectedProgram.name}
                />
            )}
        </>
    );
}
