import { BarrasH, Pasos, Seccion, Sello } from '../../components/Explica.tsx'
import { fmtDecimal } from '../../lib/formato.ts'
import { useJson } from '../../lib/datos.ts'
import type { Pruebas } from '../../lib/datos.ts'

const ROTULO: Record<string, string> = {
  V0_ref: 'PPO (referencia V0)',
  V1_clip: 'PPO con recorte (V1)',
  V2_permuni: 'PPO por municipio (V2)',
  static_topk: 'Ranking estático top-K',
  ranker_ctx: 'Ranker contextual',
  random: 'Aleatorio',
  oracle_ref: 'Oráculo (techo)',
}
const SELLO_DE: Record<string, 'hecho' | 'hipotesis'> = { oracle_ref: 'hipotesis' }

function Diagrama({ k }: { k: number }) {
  return (
    <svg className="diagrama" viewBox="0 0 760 150" role="img" aria-label={`Episodio: corte mensual, el agente elige ${k} municipios antes de ver el resultado, la recompensa llega al final`}>
      <defs>
        <marker id="punta" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
          <path d="M0,0 L8,4 L0,8 z" className="dg-punta" />
        </marker>
      </defs>
      <rect x="10" y="30" width="200" height="80" />
      <text x="24" y="60">1. Corte mensual</text>
      <text x="24" y="82" className="dg-sub">estado: actividad hasta el mes</text>
      <rect x="280" y="30" width="200" height="80" className="dg-acento" />
      <text x="294" y="60">{`2. Elige K = ${k}`}</text>
      <text x="294" y="82" className="dg-sub">antes de ver el resultado</text>
      <rect x="550" y="30" width="200" height="80" />
      <text x="564" y="60">3. Recompensa final</text>
      <text x="564" y="82" className="dg-sub">actividad M≥3 del mes siguiente</text>
      <path d="M210,70 H278" className="dg-flecha" markerEnd="url(#punta)" />
      <path d="M480,70 H548" className="dg-flecha" markerEnd="url(#punta)" />
      <text x="10" y="138" className="dg-sub">Sin recompensa intermedia: solo se evalúa al cerrar el episodio.</text>
    </svg>
  )
}

function Comparacion({ p }: { p: Pruebas }) {
  const filas = p.rl.validacion
  return (
    <Seccion eyebrow="Resultados" titulo="PPO frente a las referencias (validación)">
      <BarrasH
        titulo="Recompensa media de validación por política"
        max={1}
        filas={filas.map((f) => ({
          etiqueta: ROTULO[f.politica] ?? f.politica,
          valor: f.val_media,
          texto: fmtDecimal(f.val_media, 4),
          destacada: f.politica === 'V0_ref',
        }))}
      />
      <div className="tabla-wrap">
        <table>
          <caption className="visually-hidden">Validación por política</caption>
          <thead>
            <tr><th>Política</th><th>Validación</th><th>± desv.</th><th>Selecciones distintas (por semilla)</th></tr>
          </thead>
          <tbody>
            {filas.map((f) => (
              <tr key={f.politica} className={f.politica === 'V0_ref' ? 'fila-sel' : undefined}>
                <td>{ROTULO[f.politica] ?? f.politica} {SELLO_DE[f.politica] ? <Sello tipo="hipotesis" /> : null}</td>
                <td className="mono">{fmtDecimal(f.val_media, 4)}</td>
                <td className="mono">{f.val_desv === null ? '—' : fmtDecimal(f.val_desv, 4)}</td>
                <td className="mono">{f.conjuntos_distintos}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p>
        Test (ya consultado): PPO <strong>{fmtDecimal(p.rl.test.mean, 4)}</strong>, ranking
        estático <strong>{fmtDecimal(p.rl.test.static_mean, 4)}</strong>, ranker contextual{' '}
        {fmtDecimal(p.rl.test.ranker_mean, 4)} <Sello tipo="limitacion" />
      </p>
    </Seccion>
  )
}

export function AvanzadoExplica() {
  const { data, error } = useJson<Pruebas>('/data/pruebas.json')
  return (
    <>
      <Seccion eyebrow="Diagrama" titulo="Cómo funciona el agente">
        <Diagrama k={data?.rl.presupuesto_k ?? 5} />
        <Pasos
          items={[
            { titulo: 'Episodio', texto: 'Un episodio es un corte mensual.' },
            { titulo: 'Acción', texto: 'Elige K municipios sin conocer el mes siguiente.' },
            { titulo: 'Recompensa', texto: 'Solo al final: actividad M≥3 observada el mes siguiente.' },
          ]}
        />
      </Seccion>
      {data ? <Comparacion p={data} /> : null}
      {error ? <p className="estado estado--error" role="alert">No se pudo cargar pruebas.json: {error}</p> : null}
      <Seccion eyebrow="Hallazgo honesto" titulo="El PPO colapsa a una selección constante">
        <ul className="lista-sellos">
          <li>
            <Sello tipo="hecho" /> En las tres semillas (7, 21, 42) el PPO de referencia entrega
            1 solo conjunto de municipios: no se adapta al corte.
          </li>
          <li>
            <Sello tipo="hecho" /> En test empata con el ranking estático; en validación el
            estático lo supera.
          </li>
          <li>
            <Sello tipo="hipotesis" /> Equivale a un top-K contextual fijo; se declara así
            porque presentarlo como «aprendizaje» sería engañoso.
          </li>
          <li>
            <Sello tipo="hecho" /> Se probaron 9 experimentos (3 variantes de política × semillas
            7/21/42); la variante por municipio no mejoró y quedó muy por debajo.
          </li>
          <li>
            <Sello tipo="limitacion" /> El test fue expuesto por una pista previa: sirve de
            confirmación, no de examen intacto.
          </li>
        </ul>
        <p className="detalle__nota">
          «Ejecutar agente» sigue deshabilitado: la API v1 solo expone resultados ya calculados,
          no corre el agente.
        </p>
      </Seccion>
    </>
  )
}
