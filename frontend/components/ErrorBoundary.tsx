'use client';
import React from 'react';

interface Props {
    children: React.ReactNode;
}

interface State {
    hasError: boolean;
    error?: Error;
}

export class ErrorBoundary extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
        // Логувати помилку
        console.error('Error caught by boundary:', error, errorInfo);

        // Можна надіслати на сервер для tracking
        fetch('/api/log-error', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                error: error.message,
                stack: error.stack,
                componentStack: errorInfo.componentStack
            })
        }).catch(() => { });
    }

    render() {
        if (this.state.hasError) {
            return (
                <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
                    <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
                        <div className="text-6xl mb-4">😔</div>
                        <h1 className="text-2xl font-bold text-gray-900 mb-2">
                            Щось пішло не так
                        </h1>
                        <p className="text-gray-600 mb-6">
                            Вибачте за незручності. Спробуйте оновити сторінку.
                        </p>

                        {process.env.NODE_ENV === 'development' && this.state.error && (
                            <details className="text-left mb-6">
                                <summary className="cursor-pointer text-sm text-gray-500 hover:text-gray-700">
                                    Деталі помилки (тільки для розробки)
                                </summary>
                                <pre className="mt-2 p-4 bg-gray-100 rounded text-xs overflow-auto max-h-40">
                                    {this.state.error.message}
                                    {'\n\n'}
                                    {this.state.error.stack}
                                </pre>
                            </details>
                        )}

                        <div className="flex gap-3">
                            <button
                                onClick={() => window.location.reload()}
                                className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
                            >
                                🔄 Оновити сторінку
                            </button>
                            <button
                                onClick={() => window.location.href = '/'}
                                className="flex-1 bg-gray-200 text-gray-800 py-2 px-4 rounded-lg hover:bg-gray-300"
                            >
                                🏠 На головну
                            </button>
                        </div>

                        <p className="text-sm text-gray-500 mt-6">
                            Якщо проблема повторюється, зверніться до{' '}
                            <a href="mailto:support@codex.com" className="text-blue-600 hover:underline">
                                підтримки
                            </a>
                        </p>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}
