/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'standalone',

    // API rewrites for backend proxy
    async rewrites() {
        return [
            {
                source: '/api/:path*',
                destination: process.env.NEXT_PUBLIC_API_URL
                    ? `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`
                    : 'http://localhost:8000/api/:path*',
            },
        ];
    },

    // CORS and headers configuration
    async headers() {
        return [
            {
                source: '/api/:path*',
                headers: [
                    { key: 'Access-Control-Allow-Credentials', value: 'true' },
                    { key: 'Access-Control-Allow-Origin', value: '*' },
                    { key: 'Access-Control-Allow-Methods', value: 'GET,DELETE,PATCH,POST,PUT' },
                    { key: 'Access-Control-Allow-Headers', value: 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, Authorization' },
                ],
            },
            // Prevent caching of HTML pages to avoid stale chunks
            {
                source: '/:path*',
                headers: [
                    {
                        key: 'Cache-Control',
                        value: 'no-cache, no-store, must-revalidate',
                    },
                ],
            },
        ];
    },

    // Generate unique build ID to prevent chunk loading errors
    generateBuildId: async () => {
        // Use timestamp to ensure unique build ID
        return `build-${Date.now()}`;
    },

    // Disable static optimization for dynamic imports
    experimental: {
        optimizeCss: false,
    },
};

module.exports = nextConfig;
