'use client';

import { useAuth } from '@/contexts/AuthContext';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import JurisdictionSelector from '@/components/JurisdictionSelector';
import LanguageSwitcher from '@/components/LanguageSwitcher';

export default function Navigation() {
    const { user, isAuthenticated, logout, isAdmin, isLawyer } = useAuth();
    const pathname = usePathname();

    if (!isAuthenticated) {
        return null;
    }

    const isActive = (path: string) => pathname === path;

    // Role-based navigation items
    const getNavItems = () => {
        const items = [
            { label: 'Home', href: '/', roles: ['user', 'admin', 'partner_lawyer'] },
            { label: 'Documents', href: '/documents', roles: ['user', 'admin', 'partner_lawyer'] },
            { label: 'Chat', href: '/chat', roles: ['user', 'admin', 'partner_lawyer'] },
            { label: 'Marketplace', href: '/marketplace', roles: ['user', 'admin', 'partner_lawyer'] },
        ];

        // User-specific items
        if (user?.role === 'user') {
            items.push({ label: 'My Cases', href: '/cases', roles: ['user'] });
        }

        // Lawyer-specific items
        if (isLawyer()) {
            items.push({ label: 'Assigned Cases', href: '/lawyer/cases', roles: ['partner_lawyer', 'admin'] });
            items.push({ label: 'Templates', href: '/lawyer/templates', roles: ['partner_lawyer', 'admin'] });
        }

        // Admin-specific items
        if (isAdmin()) {
            items.push({ label: 'Admin Panel', href: '/admin', roles: ['admin'] });
            items.push({ label: 'User Management', href: '/admin/users', roles: ['admin'] });
        }

        return items;
    };

    const navItems = getNavItems();

    return (
        <nav className="bg-white shadow-sm border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                    {/* Logo and Navigation Links */}
                    <div className="flex">
                        <div className="flex-shrink-0 flex items-center">
                            <Link href="/dashboard" className="text-2xl font-bold text-blue-600 hover:text-blue-700 transition-colors">
                                Student Advisor
                            </Link>
                        </div>
                        <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                            {navItems.map((item) => (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition ${isActive(item.href)
                                        ? 'border-blue-500 text-gray-900'
                                        : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                                        }`}
                                >
                                    {item.label}
                                </Link>
                            ))}
                        </div>
                    </div>

                    {/* User Menu */}
                    <div className="flex items-center space-x-4">
                        {/* Jurisdiction Selector */}
                        <JurisdictionSelector />

                        {/* Language Switcher */}
                        <LanguageSwitcher />

                        {/* Role Badge */}
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${user?.role === 'admin'
                            ? 'bg-purple-100 text-purple-800'
                            : user?.role === 'partner_lawyer'
                                ? 'bg-green-100 text-green-800'
                                : 'bg-blue-100 text-blue-800'
                            }`}>
                            {user?.role === 'partner_lawyer' ? 'Lawyer' : user?.role?.toUpperCase()}
                        </span>

                        {/* User Info */}
                        <div className="flex items-center space-x-3">
                            <div className="text-right">
                                <p className="text-sm font-medium text-gray-900">{user?.name}</p>
                                <p className="text-xs text-gray-500">{user?.email}</p>
                            </div>

                            {/* Avatar */}
                            <div className="h-10 w-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-semibold">
                                {user?.name?.charAt(0).toUpperCase()}
                            </div>
                        </div>

                        {/* Logout Button */}
                        <button
                            onClick={logout}
                            className="px-4 py-2 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition"
                        >
                            Logout
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile menu (optional - simplified) */}
            <div className="sm:hidden">
                <div className="pt-2 pb-3 space-y-1">
                    {navItems.map((item) => (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={`block pl-3 pr-4 py-2 border-l-4 text-base font-medium ${isActive(item.href)
                                ? 'bg-blue-50 border-blue-500 text-blue-700'
                                : 'border-transparent text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800'
                                }`}
                        >
                            {item.label}
                        </Link>
                    ))}
                </div>
            </div>
        </nav>
    );
}
