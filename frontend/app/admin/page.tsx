'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

interface StatsOverview {
    total_users: number;
    active_users: number;
    users_today: number;
    total_universities: number;
    total_consultations: number;
    consultations_today: number;
    total_documents: number;
    total_job_agencies: number;
    total_housing_agencies: number;
    timestamp: string;
}

interface Activity {
    type: string;
    icon: string;
    message: string;
    timestamp: string;
}

export default function AdminDashboard() {
    const router = useRouter();
    const [isAdmin, setIsAdmin] = useState(false);
    const [loading, setLoading] = useState(true);
    const [userData, setUserData] = useState<any>(null);
    const [stats, setStats] = useState<StatsOverview | null>(null);
    const [activities, setActivities] = useState<Activity[]>([]);
    const [statsLoading, setStatsLoading] = useState(true);

    useEffect(() => {
        checkAdminAccess();
    }, []);

    const checkAdminAccess = async () => {
        try {
            const token = localStorage.getItem('token');

            if (!token) {
                router.push('/login');
                return;
            }

            const response = await fetch('http://localhost:8002/api/auth/me', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                router.push('/login');
                return;
            }

            const data = await response.json();

            if (!data.is_admin) {
                router.push('/');
                return;
            }

            setUserData(data);
            setIsAdmin(true);

            // Fetch stats after admin verification
            fetchStats(token);
            fetchActivities(token);
        } catch (error) {
            console.error('Auth check failed:', error);
            router.push('/login');
        } finally {
            setLoading(false);
        }
    };

    const fetchStats = async (token: string) => {
        try {
            const response = await fetch('http://localhost:8002/api/admin/stats/overview', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                const data = await response.json();
                setStats(data);
            }
        } catch (error) {
            console.error('Failed to fetch stats:', error);
        } finally {
            setStatsLoading(false);
        }
    };

    const fetchActivities = async (token: string) => {
        try {
            const response = await fetch('http://localhost:8002/api/admin/stats/recent-activity?limit=5', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                const data = await response.json();
                setActivities(data.activities || []);
            }
        } catch (error) {
            console.error('Failed to fetch activities:', error);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading...</p>
                </div>
            </div>
        );
    }

    if (!isAdmin) {
        return null;
    }

    const adminCards = [
        {
            title: 'User Management',
            description: 'Manage user accounts, view activity, block/unblock users',
            icon: '👥',
            href: '/admin/users',
            color: 'from-purple-500 to-purple-600'
        },
        {
            title: 'Universities',
            description: 'View educational institutions statistics by country and type',
            icon: '🎓',
            href: '/admin/universities',
            color: 'from-indigo-500 to-indigo-600'
        },
        {
            title: 'Template Management',
            description: 'Manage document templates (DOCX files)',
            icon: '📝',
            href: '/admin/templates',
            color: 'from-blue-500 to-blue-600'
        },
        {
            title: 'Document Processing',
            description: 'View all processed documents',
            icon: '📄',
            href: '/admin/documents',
            color: 'from-green-500 to-green-600'
        },
        {
            title: 'System Settings',
            description: 'Configure system settings',
            icon: '⚙️',
            href: '/admin/settings',
            color: 'from-orange-500 to-orange-600'
        }
    ];

    const StatCard = ({ label, value, subValue, icon, color }: {
        label: string;
        value: number | string;
        subValue?: string;
        icon: string;
        color: string;
    }) => (
        <div className={`bg-gradient-to-br ${color} rounded-xl shadow-lg p-6 text-white`}>
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-sm opacity-80">{label}</p>
                    <p className="text-3xl font-bold mt-1">
                        {statsLoading ? (
                            <span className="inline-block w-12 h-8 bg-white/20 rounded animate-pulse"></span>
                        ) : value}
                    </p>
                    {subValue && <p className="text-xs opacity-70 mt-1">{subValue}</p>}
                </div>
                <span className="text-4xl opacity-80">{icon}</span>
            </div>
        </div>
    );

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-white shadow">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
                            <p className="mt-1 text-sm text-gray-500">
                                Welcome, {userData?.name || userData?.email}
                            </p>
                        </div>
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800">
                            🔒 Admin
                        </span>
                    </div>
                </div>
            </div>

            {/* Content */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                {/* Quick Stats */}
                <div className="mb-12">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">📊 Quick Stats</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        <StatCard
                            label="Total Users"
                            value={stats?.total_users ?? '-'}
                            subValue={stats?.users_today ? `+${stats.users_today} today` : undefined}
                            icon="👥"
                            color="from-blue-500 to-blue-600"
                        />
                        <StatCard
                            label="Universities"
                            value={stats?.total_universities ?? '-'}
                            icon="🎓"
                            color="from-purple-500 to-purple-600"
                        />
                        <StatCard
                            label="AI Consultations"
                            value={stats?.total_consultations ?? '-'}
                            subValue={stats?.consultations_today ? `+${stats.consultations_today} today` : undefined}
                            icon="🤖"
                            color="from-green-500 to-green-600"
                        />
                        <StatCard
                            label="Documents"
                            value={stats?.total_documents ?? '-'}
                            icon="📄"
                            color="from-orange-500 to-orange-600"
                        />
                    </div>

                    {/* Second row of stats */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                        <StatCard
                            label="Job Agencies"
                            value={stats?.total_job_agencies ?? '-'}
                            icon="💼"
                            color="from-indigo-500 to-indigo-600"
                        />
                        <StatCard
                            label="Housing Agencies"
                            value={stats?.total_housing_agencies ?? '-'}
                            icon="🏠"
                            color="from-pink-500 to-pink-600"
                        />
                        <StatCard
                            label="Active Users (30d)"
                            value={stats?.active_users ?? '-'}
                            icon="📈"
                            color="from-teal-500 to-teal-600"
                        />
                    </div>
                </div>

                {/* Admin Cards */}
                <h2 className="text-xl font-semibold text-gray-900 mb-4">🛠️ Management</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {adminCards.map((card, index) => (
                        <Link
                            key={index}
                            href={card.href}
                            className="block group"
                        >
                            <div className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden">
                                <div className={`h-2 bg-gradient-to-r ${card.color}`}></div>
                                <div className="p-6">
                                    <div className="flex items-start">
                                        <div className="flex-shrink-0">
                                            <span className="text-4xl">{card.icon}</span>
                                        </div>
                                        <div className="ml-4 flex-1">
                                            <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                                                {card.title}
                                            </h3>
                                            <p className="mt-1 text-sm text-gray-500">
                                                {card.description}
                                            </p>
                                        </div>
                                        <svg
                                            className="w-5 h-5 text-gray-400 group-hover:text-blue-600 transition-colors"
                                            fill="none"
                                            stroke="currentColor"
                                            viewBox="0 0 24 24"
                                        >
                                            <path
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                strokeWidth={2}
                                                d="M9 5l7 7-7 7"
                                            />
                                        </svg>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>

                {/* Recent Activity */}
                {activities.length > 0 && (
                    <div className="mt-12">
                        <h2 className="text-xl font-semibold text-gray-900 mb-4">🕐 Recent Activity</h2>
                        <div className="bg-white rounded-lg shadow overflow-hidden">
                            <ul className="divide-y divide-gray-200">
                                {activities.map((activity, index) => (
                                    <li key={index} className="px-6 py-4 hover:bg-gray-50">
                                        <div className="flex items-center">
                                            <span className="text-2xl mr-4">{activity.icon}</span>
                                            <div className="flex-1">
                                                <p className="text-sm font-medium text-gray-900">{activity.message}</p>
                                                <p className="text-xs text-gray-500">
                                                    {activity.timestamp ? new Date(activity.timestamp).toLocaleString() : '-'}
                                                </p>
                                            </div>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
