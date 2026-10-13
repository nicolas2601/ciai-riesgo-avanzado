import react from '@vitejs/plugin-react'
import { defineConfig } from 'vitest/config'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // maplibre-gl starts its own web worker: pre-bundling it breaks the worker URL ("Worker failed to load").
  optimizeDeps: { exclude: ['maplibre-gl'] },
  server: { port: 5173 },
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    css: false,
  },
})
