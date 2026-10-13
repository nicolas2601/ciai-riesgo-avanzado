import react from '@vitejs/plugin-react'
import { defineConfig } from 'vitest/config'

// Single-page app served from the site root (basename "/").
export default defineConfig({
  plugins: [react()],
  server: { port: 5173 },
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    css: false,
  },
})
