import { useEffect, useState } from 'react'

export interface ModeloSup {
  modelo: string
  macro_f1: number
  balanced_accuracy: number
  accuracy: number
}
export interface PoliticaRL {
  politica: string
  val_media: number
  val_desv: number | null
  conjuntos_distintos: string
}
export interface Pruebas {
  supervisado: { modelos: ModeloSup[]; seleccionado: string }
  rl: {
    validacion: PoliticaRL[]
    test: { mean: number; static_mean: number; ranker_mean: number }
    presupuesto_k: number
    monitores: string[]
  }
}
export interface MetaPanel {
  rows: number
  features: string[]
  target_balance: Record<string, number>
}

export function useJson<T>(ruta: string): { data: T | null; error: string | null } {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<string | null>(null)
  useEffect(() => {
    fetch(ruta)
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`))))
      .then((d: T) => setData(d))
      .catch((e: unknown) => setError(e instanceof Error ? e.message : String(e)))
  }, [ruta])
  return { data, error }
}
