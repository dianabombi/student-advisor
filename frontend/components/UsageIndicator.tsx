'use client';

import { useEffect, useState } from 'react';
import { AlertCircle, TrendingUp } from 'lucide-react';

interface UsageData {
    used: number;
    limit: number;
    remaining: number;
    usage_percent: number;
    reset_date: string;
    warning: string | null;
}

export default function UsageIndicator() {
    const [usage, setUsage] = useState<UsageData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchUsage();
    }, []);

    const fetchUsage = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/usage', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                setUsage(data);
            }
        } catch (error) {
            console.error('Failed to load usage:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading || !usage) return null;

    const percent = usage.usage_percent;
    const getColor = () => {
        if (percent >= 90) return 'bg-red-500';
        if (percent >= 80) return 'bg-yellow-500';
        return 'bg-green-500';
    };

    const getTextColor = () => {
        if (percent >= 90) return 'text-red-600';
        if (percent >= 80) return 'text-yellow-600';
        return 'text-green-600';
    };

    const formatResetDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('uk-UA', { day: 'numeric', month: 'long', year: 'numeric' });
    };

    return (
        <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl p-4 mb-4">
            <div className="flex justify-between items-center mb-2">
                <div className="flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-purple-400" />
                    <span className="text-sm text-gray-300">Використано запитів</span>
                </div>
                <span className={`text-sm font-semibold ${getTextColor()}`}>
                    {usage.used} / {usage.limit}
                </span>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-gray-700 rounded-full h-2 mb-2">
                <div
                    className={`h-2 rounded-full transition-all duration-300 ${getColor()}`}
                    style={{ width: `${Math.min(percent, 100)}%` }}
                />
            </div>

            {/* Warning Message */}
            {usage.warning && (
                <div className="mt-3 flex items-start gap-2 bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3">
                    <AlertCircle className="w-4 h-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-yellow-200">{usage.warning}</p>
                </div>
            )}

            {/* Reset Date */}
            <div className="mt-2 text-xs text-gray-400">
                Оновлення: {formatResetDate(usage.reset_date)}
            </div>
        </div>
    );
}
