import { useState, useEffect } from 'react';
import { useLanguage } from '@/lib/LanguageContext';
import { useJurisdiction } from '@/contexts/JurisdictionContext';
import UniversityChatModal from './UniversityChatModal';

interface University {
    id: number;
    name: string;
    name_local: string;
    city: string;
    country: string;
    description: string;
    student_count: number;
    programs_count: number;
}

export default function UniversitiesGrid() {
    const [universities, setUniversities] = useState<University[]>([]);
    const [loading, setLoading] = useState(true);
    const { language, t } = useLanguage();
    const { jurisdiction } = useJurisdiction();
    const [selectedUniversity, setSelectedUniversity] = useState<University | null>(null);
    const [isChatModalOpen, setIsChatModalOpen] = useState(false);

    useEffect(() => {
        async function fetchUniversities() {
            try {
                const response = await fetch(`/api/universities?jurisdiction_code=${jurisdiction}&type=university`);
                const data = await response.json();
                setUniversities(data.universities || []);
            } catch (error) {
                console.error('Failed to fetch universities:', error);
            } finally {
                setLoading(false);
            }
        }

        fetchUniversities();
    }, [jurisdiction]);

    if (loading) {
        return (
            <div className="grid-courses">
                {[1, 2, 3, 4, 5].map((i) => (
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
        'from-blue-500 to-blue-600',
        'from-green-500 to-green-600',
        'from-purple-500 to-purple-600',
        'from-orange-500 to-orange-600',
        'from-red-500 to-red-600',
    ];

    return (
        <div className="grid-courses">
            {universities.map((university, index) => (
                <div
                    key={university.id}
                    className="card-course hover:shadow-xl transition-shadow duration-300 relative"
                >
                    <div
                        className={`h-40 bg-gradient-to-br ${colors[index % colors.length]} flex items-center justify-center cursor-pointer`}
                        onClick={() => window.open(university.website_url, '_blank')}
                    >
                        <div className="text-white text-center p-4">
                            <h3 className="font-bold text-xl mb-2">
                                {language === 'sk' ? university.name_local : university.name}
                            </h3>
                        </div>
                    </div>
                    <div className="p-4">
                        <p className="text-sm text-gray-600 mb-2">📍 {university.city}, {university.country}</p>
                        <p className="text-gray-700 mb-3 line-clamp-2">
                            {t(`universities.${university.id}.description`)}
                        </p>
                        <div className="flex items-center justify-between text-sm mb-3">
                            <span className="text-gray-600">
                                👥 {university.student_count?.toLocaleString()} {t('common.students')}
                            </span>
                            <span className="text-blue-600 font-semibold">
                                {university.programs_count} {t('common.programs')}
                            </span>
                        </div>
                        <button
                            className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-semibold transition-colors duration-300 flex items-center justify-center gap-2"
                            onClick={(e) => {
                                e.stopPropagation();

                                // Save university context for housing/jobs modules
                                localStorage.setItem('lastViewedUniversity', JSON.stringify({
                                    id: university.id,
                                    name: language === 'sk' ? university.name_local : university.name,
                                    city: university.city,
                                    country: university.country
                                }));

                                setSelectedUniversity(university);
                                setIsChatModalOpen(true);
                            }}
                        >
                            <span>🤖</span>
                            <span>{t('university.aiConsultant')}</span>
                        </button>
                    </div>
                </div>
            ))}

            {/* Chat Modal */}
            {selectedUniversity && (
                <UniversityChatModal
                    isOpen={isChatModalOpen}
                    onClose={() => {
                        setIsChatModalOpen(false);
                        setSelectedUniversity(null);
                    }}
                    universityId={selectedUniversity.id}
                    universityName={language === 'sk' ? selectedUniversity.name_local : selectedUniversity.name}
                />
            )}
        </div>
    );
}
