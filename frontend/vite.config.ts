import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,   // = 0.0.0.0 în container
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://fullstack:5001', // serviciul backend din docker-compose
        changeOrigin: true,
      },
    },
  },
})
