'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { AlertCircle, Clock, X } from 'lucide-react';

export default function SubscriptionBanner() {
    const { user } = useAuth();
    const [daysRemaining, setDaysRemaining] = useState<number>(0);
    const [isVisible, setIsVisible] = useState(true);

    useEffect(() => {
        if (user?.trial_end_date) {
            const endDate = new Date(user.trial_end_date);
            const now = new Date();
            const diffTime = endDate.getTime() - now.getTime();
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            setDaysRemaining(Math.max(0, diffDays));
        }
    }, [user]);

    // Don't show banner if user has active paid subscription
    if (user?.subscription_status === 'active') {
        return null;
    }

    // Don't show if user manually closed it
    if (!isVisible) {
        return null;
    }

    // Determine banner style based on days remaining
    const getBannerStyle = () => {
        if (daysRemaining === 0) {
            return 'bg-red-50 border-red-200 text-red-800';
        } else if (daysRemaining <= 3) {
            return 'bg-yellow-50 border-yellow-200 text-yellow-800';
        } else {
            return 'bg-blue-50 border-blue-200 text-blue-800';
        }
    };

    const getIcon = () => {
        if (daysRemaining === 0) {
            return <AlertCircle className="w-5 h-5 text-red-600" />;
        }
        return <Clock className="w-5 h-5 text-blue-600" />;
    };

    const getMessage = () => {
        if (daysRemaining === 0) {
            return 'Váš skúšobný obdobie skončilo. Prosím, vyberte si predplatné pre pokračovanie.';
        } else if (daysRemaining === 1) {
            return `Zostáva ${daysRemaining} deň skúšobného obdobia. Nezabudnite si vybrať predplatné!`;
        } else if (daysRemaining <= 4) {
            return `Zostávajú ${daysRemaining} dni skúšobného obdobia. Vyberte si predplatné včas!`;
        } else {
            return `Máte ${daysRemaining} dní bezplatného skúšobného obdobia.`;
        }
    };

    return (
        <div className={`border-b ${getBannerStyle()} transition-all duration-300`}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        {getIcon()}
                        <p className="text-sm font-medium">
                            {getMessage()}
                        </p>
                    </div>
                    <div className="flex items-center space-x-4">
                        {daysRemaining <= 3 && (
                            <a
                                href="/#subscription"
                                className="text-sm font-semibold underline hover:no-underline"
                            >
                                Vybrať predplatné
                            </a>
                        )}
                        <button
                            onClick={() => setIsVisible(false)}
                            className="text-gray-400 hover:text-gray-600"
                        >
                            <X className="w-4 h-4" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
