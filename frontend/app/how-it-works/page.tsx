'use client';

import { useLanguage } from '@/lib/LanguageContext';
import { Sparkles, Upload, MessageSquare, FileText, CheckCircle, Shield, Clock, Zap } from 'lucide-react';

export default function HowItWorksPage() {
    const { t } = useLanguage();

    const steps = [
        { icon: CheckCircle, key: 'step1' },
        { icon: Upload, key: 'step2' },
        { icon: FileText, key: 'step3' },
        { icon: MessageSquare, key: 'step4' },
        { icon: Zap, key: 'step5' },
        { icon: Shield, key: 'step6' },
        { icon: Clock, key: 'step7' },
        { icon: CheckCircle, key: 'step8' },
        { icon: Upload, key: 'step9' },
        { icon: MessageSquare, key: 'step10' },
        { icon: Sparkles, key: 'step11' },
        { icon: Shield, key: 'step12' },
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
            {/* Header */}
            <div className="border-b border-white/10 bg-white/5 backdrop-blur-lg">
                <div className="container mx-auto px-6 py-8">
                    <div className="flex items-center space-x-3">
                        <Sparkles className="w-10 h-10 text-purple-400" />
                        <h1 className="text-4xl font-bold text-white">{t('howItWorks.title')}</h1>
                    </div>
                    <p className="text-gray-300 text-lg mt-4">{t('howItWorks.subtitle')}</p>
                </div>
            </div>

            {/* Main Content */}
            <div className="container mx-auto px-6 py-12 max-w-4xl">
                <div className="space-y-8">
                    {steps.map((step, index) => {
                        const Icon = step.icon;
                        return (
                            <div
                                key={index}
                                className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all"
                            >
                                <div className="flex items-start space-x-4">
                                    <div className="flex-shrink-0">
                                        <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                                            <Icon className="w-6 h-6 text-white" />
                                        </div>
                                    </div>
                                    <div className="flex-1">
                                        <h3 className="text-xl font-bold text-white mb-2">
                                            {index + 1}. {t(`howItWorks.${step.key}.title`)}
                                        </h3>
                                        <p className="text-gray-300 leading-relaxed">
                                            {t(`howItWorks.${step.key}.description`)}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>

                {/* CTA Section */}
                <div className="mt-12 bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl p-8 text-center">
                    <h2 className="text-3xl font-bold text-white mb-4">{t('howItWorks.cta.title')}</h2>
                    <p className="text-white/90 text-lg mb-6">{t('howItWorks.cta.description')}</p>
                    <a
                        href="/register"
                        className="inline-block bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
                    >
                        {t('howItWorks.cta.button')}
                    </a>
                </div>
            </div>
        </div>
    );
}
