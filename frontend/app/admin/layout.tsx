'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import AdminSidebar from '@/components/admin/Sidebar';
import LanguageSwitcher from '@/components/admin/LanguageSwitcher';

export default function AdminLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const router = useRouter();
    const { user, isLoading, isAdmin } = useAuth();

    useEffect(() => {
        // Чекаємо поки завантажується
        if (isLoading) {
            console.log('⏳ Loading user...');
            return;
        }

        // Якщо немає користувача - на логін
        if (!user) {
            console.log('❌ No user, redirecting to login');
            window.location.href = '/auth/login';
            return;
        }

        // Якщо не адмін - на головну
        if (!isAdmin()) {
            console.log('⛔ Not admin, redirecting to home');
            window.location.href = '/';
            return;
        }

        // Все ОК - користувач адмін
        console.log('✅ Admin access granted');
    }, [user, isLoading, isAdmin]);

    // Показуємо loading поки перевіряємо
    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                    <p className="mt-4 text-gray-600">Loading...</p>
                </div>
            </div>
        );
    }

    // Якщо не адмін - показуємо null (редірект вже викликаний)
    if (!user || !isAdmin()) {
        return null;
    }

    // Рендеримо admin панель
    return (
        <div className="flex h-screen bg-gray-900">
            <AdminSidebar isOpen={true} onClose={() => { }} />
            <main className="flex-1 overflow-y-auto">
                {/* Header with language switcher */}
                <div className="bg-gray-800 border-b border-gray-700 px-6 py-4 flex justify-end">
                    <LanguageSwitcher />
                </div>
                <div className="container mx-auto px-6 py-8">
                    {children}
                </div>
            </main>
        </div>
    );
}
