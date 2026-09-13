import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Served by the bot's aiohttp app under / and /app.
// In dev, /api is proxied to the local API server so initData-authed calls just work.
export default defineConfig({
  plugins: [react()],
  base: '/',
  server: {
    host: true,
    allowedHosts: true, // let ngrok / any tunnel host through in dev
    proxy: {
      '/api': { target: 'http://localhost:8080', changeOrigin: true },
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './tests/setup.js',
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    target: ['es2021', 'chrome100', 'safari15'],
  },
})
