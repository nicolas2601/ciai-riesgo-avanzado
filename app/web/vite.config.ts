import react from '@vitejs/plugin-react'
import { defineConfig } from 'vitest/config'

// https://vite.dev/config/
// App multipagina: cuatro entradas HTML (landing + tres modelos). Cada una
// monta su propia pagina con el shell compartido.
const entradas = {
  landing: import.meta.dirname + '/index.html',
  clasificacion: import.meta.dirname + '/modelo-clasificacion.html',
  supervisado: import.meta.dirname + '/modelo-supervisado.html',
  refuerzo: import.meta.dirname + '/modelo-refuerzo.html',
}

export default defineConfig({
  plugins: [react()],
  // maplibre-gl starts its own web worker: pre-bundling it breaks the worker URL ("Worker failed to load").
  optimizeDeps: { exclude: ['maplibre-gl'] },
  server: { port: 5173 },
  build: {
    rollupOptions: {
      input: entradas,
    },
  },
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    css: false,
  },
})