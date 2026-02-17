'use client';

import { useEffect, useState } from 'react';
import { useLanguage } from '@/lib/LanguageContext';
import {
    Users,
    GraduationCap,
    MessageSquare,
    TrendingUp,
    Activity,
    Globe,
    Calendar,
    BarChart3,
    MapPin,
    Building2
} from 'lucide-react';
import PieChart from '@/components/charts/PieChart';
import BarChart from '@/components/charts/BarChart';
import LineChart from '@/components/charts/LineChart';

interface AnalyticsData {
    totalUsers: number;
    totalUniversities: number;
    totalConsultations: number;
    activeUsers: number;
    newUsersToday: number;
    consultationsToday: number;
}

interface CountryStats {
    country: string;
    flag: string;
    users: number;
    percentage: number;
}

interface InstitutionStats {
    name: string;
    type: string;
    views: number;
    consultations: number;
    country: string;
}

export default function AnalyticsPage() {
    const { t } = useLanguage();
    const [analytics, setAnalytics] = useState<AnalyticsData>({
        totalUsers: 0,
        totalUniversities: 0,
        totalConsultations: 0,
        activeUsers: 0,
        newUsersToday: 0,
        consultationsToday: 0,
    });
    const [loading, setLoading] = useState(true);

    // Статистика по країнах (визначається по IP)
    const [countryStats, setCountryStats] = useState<CountryStats[]>([]);

    // Статистика по навчальних закладах
    const [institutionStats, setInstitutionStats] = useState<InstitutionStats[]>([]);

    // Тренд зростання користувачів з різними періодами
    const [selectedPeriod, setSelectedPeriod] = useState<string>('7d');
    const [userGrowthData, setUserGrowthData] = useState<Record<string, { label: string; value: number }[]>>({});

    useEffect(() => {
        // Симулюємо завантаження даних
        // TODO: Замінити на реальний API запит з бекенду
        setTimeout(() => {
            setAnalytics({
                totalUsers: 1247,
                totalUniversities: 156,
                totalConsultations: 3892,
                activeUsers: 342,
                newUsersToday: 23,
                consultationsToday: 89,
            });

            // Статистика по країнах (визначено по IP адресах користувачів)
            setCountryStats([
                { country: 'Slovakia', flag: '🇸🇰', users: 456, percentage: 36.6 },
                { country: 'Ukraine', flag: '🇺🇦', users: 312, percentage: 25.0 },
                { country: 'Czech Republic', flag: '🇨🇿', users: 189, percentage: 15.2 },
                { country: 'Poland', flag: '🇵🇱', users: 134, percentage: 10.7 },
                { country: 'Germany', flag: '🇩🇪', users: 78, percentage: 6.3 },
                { country: 'Austria', flag: '🇦🇹', users: 45, percentage: 3.6 },
                { country: 'Other', flag: '🌍', users: 33, percentage: 2.6 },
            ]);

            // Топ навчальні заклади по зацікавленості
            setInstitutionStats([
                {
                    name: 'Comenius University',
                    type: 'University',
                    views: 1234,
                    consultations: 456,
                    country: 'Slovakia'
                },
                {
                    name: 'Slovak Technical University',
                    type: 'University',
                    views: 1089,
                    consultations: 389,
                    country: 'Slovakia'
                },
                {
                    name: 'University of Economics in Bratislava',
                    type: 'University',
                    views: 967,
                    consultations: 312,
                    country: 'Slovakia'
                },
                {
                    name: 'Pavol Jozef Šafárik University',
                    type: 'University',
                    views: 845,
                    consultations: 287,
                    country: 'Slovakia'
                },
                {
                    name: 'Charles University',
                    type: 'University',
                    views: 723,
                    consultations: 234,
                    country: 'Czech Republic'
                },
                {
                    name: 'Technical University of Munich',
                    type: 'University',
                    views: 678,
                    consultations: 198,
                    country: 'Germany'
                },
                {
                    name: 'University of Vienna',
                    type: 'University',
                    views: 589,
                    consultations: 176,
                    country: 'Austria'
                },
                {
                    name: 'Jagiellonian University',
                    type: 'University',
                    views: 534,
                    consultations: 165,
                    country: 'Poland'
                },
            ]);

            // Дані зростання користувачів для різних періодів
            setUserGrowthData({
                '7d': [
                    { label: 'Mon', value: 1180 },
                    { label: 'Tue', value: 1195 },
                    { label: 'Wed', value: 1210 },
                    { label: 'Thu', value: 1220 },
                    { label: 'Fri', value: 1235 },
                    { label: 'Sat', value: 1242 },
                    { label: 'Sun', value: 1247 },
                ],
                '15d': [
                    { label: 'Day 1', value: 1150 },
                    { label: 'Day 3', value: 1165 },
                    { label: 'Day 5', value: 1180 },
                    { label: 'Day 7', value: 1195 },
                    { label: 'Day 9', value: 1210 },
                    { label: 'Day 11', value: 1220 },
                    { label: 'Day 13', value: 1235 },
                    { label: 'Day 15', value: 1247 },
                ],
                '1m': [
                    { label: 'Week 1', value: 1100 },
                    { label: 'Week 2', value: 1150 },
                    { label: 'Week 3', value: 1200 },
                    { label: 'Week 4', value: 1247 },
                ],
                '2m': [
                    { label: 'Jan W1', value: 1050 },
                    { label: 'Jan W3', value: 1100 },
                    { label: 'Feb W1', value: 1150 },
                    { label: 'Feb W3', value: 1200 },
                    { label: 'Mar W1', value: 1230 },
                    { label: 'Mar W3', value: 1247 },
                ],
                '3m': [
                    { label: 'Dec', value: 980 },
                    { label: 'Jan', value: 1050 },
                    { label: 'Feb', value: 1150 },
                    { label: 'Mar', value: 1247 },
                ],
                '6m': [
                    { label: 'Sep', value: 750 },
                    { label: 'Oct', value: 820 },
                    { label: 'Nov', value: 900 },
                    { label: 'Dec', value: 980 },
                    { label: 'Jan', value: 1050 },
                    { label: 'Feb', value: 1150 },
                    { label: 'Mar', value: 1247 },
                ],
                '1y': [
                    { label: 'Apr', value: 450 },
                    { label: 'May', value: 520 },
                    { label: 'Jun', value: 580 },
                    { label: 'Jul', value: 630 },
                    { label: 'Aug', value: 690 },
                    { label: 'Sep', value: 750 },
                    { label: 'Oct', value: 820 },
                    { label: 'Nov', value: 900 },
                    { label: 'Dec', value: 980 },
                    { label: 'Jan', value: 1050 },
                    { label: 'Feb', value: 1150 },
                    { label: 'Mar', value: 1247 },
                ],
                'all': [
                    { label: '2024 Q1', value: 120 },
                    { label: '2024 Q2', value: 280 },
                    { label: '2024 Q3', value: 450 },
                    { label: '2024 Q4', value: 690 },
                    { label: '2025 Q1', value: 980 },
                    { label: '2026 Q1', value: 1247 },
                ],
            });

            setLoading(false);
        }, 500);
    }, []);

    const stats = [
        {
            title: t('admin.analytics.stats.totalUsers'),
            value: analytics.totalUsers,
            icon: Users,
            color: 'from-blue-500 to-blue-600',
            bgColor: 'bg-blue-500/10',
            change: '+12%',
            changeType: 'positive' as const,
        },
        {
            title: t('admin.analytics.stats.universities'),
            value: analytics.totalUniversities,
            icon: GraduationCap,
            color: 'from-purple-500 to-purple-600',
            bgColor: 'bg-purple-500/10',
            change: '+5',
            changeType: 'positive' as const,
        },
        {
            title: t('admin.analytics.stats.aiConsultations'),
            value: analytics.totalConsultations,
            icon: MessageSquare,
            color: 'from-green-500 to-green-600',
            bgColor: 'bg-green-500/10',
            change: '+23%',
            changeType: 'positive' as const,
        },
        {
            title: t('admin.analytics.stats.activeUsers'),
            value: analytics.activeUsers,
            icon: Activity,
            color: 'from-orange-500 to-orange-600',
            bgColor: 'bg-orange-500/10',
            change: '+8%',
            changeType: 'positive' as const,
        },
    ];

    const todayStats = [
        {
            title: t('admin.analytics.today.newUsers'),
            value: analytics.newUsersToday,
            icon: TrendingUp,
            color: 'text-blue-400',
        },
        {
            title: t('admin.analytics.today.consultations'),
            value: analytics.consultationsToday,
            icon: MessageSquare,
            color: 'text-green-400',
        },
        {
            title: t('admin.analytics.today.activeSessions'),
            value: 45,
            icon: Globe,
            color: 'text-purple-400',
        },
    ];

    if (loading) {
        return (
            <div className="flex items-center justify-center h-96">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                        <BarChart3 className="w-8 h-8 text-blue-400" />
                        {t('admin.analytics.title')}
                    </h1>
                    <p className="text-gray-400 mt-2">{t('admin.analytics.subtitle')}</p>
                </div>
                <div className="flex items-center gap-2 text-gray-400">
                    <Calendar className="w-5 h-5" />
                    <span>{new Date().toLocaleDateString()}</span>
                </div>
            </div>

            {/* Main Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat, index) => {
                    const Icon = stat.icon;
                    return (
                        <div
                            key={index}
                            className="bg-gray-800 rounded-xl p-6 border border-gray-700 hover:border-gray-600 transition-all"
                        >
                            <div className="flex items-start justify-between">
                                <div className="flex-1">
                                    <p className="text-gray-400 text-sm font-medium mb-2">
                                        {stat.title}
                                    </p>
                                    <p className="text-3xl font-bold text-white mb-3">
                                        {stat.value.toLocaleString()}
                                    </p>
                                    <div className="flex items-center gap-1">
                                        <TrendingUp className="w-4 h-4 text-green-400" />
                                        <span className="text-green-400 text-sm font-medium">
                                            {stat.change}
                                        </span>
                                        <span className="text-gray-500 text-sm">{t('admin.analytics.stats.vsLastMonth')}</span>
                                    </div>
                                </div>
                                <div className={`${stat.bgColor} p-3 rounded-lg`}>
                                    <Icon className={`w-6 h-6 bg-gradient-to-r ${stat.color} bg-clip-text text-transparent`} />
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Today's Activity */}
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                    <Activity className="w-6 h-6 text-blue-400" />
                    {t('admin.analytics.today.title')}
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {todayStats.map((stat, index) => {
                        const Icon = stat.icon;
                        return (
                            <div key={index} className="flex items-center gap-4">
                                <div className="bg-gray-700/50 p-3 rounded-lg">
                                    <Icon className={`w-6 h-6 ${stat.color}`} />
                                </div>
                                <div>
                                    <p className="text-gray-400 text-sm">{stat.title}</p>
                                    <p className="text-2xl font-bold text-white">
                                        {stat.value}
                                    </p>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* User Growth Trend */}
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h2 className="text-xl font-bold text-white flex items-center gap-2">
                            <TrendingUp className="w-6 h-6 text-green-400" />
                            {t('admin.analytics.userGrowth.title')}
                        </h2>
                        <p className="text-gray-400 text-sm mt-1">{t('admin.analytics.userGrowth.subtitle')}</p>
                    </div>

                    {/* Period Selector */}
                    <div className="flex gap-2 flex-wrap">
                        {[
                            { key: '7d', label: t('admin.analytics.userGrowth.periods.7d') },
                            { key: '15d', label: t('admin.analytics.userGrowth.periods.15d') },
                            { key: '1m', label: t('admin.analytics.userGrowth.periods.1m') },
                            { key: '2m', label: t('admin.analytics.userGrowth.periods.2m') },
                            { key: '3m', label: t('admin.analytics.userGrowth.periods.3m') },
                            { key: '6m', label: t('admin.analytics.userGrowth.periods.6m') },
                            { key: '1y', label: t('admin.analytics.userGrowth.periods.1y') },
                            { key: 'all', label: t('admin.analytics.userGrowth.periods.all') },
                        ].map((period) => (
                            <button
                                key={period.key}
                                onClick={() => setSelectedPeriod(period.key)}
                                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${selectedPeriod === period.key
                                        ? 'bg-green-600 text-white'
                                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                                    }`}
                            >
                                {period.label}
                            </button>
                        ))}
                    </div>
                </div>
                <LineChart
                    data={userGrowthData[selectedPeriod] || []}
                    color="#10b981"
                    height={250}
                />
            </div>

            {/* Geographic Distribution & Institution Interest */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Users by Country (based on IP) */}
                <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                    <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                        <MapPin className="w-6 h-6 text-blue-400" />
                        {t('admin.analytics.geography.title')}
                        <span className="text-sm text-gray-500 font-normal ml-2">({t('admin.analytics.geography.detectedByIp')})</span>
                    </h2>
                    <div className="flex justify-center py-4">
                        <PieChart
                            data={countryStats.map((stat, index) => ({
                                label: `${stat.flag} ${stat.country}`,
                                value: stat.users,
                                color: [
                                    '#3b82f6', // blue
                                    '#8b5cf6', // purple
                                    '#ec4899', // pink
                                    '#f59e0b', // amber
                                    '#10b981', // green
                                    '#06b6d4', // cyan
                                    '#6b7280', // gray
                                ][index % 7],
                            }))}
                            size={280}
                        />
                    </div>
                </div>

                {/* Top Institutions by Interest */}
                <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                    <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                        <Building2 className="w-6 h-6 text-purple-400" />
                        {t('admin.analytics.institutions.title')}
                    </h2>
                    <div className="space-y-3 max-h-[400px] overflow-y-auto">
                        {institutionStats.map((inst, index) => (
                            <div key={index} className="bg-gray-700/30 p-3 rounded-lg hover:bg-gray-700/50 transition-colors">
                                <div className="flex items-start justify-between mb-2">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2">
                                            <span className="text-gray-400 text-sm font-semibold">#{index + 1}</span>
                                            <h3 className="text-white font-medium">{inst.name}</h3>
                                        </div>
                                        <p className="text-gray-500 text-xs mt-1">{inst.country}</p>
                                    </div>
                                </div>
                                <div className="grid grid-cols-2 gap-3 mt-2">
                                    <div className="bg-gray-800/50 p-2 rounded">
                                        <p className="text-gray-400 text-xs">{t('admin.analytics.institutions.views')}</p>
                                        <p className="text-blue-400 font-bold">{inst.views.toLocaleString()}</p>
                                    </div>
                                    <div className="bg-gray-800/50 p-2 rounded">
                                        <p className="text-gray-400 text-xs">{t('admin.analytics.institutions.aiChats')}</p>
                                        <p className="text-green-400 font-bold">{inst.consultations}</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Popular Queries */}
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                    <MessageSquare className="w-5 h-5 text-green-400" />
                    {t('admin.analytics.queries.title')}
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {[
                        { query: 'Admission requirements', count: 456, category: t('admin.analytics.queries.categories.admissions') },
                        { query: 'Tuition fees and costs', count: 389, category: t('admin.analytics.queries.categories.finance') },
                        { query: 'Scholarship programs', count: 312, category: t('admin.analytics.queries.categories.finance') },
                        { query: 'Application deadlines', count: 287, category: t('admin.analytics.queries.categories.admissions') },
                        { query: 'Student housing options', count: 234, category: t('admin.analytics.queries.categories.housing') },
                        { query: 'Part-time job opportunities', count: 198, category: t('admin.analytics.queries.categories.jobs') },
                    ].map((item, index) => (
                        <div key={index} className="flex items-center justify-between bg-gray-700/30 p-3 rounded-lg">
                            <div className="flex-1">
                                <span className="text-gray-300">{item.query}</span>
                                <p className="text-gray-500 text-xs mt-1">{item.category}</p>
                            </div>
                            <span className="text-green-400 font-semibold ml-3">{item.count}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
