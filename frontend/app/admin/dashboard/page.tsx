'use client';

import { useEffect, useState } from 'react';
import StatCard from '@/components/admin/StatCard';
import LineChart from '@/components/admin/charts/LineChart';
import { Users, GraduationCap, MessageSquare, FileText } from 'lucide-react';
import { StatCardSkeleton, ChartSkeleton, ActivityFeedSkeleton } from '@/components/admin/LoadingSkeletons';
import { NoActivityFound } from '@/components/admin/EmptyState';

interface StatsOverview {
    total_users: number;
    total_universities: number;
    total_consultations: number;
    total_documents: number;
}

interface RecentActivity {
    id: number;
    type: string;
    user_email: string;
    timestamp: string;
    details: string;
}

interface UserGrowthPoint {
    date: string;
    count: number;
    [key: string]: string | number;
}

export default function DashboardPage() {
    const [stats, setStats] = useState<StatsOverview | null>(null);
    const [activities, setActivities] = useState<RecentActivity[]>([]);
    const [userGrowthData, setUserGrowthData] = useState<UserGrowthPoint[]>([]);
    const [loading, setLoading] = useState(true);
    const [activitiesLoading, setActivitiesLoading] = useState(true);
    const [growthLoading, setGrowthLoading] = useState(true);
    const [growthPeriod, setGrowthPeriod] = useState(30);

    useEffect(() => {
        fetchStats();
        fetchRecentActivity();
    }, []);

    useEffect(() => {
        fetchUserGrowth();
    }, [growthPeriod]);

    const fetchStats = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                window.location.href = '/auth/login';
                return;
            }

            const response = await fetch('http://localhost:8002/api/admin/stats/overview', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                setStats(data);
            } else if (response.status === 401 || response.status === 403) {
                window.location.href = '/auth/login';
            }
        } catch (error) {
            console.error('Failed to fetch stats:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchRecentActivity = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) return;

            const response = await fetch('http://localhost:8002/api/admin/stats/recent-activity?limit=5', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                setActivities(data);
            }
        } catch (error) {
            console.error('Failed to fetch activities:', error);
        } finally {
            setActivitiesLoading(false);
        }
    };

    const fetchUserGrowth = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) return;

            const response = await fetch(`http://localhost:8002/api/admin/stats/users-growth?days=${growthPeriod}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                setUserGrowthData(data);
            }
        } catch (error) {
            console.error('Failed to fetch user growth:', error);
        } finally {
            setGrowthLoading(false);
        }
    };

    const formatDate = (dateString: string) => {
        try {
            return new Date(dateString).toLocaleString('en-US', {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch {
            return dateString;
        }
    };

    const getActivityIcon = (type: string) => {
        switch (type) {
            case 'registration':
                return '👤';
            case 'document_upload':
                return '📄';
            case 'consultation':
                return '💬';
            default:
                return '📌';
        }
    };

    return (
        <div className="space-y-8">
            {/* Header */}
            <div>
                <h1 className="text-3xl font-bold text-white">Dashboard</h1>
                <p className="text-gray-400 mt-2">Overview of platform statistics</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
                <StatCard
                    title="Total Users"
                    value={stats?.total_users ?? 0}
                    icon={<Users className="w-6 h-6" />}
                    loading={loading}
                />
                <StatCard
                    title="Universities"
                    value={stats?.total_universities ?? 0}
                    icon={<GraduationCap className="w-6 h-6" />}
                    loading={loading}
                />
                <StatCard
                    title="Consultations"
                    value={stats?.total_consultations ?? 0}
                    icon={<MessageSquare className="w-6 h-6" />}
                    loading={loading}
                />
                <StatCard
                    title="Documents"
                    value={stats?.total_documents ?? 0}
                    icon={<FileText className="w-6 h-6" />}
                    loading={loading}
                />
            </div>

            {/* User Growth Chart */}
            <div className="bg-gray-800 rounded-xl border border-gray-700">
                <div className="p-6 border-b border-gray-700 flex items-center justify-between">
                    <h2 className="text-xl font-semibold text-white">User Growth</h2>
                    <div className="flex gap-2">
                        <button
                            onClick={() => setGrowthPeriod(30)}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${growthPeriod === 30
                                ? 'bg-blue-600 text-white'
                                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                                }`}
                        >
                            30 Days
                        </button>
                        <button
                            onClick={() => setGrowthPeriod(90)}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${growthPeriod === 90
                                ? 'bg-blue-600 text-white'
                                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                                }`}
                        >
                            3 Months
                        </button>
                        <button
                            onClick={() => setGrowthPeriod(365)}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${growthPeriod === 365
                                ? 'bg-blue-600 text-white'
                                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                                }`}
                        >
                            1 Year
                        </button>
                        <button
                            onClick={() => setGrowthPeriod(9999)}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${growthPeriod === 9999
                                ? 'bg-blue-600 text-white'
                                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                                }`}
                        >
                            All Time
                        </button>
                    </div>
                </div>
                <div className="p-6">
                    {growthLoading ? (
                        <div className="flex items-center justify-center h-[300px]">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                        </div>
                    ) : userGrowthData.length > 0 ? (
                        <LineChart
                            data={userGrowthData}
                            lines={[
                                { dataKey: 'count', stroke: '#3B82F6', name: 'New Users' }
                            ]}
                            xAxisKey="date"
                            height={300}
                        />
                    ) : (
                        <p className="text-gray-400 text-center py-8">No growth data available</p>
                    )}
                </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-gray-800 rounded-xl border border-gray-700">
                <div className="p-6 border-b border-gray-700">
                    <h2 className="text-xl font-semibold text-white">Recent Activity</h2>
                </div>
                <div className="p-6">
                    {activitiesLoading ? (
                        <div className="space-y-4">
                            {[1, 2, 3].map((i) => (
                                <div key={i} className="flex items-center gap-4 animate-pulse">
                                    <div className="w-10 h-10 bg-gray-700 rounded-lg"></div>
                                    <div className="flex-1 space-y-2">
                                        <div className="h-4 bg-gray-700 rounded w-3/4"></div>
                                        <div className="h-3 bg-gray-700 rounded w-1/2"></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : activities.length > 0 ? (
                        <div className="space-y-4">
                            {activities.map((activity) => (
                                <div key={activity.id} className="flex items-start gap-4 p-4 rounded-lg hover:bg-gray-700/50 transition-colors">
                                    <div className="w-10 h-10 bg-gray-700 rounded-lg flex items-center justify-center text-xl">
                                        {getActivityIcon(activity.type)}
                                    </div>
                                    <div className="flex-1">
                                        <p className="text-white font-medium">{activity.details}</p>
                                        <p className="text-gray-400 text-sm mt-1">
                                            {activity.user_email} • {formatDate(activity.timestamp)}
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <NoActivityFound />
                    )}
                </div>
            </div>
        </div>
    );
}
