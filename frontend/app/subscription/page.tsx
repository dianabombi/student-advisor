'use client';

import { useRouter } from 'next/navigation';
import { Check, Zap, Shield, HeadphonesIcon } from 'lucide-react';

export default function SubscriptionPage() {
    const router = useRouter();

    const plans = [
        {
            name: 'Basic',
            requests: 500,
            monthly: 30,
            sixMonths: 150,
            yearly: 270,
            features: [
                '500 AI запитів на місяць',
                'Завантаження до 100 документів',
                'Підтримка електронною поштою',
                'Доступ до всіх базових функцій'
            ],
            icon: Zap,
            color: 'blue'
        },
        {
            name: 'Professional',
            requests: 1500,
            monthly: 70,
            sixMonths: 360,
            yearly: 660,
            features: [
                '1500 AI запитів на місяць',
                'Завантаження до 500 документів',
                'Пріоритетна підтримка',
                'Розширена аналітика',
                'Експорт даних'
            ],
            icon: Shield,
            color: 'purple',
            popular: true
        },
        {
            name: 'Enterprise',
            requests: 3500,
            monthly: 150,
            sixMonths: 780,
            yearly: 1440,
            features: [
                '3500 AI запитів на місяць',
                'Необмежене завантаження документів',
                'Підтримка 24/7',
                'Персональний менеджер',
                'API доступ',
                'Власний домен'
            ],
            icon: HeadphonesIcon,
            color: 'pink'
        }
    ];

    const calculateSavings = (monthly: number, total: number, months: number) => {
        return monthly * months - total;
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 py-12 px-4">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold text-white mb-4">Оберіть ваш план</h1>
                    <p className="text-gray-300 text-lg">Виберіть тариф, який найкраще підходить для ваших потреб</p>
                </div>

                {/* Plans Grid */}
                <div className="grid md:grid-cols-3 gap-8 mb-12">
                    {plans.map((plan) => {
                        const Icon = plan.icon;
                        return (
                            <div
                                key={plan.name}
                                className={`relative bg-white/10 backdrop-blur-lg border ${plan.popular ? 'border-purple-500 ring-2 ring-purple-500' : 'border-white/20'
                                    } rounded-2xl p-8 hover:scale-105 transition-transform`}
                            >
                                {plan.popular && (
                                    <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                                        <span className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-1 rounded-full text-sm font-semibold">
                                            Найпопулярніший
                                        </span>
                                    </div>
                                )}

                                <div className="text-center mb-6">
                                    <Icon className={`w-12 h-12 mx-auto mb-4 text-${plan.color}-400`} />
                                    <h2 className="text-2xl font-bold text-white mb-2">{plan.name}</h2>
                                    <div className="text-4xl font-bold text-white mb-2">
                                        €{plan.monthly}
                                        <span className="text-lg text-gray-400">/міс</span>
                                    </div>
                                    <p className="text-gray-300">{plan.requests} запитів/місяць</p>
                                </div>

                                {/* Features */}
                                <ul className="space-y-3 mb-6">
                                    {plan.features.map((feature, idx) => (
                                        <li key={idx} className="flex items-start gap-2 text-gray-200">
                                            <Check className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                                            <span>{feature}</span>
                                        </li>
                                    ))}
                                </ul>

                                {/* Pricing Options */}
                                <div className="space-y-3 mb-6">
                                    <button className="w-full py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-semibold hover:from-purple-600 hover:to-pink-600 transition-all">
                                        Обрати {plan.name}
                                    </button>

                                    <div className="bg-white/5 rounded-lg p-3 space-y-2">
                                        <div className="flex justify-between text-sm">
                                            <span className="text-gray-300">6 місяців</span>
                                            <div className="text-right">
                                                <div className="text-white font-semibold">€{plan.sixMonths}</div>
                                                <div className="text-green-400 text-xs">
                                                    Економія €{calculateSavings(plan.monthly, plan.sixMonths, 6)}
                                                </div>
                                            </div>
                                        </div>
                                        <div className="flex justify-between text-sm">
                                            <span className="text-gray-300">1 рік</span>
                                            <div className="text-right">
                                                <div className="text-white font-semibold">€{plan.yearly}</div>
                                                <div className="text-green-400 text-xs">
                                                    Економія €{calculateSavings(plan.monthly, plan.yearly, 12)}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>

                {/* FAQ Section */}
                <div className="bg-white/5 backdrop-blur-lg border border-white/20 rounded-2xl p-8">
                    <h3 className="text-2xl font-bold text-white mb-6">Часті питання</h3>

                    <div className="space-y-6">
                        <div>
                            <h4 className="font-semibold text-white mb-2">❓ Що таке "AI запит"?</h4>
                            <p className="text-gray-300">
                                Кожне повідомлення, яке ви надсилаєте AI асистенту, вважається одним запитом.
                                Наприклад: "Які умови дійсності договору?" = 1 запит.
                            </p>
                        </div>

                        <div>
                            <h4 className="font-semibold text-white mb-2">📊 Чи вистачить мені 500 запитів?</h4>
                            <p className="text-gray-300 mb-2">
                                Для більшості користувачів 500 запитів більш ніж достатньо:
                            </p>
                            <ul className="list-disc ml-6 text-gray-300 space-y-1">
                                <li>60% користувачів використовують 50-150 запитів/міс</li>
                                <li>30% використовують 200-350 запитів/міс</li>
                                <li>Тільки 10% досягають ліміту 500</li>
                            </ul>
                        </div>

                        <div>
                            <h4 className="font-semibold text-white mb-2">🔄 Коли оновлюється ліміт?</h4>
                            <p className="text-gray-300">
                                Ліміт запитів автоматично оновлюється 1-го числа кожного місяця о 00:00.
                                При підписці ви отримуєте повний ліміт одразу (бонус для нових користувачів!).
                            </p>
                        </div>

                        <div>
                            <h4 className="font-semibold text-white mb-2">⚠️ Що буде, якщо я досягну ліміту?</h4>
                            <p className="text-gray-300">
                                Після використання всіх запитів доступ до AI буде призупинено до наступного місяця.
                                Ви завжди можете оновити план або купити додаткові запити.
                            </p>
                        </div>
                    </div>
                </div>

                {/* Back Button */}
                <div className="text-center mt-8">
                    <button
                        onClick={() => router.push('/dashboard')}
                        className="px-6 py-3 text-white hover:bg-white/10 rounded-lg transition-all"
                    >
                        ← Повернутися до панелі
                    </button>
                </div>
            </div>
        </div>
    );
}
