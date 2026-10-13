import { useCallback, useEffect, useState, type ReactNode } from 'react'
import { fmtDecimal } from '../lib/formato.ts'

type Modelo = { modelo: string; macro_f1: number; balanced_accuracy: number; accuracy: number }
type FilaRl = { politica: string; val_media: number; val_desv: number | null; conjuntos_distintos: string }
type Datos = {
  supervisado: { modelos: Modelo[]; seleccionado: string; baseline_mayoritario: string }
  medio: {
    k: number
    silhouette: number
    davies_bouldin: number
    ari_por_semilla: Record<string, number>
    tamanos: { grupo: number; n_municipios: number }[]
  }
  rl: {
    validacion: FilaRl[]
    test: { mean: number; static_mean: number; ranker_mean: number }
    test_caveat: string
  }
  pruebas: { estado: string; pasan?: number; fallan?: number; resumen?: string; motivo?: string }
}

type Sello = 'HECHO' | 'HIPÓTESIS' | 'LIMITACIÓN'
const SELLO_ICONO: Record<Sello, string> = { HECHO: '■', HIPÓTESIS: '◆', LIMITACIÓN: '▲' }

const AZUL = '#2438c8'
const GRIS = '#5a6472'
const NEGRO = '#101418'
const BARRA_X = 190
const BARRA_W = 360

function SelloTag({ s }: { s: Sello }) {
  return (
    <span className="mono" style={{ border: '1px solid currentColor', borderRadius: 4, padding: '2px 8px', fontSize: 12 }}>
      {SELLO_ICONO[s]} {s}
    </span>
  )
}

function Bloque({ titulo, sellos, children }: { titulo: string; sellos: Sello[]; children: ReactNode }) {
  return (
    <section className="bloque panel" aria-label={titulo} style={{ padding: 'var(--s-5)' }}>
      <h2 className="tarjeta__titulo">{titulo}</h2>
      <p style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        {sellos.map((s) => (
          <SelloTag key={s} s={s} />
        ))}
      </p>
      {children}
    </section>
  )
}

type Barra = { etiqueta: string; valor: number; desv?: number | null; relleno: string; marca?: string }

function Barras({ filas, max, titulo }: { filas: Barra[]; max: number; titulo: string }) {
  const alto = 34
  const x = (v: number) => BARRA_X + (v / max) * BARRA_W
  return (
    <svg viewBox={`0 0 640 ${filas.length * alto + 30}`} role="img" aria-label={titulo} style={{ width: '100%', height: 'auto' }}>
      {filas.map((f, i) => {
        const y = i * alto + 6
        return (
          <g key={f.etiqueta}>
            <text x={BARRA_X - 8} y={y + 16} textAnchor="end" fontSize="12" fill={NEGRO}>
              {f.etiqueta}
            </text>
            <rect x={BARRA_X} y={y} width={Math.max(x(f.valor) - BARRA_X, 1)} height={22} fill={f.relleno} />
            {f.desv ? (
              <path
                d={`M${x(Math.max(f.valor - f.desv, 0))} ${y + 11}H${x(f.valor + f.desv)}M${x(Math.max(f.valor - f.desv, 0))} ${y + 5}v12M${x(f.valor + f.desv)} ${y + 5}v12`}
                stroke={NEGRO}
                strokeWidth="1.5"
                fill="none"
              />
            ) : null}
            <text x={x(f.valor + (f.desv ?? 0)) + 6} y={y + 16} fontSize="12" className="mono" fill={NEGRO}>
              {fmtDecimal(f.valor, 3)}
              {f.desv ? ` ± ${fmtDecimal(f.desv, 3)}` : ''}
              {f.marca ? ` · ${f.marca}` : ''}
            </text>
          </g>
        )
      })}
      <line x1={BARRA_X} x2={BARRA_X} y1={0} y2={filas.length * alto} stroke={GRIS} />
    </svg>
  )
}

function Supervisado({ d }: { d: Datos['supervisado'] }) {
  const base = d.modelos.find((m) => m.modelo === d.baseline_mayoritario)
  const filas: Barra[] = d.modelos.map((m) => {
    const sel = m.modelo === d.seleccionado
    const bas = m.modelo === d.baseline_mayoritario
    return {
      etiqueta: m.modelo,
      valor: m.macro_f1,
      relleno: sel ? AZUL : bas ? '#fff' : GRIS,
      marca: sel ? 'seleccionado' : bas ? 'baseline mayoritario' : undefined,
    }
  })
  return (
    <Bloque titulo="Supervisado: macro-F1 en validación" sellos={['HECHO', 'LIMITACIÓN']}>
      <Barras filas={filas} max={1} titulo="Macro-F1 por modelo en validación" />
      <p className="detalle__nota">
        Barra azul: modelo seleccionado. Barra con borde vacío: baseline que siempre predice «bajo».
        {base ? ` Accuracy ${fmtDecimal(base.accuracy, 2)} engaña por el desbalance: el baseline mayoritario ya la logra con macro-F1 ${fmtDecimal(base.macro_f1, 2)}.` : ''}
      </p>
    </Bloque>
  )
}

