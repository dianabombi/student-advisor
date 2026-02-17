'use client';

import { useEffect, useState } from 'react';
import { Search, Eye, Edit, Building2, ChevronLeft, Globe } from 'lucide-react';
import Link from 'next/link';

interface University {
    id: number;
    name: string;
    country: string;
    city: string;
    type: string;
    website: string;
    created_at: string;
}

interface UniversitiesResponse {
    universities: University[];
    total: number;
    page: number;
    limit: number;
}

interface UniversityStats {
    total: number;
    by_country: { [key: string]: number };
    by_type: { [key: string]: number };
}

export default function UniversitiesPage() {
    const [universities, setUniversities] = useState<University[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [totalUniversities, setTotalUniversities] = useState(0);
    const [countryFilter, setCountryFilter] = useState('');
    const [stats, setStats] = useState<UniversityStats | null>(null);
    const limit = 50;

    useEffect(() => {
        fetchStats();
    }, []);

    useEffect(() => {
        fetchUniversities();
    }, [currentPage, countryFilter]);

    const fetchStats = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) return;

            const response = await fetch(
                '/api/admin/universities/stats',
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );

            if (response.ok) {
                const data = await response.json();
                setStats(data);
            }
        } catch (error) {
            console.error('Failed to fetch stats:', error);
        }
    };

    const fetchUniversities = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) return;

            setLoading(true);
            const response = await fetch(
                `/api/admin/universities?page=${currentPage}&limit=${limit}`,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );

            if (response.ok) {
                const data: UniversitiesResponse = await response.json();
                setUniversities(data.universities);
                setTotalUniversities(data.total);
            }
        } catch (error) {
            console.error('Failed to fetch universities:', error);
        } finally {
            setLoading(false);
        }
    };

    const filteredUniversities = universities.filter(uni => {
        const matchesSearch = uni.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            uni.city.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesCountry = !countryFilter || uni.country === countryFilter;
        return matchesSearch && matchesCountry;
    });

    const totalPages = Math.ceil(totalUniversities / limit);

    const getTypeBadgeColor = (type: string) => {
        switch (type) {
            case 'university':
                return 'bg-blue-900/50 text-blue-300 border-blue-700';
            case 'vocational_school':
                return 'bg-green-900/50 text-green-300 border-green-700';
            case 'language_school':
                return 'bg-purple-900/50 text-purple-300 border-purple-700';
            case 'conservatory':
                return 'bg-pink-900/50 text-pink-300 border-pink-700';
            case 'foundation_program':
                return 'bg-orange-900/50 text-orange-300 border-orange-700';
            default:
                return 'bg-gray-900/50 text-gray-300 border-gray-700';
        }
    };

    const getTypeLabel = (type: string) => {
        return type.split('_').map(word =>
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    };

    const getCountryFlag = (countryCode: string) => {
        const flags: { [key: string]: string } = {
            'SK': '🇸🇰', 'CZ': '🇨🇿', 'PL': '🇵🇱', 'HU': '🇭🇺',
            'AT': '🇦🇹', 'DE': '🇩🇪', 'SI': '🇸🇮', 'HR': '🇭🇷',
            'RO': '🇷🇴', 'BG': '🇧🇬', 'LT': '🇱🇹', 'LV': '🇱🇻',
            'EE': '🇪🇪', 'NL': '🇳🇱', 'BE': '🇧🇪', 'LU': '🇱🇺',
            'LI': '🇱🇮', 'SE': '🇸🇪'
        };
        return flags[countryCode] || '🏳️';
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <Link
                        href="/admin/dashboard"
                        className="p-2 hover:bg-gray-800 rounded-lg transition-colors text-gray-400 hover:text-white"
                    >
                        <ChevronLeft className="w-5 h-5" />
                    </Link>
                    <div>
                        <h1 className="text-3xl font-bold text-white">Universities Management</h1>
                        <p className="text-gray-400 mt-2">Manage educational institutions across Europe</p>
                    </div>
                </div>
                <div className="text-gray-400">
                    Total: <span className="text-white font-semibold">{stats?.total || 0}</span> institutions
                </div>
            </div>

            {/* Stats Cards */}
            {stats && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
                        <div className="flex items-center gap-3">
                            <div className="p-3 bg-blue-900/50 rounded-lg">
                                <Building2 className="w-6 h-6 text-blue-400" />
                            </div>
                            <div>
                                <p className="text-gray-400 text-sm">Universities</p>
                                <p className="text-white text-2xl font-bold">{stats.by_type.university || 0}</p>
                            </div>
                        </div>
                    </div>
                    <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
                        <div className="flex items-center gap-3">
                            <div className="p-3 bg-green-900/50 rounded-lg">
                                <Building2 className="w-6 h-6 text-green-400" />
                            </div>
                            <div>
                                <p className="text-gray-400 text-sm">Vocational Schools</p>
                                <p className="text-white text-2xl font-bold">{stats.by_type.vocational_school || 0}</p>
                            </div>
                        </div>
                    </div>
                    <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
                        <div className="flex items-center gap-3">
                            <div className="p-3 bg-purple-900/50 rounded-lg">
                                <Globe className="w-6 h-6 text-purple-400" />
                            </div>
                            <div>
                                <p className="text-gray-400 text-sm">Countries</p>
                                <p className="text-white text-2xl font-bold">{Object.keys(stats.by_country).length}</p>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Filters */}
            <div className="bg-gray-800 rounded-xl p-4 border border-gray-700 space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Search */}
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                        <input
                            type="text"
                            placeholder="Search by name or city..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-full pl-10 pr-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
                        />
                    </div>

                    {/* Country Filter */}
                    <select
                        value={countryFilter}
                        onChange={(e) => {
                            setCountryFilter(e.target.value);
                            setCurrentPage(1);
                        }}
                        className="px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500 transition-colors"
                    >
                        <option value="">All Countries</option>
                        {stats && Object.keys(stats.by_country).sort().map(country => (
                            <option key={country} value={country}>
                                {getCountryFlag(country)} {country} ({stats.by_country[country]})
                            </option>
                        ))}
                    </select>
                </div>
            </div>

            {/* Universities Table */}
            <div className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
                {loading ? (
                    <div className="p-12 text-center">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                        <p className="mt-4 text-gray-400">Loading universities...</p>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead className="bg-gray-900 border-b border-gray-700">
                                <tr>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">
                                        Institution
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">
                                        Location
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">
                                        Type
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">
                                        Website
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-700">
                                {filteredUniversities.map((uni) => (
                                    <tr key={uni.id} className="hover:bg-gray-700/50 transition-colors">
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-3">
                                                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold">
                                                    {uni.name.charAt(0)}
                                                </div>
                                                <div>
                                                    <div className="text-white font-medium">{uni.name}</div>
                                                    <div className="text-gray-400 text-sm">ID: {uni.id}</div>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-2">
                                                <span className="text-2xl">{getCountryFlag(uni.country)}</span>
                                                <div>
                                                    <div className="text-white">{uni.city}</div>
                                                    <div className="text-gray-400 text-sm">{uni.country}</div>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getTypeBadgeColor(uni.type)}`}>
                                                {getTypeLabel(uni.type)}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            {uni.website ? (
                                                <a
                                                    href={uni.website}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    className="text-blue-400 hover:text-blue-300 text-sm flex items-center gap-1"
                                                >
                                                    <Globe className="w-4 h-4" />
                                                    Visit
                                                </a>
                                            ) : (
                                                <span className="text-gray-500 text-sm">N/A</span>
                                            )}
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-2">
                                                <button
                                                    onClick={() => window.location.href = `/admin/universities/${uni.id}`}
                                                    className="p-2 hover:bg-gray-600 rounded-lg transition-colors text-blue-400 hover:text-blue-300"
                                                    title="View Details"
                                                >
                                                    <Eye className="w-4 h-4" />
                                                </button>
                                                <button
                                                    onClick={() => window.location.href = `/admin/universities/${uni.id}/edit`}
                                                    className="p-2 hover:bg-gray-600 rounded-lg transition-colors text-green-400 hover:text-green-300"
                                                    title="Edit"
                                                >
                                                    <Edit className="w-4 h-4" />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                        {filteredUniversities.length === 0 && (
                            <div className="p-12 text-center text-gray-400">
                                No universities found
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
                <div className="flex items-center justify-between bg-gray-800 rounded-xl p-4 border border-gray-700">
                    <div className="text-gray-400">
                        Page {currentPage} of {totalPages}
                    </div>
                    <div className="flex gap-2">
                        <button
                            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                            disabled={currentPage === 1}
                            className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            Previous
                        </button>
                        <button
                            onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                            disabled={currentPage === totalPages}
                            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            Next
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
