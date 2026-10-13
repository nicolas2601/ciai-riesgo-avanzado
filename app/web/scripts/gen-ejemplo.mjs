#!/usr/bin/env node
// Generates synthetic "ejemplo" JSONs so the web builds before real data lands.
// Every file carries "ejemplo": true and the UI must show the example banner.
// When Nico/Zabdiel deliver the real files, these are overwritten (same names).
// Municipality names and centroids come from the real file; everything else is
// deterministic synthetic data, NEVER presented as real.

import { createHash } from 'node:crypto'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = join(dirname(fileURLToPath(import.meta.url)), '..', '..', '..')
const out = join(root, 'app', 'web', 'public', 'data')
mkdirSync(out, { recursive: true })

const reales = JSON.parse(
  readFileSync(join(root, 'app', 'api', 'data', 'municipios_santander.json'), 'utf8'),
)

const unit = (...parts) =>
  parseInt(
    createHash('sha256').update(parts.join('|')).digest('hex').slice(0, 8),
    16,
  ) / 0xffffffff

const NIVELES = ['bajo', 'medio', 'alto']
const nivelDe = (id, corte) => NIVELES[Math.floor(unit(id, corte) * 3) % 3]
const CORTES = ['2024-10', '2024-11', '2024-12', '2025-01', '2025-02', '2025-03']

const municipios = reales.map((m, i) => ({
  id: m.zone_id,
  nombre: m.municipality,
  lat: m.lat,
  lon: m.lon,
  poblacion: 5000 + Math.floor(unit(m.zone_id, 'pob') * 450000),
  cluster: `C${1 + (i % 4)}`,
  nivel: nivelDe(m.zone_id, '2025-03'),
}))

const serie = []
for (const m of reales) {
  for (const corte of CORTES) {
    const ev = Math.floor(unit(m.zone_id, corte, 'ev') * 9)
    serie.push({
      municipio: m.zone_id,
      mes: corte,
      eventos: ev,
      mag_max: ev === 0 ? null : Math.round((2.1 + unit(m.zone_id, corte, 'm') * 3.4) * 10) / 10,
      sacudida: null,
      nivel_real: nivelDe(m.zone_id, corte),
      nivel_predicho: nivelDe(m.zone_id, `${corte}-pred`),
    })
  }
}

const clusters = [1, 2, 3, 4].map((k) => ({
  id: `C${k}`,
  nombre: `Grupo ${k}`,
  descripcion: 'Perfil de ejemplo: se reemplaza con la lectura del Medio.',
  variables: ['eventos_12m', 'mag_max_12m', 'prof_mediana_km'],
  importancia: [0.5, 0.3, 0.2],
  municipios: reales.filter((_, i) => i % 4 === k - 1).map((m) => m.zone_id),
}))

const top = (corte, semilla, k = 5) =>
  [...reales]
    .sort((a, b) => unit(b.zone_id, corte, semilla) - unit(a.zone_id, corte, semilla))
    .slice(0, k)
    .map((m) => m.zone_id)

const priorizacion = {
  k: 5,
  cortes: CORTES.slice(-2).map((corte) => ({
    corte,
    agente: top(corte, 'agente'),
    baselines: { top_estatico: top(corte, 'estatico'), frecuencia: top(corte, 'frec') },
    oraculo: top(corte, 'oraculo'),
    real: Object.fromEntries(
      [...reales].slice(0, 12).map((m) => [m.zone_id, unit(m.zone_id, corte, 'y') > 0.6 ? 1 : 0]),
    ),
  })),
}

const metricas = {
  basico: { matriz: null, f1_macro: null, nota: 'Sin entrenar: ejemplo.' },
  rl: { curvas: null, retorno_medio: null, semillas: [] },
  comparacion: { diferencia_pareada: null, intervalo: null, nota: 'Sin evaluar: ejemplo.' },
}

const diccionario = [
  { nombre: 'eventos_12m', tipo: 'conteo', unidad: 'eventos', fuente: 'SGC', porque: 'Actividad reciente.' },
  { nombre: 'mag_max_12m', tipo: 'continua', unidad: 'Mw', fuente: 'SGC', porque: 'Tamano maximo reciente.' },
  { nombre: 'prof_mediana_km', tipo: 'continua', unidad: 'km', fuente: 'SGC', porque: 'Nido intermedio vs cortical.' },
  { nombre: 'poblacion', tipo: 'conteo', unidad: 'habitantes', fuente: 'DANE', porque: 'Exposicion.' },
]

const fuentes = [
  { nombre: 'SGC catalogo sismico', url: 'https://www.sgc.gov.co', fecha: '2026-10-13', filtros: 'Santander, ejemplo' },
  { nombre: 'DANE proyecciones', url: 'https://www.dane.gov.co', fecha: '2026-10-13', filtros: 'Municipal, ejemplo' },
]

const files = {
  'municipios.json': { ejemplo: true, municipios },
  'serie_mensual.json': { ejemplo: true, cortes: CORTES, serie },
  'clusters.json': { ejemplo: true, clusters },
  'priorizacion.json': { ejemplo: true, ...priorizacion },
  'metricas.json': { ejemplo: true, ...metricas },
  'diccionario.json': { ejemplo: true, variables: diccionario },
  'fuentes.json': { ejemplo: true, fuentes },
}

for (const [name, data] of Object.entries(files)) {
  writeFileSync(join(out, name), `${JSON.stringify(data)}\n`)
  console.log(`${name}: ${JSON.stringify(data).length} bytes`)
}
