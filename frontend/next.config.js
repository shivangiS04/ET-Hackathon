/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
  // Ensure path alias works properly
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.alias = {
        ...config.resolve.alias,
        '@/components': require('path').resolve(__dirname, 'components'),
        '@/app': require('path').resolve(__dirname, 'app'),
      };
    }
    return config;
  },
}

module.exports = nextConfig
