/**
 * Service Jour 2 — Appels vers l'API FastAPI.
 * L'API doit tourner sur http://localhost:8000 (ou APP_API_URL en .env).
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

// Cache local pour éviter les rechargements inutiles
let _allCache: NafRomeRecord[] | null = null

/**
 * Charge TOUS les enregistrements (NAF + ROME) depuis l'API.
 * Compatible avec l'interface attendue par csvService.
 */
export async function loadData(): Promise<NafRomeRecord[]> {
  if (_allCache) return _allCache

  const [nafResp, romeResp] = await Promise.all([
    apiFetch<{ data: Record<string, string>[] }>('/api/v1/naf?limit=100'),
    apiFetch<{ data: Record<string, string>[] }>('/api/v1/rome?limit=100'),
  ])

  const nafs: NafRomeRecord[] = nafResp.data.map((r) => ({
    code_naf:  r['code_naf']  ?? '',
    code_rome: r['code_rome'] ?? '',
    name:      r['name']      ?? '',
    desc:      r['desc']      ?? '',
    type:      'naf' as const,
  }))

  const romes: NafRomeRecord[] = romeResp.data.map((r) => ({
    code_naf:  r['code_naf']  ?? '',
    code_rome: r['code_rome'] ?? '',
    name:      r['name']      ?? '',
    desc:      r['desc']      ?? '',
    type:      'rome' as const,
  }))

  _allCache = [...nafs, ...romes]
  return _allCache
}

/**
 * Recherche via l'endpoint /api/v1/search (côté serveur).
 * Retombe sur la recherche locale si query vide.
 */
export async function searchApi(query: string, limit = 50): Promise<NafRomeRecord[]> {
  if (!query.trim()) return []

  const resp = await apiFetch<{
    results: { code_naf: string; code_rome: string; name: string; desc: string }[]
  }>('/api/v1/search', {
    method: 'POST',
    body: JSON.stringify({ query, limit }),
  })

  return resp.results.map((r) => ({
    ...r,
    type: r.code_naf ? 'naf' : ('rome' as 'naf' | 'rome'),
  }))
}

// Réexporte exportToCsv (pas besoin de l'API pour ça)
export { exportToCsv } from './csvService'

// Réexporte search pour la compatibilité (filtrage local sur les données chargées)
export { search } from './csvService'