function Medio({ d }: { d: Datos['medio'] }) {
  return (
    <Bloque titulo="Medio: grupos de municipios" sellos={['HECHO', 'LIMITACIÓN']}>
      <p className="mono">
        k = {d.k} · silhouette {fmtDecimal(d.silhouette, 2)} · Davies-Bouldin {fmtDecimal(d.davies_bouldin, 2)}
      </p>
      <Barras
        titulo="Estabilidad ARI por semilla"
        max={1}
        filas={Object.entries(d.ari_por_semilla).map(([s, v]) => ({
          etiqueta: `ARI semilla ${s}`,
          valor: v,
          relleno: v >= 0.99 ? GRIS : '#fff',
          marca: v >= 0.99 ? 'estable' : 'inestable',
        }))}
      />
      <p className="detalle__nota">
        Advertencia: silhouette de {fmtDecimal(d.silhouette, 2)} es modesto; la estructura es débil y una semilla (ARI{' '}
        {fmtDecimal(d.ari_por_semilla['21'] ?? 0, 2)}) cambia la partición. Tamaños:{' '}
        {d.tamanos.map((t) => `grupo ${t.grupo}: ${t.n_municipios}`).join(' · ')}.
      </p>
    </Bloque>
  )
}

const NOMBRES_RL: Record<string, string> = {
  V0_ref: 'PPO (V0, 3 semillas)',
  static_topk: 'Ranking estático',
  random: 'Aleatorio',
}

function Rl({ d }: { d: Datos['rl'] }) {
  const filas: Barra[] = d.validacion
    .filter((f) => f.politica in NOMBRES_RL)
    .map((f) => ({
      etiqueta: NOMBRES_RL[f.politica],
      valor: f.val_media,
      desv: f.val_desv,
      relleno: f.politica === 'V0_ref' ? AZUL : f.politica === 'random' ? '#fff' : GRIS,
      marca: f.politica === 'V0_ref' ? `${f.conjuntos_distintos.split(',')[0]} conjunto fijo` : undefined,
    }))
  return (
    <Bloque titulo="RL: validación de la política" sellos={['HECHO', 'HIPÓTESIS', 'LIMITACIÓN']}>
      <Barras filas={filas} max={0.7} titulo="Recompensa en validación: PPO, ranking estático y aleatorio" />
      <p className="detalle__nota">
        Barras de error: desviación entre semillas (solo PPO). PPO colapsa a una selección constante: no usa el contexto.
        Test ya consultado, no es independiente: PPO {fmtDecimal(d.test.mean, 4)} frente a estático {fmtDecimal(d.test.static_mean, 4)}.
        Que más entrenamiento lo cambie es hipótesis, no resultado.
      </p>
    </Bloque>
  )
}

function Automaticas({ d }: { d: Datos['pruebas'] }) {
  const ok = d.estado === 'ejecutado'
  return (
    <Bloque titulo="Pruebas automáticas" sellos={['HECHO']}>
      {ok ? (
        <p className="mono" role="status">
          {d.pasan} pasan · {d.fallan} fallan {d.fallan === 0 ? '(todas en verde)' : '(hay fallos)'}
        </p>
      ) : (
        <p role="status">No ejecutado: {d.motivo}</p>
      )}
      {d.resumen ? <p className="detalle__nota mono">{d.resumen}</p> : null}
    </Bloque>
  )
}

function useDatos() {
  const [datos, setDatos] = useState<Datos | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [intento, setIntento] = useState(0)
  useEffect(() => {
    let vivo = true
    fetch('/data/pruebas.json')
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`))))
      .then((j: Datos) => vivo && (setDatos(j), setError(null)))
      .catch((e: Error) => vivo && setError(e.message))
    return () => {
      vivo = false
    }
  }, [intento])
  return { datos, error, recargar: useCallback(() => setIntento((n) => n + 1), []) }
}

export default function Pruebas() {
  const { datos, error, recargar } = useDatos()
  return (
    <div className="contenedor">
      <section className="portada-pagina">
        <p className="eyebrow">Pruebas</p>
        <h1 className="pitch__titulo">Qué se midió y qué no</h1>
      </section>
      {error ? (
        <div className="estado estado--error" role="alert">
          <p>No se pudo cargar /data/pruebas.json: {error}</p>
          <button type="button" className="btn btn--secundario" onClick={recargar}>
            Reintentar
          </button>
        </div>
      ) : !datos ? (
        <p className="estado" role="status">
          Cargando pruebas…
        </p>
      ) : (
        <>
          <Supervisado d={datos.supervisado} />
          <Medio d={datos.medio} />
          <Rl d={datos.rl} />
          <Automaticas d={datos.pruebas} />
        </>
      )}
    </div>
  )
}
