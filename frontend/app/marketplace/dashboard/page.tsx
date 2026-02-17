'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import '@/lib/i18n'; // Initialize i18next
import { useTranslation } from 'react-i18next';
import { useAuth } from '@/contexts/AuthContext';
import {
    Star, TrendingUp, Users, DollarSign, Calendar, Clock, CheckCircle, XCircle, Edit
} from 'lucide-react';
import Navigation from '@/components/Navigation';
import { getLawyerDashboard, updateLawyerAvailability } from '@/lib/marketplaceService';

export default function LawyerDashboardPage() {
    const router = useRouter();
    const { t } = useTranslation('common');
    const { user, isAuthenticated } = useAuth();
    const [dashboard, setDashboard] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [updatingAvailability, setUpdatingAvailability] = useState(false);

    useEffect(() => {
        fetchDashboard();
    }, []);

    const fetchDashboard = async () => {
        try {
            const data = await getLawyerDashboard();
            setDashboard(data);
        } catch (err) {
            console.error('Error fetching dashboard:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleToggleAvailability = async () => {
        setUpdatingAvailability(true);
        try {
            await updateLawyerAvailability(!dashboard.is_available);
            setDashboard((prev: any) => ({ ...prev, is_available: !prev.is_available }));
        } catch (err) {
            console.error('Error updating availability:', err);
        } finally {
            setUpdatingAvailability(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
                <div className="text-gray-600 dark:text-gray-400">Loading...</div>
            </div>
        );
    }

    if (!dashboard) {
        return (
            <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
                <div className="text-center">
                    <p className="text-gray-600 dark:text-gray-400 mb-4">
                        You are not registered as a lawyer yet.
                    </p>
                    <a
                        href="/marketplace/register"
                        className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg inline-block"
                    >
                        Register as Lawyer
                    </a>
                </div>
            </div>
        );
    }

    return (
        <>
            <Navigation />
            <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    {/* Header */}
                    <div className="mb-8">
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                            {t('marketplace.dashboard.dashboardTitle')}
                        </h1>
                        <p className="text-gray-600 dark:text-gray-400">
                            {t('marketplace.dashboard.welcome', { name: user?.name })}
                        </p>
                    </div>

                    {/* Stats Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                        {/* Rating */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-sm text-gray-600 dark:text-gray-400">
                                    {t('marketplace.dashboard.stats.rating')}
                                </span>
                                <Star className="w-5 h-5 text-yellow-400" />
                            </div>
                            <div className="text-3xl font-bold text-gray-900 dark:text-white">
                                {dashboard.rating?.toFixed(1) || 'N/A'}
                            </div>
                        </div>

                        {/* Reviews */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-sm text-gray-600 dark:text-gray-400">
                                    {t('marketplace.dashboard.stats.reviews')}
                                </span>
                                <Users className="w-5 h-5 text-blue-500" />
                            </div>
                            <div className="text-3xl font-bold text-gray-900 dark:text-white">
                                {dashboard.total_reviews || 0}
                            </div>
                        </div>

                        {/* Active Orders */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-sm text-gray-600 dark:text-gray-400">
                                    {t('marketplace.dashboard.stats.activeOrders')}
                                </span>
                                <Clock className="w-5 h-5 text-orange-500" />
                            </div>
                            <div className="text-3xl font-bold text-gray-900 dark:text-white">
                                {dashboard.active_orders || 0}
                            </div>
                        </div>

                        {/* Completed Orders */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-sm text-gray-600 dark:text-gray-400">
                                    {t('marketplace.dashboard.stats.completedOrders')}
                                </span>
                                <CheckCircle className="w-5 h-5 text-green-500" />
                            </div>
                            <div className="text-3xl font-bold text-gray-900 dark:text-white">
                                {dashboard.completed_orders || 0}
                            </div>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        {/* Left Column - Profile & Availability */}
                        <div className="lg:col-span-2 space-y-6">
                            {/* Availability Card */}
                            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                                    {t('marketplace.dashboard.availability.title')}
                                </h2>
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-gray-700 dark:text-gray-300 mb-2">
                                            {dashboard.is_available
                                                ? t('marketplace.dashboard.availability.available')
                                                : t('marketplace.dashboard.availability.unavailable')
                                            }
                                        </p>
                                        <p className="text-sm text-gray-600 dark:text-gray-400">
                                            {dashboard.is_available
                                                ? 'Clients can book consultations with you'
                                                : 'You are not accepting new consultations'
                                            }
                                        </p>
                                    </div>
                                    <button
                                        onClick={handleToggleAvailability}
                                        disabled={updatingAvailability}
                                        className={`px-6 py-3 rounded-lg font-medium transition ${dashboard.is_available
                                            ? 'bg-green-600 hover:bg-green-700 text-white'
                                            : 'bg-gray-600 hover:bg-gray-700 text-white'
                                            } disabled:opacity-50`}
                                    >
                                        {updatingAvailability
                                            ? 'Updating...'
                                            : t('marketplace.dashboard.availability.toggle')
                                        }
                                    </button>
                                </div>
                            </div>

                            {/* Profile Card */}
                            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                                <div className="flex items-center justify-between mb-4">
                                    <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                                        {t('marketplace.dashboard.profile.title')}
                                    </h2>
                                    <a
                                        href={`/marketplace/lawyers/${dashboard.id}`}
                                        className="flex items-center gap-2 text-blue-600 hover:text-blue-700"
                                    >
                                        <Edit className="w-4 h-4" />
                                        {t('marketplace.dashboard.profile.edit')}
                                    </a>
                                </div>

                                <div className="space-y-4">
                                    <div>
                                        <span className="text-sm text-gray-600 dark:text-gray-400">Full Name:</span>
                                        <p className="font-medium text-gray-900 dark:text-white">{dashboard.full_name}</p>
                                    </div>

                                    {dashboard.title && (
                                        <div>
                                            <span className="text-sm text-gray-600 dark:text-gray-400">Title:</span>
                                            <p className="font-medium text-gray-900 dark:text-white">{dashboard.title}</p>
                                        </div>
                                    )}

                                    <div>
                                        <span className="text-sm text-gray-600 dark:text-gray-400">Experience:</span>
                                        <p className="font-medium text-gray-900 dark:text-white">
                                            {dashboard.experience_years} years
                                        </p>
                                    </div>

                                    <div>
                                        <span className="text-sm text-gray-600 dark:text-gray-400">Specializations:</span>
                                        <div className="flex flex-wrap gap-2 mt-1">
                                            {dashboard.specializations?.map((spec: string, index: number) => (
                                                <span
                                                    key={index}
                                                    className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded-full"
                                                >
                                                    {t(`marketplace.specializations.${spec}`)}
                                                </span>
                                            ))}
                                        </div>
                                    </div>

                                    <div>
                                        <span className="text-sm text-gray-600 dark:text-gray-400">Jurisdictions:</span>
                                        <p className="font-medium text-gray-900 dark:text-white">
                                            {dashboard.jurisdictions?.join(', ')}
                                        </p>
                                    </div>

                                    {dashboard.hourly_rate && (
                                        <div>
                                            <span className="text-sm text-gray-600 dark:text-gray-400">Hourly Rate:</span>
                                            <p className="font-medium text-gray-900 dark:text-white">€{dashboard.hourly_rate}/hr</p>
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* Recent Orders */}
                            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                                    {t('marketplace.dashboard.orders.title')}
                                </h2>

                                {dashboard.recent_orders && dashboard.recent_orders.length > 0 ? (
                                    <div className="space-y-3">
                                        {dashboard.recent_orders.map((order: any) => (
                                            <div
                                                key={order.id}
                                                className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700 transition"
                                            >
                                                <div className="flex items-center justify-between mb-2">
                                                    <span className="font-medium text-gray-900 dark:text-white">
                                                        {order.client_name}
                                                    </span>
                                                    <span className={`px-2 py-1 rounded-full text-xs ${order.status === 'active'
                                                        ? 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
                                                        : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                                                        }`}>
                                                        {order.status}
                                                    </span>
                                                </div>
                                                <p className="text-sm text-gray-600 dark:text-gray-400">
                                                    {order.service_type} - €{order.amount}
                                                </p>
                                            </div>
                                        ))}
                                    </div>
                                ) : (
                                    <p className="text-gray-600 dark:text-gray-400 text-center py-8">
                                        {t('marketplace.dashboard.orders.noOrders')}
                                    </p>
                                )}

                                {dashboard.recent_orders && dashboard.recent_orders.length > 0 && (
                                    <button className="w-full mt-4 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700">
                                        {t('marketplace.dashboard.orders.viewAll')}
                                    </button>
                                )}
                            </div>
                        </div>

                        {/* Right Column - Quick Stats */}
                        <div className="space-y-6">
                            {/* Verification Status */}
                            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                                    Verification Status
                                </h3>
                                <div className="flex items-center gap-3">
                                    {dashboard.is_verified ? (
                                        <>
                                            <CheckCircle className="w-6 h-6 text-green-500" />
                                            <div>
                                                <p className="font-medium text-green-700 dark:text-green-400">Verified</p>
                                                <p className="text-sm text-gray-600 dark:text-gray-400">
                                                    Your profile is verified
                                                </p>
                                            </div>
                                        </>
                                    ) : (
                                        <>
                                            <Clock className="w-6 h-6 text-orange-500" />
                                            <div>
                                                <p className="font-medium text-orange-700 dark:text-orange-400">Pending</p>
                                                <p className="text-sm text-gray-600 dark:text-gray-400">
                                                    Awaiting admin verification
                                                </p>
                                            </div>
                                        </>
                                    )}
                                </div>
                            </div>

                            {/* Quick Actions */}
                            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                                    Quick Actions
                                </h3>
                                <div className="space-y-2">
                                    <a
                                        href={`/marketplace/lawyers/${dashboard.id}`}
                                        className="block w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-center rounded-lg transition"
                                    >
                                        View Public Profile
                                    </a>
                                    <button className="block w-full px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg transition">
                                        Update Profile
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}
