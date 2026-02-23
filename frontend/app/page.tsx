'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowRight, BookOpen, GraduationCap, Users, Globe, Sparkles, Home, Briefcase } from 'lucide-react';
import { useLanguage } from '@/lib/LanguageContext';
import UniversitiesGrid from '@/components/UniversitiesGrid';
import LanguageSchoolsGrid from '@/components/LanguageSchoolsGrid';
import VocationalSchoolsGrid from '@/components/VocationalSchoolsGrid';
import ConservatoriesGrid from '@/components/ConservatoriesGrid';
import FoundationProgramsGrid from '@/components/FoundationProgramsGrid';
import LanguageSwitcher from '@/components/LanguageSwitcher';
import JurisdictionSelector from '@/components/JurisdictionSelector';
import AuthPromptModal from '@/components/AuthPromptModal';
import { useAuth } from '@/contexts/AuthContext';
import { useJurisdiction } from '@/contexts/JurisdictionContext';

export default function LandingPage() {
    const { t, language } = useLanguage();
    const { isAuthenticated, user, isLoading } = useAuth();
    const { jurisdiction } = useJurisdiction();
    const [localUser, setLocalUser] = useState<any>(null);
    const [showAuthModal, setShowAuthModal] = useState(false);

    // Check localStorage directly as fallback
    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        const storedToken = localStorage.getItem('token');

        console.log('🔍 Auth State:', { isAuthenticated, user, isLoading });
        console.log('📦 LocalStorage:', {
            hasToken: !!storedToken,
            hasUser: !!storedUser,
            userFromStorage: storedUser ? JSON.parse(storedUser) : null
        });

        if (storedUser && storedToken) {
            setLocalUser(JSON.parse(storedUser));
        }
    }, [isAuthenticated, user, isLoading]);

    // Use either AuthContext user or localStorage user
    const currentUser = user || localUser;
    const isUserLoggedIn = isAuthenticated || (!!localUser && !!localStorage.getItem('token'));

    // Helper function to handle protected actions
    const handleProtectedAction = (action: () => void) => {
        if (isUserLoggedIn) {
            action();
        } else {
            setShowAuthModal(true);
        }
    };

    // Show loading state
    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-white">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    // Show dashboard for authenticated users - SAME as guest view but with user name
    if (isUserLoggedIn) {
        return (
            <div className="min-h-screen bg-blue-50">
                {/* Navigation */}
                <nav className="bg-white border-b border-gray-200">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                        <div className="flex items-center justify-between">
                            <Link href="/" className="flex items-center space-x-2">
                                <Sparkles className="w-8 h-8 text-blue-600" />
                                <span className="text-2xl font-bold text-blue-600">Student Advisor</span>
                            </Link>
                            <div className="flex items-center space-x-4">
                                <LanguageSwitcher />
                                {/* Show user name instead of register button */}
                                <div className="flex items-center space-x-3">
                                    <span className="text-gray-700 font-medium">👤 {currentUser?.name}</span>
                                    <button
                                        onClick={() => {
                                            localStorage.removeItem('token');
                                            localStorage.removeItem('user');
                                            window.location.href = '/';
                                        }}
                                        className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
                                    >
                                        Logout
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </nav>

                {/* Rest of authenticated content - same as guest but with full access */}
                {/* Hero Section */}
                <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-32">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="text-center">
                            <h1 className="text-5xl font-bold mb-6">
                                {t('student.hero.title')}
                            </h1>
                            <p className="text-xl mb-8 text-blue-100">
                                {t('student.hero.subtitle')}
                            </p>
                            <div className="flex justify-center space-x-4">
                                <Link
                                    href="/chat"
                                    className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors inline-flex items-center"
                                >
                                    {t('student.hero.getStarted')}
                                    <ArrowRight className="ml-2 w-5 h-5" />
                                </Link>
                                <Link
                                    href="/housing"
                                    className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors border-2 border-blue-600"
                                >
                                    {t('student.hero.findHousing')}
                                </Link>
                                <Link
                                    href="/jobs"
                                    className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors border-2 border-blue-600"
                                >
                                    {t('student.hero.studentJobs')}
                                </Link>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Pricing Section */}
                <section className="py-20 bg-gradient-to-b from-blue-50 to-white">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="text-center mb-16">
                            <h2 className="text-4xl font-bold text-gray-900 mb-4">
                                {t('student.pricing.title')}
                            </h2>
                            <p className="text-xl text-gray-600">
                                {t('student.pricing.subtitle')}
                            </p>
                        </div>

                        <div className="grid md:grid-cols-4 gap-8">
                            {/* FREE Plan */}
                            <div className="bg-white rounded-2xl shadow-lg p-8 border-2 border-gray-200 hover:border-blue-300 transition-all hover:shadow-xl">
                                <div className="text-center mb-6">
                                    <h3 className="text-2xl font-bold text-gray-900 mb-2">{t('student.pricing.free.name')}</h3>
                                    <div className="mb-4">
                                        <span className="text-5xl font-bold text-gray-900">€0</span>
                                        <span className="text-gray-500 ml-2">{t('student.pricing.free.period')}</span>
                                    </div>
                                    <p className="text-sm text-gray-600">{t('student.pricing.free.description')}</p>
                                </div>

                                <ul className="space-y-3 mb-8">
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600">{t('student.pricing.free.features.browse')}</span>
                                    </li>
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600">{t('student.pricing.free.features.links')}</span>
                                    </li>
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600">{t('student.pricing.free.features.info')}</span>
                                    </li>
                                    <li className="flex items-start opacity-50">
                                        <svg className="w-5 h-5 text-gray-300 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-400">{t('student.pricing.free.features.noAI')}</span>
                                    </li>
                                </ul>

                                <button
                                    disabled
                                    className="block w-full text-center bg-gray-100 text-gray-400 px-6 py-3 rounded-lg font-semibold cursor-not-allowed"
                                >
                                    {t('student.pricing.free.currentPlan')}
                                </button>
                            </div>

                            {/* BASIC Plan */}
                            <div className="bg-white rounded-2xl shadow-lg p-8 border-2 border-blue-500 hover:border-blue-600 transition-all hover:shadow-2xl relative">
                                <div className="absolute top-0 right-0 bg-blue-500 text-white px-4 py-1 rounded-bl-lg rounded-tr-lg text-sm font-semibold">
                                    {t('student.pricing.basic.badge')}
                                </div>
                                <div className="text-center mb-6">
                                    <h3 className="text-2xl font-bold text-gray-900 mb-2">{t('student.pricing.basic.name')}</h3>
                                    <div className="mb-4">
                                        <span className="text-5xl font-bold text-blue-600">€10</span>
                                        <span className="text-gray-500 ml-2">{t('student.pricing.free.period')}</span>
                                    </div>
                                    <p className="text-sm text-gray-600">{t('student.pricing.basic.description')}</p>
                                </div>

                                <ul className="space-y-3 mb-8">
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600">{t('student.pricing.basic.features.allFree')}</span>
                                    </li>
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600"><strong>{t('student.pricing.basic.features.aiConsultations')}</strong></span>
                                    </li>
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600">{t('student.pricing.basic.features.detailed')}</span>
                                    </li>
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600">{t('student.pricing.basic.features.housing')}</span>
                                    </li>
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600">{t('student.pricing.basic.features.jobs')}</span>
                                    </li>
                                </ul>

                                <Link
                                    href="/subscription"
                                    className="block w-full text-center bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-md"
                                >
                                    Vybrať BASIC
                                </Link>
                            </div>

                            {/* STANDARD Plan */}
                            <div className="bg-white rounded-2xl shadow-lg p-8 border-2 border-purple-500 hover:border-purple-600 transition-all hover:shadow-2xl">
                                <div className="text-center mb-6">
                                    <h3 className="text-2xl font-bold text-gray-900 mb-2">{t('student.pricing.standard.name')}</h3>
                                    <div className="mb-4">
                                        <span className="text-5xl font-bold text-purple-600">€20</span>
                                        <span className="text-gray-500 ml-2">{t('student.pricing.free.period')}</span>
                                    </div>
                                    <p className="text-sm text-gray-600">{t('student.pricing.standard.description')}</p>
                                </div>

                                <ul className="space-y-3 mb-8">
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600">{t('student.pricing.standard.features.allBasic')}</span>
                                    </li>
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600"><strong>{t('student.pricing.standard.features.aiConsultations')}</strong></span>
                                    </li>
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600">{t('student.pricing.standard.features.plans')}</span>
                                    </li>
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600">{t('student.pricing.standard.features.advice')}</span>
                                    </li>
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600">{t('student.pricing.standard.features.templates')}</span>
                                    </li>
                                </ul>

                                <Link
                                    href="/subscription"
                                    className="block w-full text-center bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-purple-700 transition-colors shadow-md"
                                >
                                    Vybrať STANDARD
                                </Link>
                            </div>

                            {/* PREMIUM Plan */}
                            <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-2xl shadow-lg p-8 border-2 border-yellow-400 hover:border-yellow-500 transition-all hover:shadow-2xl relative">
                                <div className="absolute top-0 right-0 bg-gradient-to-r from-yellow-400 to-orange-400 text-white px-4 py-1 rounded-bl-lg rounded-tr-lg text-sm font-semibold">
                                    {t('student.pricing.premium.badge')}
                                </div>
                                <div className="text-center mb-6">
                                    <h3 className="text-2xl font-bold text-gray-900 mb-2">{t('student.pricing.premium.name')}</h3>
                                    <div className="mb-4">
                                        <span className="text-5xl font-bold bg-gradient-to-r from-yellow-600 to-orange-600 bg-clip-text text-transparent">€30</span>
                                        <span className="text-gray-500 ml-2">{t('student.pricing.free.period')}</span>
                                    </div>
                                    <p className="text-sm text-gray-600">{t('student.pricing.premium.description')}</p>
                                </div>

                                <ul className="space-y-3 mb-8">
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600">{t('student.pricing.premium.features.allStandard')}</span>
                                    </li>
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600"><strong>{t('student.pricing.premium.features.aiConsultations')}</strong></span>
                                    </li>
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600">{t('student.pricing.premium.features.expert')}</span>
                                    </li>
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600">{t('student.pricing.premium.features.support')}</span>
                                    </li>
                                    <li className="flex items-start">
                                        <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-600">{t('student.pricing.premium.features.personalPlan')}</span>
                                    </li>
                                </ul>

                                <Link
                                    href="/subscription"
                                    className="block w-full text-center bg-gradient-to-r from-yellow-500 to-orange-500 text-white px-6 py-3 rounded-lg font-semibold hover:from-yellow-600 hover:to-orange-600 transition-all shadow-md"
                                >
                                    Vybrať PREMIUM
                                </Link>
                            </div>
                        </div>

                        {/* Money-back guarantee */}
                        <div className="text-center mt-12">
                            <p className="text-gray-600">
                                {t('student.pricing.guarantee')}
                            </p>
                        </div>
                    </div>
                </section>

                {/* Features Section */}
                <section className="py-16 bg-white">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <h2 className="text-3xl font-bold text-center mb-12">
                            {t('student.features.title')}
                        </h2>

                        <div className="grid md:grid-cols-5 gap-6">
                            <div className="text-center p-6">
                                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <GraduationCap className="w-8 h-8 text-blue-600" />
                                </div>
                                <h3 className="text-xl font-semibold mb-2">
                                    {t('student.features.feature1.title')}
                                </h3>
                                <p className="text-gray-600">
                                    {t('student.features.feature1.description')}
                                </p>
                            </div>

                            <div className="text-center p-6">
                                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <Users className="w-8 h-8 text-blue-600" />
                                </div>
                                <h3 className="text-xl font-semibold mb-2">
                                    {t('student.features.feature2.title')}
                                </h3>
                                <p className="text-gray-600">
                                    {t('student.features.feature2.description')}
                                </p>
                            </div>

                            <div className="text-center p-6">
                                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <Globe className="w-8 h-8 text-blue-600" />
                                </div>
                                <h3 className="text-xl font-semibold mb-2">
                                    {t('student.features.feature3.title')}
                                </h3>
                                <p className="text-gray-600">
                                    {t('student.features.feature3.description')}
                                </p>
                            </div>

                            <div className="text-center p-6">
                                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <Home className="w-8 h-8 text-green-600" />
                                </div>
                                <h3 className="text-xl font-semibold mb-2">
                                    {t('student.features.feature4.title')}
                                </h3>
                                <p className="text-gray-600">
                                    {t('student.features.feature4.description')}
                                </p>
                            </div>

                            <div className="text-center p-6">
                                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <Briefcase className="w-8 h-8 text-purple-600" />
                                </div>
                                <h3 className="text-xl font-semibold mb-2">
                                    {t('student.features.feature5.title')}
                                </h3>
                                <p className="text-gray-600">
                                    {t('student.features.feature5.description')}
                                </p>
                            </div>
                        </div>
                    </div>
                </section>

                <UniversitiesGrid />
                <LanguageSchoolsGrid />
                <VocationalSchoolsGrid />
                <ConservatoriesGrid />
                <FoundationProgramsGrid />

                {/* CTA Section */}
                <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-16">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                        <h2 className="text-3xl font-bold mb-4">
                            {t('student.cta.title')}
                        </h2>
                        <p className="text-xl mb-8 text-blue-100">
                            {t('student.cta.subtitle')}
                        </p>
                        <Link
                            href="/chat"
                            className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors inline-block"
                        >
                            {t('student.cta.button')}
                        </Link>
                    </div>
                </section>

                {/* Footer */}
                <footer className="bg-gray-900 text-white py-12">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="grid md:grid-cols-4 gap-8">
                            <div>
                                <h3 className="text-lg font-semibold mb-4">{t('footer.about')}</h3>
                                <ul className="space-y-2">
                                    <li><Link href="/about" className="text-gray-400 hover:text-white">{t('footer.aboutUs')}</Link></li>
                                    <li><Link href="/contact" className="text-gray-400 hover:text-white">{t('footer.contact')}</Link></li>
                                </ul>
                            </div>
                            <div>
                                <h3 className="text-lg font-semibold mb-4">{t('footer.resources')}</h3>
                                <ul className="space-y-2">
                                    <li><Link href="/universities" className="text-gray-400 hover:text-white">{t('footer.universities')}</Link></li>
                                    <li><Link href="/language-schools" className="text-gray-400 hover:text-white">{t('footer.languageSchools')}</Link></li>
                                    <li><Link href="/vocational-schools" className="text-gray-400 hover:text-white">{t('footer.vocationalSchools')}</Link></li>
                                </ul>
                            </div>
                            <div>
                                <h3 className="text-lg font-semibold mb-4">{t('footer.support')}</h3>
                                <ul className="space-y-2">
                                    <li><Link href="/help" className="text-gray-400 hover:text-white">{t('footer.helpCenter')}</Link></li>
                                    <li><Link href="/faq" className="text-gray-400 hover:text-white">{t('footer.faq')}</Link></li>
                                </ul>
                            </div>
                            <div>
                                <h3 className="text-lg font-semibold mb-4">{t('footer.legal')}</h3>
                                <ul className="space-y-2">
                                    <li><Link href="/privacy" className="text-gray-400 hover:text-white">{t('footer.privacyPolicy')}</Link></li>
                                    <li><Link href="/terms" className="text-gray-400 hover:text-white">{t('footer.termsOfService')}</Link></li>
                                </ul>
                            </div>
                        </div>
                        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
                            <p>{t('footer.copyright')}</p>
                        </div>
                    </div>
                </footer>

                {/* Auth Modal */}
                <AuthPromptModal isOpen={showAuthModal} onClose={() => setShowAuthModal(false)} />
            </div>
        );
    }

    // Guest view - show everything but with auth prompts on protected actions
    return (
        <div className="min-h-screen bg-blue-50">
            {/* Navigation */}
            <nav className="bg-white border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between">
                        <Link href="/" className="flex items-center space-x-2">
                            <Sparkles className="w-8 h-8 text-blue-600" />
                            <span className="text-2xl font-bold text-blue-600">Student Advisor</span>
                        </Link>
                        <div className="flex items-center space-x-4">
                            <LanguageSwitcher />
                            <Link
                                href="/login"
                                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                            >
                                {t('auth.loginButton')}
                            </Link>
                            <Link
                                href="/register"
                                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                            >
                                {t('auth.registerButton')}
                            </Link>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-32">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center">
                        <h1 className="text-5xl font-bold mb-6">
                            {t('student.hero.title')}
                        </h1>
                        <p className="text-xl mb-8 text-blue-100">
                            {t('student.hero.subtitle')}
                        </p>
                        <div className="flex justify-center space-x-4">
                            <button
                                onClick={() => handleProtectedAction(() => window.location.href = '/chat')}
                                className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors inline-flex items-center cursor-pointer"
                            >
                                {t('student.hero.getStarted')}
                                <ArrowRight className="ml-2 w-5 h-5" />
                            </button>
                            <Link
                                href="/housing"
                                className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors cursor-pointer border-2 border-blue-600"
                            >
                                {t('student.hero.findHousing')}
                            </Link>
                            <Link
                                href="/jobs"
                                className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors cursor-pointer border-2 border-blue-600"
                            >
                                {t('student.hero.studentJobs')}
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

            {/* Pricing Section */}
            <section className="py-20 bg-gradient-to-b from-blue-50 to-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-4xl font-bold text-gray-900 mb-4">
                            {t('student.pricing.title')}
                        </h2>
                        <p className="text-xl text-gray-600">
                            {t('student.pricing.subtitle')}
                        </p>
                    </div>

                    <div className="grid md:grid-cols-4 gap-8">
                        {/* FREE Plan */}
                        <div className="bg-white rounded-2xl shadow-lg p-8 border-2 border-gray-200 hover:border-blue-300 transition-all hover:shadow-xl">
                            <div className="text-center mb-6">
                                <h3 className="text-2xl font-bold text-gray-900 mb-2">{t('student.pricing.free.name')}</h3>
                                <div className="mb-4">
                                    <span className="text-5xl font-bold text-gray-900">€0</span>
                                    <span className="text-gray-500 ml-2">{t('student.pricing.free.period')}</span>
                                </div>
                                <p className="text-sm text-gray-600">{t('student.pricing.free.description')}</p>
                            </div>

                            <ul className="space-y-3 mb-8">
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{t('student.pricing.free.features.browse')}</span>
                                </li>
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{t('student.pricing.free.features.links')}</span>
                                </li>
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{t('student.pricing.free.features.info')}</span>
                                </li>
                                <li className="flex items-start opacity-50">
                                    <svg className="w-5 h-5 text-gray-300 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-400">{t('student.pricing.free.features.noAI')}</span>
                                </li>
                            </ul>

                            <Link
                                href="/register"
                                className="block w-full text-center bg-gray-100 text-gray-700 px-6 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
                            >
                                Začať zadarmo
                            </Link>
                        </div>

                        {/* BASIC Plan */}
                        <div className="bg-white rounded-2xl shadow-lg p-8 border-2 border-blue-500 hover:border-blue-600 transition-all hover:shadow-2xl relative">
                            <div className="absolute top-0 right-0 bg-blue-500 text-white px-4 py-1 rounded-bl-lg rounded-tr-lg text-sm font-semibold">
                                {t('student.pricing.basic.badge')}
                            </div>
                            <div className="text-center mb-6">
                                <h3 className="text-2xl font-bold text-gray-900 mb-2">{t('student.pricing.basic.name')}</h3>
                                <div className="mb-4">
                                    <span className="text-5xl font-bold text-blue-600">€10</span>
                                    <span className="text-gray-500 ml-2">{t('student.pricing.free.period')}</span>
                                </div>
                                <p className="text-sm text-gray-600">{t('student.pricing.basic.description')}</p>
                            </div>

                            <ul className="space-y-3 mb-8">
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{t('student.pricing.basic.features.allFree')}</span>
                                </li>
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600"><strong>{t('student.pricing.basic.features.aiConsultations')}</strong></span>
                                </li>
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{t('student.pricing.basic.features.detailed')}</span>
                                </li>
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{t('student.pricing.basic.features.housing')}</span>
                                </li>
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{t('student.pricing.basic.features.jobs')}</span>
                                </li>
                            </ul>

                            <Link
                                href="/register"
                                className="block w-full text-center bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-md"
                            >
                                Vybrať BASIC
                            </Link>
                        </div>

                        {/* STANDARD Plan */}
                        <div className="bg-white rounded-2xl shadow-lg p-8 border-2 border-purple-500 hover:border-purple-600 transition-all hover:shadow-2xl">
                            <div className="text-center mb-6">
                                <h3 className="text-2xl font-bold text-gray-900 mb-2">{t('student.pricing.standard.name')}</h3>
                                <div className="mb-4">
                                    <span className="text-5xl font-bold text-purple-600">€20</span>
                                    <span className="text-gray-500 ml-2">{t('student.pricing.free.period')}</span>
                                </div>
                                <p className="text-sm text-gray-600">{t('student.pricing.standard.description')}</p>
                            </div>

                            <ul className="space-y-3 mb-8">
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{t('student.pricing.standard.features.allBasic')}</span>
                                </li>
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600"><strong>{t('student.pricing.standard.features.aiConsultations')}</strong></span>
                                </li>
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{t('student.pricing.standard.features.plans')}</span>
                                </li>
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{t('student.pricing.standard.features.advice')}</span>
                                </li>
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{t('student.pricing.standard.features.templates')}</span>
                                </li>
                            </ul>

                            <Link
                                href="/register"
                                className="block w-full text-center bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-purple-700 transition-colors shadow-md"
                            >
                                Vybrať STANDARD
                            </Link>
                        </div>

                        {/* PREMIUM Plan */}
                        <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-2xl shadow-lg p-8 border-2 border-yellow-400 hover:border-yellow-500 transition-all hover:shadow-2xl relative">
                            <div className="absolute top-0 right-0 bg-gradient-to-r from-yellow-400 to-orange-400 text-white px-4 py-1 rounded-bl-lg rounded-tr-lg text-sm font-semibold">
                                {t('student.pricing.premium.badge')}
                            </div>
                            <div className="text-center mb-6">
                                <h3 className="text-2xl font-bold text-gray-900 mb-2">{t('student.pricing.premium.name')}</h3>
                                <div className="mb-4">
                                    <span className="text-5xl font-bold bg-gradient-to-r from-yellow-600 to-orange-600 bg-clip-text text-transparent">€30</span>
                                    <span className="text-gray-500 ml-2">{t('student.pricing.free.period')}</span>
                                </div>
                                <p className="text-sm text-gray-600">{t('student.pricing.premium.description')}</p>
                            </div>

                            <ul className="space-y-3 mb-8">
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{t('student.pricing.premium.features.allStandard')}</span>
                                </li>
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600"><strong>{t('student.pricing.premium.features.aiConsultations')}</strong></span>
                                </li>
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{t('student.pricing.premium.features.expert')}</span>
                                </li>
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{t('student.pricing.premium.features.support')}</span>
                                </li>
                                <li className="flex items-start">
                                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{t('student.pricing.premium.features.personalPlan')}</span>
                                </li>
                            </ul>

                            <Link
                                href="/register"
                                className="block w-full text-center bg-gradient-to-r from-yellow-500 to-orange-500 text-white px-6 py-3 rounded-lg font-semibold hover:from-yellow-600 hover:to-orange-600 transition-all shadow-md"
                            >
                                Vybrať PREMIUM
                            </Link>
                        </div>
                    </div>

                    {/* Money-back guarantee */}
                    <div className="text-center mt-12">
                        <p className="text-gray-600">
                            {t('student.pricing.guarantee')}
                        </p>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-16 bg-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <h2 className="text-3xl font-bold text-center mb-12">
                        {t('student.features.title')}
                    </h2>

                    <div className="grid md:grid-cols-3 gap-8">
                        <div className="text-center p-6">
                            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                <GraduationCap className="w-8 h-8 text-blue-600" />
                            </div>
                            <h3 className="text-xl font-semibold mb-2">
                                {t('student.features.feature1.title')}
                            </h3>
                            <p className="text-gray-600">
                                {t('student.features.feature1.description')}
                            </p>
                        </div>

                        <div className="text-center p-6">
                            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                <Users className="w-8 h-8 text-blue-600" />
                            </div>
                            <h3 className="text-xl font-semibold mb-2">
                                {t('student.features.feature2.title')}
                            </h3>
                            <p className="text-gray-600">
                                {t('student.features.feature2.description')}
                            </p>
                        </div>

                        <div className="text-center p-6">
                            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                <Globe className="w-8 h-8 text-blue-600" />
                            </div>
                            <h3 className="text-xl font-semibold mb-2">
                                {t('student.features.feature3.title')}
                            </h3>
                            <p className="text-gray-600">
                                {t('student.features.feature3.description')}
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            <UniversitiesGrid />
            <LanguageSchoolsGrid />
            <VocationalSchoolsGrid />
            <ConservatoriesGrid />
            <FoundationProgramsGrid />

            {/* CTA Section */}
            <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h2 className="text-3xl font-bold mb-4">
                        {t('student.cta.title')}
                    </h2>
                    <p className="text-xl mb-8 text-blue-100">
                        {t('student.cta.subtitle')}
                    </p>
                    <button
                        onClick={() => handleProtectedAction(() => window.location.href = '/register')}
                        className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors inline-block cursor-pointer"
                    >
                        {t('student.cta.button')}
                    </button>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-gray-900 text-white py-12">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid md:grid-cols-4 gap-8">
                        <div>
                            <h3 className="text-lg font-semibold mb-4">{t('footer.about')}</h3>
                            <ul className="space-y-2">
                                <li><Link href="/about" className="text-gray-400 hover:text-white">{t('footer.aboutUs')}</Link></li>
                                <li><Link href="/contact" className="text-gray-400 hover:text-white">{t('footer.contact')}</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h3 className="text-lg font-semibold mb-4">{t('footer.resources')}</h3>
                            <ul className="space-y-2">
                                <li><Link href="/universities" className="text-gray-400 hover:text-white">{t('footer.universities')}</Link></li>
                                <li><Link href="/language-schools" className="text-gray-400 hover:text-white">{t('footer.languageSchools')}</Link></li>
                                <li><Link href="/vocational-schools" className="text-gray-400 hover:text-white">{t('footer.vocationalSchools')}</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h3 className="text-lg font-semibold mb-4">{t('footer.support')}</h3>
                            <ul className="space-y-2">
                                <li><Link href="/help" className="text-gray-400 hover:text-white">{t('footer.helpCenter')}</Link></li>
                                <li><Link href="/faq" className="text-gray-400 hover:text-white">{t('footer.faq')}</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h3 className="text-lg font-semibold mb-4">{t('footer.legal')}</h3>
                            <ul className="space-y-2">
                                <li><Link href="/privacy" className="text-gray-400 hover:text-white">{t('footer.privacyPolicy')}</Link></li>
                                <li><Link href="/terms" className="text-gray-400 hover:text-white">{t('footer.termsOfService')}</Link></li>
                            </ul>
                        </div>
                    </div>
                    <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
                        <p>{t('footer.copyright')}</p>
                    </div>
                </div>
            </footer>

            {/* Auth Modal */}
            <AuthPromptModal isOpen={showAuthModal} onClose={() => setShowAuthModal(false)} />
        </div>
    );
}
