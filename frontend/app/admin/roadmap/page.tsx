'use client';

import { useLanguage } from '@/lib/LanguageContext';
import {
    TrendingUp,
    Users,
    Mail,
    Gift,
    Bot,
    Bell,
    DollarSign,
    Building2,
    FileText,
    CheckCircle2,
    MessageSquare,
    BarChart3,
    Target,
    TestTube,
    Sparkles,
    Smartphone,
    Shield,
    Lightbulb,
    Circle,
    CheckCircle,
    Clock
} from 'lucide-react';
import { useState } from 'react';

interface RoadmapItem {
    id: number;
    category: string;
    title: string;
    description: string;
    priority: 'high' | 'medium' | 'low';
    status: 'planned' | 'in-progress' | 'completed';
    icon: React.ComponentType<{ className?: string }>;
    estimatedTime: string;
    benefits: string[];
}

export default function RoadmapPage() {
    const { t } = useLanguage();
    const [filter, setFilter] = useState<'all' | 'planned' | 'in-progress' | 'completed'>('all');

    const roadmapItems: RoadmapItem[] = [
        // Аналітика та Insights
        {
            id: 1,
            category: t('roadmap.categories.analytics'),
            title: t('roadmap.items.conversionFunnel.title'),
            description: t('roadmap.items.conversionFunnel.description'),
            priority: 'high',
            status: 'planned',
            icon: TrendingUp,
            estimatedTime: '2-3 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.conversionFunnel.benefits.0'),
                t('roadmap.items.conversionFunnel.benefits.1'),
                t('roadmap.items.conversionFunnel.benefits.2'),
            ],
        },
        {
            id: 2,
            category: t('roadmap.categories.analytics'),
            title: t('roadmap.items.cohortAnalysis.title'),
            description: t('roadmap.items.cohortAnalysis.description'),
            priority: 'high',
            status: 'planned',
            icon: Users,
            estimatedTime: '2-3 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.cohortAnalysis.benefits.0'),
                t('roadmap.items.cohortAnalysis.benefits.1'),
                t('roadmap.items.cohortAnalysis.benefits.2'),
            ],
        },
        {
            id: 3,
            category: t('roadmap.categories.analytics'),
            title: t('roadmap.items.heatmaps.title'),
            description: t('roadmap.items.heatmaps.description'),
            priority: 'medium',
            status: 'planned',
            icon: Target,
            estimatedTime: '3-4 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.heatmaps.benefits.0'),
                t('roadmap.items.heatmaps.benefits.1'),
                t('roadmap.items.heatmaps.benefits.2'),
            ],
        },

        // Маркетинг та Залучення
        {
            id: 4,
            category: t('roadmap.categories.marketing'),
            title: t('roadmap.items.utmTracking.title'),
            description: t('roadmap.items.utmTracking.description'),
            priority: 'high',
            status: 'planned',
            icon: BarChart3,
            estimatedTime: '1-2 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.utmTracking.benefits.0'),
                t('roadmap.items.utmTracking.benefits.1'),
                t('roadmap.items.utmTracking.benefits.2'),
            ],
        },
        {
            id: 5,
            category: t('roadmap.categories.marketing'),
            title: t('roadmap.items.emailCampaigns.title'),
            description: t('roadmap.items.emailCampaigns.description'),
            priority: 'medium',
            status: 'planned',
            icon: Mail,
            estimatedTime: '3-4 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.emailCampaigns.benefits.0'),
                t('roadmap.items.emailCampaigns.benefits.1'),
                t('roadmap.items.emailCampaigns.benefits.2'),
            ],
        },
        {
            id: 6,
            category: t('roadmap.categories.marketing'),
            title: t('roadmap.items.referralProgram.title'),
            description: t('roadmap.items.referralProgram.description'),
            priority: 'medium',
            status: 'planned',
            icon: Gift,
            estimatedTime: '2-3 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.referralProgram.benefits.0'),
                t('roadmap.items.referralProgram.benefits.1'),
                t('roadmap.items.referralProgram.benefits.2'),
            ],
        },

        // AI та Автоматизація
        {
            id: 7,
            category: t('roadmap.categories.ai'),
            title: t('roadmap.items.aiPerformance.title'),
            description: t('roadmap.items.aiPerformance.description'),
            priority: 'high',
            status: 'planned',
            icon: Bot,
            estimatedTime: '2-3 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.aiPerformance.benefits.0'),
                t('roadmap.items.aiPerformance.benefits.1'),
                t('roadmap.items.aiPerformance.benefits.2'),
            ],
        },
        {
            id: 8,
            category: t('roadmap.categories.ai'),
            title: t('roadmap.items.automatedAlerts.title'),
            description: t('roadmap.items.automatedAlerts.description'),
            priority: 'medium',
            status: 'planned',
            icon: Bell,
            estimatedTime: '1-2 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.automatedAlerts.benefits.0'),
                t('roadmap.items.automatedAlerts.benefits.1'),
                t('roadmap.items.automatedAlerts.benefits.2'),
            ],
        },

        // Монетизація та Фінанси
        {
            id: 9,
            category: t('roadmap.categories.monetization'),
            title: t('roadmap.items.revenueDashboard.title'),
            description: t('roadmap.items.revenueDashboard.description'),
            priority: 'high',
            status: 'planned',
            icon: DollarSign,
            estimatedTime: '2-3 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.revenueDashboard.benefits.0'),
                t('roadmap.items.revenueDashboard.benefits.1'),
                t('roadmap.items.revenueDashboard.benefits.2'),
            ],
        },
        {
            id: 10,
            category: t('roadmap.categories.monetization'),
            title: t('roadmap.items.universityPortal.title'),
            description: t('roadmap.items.universityPortal.description'),
            priority: 'high',
            status: 'planned',
            icon: Building2,
            estimatedTime: '4-6 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.universityPortal.benefits.0'),
                t('roadmap.items.universityPortal.benefits.1'),
                t('roadmap.items.universityPortal.benefits.2'),
            ],
        },

        // Контент та Якість
        {
            id: 11,
            category: t('roadmap.categories.content'),
            title: t('roadmap.items.cms.title'),
            description: t('roadmap.items.cms.description'),
            priority: 'medium',
            status: 'planned',
            icon: FileText,
            estimatedTime: '3-4 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.cms.benefits.0'),
                t('roadmap.items.cms.benefits.1'),
                t('roadmap.items.cms.benefits.2'),
            ],
        },
        {
            id: 12,
            category: t('roadmap.categories.content'),
            title: t('roadmap.items.qualityAssurance.title'),
            description: t('roadmap.items.qualityAssurance.description'),
            priority: 'medium',
            status: 'planned',
            icon: CheckCircle2,
            estimatedTime: '2-3 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.qualityAssurance.benefits.0'),
                t('roadmap.items.qualityAssurance.benefits.1'),
                t('roadmap.items.qualityAssurance.benefits.2'),
            ],
        },

        // User Experience
        {
            id: 13,
            category: t('roadmap.categories.userExperience'),
            title: t('roadmap.items.feedbackHub.title'),
            description: t('roadmap.items.feedbackHub.description'),
            priority: 'high',
            status: 'planned',
            icon: MessageSquare,
            estimatedTime: '2-3 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.feedbackHub.benefits.0'),
                t('roadmap.items.feedbackHub.benefits.1'),
                t('roadmap.items.feedbackHub.benefits.2'),
            ],
        },
        {
            id: 14,
            category: t('roadmap.categories.userExperience'),
            title: t('roadmap.items.supportTickets.title'),
            description: t('roadmap.items.supportTickets.description'),
            priority: 'medium',
            status: 'planned',
            icon: MessageSquare,
            estimatedTime: '3-4 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.supportTickets.benefits.0'),
                t('roadmap.items.supportTickets.benefits.1'),
                t('roadmap.items.supportTickets.benefits.2'),
            ],
        },

        // Competitive Intelligence
        {
            id: 15,
            category: t('roadmap.categories.competitive'),
            title: t('roadmap.items.marketResearch.title'),
            description: t('roadmap.items.marketResearch.description'),
            priority: 'low',
            status: 'planned',
            icon: Target,
            estimatedTime: '2-3 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.marketResearch.benefits.0'),
                t('roadmap.items.marketResearch.benefits.1'),
                t('roadmap.items.marketResearch.benefits.2'),
            ],
        },

        // Growth Experiments
        {
            id: 16,
            category: t('roadmap.categories.growth'),
            title: t('roadmap.items.abTesting.title'),
            description: t('roadmap.items.abTesting.description'),
            priority: 'medium',
            status: 'planned',
            icon: TestTube,
            estimatedTime: '3-4 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.abTesting.benefits.0'),
                t('roadmap.items.abTesting.benefits.1'),
                t('roadmap.items.abTesting.benefits.2'),
            ],
        },
        {
            id: 17,
            category: t('roadmap.categories.growth'),
            title: t('roadmap.items.personalization.title'),
            description: t('roadmap.items.personalization.description'),
            priority: 'medium',
            status: 'planned',
            icon: Sparkles,
            estimatedTime: '4-5 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.personalization.benefits.0'),
                t('roadmap.items.personalization.benefits.1'),
                t('roadmap.items.personalization.benefits.2'),
            ],
        },

        // Multi-Channel Analytics
        {
            id: 18,
            category: t('roadmap.categories.multiChannel'),
            title: t('roadmap.items.mobileAnalytics.title'),
            description: t('roadmap.items.mobileAnalytics.description'),
            priority: 'low',
            status: 'planned',
            icon: Smartphone,
            estimatedTime: '2-3 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.mobileAnalytics.benefits.0'),
                t('roadmap.items.mobileAnalytics.benefits.1'),
                t('roadmap.items.mobileAnalytics.benefits.2'),
            ],
        },

        // Security & Compliance
        {
            id: 19,
            category: t('roadmap.categories.security'),
            title: t('roadmap.items.securityDashboard.title'),
            description: t('roadmap.items.securityDashboard.description'),
            priority: 'high',
            status: 'planned',
            icon: Shield,
            estimatedTime: '2-3 ' + t('roadmap.weeks'),
            benefits: [
                t('roadmap.items.securityDashboard.benefits.0'),
                t('roadmap.items.securityDashboard.benefits.1'),
                t('roadmap.items.securityDashboard.benefits.2'),
            ],
        },
    ];

    const filteredItems = roadmapItems.filter(item =>
        filter === 'all' || item.status === filter
    );

    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case 'high': return 'text-red-400 bg-red-400/10 border-red-400/20';
            case 'medium': return 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20';
            case 'low': return 'text-blue-400 bg-blue-400/10 border-blue-400/20';
            default: return 'text-gray-400 bg-gray-400/10 border-gray-400/20';
        }
    };

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'completed': return <CheckCircle className="w-5 h-5 text-green-400" />;
            case 'in-progress': return <Clock className="w-5 h-5 text-yellow-400" />;
            case 'planned': return <Circle className="w-5 h-5 text-gray-400" />;
            default: return <Circle className="w-5 h-5 text-gray-400" />;
        }
    };

    const stats = {
        total: roadmapItems.length,
        completed: roadmapItems.filter(i => i.status === 'completed').length,
        inProgress: roadmapItems.filter(i => i.status === 'in-progress').length,
        planned: roadmapItems.filter(i => i.status === 'planned').length,
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                    <Lightbulb className="w-8 h-8 text-yellow-400" />
                    {t('roadmap.title')}
                </h1>
                <p className="text-gray-400 mt-2">{t('roadmap.subtitle')}</p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
                    <p className="text-gray-400 text-sm">{t('roadmap.stats.total')}</p>
                    <p className="text-3xl font-bold text-white mt-1">{stats.total}</p>
                </div>
                <div className="bg-gray-800 rounded-xl p-4 border border-green-700/30">
                    <p className="text-gray-400 text-sm">{t('roadmap.stats.completed')}</p>
                    <p className="text-3xl font-bold text-green-400 mt-1">{stats.completed}</p>
                </div>
                <div className="bg-gray-800 rounded-xl p-4 border border-yellow-700/30">
                    <p className="text-gray-400 text-sm">{t('roadmap.stats.inProgress')}</p>
                    <p className="text-3xl font-bold text-yellow-400 mt-1">{stats.inProgress}</p>
                </div>
                <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
                    <p className="text-gray-400 text-sm">{t('roadmap.stats.planned')}</p>
                    <p className="text-3xl font-bold text-gray-400 mt-1">{stats.planned}</p>
                </div>
            </div>

            {/* Filters */}
            <div className="flex gap-2">
                {['all', 'planned', 'in-progress', 'completed'].map((status) => (
                    <button
                        key={status}
                        onClick={() => setFilter(status as any)}
                        className={`px-4 py-2 rounded-lg font-medium transition-all ${filter === status
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                            }`}
                    >
                        {t(`roadmap.filters.${status}`)}
                    </button>
                ))}
            </div>

            {/* Roadmap Items */}
            <div className="grid grid-cols-1 gap-4">
                {filteredItems.map((item) => {
                    const Icon = item.icon;
                    return (
                        <div
                            key={item.id}
                            className="bg-gray-800 rounded-xl p-6 border border-gray-700 hover:border-gray-600 transition-all"
                        >
                            <div className="flex items-start gap-4">
                                {/* Icon */}
                                <div className="bg-blue-600/10 p-3 rounded-lg border border-blue-600/20">
                                    <Icon className="w-6 h-6 text-blue-400" />
                                </div>

                                {/* Content */}
                                <div className="flex-1">
                                    <div className="flex items-start justify-between mb-2">
                                        <div>
                                            <div className="flex items-center gap-2 mb-1">
                                                <span className="text-xs text-gray-500 font-medium">
                                                    #{item.id}
                                                </span>
                                                <span className="text-xs text-gray-500">•</span>
                                                <span className="text-xs text-gray-400">{item.category}</span>
                                            </div>
                                            <h3 className="text-lg font-bold text-white">{item.title}</h3>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            {getStatusIcon(item.status)}
                                            <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getPriorityColor(item.priority)}`}>
                                                {t(`roadmap.priority.${item.priority}`)}
                                            </span>
                                        </div>
                                    </div>

                                    <p className="text-gray-400 text-sm mb-4">{item.description}</p>

                                    {/* Benefits */}
                                    <div className="mb-4">
                                        <p className="text-xs text-gray-500 font-medium mb-2">
                                            {t('roadmap.benefits')}:
                                        </p>
                                        <ul className="space-y-1">
                                            {item.benefits.map((benefit, index) => (
                                                <li key={index} className="flex items-start gap-2 text-sm text-gray-300">
                                                    <CheckCircle2 className="w-4 h-4 text-green-400 mt-0.5 flex-shrink-0" />
                                                    <span>{benefit}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>

                                    {/* Footer */}
                                    <div className="flex items-center gap-4 text-xs text-gray-500">
                                        <div className="flex items-center gap-1">
                                            <Clock className="w-4 h-4" />
                                            <span>{item.estimatedTime}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
