'use client';

import Link from 'next/link';
import { useLanguage } from '@/lib/LanguageContext';

export default function GlobalSidebar() {
    const { t } = useLanguage();

    return (
        <aside className="fixed left-0 top-20 w-64 h-[calc(100vh-5rem)] border-r border-white/10 bg-slate-900/95 backdrop-blur-lg p-6 z-40">
            <nav className="space-y-2">
                <Link
                    href="/about"
                    className="block px-4 py-3 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                >
                    {t('sidebar.about')}
                </Link>
                <Link
                    href="/how-it-works"
                    className="block px-4 py-3 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                >
                    {t('sidebar.howItWorks')}
                </Link>
                <Link
                    href="/feedback"
                    className="block px-4 py-3 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                >
                    {t('sidebar.feedback')}
                </Link>
            </nav>
        </aside>
    );
}
