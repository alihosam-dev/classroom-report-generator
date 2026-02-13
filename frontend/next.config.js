/** @type {import('next').NextConfig} */
const path = require('path');

const projectRoot = path.resolve(__dirname);

const nextConfig = {
  output: 'standalone',
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001'
  },
  turbopack: {
    resolveAlias: {
      '@': projectRoot
    }
  },
  webpack: (config) => {
    config.resolve.alias['@'] = projectRoot;
    return config;
  }
}

module.exports = nextConfig