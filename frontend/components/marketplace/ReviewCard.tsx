'use client';

import React from 'react';
import { Star } from 'lucide-react';

interface ReviewCardProps {
    review: {
        id: number;
        client_name: string;
        rating: number;
        comment: string;
        created_at: string;
        service_type?: string;
    };
}

export default function ReviewCard({ review }: ReviewCardProps) {
    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        const now = new Date();
        const diffInDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));

        if (diffInDays === 0) {
            return 'Today';
        } else if (diffInDays === 1) {
            return 'Yesterday';
        } else if (diffInDays < 7) {
            return `${diffInDays} days ago`;
        } else if (diffInDays < 30) {
            const weeks = Math.floor(diffInDays / 7);
            return `${weeks} ${weeks === 1 ? 'week' : 'weeks'} ago`;
        } else if (diffInDays < 365) {
            const months = Math.floor(diffInDays / 30);
            return `${months} ${months === 1 ? 'month' : 'months'} ago`;
        } else {
            const years = Math.floor(diffInDays / 365);
            return `${years} ${years === 1 ? 'year' : 'years'} ago`;
        }
    };

    const renderStars = (rating: number) => {
        return (
            <div className="flex items-center gap-1">
                {[1, 2, 3, 4, 5].map((star) => (
                    <Star
                        key={star}
                        className={`w-4 h-4 ${star <= rating
                                ? 'fill-yellow-400 text-yellow-400'
                                : 'text-gray-300 dark:text-gray-600'
                            }`}
                    />
                ))}
            </div>
        );
    };

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            {/* Header */}
            <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                        {/* Avatar */}
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-semibold">
                            {review.client_name.charAt(0).toUpperCase()}
                        </div>
                        <div>
                            <h4 className="font-semibold text-gray-900 dark:text-white">
                                {review.client_name}
                            </h4>
                            <p className="text-sm text-gray-500 dark:text-gray-400">
                                {formatDate(review.created_at)}
                            </p>
                        </div>
                    </div>
                </div>
                {renderStars(review.rating)}
            </div>

            {/* Service Type */}
            {review.service_type && (
                <div className="mb-3">
                    <span className="inline-block px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded-full">
                        {review.service_type}
                    </span>
                </div>
            )}

            {/* Comment */}
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                {review.comment}
            </p>
        </div>
    );
}
