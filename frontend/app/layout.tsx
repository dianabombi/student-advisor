import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";
import { LanguageProvider } from "@/lib/LanguageContext";
import { JurisdictionProvider } from "@/contexts/JurisdictionContext";
import AISupportButton from "@/components/AISupportButton";
import { ClientErrorBoundary } from "@/components/ClientErrorBoundary";

const inter = Inter({ subsets: ["latin", "latin-ext", "cyrillic"] });

export const metadata: Metadata = {
    title: "Student Advisor - Educational Platform",
    description: "AI-powered student consultation and university information platform",
    metadataBase: new URL('http://localhost:3001'),
    other: {
        charset: 'utf-8',
    },
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <ClientErrorBoundary>
                    <LanguageProvider>
                        <JurisdictionProvider>
                            <AuthProvider>
                                {children}
                                <AISupportButton />
                            </AuthProvider>
                        </JurisdictionProvider>
                    </LanguageProvider>
                </ClientErrorBoundary>
            </body>
        </html>
    );
}
