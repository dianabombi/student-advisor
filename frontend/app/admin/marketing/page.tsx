'use client';

import { useState } from 'react';
import {
    TrendingUp,
    Users,
    Target,
    DollarSign,
    ArrowUpRight,
    ArrowDownRight,
} from 'lucide-react';
import {
    PieChart,
    Pie,
    Cell,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from 'recharts';

export default function MarketingPage() {
    const [selectedPeriod, setSelectedPeriod] = useState<string>('30d');

    // Mock data - traffic sources
    const trafficSources = [
        { name: 'Google Ads', value: 3500, color: '#3b82f6' },
        { name: 'Facebook', value: 2800, color: '#8b5cf6' },
        { name: 'Email', value: 2200, color: '#10b981' },
        { name: 'Direct', value: 1800, color: '#f59e0b' },
        { name: 'Organic', value: 1500, color: '#ef4444' },
        { name: 'Referral', value: 1200, color: '#ec4899' },
    ];

    // Mock data - performance trend
    const performanceTrend = [
        { date: 'Jan 1', visits: 1200, conversions: 45 },
        { date: 'Jan 8', visits: 1450, conversions: 52 },
        { date: 'Jan 15', visits: 1680, conversions: 61 },
        { date: 'Jan 22', visits: 1920, conversions: 68 },
        { date: 'Jan 29', visits: 2100, conversions: 75 },
        { date: 'Feb 5', visits: 2350, conversions: 84 },
        { date: 'Feb 12', visits: 2580, conversions: 91 },
    ];

    // Mock data - campaigns
    const campaigns = [
        {
            id: 1,
            name: 'Spring Enrollment 2024',
            source: 'Google',
            medium: 'CPC',
            visits: 4520,
            conversions: 156,
            conversionRate: 3.45,
            revenue: 78000,
            cost: 12500,
            roi: 524,
            cac: 80.13,
        },
        {
            id: 2,
            name: 'Facebook Student Campaign',
            source: 'Facebook',
            medium: 'Social',
            visits: 3890,
            conversions: 128,
            conversionRate: 3.29,
            revenue: 64000,
            cost: 9800,
            roi: 553,
            cac: 76.56,
        },
        {
            id: 3,
            name: 'Email Newsletter Q1',
            source: 'Email',
            medium: 'Email',
            visits: 2650,
            conversions: 98,
            conversionRate: 3.70,
            revenue: 49000,
            cost: 1200,
            roi: 3983,
            cac: 12.24,
        },
        {
            id: 4,
            name: 'LinkedIn Professional',
            source: 'LinkedIn',
            medium: 'Social',
            visits: 1820,
            conversions: 67,
            conversionRate: 3.68,
            revenue: 33500,
            cost: 8900,
            roi: 276,
            cac: 132.84,
        },
        {
            id: 5,
            name: 'Instagram Stories',
            source: 'Instagram',
            medium: 'Social',
            visits: 2980,
            conversions: 89,
            conversionRate: 2.99,
            revenue: 44500,
            cost: 6700,
            roi: 564,
            cac: 75.28,
        },
    ];

    // Calculate metrics
    const totalVisits = campaigns.reduce((sum, c) => sum + c.visits, 0);
    const totalConversions = campaigns.reduce((sum, c) => sum + c.conversions, 0);
    const avgROI = campaigns.reduce((sum, c) => sum + c.roi, 0) / campaigns.length;
    const avgCAC = campaigns.reduce((sum, c) => sum + c.cac, 0) / campaigns.length;

    const periods = [
        { value: '7d', label: '7 days' },
        { value: '30d', label: '30 days' },
        { value: '90d', label: '90 days' },
        { value: '1y', label: '1 year' },
        { value: 'all', label: 'All time' },
    ];

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                        <TrendingUp className="w-8 h-8 text-blue-400" />
                        Marketing & Acquisition
                    </h1>
                    <p className="text-gray-400 mt-2">UTM Tracking Dashboard - Traffic Sources and ROI Analytics</p>
                </div>

                {/* Period Selector */}
                <div className="flex gap-2">
                    {periods.map((period) => (
                        <button
                            key={period.value}
                            onClick={() => setSelectedPeriod(period.value)}
                            className={`px-4 py-2 rounded-lg font-medium transition-colors ${selectedPeriod === period.value
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                                }`}
                        >
                            {period.label}
                        </button>
                    ))}
                </div>
            </div>

            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                    <div className="flex items-center justify-between mb-2">
                        <p className="text-gray-400 text-sm">Total Visits</p>
                        <Users className="w-5 h-5 text-blue-400" />
                    </div>
                    <p className="text-3xl font-bold text-white">{totalVisits.toLocaleString()}</p>
                    <div className="flex items-center gap-1 mt-2">
                        <ArrowUpRight className="w-4 h-4 text-green-400" />
                        <span className="text-green-400 text-sm">+12.5%</span>
                    </div>
                </div>

                <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                    <div className="flex items-center justify-between mb-2">
                        <p className="text-gray-400 text-sm">Conversions</p>
                        <Target className="w-5 h-5 text-green-400" />
                    </div>
                    <p className="text-3xl font-bold text-white">{totalConversions}</p>
                    <div className="flex items-center gap-1 mt-2">
                        <ArrowUpRight className="w-4 h-4 text-green-400" />
                        <span className="text-green-400 text-sm">+8.3%</span>
                    </div>
                </div>

                <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                    <div className="flex items-center justify-between mb-2">
                        <p className="text-gray-400 text-sm">ROI</p>
                        <TrendingUp className="w-5 h-5 text-purple-400" />
                    </div>
                    <p className="text-3xl font-bold text-white">{avgROI.toFixed(0)}%</p>
                    <div className="flex items-center gap-1 mt-2">
                        <ArrowUpRight className="w-4 h-4 text-green-400" />
                        <span className="text-green-400 text-sm">+15.2%</span>
                    </div>
                </div>

                <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                    <div className="flex items-center justify-between mb-2">
                        <p className="text-gray-400 text-sm">CAC</p>
                        <DollarSign className="w-5 h-5 text-yellow-400" />
                    </div>
                    <p className="text-3xl font-bold text-white">${avgCAC.toFixed(0)}</p>
                    <div className="flex items-center gap-1 mt-2">
                        <ArrowDownRight className="w-4 h-4 text-green-400" />
                        <span className="text-green-400 text-sm">-5.7%</span>
                    </div>
                </div>
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Traffic Sources Pie Chart */}
                <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                    <h3 className="text-lg font-bold text-white mb-4">Traffic Sources</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                            <Pie
                                data={trafficSources}
                                cx="50%"
                                cy="50%"
                                labelLine={false}
                                label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
                                outerRadius={100}
                                fill="#8884d8"
                                dataKey="value"
                            >
                                {trafficSources.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={entry.color} />
                                ))}
                            </Pie>
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: '#1f2937',
                                    border: '1px solid #374151',
                                    borderRadius: '8px',
                                    color: '#fff'
                                }}
                            />
                        </PieChart>
                    </ResponsiveContainer>
                </div>

                {/* Performance Trend Line Chart */}
                <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                    <h3 className="text-lg font-bold text-white mb-4">Performance Trend</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={performanceTrend}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                            <XAxis dataKey="date" stroke="#9ca3af" />
                            <YAxis stroke="#9ca3af" />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: '#1f2937',
                                    border: '1px solid #374151',
                                    borderRadius: '8px',
                                    color: '#fff'
                                }}
                            />
                            <Legend />
                            <Line type="monotone" dataKey="visits" stroke="#3b82f6" name="Visits" />
                            <Line type="monotone" dataKey="conversions" stroke="#10b981" name="Conversions" />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>

            {/* Campaigns Table */}
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                <h3 className="text-lg font-bold text-white mb-4">Active Campaigns</h3>
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead>
                            <tr className="border-b border-gray-700">
                                <th className="text-left py-3 px-4 text-gray-400 font-medium">Campaign Name</th>
                                <th className="text-left py-3 px-4 text-gray-400 font-medium">Source</th>
                                <th className="text-right py-3 px-4 text-gray-400 font-medium">Visits</th>
                                <th className="text-right py-3 px-4 text-gray-400 font-medium">Conversions</th>
                                <th className="text-right py-3 px-4 text-gray-400 font-medium">Conversion %</th>
                                <th className="text-right py-3 px-4 text-gray-400 font-medium">Revenue</th>
                                <th className="text-right py-3 px-4 text-gray-400 font-medium">Cost</th>
                                <th className="text-right py-3 px-4 text-gray-400 font-medium">ROI %</th>
                                <th className="text-right py-3 px-4 text-gray-400 font-medium">CAC</th>
                            </tr>
                        </thead>
                        <tbody>
                            {campaigns.map((campaign) => (
                                <tr key={campaign.id} className="border-b border-gray-700 hover:bg-gray-700/50 transition-colors">
                                    <td className="py-3 px-4">
                                        <div className="flex items-center gap-2">
                                            <span className="text-white font-medium">{campaign.name}</span>
                                        </div>
                                    </td>
                                    <td className="py-3 px-4">
                                        <span className="text-gray-300">{campaign.source}</span>
                                        <span className="text-gray-500 text-sm ml-1">/ {campaign.medium}</span>
                                    </td>
                                    <td className="py-3 px-4 text-right text-gray-300">{campaign.visits.toLocaleString()}</td>
                                    <td className="py-3 px-4 text-right text-gray-300">{campaign.conversions}</td>
                                    <td className="py-3 px-4 text-right">
                                        <span className="text-green-400 font-medium">{campaign.conversionRate.toFixed(2)}%</span>
                                    </td>
                                    <td className="py-3 px-4 text-right text-gray-300">${campaign.revenue.toLocaleString()}</td>
                                    <td className="py-3 px-4 text-right text-gray-300">${campaign.cost.toLocaleString()}</td>
                                    <td className="py-3 px-4 text-right">
                                        <span className={`font-medium ${campaign.roi > 200 ? 'text-green-400' : campaign.roi > 100 ? 'text-yellow-400' : 'text-red-400'}`}>
                                            {campaign.roi.toFixed(1)}%
                                        </span>
                                    </td>
                                    <td className="py-3 px-4 text-right text-gray-300">${campaign.cac.toFixed(2)}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
