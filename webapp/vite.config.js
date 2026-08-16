import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Served by the bot's aiohttp app under /app, so assets must resolve relative to /app/.
// In dev, /api is proxied to the local API server so initData-authed calls just work.
export default defineConfig({
  plugins: [react()],
  base: '/app/',
  server: {
    host: true,
    allowedHosts: true, // let ngrok / any tunnel host through in dev
    proxy: {
      '/api': { target: 'http://localhost:8080', changeOrigin: true },
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    target: ['es2021', 'chrome100', 'safari15'],
  },
})
