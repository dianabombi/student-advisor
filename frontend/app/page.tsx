'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowRight, BookOpen, GraduationCap, Users, Globe, Sparkles, Home, Briefcase, Menu, X } from 'lucide-react';
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
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

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
            <div className="min-h-screen pt-3 glass-bg" style={{ background: 'linear-gradient(135deg, #e0f2fe 0%, #f0f4ff 30%, #faf5ff 60%, #e0f2fe 100%)' }}>
                {/* Navigation */}
                <nav className="glass-strong sticky top-0 z-50 shadow-lg shadow-black/5 mx-3 sm:mx-5 lg:mx-8 rounded-2xl">
                    <div className="w-full px-4 sm:px-6 lg:px-8 py-3 relative z-10">
                        <div className="flex items-center justify-between">
                            <Link href="/" className="flex items-center space-x-2">
                                <Sparkles className="w-8 h-8 text-blue-600" />
                                <span className="text-2xl font-bold text-blue-600">Student Advisor</span>
                            </Link>
                            {/* Desktop menu */}
                            <div className="hidden md:flex items-center space-x-3">
                                <LanguageSwitcher />
                                <div className="flex items-center space-x-3">
                                    <span className="text-gray-700 font-medium">👤 {currentUser?.name}</span>
                                    <button
                                        onClick={() => {
                                            localStorage.removeItem('token');
                                            localStorage.removeItem('user');
                                            window.location.href = '/';
                                        }}
                                        className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 rounded-xl bg-gray-200/60 hover:bg-gray-200 transition-colors"
                                    >
                                        Logout
                                    </button>
                                </div>
                            </div>
                            {/* Mobile hamburger */}
                            <button
                                className="md:hidden p-2 rounded-xl hover:bg-gray-100 transition-colors"
                                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                            >
                                {mobileMenuOpen ? <X className="w-6 h-6 text-gray-700" /> : <Menu className="w-6 h-6 text-gray-700" />}
                            </button>
                        </div>
                        {/* Mobile dropdown */}
                        {mobileMenuOpen && (
                            <div className="md:hidden mt-3 pt-3 border-t border-gray-200/50 pb-2 space-y-3">
                                <div className="flex items-center justify-between">
                                    <span className="text-gray-700 font-medium">👤 {currentUser?.name}</span>
                                    <LanguageSwitcher />
                                </div>
                                <div className="flex flex-col gap-2">
                                    <Link href="/housing" className="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-xl transition-colors" onClick={() => setMobileMenuOpen(false)}>
                                        {t('student.hero.findHousing')}
                                    </Link>
                                    <Link href="/jobs" className="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-xl transition-colors" onClick={() => setMobileMenuOpen(false)}>
                                        {t('student.hero.studentJobs')}
                                    </Link>
                                    <button
                                        onClick={() => {
                                            localStorage.removeItem('token');
                                            localStorage.removeItem('user');
                                            window.location.href = '/';
                                        }}
                                        className="px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-xl transition-colors text-left"
                                    >
                                        Logout
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                </nav>

                {/* Rest of authenticated content - same as guest but with full access */}
                {/* Hero Section */}
                <section className="relative overflow-hidden text-white pt-44 pb-16 mx-4 sm:mx-8 lg:mx-16 mt-6 rounded-3xl" style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.85) 0%, rgba(99,102,241,0.85) 50%, rgba(139,92,246,0.8) 100%)' }}>
                    <div className="absolute inset-0 rounded-3xl" style={{ background: 'radial-gradient(circle at 30% 20%, rgba(255,255,255,0.15) 0%, transparent 50%), radial-gradient(circle at 70% 80%, rgba(255,255,255,0.1) 0%, transparent 50%)' }} />
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
                        <div className="text-center">
                            <h1 className="text-5xl font-bold mb-6 drop-shadow-lg">
                                {t('student.hero.title')}
                            </h1>
                            <p className="text-xl mb-8 text-white/80">
                                {t('student.hero.subtitle')}
                            </p>
                            <div className="flex justify-center space-x-4">
                                <Link
                                    href="/housing"
                                    className="bg-white text-blue-700 px-8 py-3 rounded-2xl font-semibold hover:bg-white/90 transition-all shadow-md"
                                >
                                    {t('student.hero.findHousing')}
                                </Link>
                                <Link
                                    href="/jobs"
                                    className="bg-white text-blue-700 px-8 py-3 rounded-2xl font-semibold hover:bg-white/90 transition-all shadow-md"
                                >
                                    {t('student.hero.studentJobs')}
                                </Link>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Pricing Section */}
                <section className="py-20 relative z-10">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="text-center mb-16">
                            <h2 className="text-4xl font-bold text-gray-900 mb-4">
                                {t('student.pricing.title')}
                            </h2>
                            <p className="text-xl text-gray-600">
                                {t('student.pricing.subtitle')}
                            </p>
                        </div>

                        <div className="grid md:grid-cols-4 gap-6">
                            {/* FREE Plan */}
                            <div className="glass-card rounded-3xl p-8 transition-all duration-300 hover:scale-[1.02]">
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
                                    className="glass-btn block w-full text-center bg-gray-500/10 text-gray-700 px-6 py-3 rounded-2xl font-semibold hover:bg-gray-500/20 transition-all"
                                >
                                    {t('student.pricing.free.button')}
                                </Link>
                            </div>

                            {/* BASIC Plan */}
                            <div className="glass-card rounded-3xl p-8 transition-all duration-300 hover:scale-[1.02] relative" style={{ borderColor: 'rgba(59,130,246,0.3)' }}>
                                <div className="absolute top-0 right-0 px-4 py-1 rounded-bl-xl rounded-tr-3xl text-sm font-semibold text-white" style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.8), rgba(99,102,241,0.8))' }}>
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
                                    href="/subscription?plan=basic"
                                    className="glass-btn block w-full text-center text-white px-6 py-3 rounded-2xl font-semibold transition-all shadow-lg shadow-blue-500/20" style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.85), rgba(99,102,241,0.85))' }}
                                >
                                    {t('student.pricing.basic.button')}
                                </Link>
                            </div>

                            {/* STANDARD Plan */}
                            <div className="glass-card rounded-3xl p-8 transition-all duration-300 hover:scale-[1.02]" style={{ borderColor: 'rgba(168,85,247,0.3)' }}>
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
                                    href="/subscription?plan=standard"
                                    className="glass-btn block w-full text-center text-white px-6 py-3 rounded-2xl font-semibold transition-all shadow-lg shadow-purple-500/20" style={{ background: 'linear-gradient(135deg, rgba(168,85,247,0.85), rgba(139,92,246,0.85))' }}
                                >
                                    {t('student.pricing.standard.button')}
                                </Link>
                            </div>

                            {/* PREMIUM Plan */}
                            <div className="glass-card rounded-3xl p-8 transition-all duration-300 hover:scale-[1.02] relative" style={{ borderColor: 'rgba(245,158,11,0.3)', background: 'rgba(255,251,235,0.5)' }}>
                                <div className="absolute top-0 right-0 px-4 py-1 rounded-bl-xl rounded-tr-3xl text-sm font-semibold text-white" style={{ background: 'linear-gradient(135deg, rgba(245,158,11,0.9), rgba(249,115,22,0.9))' }}>
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
                                    href="/subscription?plan=premium"
                                    className="glass-btn block w-full text-center text-white px-6 py-3 rounded-2xl font-semibold transition-all shadow-lg shadow-orange-500/20" style={{ background: 'linear-gradient(135deg, rgba(245,158,11,0.9), rgba(249,115,22,0.9))' }}
                                >
                                    {t('student.pricing.premium.button')}
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
                <section className="py-16 relative z-10">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">
                            {t('student.features.title')}
                        </h2>

                        <div className="grid md:grid-cols-5 gap-6">
                            <div className="glass-card rounded-2xl text-center p-6 transition-all duration-300 hover:scale-[1.02]">
                                <div className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4" style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.2), rgba(99,102,241,0.2))' }}>
                                    <GraduationCap className="w-8 h-8 text-blue-600" />
                                </div>
                                <h3 className="text-xl font-semibold mb-2">
                                    {t('student.features.feature1.title')}
                                </h3>
                                <p className="text-gray-600">
                                    {t('student.features.feature1.description')}
                                </p>
                            </div>

                            <div className="glass-card rounded-2xl text-center p-6 transition-all duration-300 hover:scale-[1.02]">
                                <div className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4" style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.2), rgba(99,102,241,0.2))' }}>
                                    <Users className="w-8 h-8 text-blue-600" />
                                </div>
                                <h3 className="text-xl font-semibold mb-2">
                                    {t('student.features.feature2.title')}
                                </h3>
                                <p className="text-gray-600">
                                    {t('student.features.feature2.description')}
                                </p>
                            </div>

                            <div className="glass-card rounded-2xl text-center p-6 transition-all duration-300 hover:scale-[1.02]">
                                <div className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4" style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.2), rgba(99,102,241,0.2))' }}>
                                    <Globe className="w-8 h-8 text-blue-600" />
                                </div>
                                <h3 className="text-xl font-semibold mb-2">
                                    {t('student.features.feature3.title')}
                                </h3>
                                <p className="text-gray-600">
                                    {t('student.features.feature3.description')}
                                </p>
                            </div>

                            <div className="glass-card rounded-2xl text-center p-6 transition-all duration-300 hover:scale-[1.02]">
                                <div className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4" style={{ background: 'linear-gradient(135deg, rgba(16,185,129,0.2), rgba(52,211,153,0.2))' }}>
                                    <Home className="w-8 h-8 text-green-600" />
                                </div>
                                <h3 className="text-xl font-semibold mb-2">
                                    {t('student.features.feature4.title')}
                                </h3>
                                <p className="text-gray-600">
                                    {t('student.features.feature4.description')}
                                </p>
                            </div>

                            <div className="glass-card rounded-2xl text-center p-6 transition-all duration-300 hover:scale-[1.02]">
                                <div className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4" style={{ background: 'linear-gradient(135deg, rgba(168,85,247,0.2), rgba(139,92,246,0.2))' }}>
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
                <section className="relative overflow-hidden text-white py-16 mx-4 sm:mx-8 lg:mx-16 mb-6 rounded-3xl" style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.85) 0%, rgba(99,102,241,0.85) 50%, rgba(139,92,246,0.8) 100%)' }}>
                    <div className="absolute inset-0 rounded-3xl" style={{ background: 'radial-gradient(circle at 20% 50%, rgba(255,255,255,0.12) 0%, transparent 50%), radial-gradient(circle at 80% 30%, rgba(255,255,255,0.08) 0%, transparent 50%)' }} />
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
                        <h2 className="text-3xl font-bold mb-4 drop-shadow-lg">
                            {t('student.cta.title')}
                        </h2>
                        <p className="text-xl mb-8 text-white/80">
                            {t('student.cta.subtitle')}
                        </p>
                        <Link
                            href="/chat"
                            className="glass-btn bg-white/90 text-blue-700 px-8 py-3 rounded-2xl font-semibold hover:bg-white transition-all inline-block"
                        >
                            {t('student.cta.button')}
                        </Link>
                    </div>
                </section>

                {/* Footer */}
                <footer className="glass-dark text-white py-6 relative z-10">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="grid md:grid-cols-4 gap-6 text-sm">
                            <div>
                                <h3 className="text-sm font-semibold mb-2 text-white/90">{t('footer.about')}</h3>
                                <ul className="space-y-1">
                                    <li><Link href="/about" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.aboutUs')}</Link></li>
                                    <li><Link href="/contact" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.contact')}</Link></li>
                                </ul>
                            </div>
                            <div>
                                <h3 className="text-sm font-semibold mb-2 text-white/90">{t('footer.resources')}</h3>
                                <ul className="space-y-1">
                                    <li><Link href="/universities" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.universities')}</Link></li>
                                    <li><Link href="/language-schools" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.languageSchools')}</Link></li>
                                    <li><Link href="/vocational-schools" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.vocationalSchools')}</Link></li>
                                </ul>
                            </div>
                            <div>
                                <h3 className="text-sm font-semibold mb-2 text-white/90">{t('footer.support')}</h3>
                                <ul className="space-y-1">
                                    <li><Link href="/help" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.helpCenter')}</Link></li>
                                    <li><Link href="/faq" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.faq')}</Link></li>
                                </ul>
                            </div>
                            <div>
                                <h3 className="text-sm font-semibold mb-2 text-white/90">{t('footer.legal')}</h3>
                                <ul className="space-y-1">
                                    <li><Link href="/privacy" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.privacyPolicy')}</Link></li>
                                    <li><Link href="/terms" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.termsOfService')}</Link></li>
                                </ul>
                            </div>
                        </div>
                        <div className="border-t border-white/10 mt-5 pt-4 text-center text-white/40 text-xs space-y-1">
                            <p>{t('footer.copyright')}</p>
                            <p>Created by <a href="https://wavelynecode.com" target="_blank" rel="noopener noreferrer" className="text-white/50 hover:text-white transition-colors">Wavelyne</a> — <a href="https://wavelynecode.com" target="_blank" rel="noopener noreferrer" className="text-white/50 hover:text-white transition-colors">wavelynecode.com</a></p>
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
        <div className="min-h-screen pt-3 glass-bg" style={{ background: 'linear-gradient(135deg, #e0f2fe 0%, #f0f4ff 30%, #faf5ff 60%, #e0f2fe 100%)' }}>
            {/* Navigation */}
            <nav className="glass-strong sticky top-0 z-50 shadow-lg shadow-black/5 mx-3 sm:mx-5 lg:mx-8 rounded-2xl">
                <div className="w-full px-4 sm:px-6 lg:px-8 py-3 relative z-10">
                    <div className="flex items-center justify-between">
                        <Link href="/" className="flex items-center space-x-2">
                            <Sparkles className="w-8 h-8 text-blue-600" />
                            <span className="text-2xl font-bold text-blue-600">Student Advisor</span>
                        </Link>
                        {/* Desktop menu */}
                        <div className="hidden md:flex items-center space-x-3">
                            <LanguageSwitcher />
                            <Link
                                href="/login"
                                className="bg-blue-500 text-white px-5 py-2 rounded-xl font-medium hover:bg-blue-600 transition-colors shadow-md"
                            >
                                {t('auth.loginButton')}
                            </Link>
                            <Link
                                href="/register"
                                className="bg-gray-900 text-white px-5 py-2 rounded-xl font-medium hover:bg-gray-800 transition-colors shadow-md"
                            >
                                {t('auth.registerButton')}
                            </Link>
                        </div>
                        {/* Mobile hamburger */}
                        <button
                            className="md:hidden p-2 rounded-xl hover:bg-gray-100 transition-colors"
                            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        >
                            {mobileMenuOpen ? <X className="w-6 h-6 text-gray-700" /> : <Menu className="w-6 h-6 text-gray-700" />}
                        </button>
                    </div>
                    {/* Mobile dropdown */}
                    {mobileMenuOpen && (
                        <div className="md:hidden mt-3 pt-3 border-t border-gray-200/50 pb-2 space-y-3">
                            <div className="flex items-center justify-center">
                                <LanguageSwitcher />
                            </div>
                            <div className="flex flex-col gap-2">
                                <Link href="/housing" className="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-xl transition-colors" onClick={() => setMobileMenuOpen(false)}>
                                    {t('student.hero.findHousing')}
                                </Link>
                                <Link href="/jobs" className="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-xl transition-colors" onClick={() => setMobileMenuOpen(false)}>
                                    {t('student.hero.studentJobs')}
                                </Link>
                                <div className="flex flex-col gap-2 pt-2 border-t border-gray-200/50">
                                    <Link
                                        href="/login"
                                        className="px-4 py-2.5 text-center text-sm font-medium bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition-colors shadow-md"
                                        onClick={() => setMobileMenuOpen(false)}
                                    >
                                        {t('auth.loginButton')}
                                    </Link>
                                    <Link
                                        href="/register"
                                        className="px-4 py-2.5 text-center text-sm font-medium bg-gray-900 text-white rounded-xl hover:bg-gray-800 transition-colors shadow-md"
                                        onClick={() => setMobileMenuOpen(false)}
                                    >
                                        {t('auth.registerButton')}
                                    </Link>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </nav>

            {/* Hero Section */}
            <section className="relative overflow-hidden text-white pt-44 pb-16 mx-4 sm:mx-8 lg:mx-16 mt-6 rounded-3xl" style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.85) 0%, rgba(99,102,241,0.85) 50%, rgba(139,92,246,0.8) 100%)' }}>
                <div className="absolute inset-0 rounded-3xl" style={{ background: 'radial-gradient(circle at 30% 20%, rgba(255,255,255,0.15) 0%, transparent 50%), radial-gradient(circle at 70% 80%, rgba(255,255,255,0.1) 0%, transparent 50%)' }} />
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
                    <div className="text-center">
                        <h1 className="text-5xl font-bold mb-6 drop-shadow-lg">
                            {t('student.hero.title')}
                        </h1>
                        <p className="text-xl mb-8 text-white/80">
                            {t('student.hero.subtitle')}
                        </p>
                        <div className="flex justify-center space-x-4">
                            <Link
                                href="/housing"
                                className="bg-white text-blue-700 px-8 py-3 rounded-2xl font-semibold hover:bg-white/90 transition-all shadow-md"
                            >
                                {t('student.hero.findHousing')}
                            </Link>
                            <Link
                                href="/jobs"
                                className="bg-white text-blue-700 px-8 py-3 rounded-2xl font-semibold hover:bg-white/90 transition-all shadow-md"
                            >
                                {t('student.hero.studentJobs')}
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

            {/* Pricing Section */}
            <section className="py-20 relative z-10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-4xl font-bold text-gray-900 mb-4">
                            {t('student.pricing.title')}
                        </h2>
                        <p className="text-xl text-gray-600">
                            {t('student.pricing.subtitle')}
                        </p>
                    </div>

                    <div className="grid md:grid-cols-4 gap-6">
                        {/* FREE Plan */}
                        <div className="glass-card rounded-3xl p-8 transition-all duration-300 hover:scale-[1.02]">
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
                                className="block w-full text-center bg-gray-200/60 text-gray-700 px-6 py-3 rounded-2xl font-semibold hover:bg-gray-200 transition-colors shadow-sm"
                            >
                                {t('student.pricing.free.button')}
                            </Link>
                        </div>

                        {/* BASIC Plan */}
                        <div className="glass-card rounded-3xl p-8 transition-all duration-300 hover:scale-[1.02] relative" style={{ borderColor: 'rgba(59,130,246,0.3)' }}>
                            <div className="absolute top-0 right-0 px-4 py-1 rounded-bl-xl rounded-tr-3xl text-sm font-semibold text-white" style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.8), rgba(99,102,241,0.8))' }}>
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
                                href="/register?plan=basic"
                                className="block w-full text-center text-white px-6 py-3 rounded-2xl font-semibold transition-colors shadow-lg shadow-blue-500/20 bg-blue-500 hover:bg-blue-600"
                            >
                                {t('student.pricing.basic.button')}
                            </Link>
                        </div>

                        {/* STANDARD Plan */}
                        <div className="glass-card rounded-3xl p-8 transition-all duration-300 hover:scale-[1.02]" style={{ borderColor: 'rgba(168,85,247,0.3)' }}>
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
                                href="/register?plan=standard"
                                className="block w-full text-center text-white px-6 py-3 rounded-2xl font-semibold transition-colors shadow-lg shadow-purple-500/20 bg-purple-500 hover:bg-purple-600"
                            >
                                {t('student.pricing.standard.button')}
                            </Link>
                        </div>

                        {/* PREMIUM Plan */}
                        <div className="glass-card rounded-3xl p-8 transition-all duration-300 hover:scale-[1.02] relative" style={{ borderColor: 'rgba(245,158,11,0.3)', background: 'rgba(255,251,235,0.5)' }}>
                            <div className="absolute top-0 right-0 px-4 py-1 rounded-bl-xl rounded-tr-3xl text-sm font-semibold text-white" style={{ background: 'linear-gradient(135deg, rgba(245,158,11,0.9), rgba(249,115,22,0.9))' }}>
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
                                href="/register?plan=premium"
                                className="block w-full text-center text-white px-6 py-3 rounded-2xl font-semibold transition-colors shadow-lg shadow-orange-500/20 bg-orange-500 hover:bg-orange-600"
                            >
                                {t('student.pricing.premium.button')}
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
            <section className="py-16 relative z-10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">
                        {t('student.features.title')}
                    </h2>

                    <div className="grid md:grid-cols-3 gap-8">
                        <div className="glass-card rounded-2xl text-center p-8 transition-all duration-300 hover:scale-[1.02]">
                            <div className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4" style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.2), rgba(99,102,241,0.2))' }}>
                                <GraduationCap className="w-8 h-8 text-blue-600" />
                            </div>
                            <h3 className="text-xl font-semibold mb-2">
                                {t('student.features.feature1.title')}
                            </h3>
                            <p className="text-gray-600">
                                {t('student.features.feature1.description')}
                            </p>
                        </div>

                        <div className="glass-card rounded-2xl text-center p-8 transition-all duration-300 hover:scale-[1.02]">
                            <div className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4" style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.2), rgba(99,102,241,0.2))' }}>
                                <Users className="w-8 h-8 text-blue-600" />
                            </div>
                            <h3 className="text-xl font-semibold mb-2">
                                {t('student.features.feature2.title')}
                            </h3>
                            <p className="text-gray-600">
                                {t('student.features.feature2.description')}
                            </p>
                        </div>

                        <div className="glass-card rounded-2xl text-center p-8 transition-all duration-300 hover:scale-[1.02]">
                            <div className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4" style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.2), rgba(99,102,241,0.2))' }}>
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
            <section className="relative overflow-hidden text-white py-16 mx-4 sm:mx-8 lg:mx-16 mb-6 rounded-3xl" style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.85) 0%, rgba(99,102,241,0.85) 50%, rgba(139,92,246,0.8) 100%)' }}>
                <div className="absolute inset-0 rounded-3xl" style={{ background: 'radial-gradient(circle at 20% 50%, rgba(255,255,255,0.12) 0%, transparent 50%), radial-gradient(circle at 80% 30%, rgba(255,255,255,0.08) 0%, transparent 50%)' }} />
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
                    <h2 className="text-3xl font-bold mb-4 drop-shadow-lg">
                        {t('student.cta.title')}
                    </h2>
                    <p className="text-xl mb-8 text-white/80">
                        {t('student.cta.subtitle')}
                    </p>
                    <button
                        onClick={() => handleProtectedAction(() => window.location.href = '/register')}
                        className="glass-btn bg-white/90 text-blue-700 px-8 py-3 rounded-2xl font-semibold hover:bg-white transition-all inline-block cursor-pointer"
                    >
                        {t('student.cta.button')}
                    </button>
                </div>
            </section>

            {/* Footer */}
            <footer className="glass-dark text-white py-6 relative z-10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid md:grid-cols-4 gap-6 text-sm">
                        <div>
                            <h3 className="text-sm font-semibold mb-2 text-white/90">{t('footer.about')}</h3>
                            <ul className="space-y-1">
                                <li><Link href="/about" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.aboutUs')}</Link></li>
                                <li><Link href="/contact" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.contact')}</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h3 className="text-sm font-semibold mb-2 text-white/90">{t('footer.resources')}</h3>
                            <ul className="space-y-1">
                                <li><Link href="/universities" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.universities')}</Link></li>
                                <li><Link href="/language-schools" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.languageSchools')}</Link></li>
                                <li><Link href="/vocational-schools" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.vocationalSchools')}</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h3 className="text-sm font-semibold mb-2 text-white/90">{t('footer.support')}</h3>
                            <ul className="space-y-1">
                                <li><Link href="/help" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.helpCenter')}</Link></li>
                                <li><Link href="/faq" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.faq')}</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h3 className="text-sm font-semibold mb-2 text-white/90">{t('footer.legal')}</h3>
                            <ul className="space-y-1">
                                <li><Link href="/privacy" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.privacyPolicy')}</Link></li>
                                <li><Link href="/terms" className="text-white/50 hover:text-white text-xs transition-colors">{t('footer.termsOfService')}</Link></li>
                            </ul>
                        </div>
                    </div>
                    <div className="border-t border-white/10 mt-5 pt-4 text-center text-white/40 text-xs space-y-1">
                        <p>{t('footer.copyright')}</p>
                        <p>Created by <a href="https://wavelynecode.com" target="_blank" rel="noopener noreferrer" className="text-white/50 hover:text-white transition-colors">Wavelyne</a> — <a href="https://wavelynecode.com" target="_blank" rel="noopener noreferrer" className="text-white/50 hover:text-white transition-colors">wavelynecode.com</a></p>
                    </div>
                </div>
            </footer>

            {/* Auth Modal */}
            <AuthPromptModal isOpen={showAuthModal} onClose={() => setShowAuthModal(false)} />
        </div>
    );
}
