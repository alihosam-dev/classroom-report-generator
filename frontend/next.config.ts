import path from 'path';
import type { NextConfig } from 'next';

const projectRoot = path.resolve(__dirname);

const nextConfig: NextConfig = {
  output: 'standalone',
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001'
  },
  reactCompiler: true,
  turbopack: {
    resolveAlias: {
      '@': projectRoot,
    },
  },
  webpack: (config) => {
    config.resolve.alias['@'] = projectRoot;
    return config;
  },
};

export default nextConfig;
