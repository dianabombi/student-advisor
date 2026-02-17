'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useLanguage } from '@/lib/LanguageContext';
import { LayoutDashboard, Users, GraduationCap, BarChart3, Settings, LogOut, X, Shield, Lightbulb, TrendingUp } from 'lucide-react';

interface NavItem {
    name: string;
    href: string;
    icon: React.ComponentType<{ className?: string }>;
}

interface SidebarProps {
    isOpen: boolean;
    onClose: () => void;
}

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
    const pathname = usePathname();
    const { t } = useLanguage();

    const navItems: NavItem[] = [
        { name: t('admin.nav.dashboard'), href: '/admin/dashboard', icon: LayoutDashboard },
        { name: t('admin.nav.users'), href: '/admin/users', icon: Users },
        { name: t('admin.nav.administrators'), href: '/admin/administrators', icon: Shield },
        { name: t('admin.nav.universities'), href: '/admin/universities', icon: GraduationCap },
        { name: t('admin.nav.analytics'), href: '/admin/analytics', icon: BarChart3 },
        { name: 'Marketing & Acquisition', href: '/admin/marketing', icon: TrendingUp },
        { name: t('admin.nav.roadmap'), href: '/admin/roadmap', icon: Lightbulb },
        { name: t('admin.nav.settings'), href: '/admin/settings', icon: Settings },
    ];

    const handleLogout = () => {
        localStorage.removeItem('token');
        window.location.href = '/auth/login';
    };

    return (
        <div className={`
            flex flex-col h-full bg-gray-900 text-gray-100 border-r border-gray-800
            fixed lg:static inset-y-0 left-0 z-50
            w-64 transform transition-transform duration-300 ease-in-out
            ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}>
            {/* Logo/Header */}
            <div className="p-6 border-b border-gray-800 flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                        {t('admin.panel')}
                    </h1>
                    <p className="text-sm text-gray-400 mt-1">{t('admin.subtitle')}</p>
                </div>
                {/* Close button for mobile */}
                <button
                    onClick={onClose}
                    className="lg:hidden p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
                >
                    <X className="w-5 h-5" />
                </button>
            </div>

            {/* Navigation */}
            <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
                {navItems.map((item) => {
                    const Icon = item.icon;
                    const isActive = pathname === item.href;

                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            onClick={() => onClose()}
                            className={`
                                flex items-center gap-3 px-4 py-3 rounded-lg
                                transition-all duration-200
                                ${isActive
                                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/50'
                                    : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                                }
                            `}
                        >
                            <Icon className="w-5 h-5" />
                            <span className="font-medium">{item.name}</span>
                        </Link>
                    );
                })}
            </nav>

            {/* Logout Button */}
            <div className="p-4 border-t border-gray-800">
                <button
                    onClick={handleLogout}
                    className="flex items-center gap-3 px-4 py-3 rounded-lg w-full
                        text-gray-400 hover:bg-red-900/20 hover:text-red-400
                        transition-all duration-200"
                >
                    <LogOut className="w-5 h-5" />
                    <span className="font-medium">{t('admin.logout')}</span>
                </button>
            </div>
        </div>
    );
}
