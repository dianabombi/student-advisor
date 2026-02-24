'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';

interface User {
    id: number;
    email: string;
    name?: string;
    role: string; // 'admin' | 'user'
}

interface AuthContextType {
    user: User | null;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
    isLoading: boolean;
    isAuthenticated: boolean;
    isAdmin: () => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    // Завантажити user при mount
    useEffect(() => {
        const loadUser = async () => {
            const token = localStorage.getItem('token');

            if (!token) {
                setIsLoading(false);
                return;
            }

            try {
                // Fetch user data з включеним role
                const response = await axios.get('/api/auth/me', {
                    headers: { Authorization: `Bearer ${token}` }
                });

                setUser(response.data);
                console.log('👤 User loaded:', response.data);
            } catch (error) {
                console.error('Failed to load user:', error);
                localStorage.removeItem('token');
            } finally {
                setIsLoading(false);
            }
        };

        loadUser();
    }, []);

    const login = async (email: string, password: string) => {
        console.log('🚀 AuthContext.login() CALLED with:', email);
        try {
            // Backend expects OAuth2PasswordRequestForm (form data)
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);

            const response = await axios.post(
                '/api/auth/login',  // Use relative path, Next.js will proxy to backend
                formData,
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    }
                }
            );

            const { access_token, user: userData } = response.data;

            // Зберегти токен і user
            localStorage.setItem('token', access_token);
            localStorage.setItem('user', JSON.stringify(userData));

            // Зберегти user в cookies для middleware
            if (typeof document !== 'undefined') {
                document.cookie = `user=${encodeURIComponent(JSON.stringify(userData))}; path=/; max-age=86400`;
            }

            // КРИТИЧНО: Оновити user state ОДРАЗУ
            setUser(userData);
            console.log('✅ Login successful, user updated:', userData);

            // НЕ викликаємо fetchSubscriptionStatus тут для адмінів
            // Адміни не потребують subscription
            if (userData.role !== 'admin') {
                // Для звичайних користувачів - можна завантажити підписку
                try {
                    await fetchSubscriptionStatus(access_token);
                } catch (err) {
                    // Ігноруємо помилки підписки при логіні
                    console.warn('Subscription fetch failed, continuing...', err);
                }
            }

            // Повертаємось успішно
            return;

        } catch (error: any) {
            console.error('Login failed:', error);
            throw error;
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
        window.location.href = '/auth/login';
    };

    const isAdmin = () => {
        return user?.role === 'admin';
    };

    // Допоміжна функція для завантаження підписки
    const fetchSubscriptionStatus = async (token?: string) => {
        const authToken = token || localStorage.getItem('token');

        if (!authToken) return;

        try {
            const response = await axios.get(
                '/api/subscription/status',
                { headers: { Authorization: `Bearer ${authToken}` } }
            );

            console.log('📊 Subscription loaded:', response.data);
        } catch (error) {
            // Не кидаємо помилку - підписка опціональна
            console.warn('Subscription not available:', error);
        }
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, isLoading, isAuthenticated: !!user, isAdmin }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
