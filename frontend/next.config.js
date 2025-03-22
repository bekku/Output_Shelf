/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: false,
    poweredByHeader: false,

    webpack: (config, { dev, isServer }) => {
      if (dev && !isServer) {
        config.devtool = 'cheap-module-source-map';
      }
      return config;
    },

    onDemandEntries: {
      maxInactiveAge: 10 * 1000,
      pagesBufferLength: 1,
    },

    experimental: {
      optimizePackageImports: ['@mui/material', '@mui/icons-material'],
    },

    serverExternalPackages: [],
  };

  module.exports = nextConfig;
