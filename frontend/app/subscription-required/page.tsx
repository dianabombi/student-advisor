'use client';

import Link from 'next/link';
import { AlertTriangle } from 'lucide-react';
import { useLanguage } from '@/lib/LanguageContext';

export default function SubscriptionRequiredPage() {
    const { t } = useLanguage();

    const handlePayment = async (plan: string, amount: number) => {
        // Redirect to home page with subscription section
        window.location.href = '/#subscription';
    };

    return (
        <div className="min-h-screen bg-gradient-mesh flex items-center justify-center px-4">
            <div className="max-w-2xl w-full">
                <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-white/20">
                    <div className="text-center mb-8">
                        <div className="inline-flex items-center justify-center w-16 h-16 bg-red-500/20 rounded-full mb-4">
                            <AlertTriangle className="w-8 h-8 text-red-500" />
                        </div>
                        <h1 className="text-3xl font-bold text-white mb-2">
                            Skúšobné obdobie skončilo
                        </h1>
                        <p className="text-gray-300 text-lg">
                            Váš 7-dňový bezplatný prístup k platforme CODEX skončil.
                        </p>
                    </div>

                    <div className="bg-white/5 rounded-xl p-6 mb-6">
                        <h2 className="text-xl font-semibold text-white mb-4">
                            Pokračujte s CODEX
                        </h2>
                        <p className="text-gray-300 mb-4">
                            Vyberte si jeden z našich predplatných plánov a pokračujte v používaní všetkých funkcií platformy:
                        </p>
                        <ul className="space-y-2 text-gray-300">
                            <li className="flex items-center">
                                <span className="text-green-400 mr-2">✓</span>
                                AI právny konzultant
                            </li>
                            <li className="flex items-center">
                                <span className="text-green-400 mr-2">✓</span>
                                Automatické spracovanie dokumentov
                            </li>
                            <li className="flex items-center">
                                <span className="text-green-400 mr-2">✓</span>
                                Vytváranie právnych dokumentov
                            </li>
                            <li className="flex items-center">
                                <span className="text-green-400 mr-2">✓</span>
                                Neobmedzený prístup k všetkým funkciám
                            </li>
                        </ul>
                    </div>

                    <div className="space-y-4">
                        <Link
                            href="/#subscription"
                            className="block w-full py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white text-center font-semibold rounded-xl hover:shadow-lg transform hover:scale-105 transition-all duration-300"
                        >
                            Vybrať predplatné
                        </Link>

                        <Link
                            href="/"
                            className="block w-full py-4 bg-white/10 text-white text-center font-semibold rounded-xl hover:bg-white/20 transition-all duration-300"
                        >
                            Späť na hlavnú stránku
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}
