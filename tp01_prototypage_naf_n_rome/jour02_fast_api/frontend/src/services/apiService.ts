/**
 * Service Jour 2 — Appels vers l'API FastAPI.
 * Contrairement au Jour 1 (CSV direct), toutes les données passent par l'API.
 * L'API doit tourner sur http://localhost:8000 (ou VITE_API_URL en .env).
 */
import type { NafRomeRecord } from '../types'

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const body = await res.text()
    throw new Error(`API ${path} → ${res.status}: ${body}`)
  }
  return res.json() as Promise<T>
}

let _allCache: NafRomeRecord[] | null = null

/**
 * Charge TOUS les enregistrements depuis l'API en un seul appel.
 * Le type (naf / rome / matching) est assigné côté serveur.
 */
export async function loadData(): Promise<NafRomeRecord[]> {
  if (_allCache) return _allCache

  const resp = await apiFetch<{ data: Record<string, string>[]; total: number }>('/api/v1/all')

  _allCache = resp.data.map((r) => ({
    code_naf:  r['code_naf']  ?? '',
    code_rome: r['code_rome'] ?? '',
    name:      r['name']      ?? '',
    desc:      r['desc']      ?? '',
    type:      (r['type'] ?? 'naf') as NafRomeRecord['type'],
  }))

  return _allCache
}

// Réexporte les utilitaires locaux (pas besoin de l'API pour ces opérations)
export { search, exportToCsv } from './csvService'
