/**
 * Service Jour 1 — Chargement et recherche directement depuis le CSV.
 * Aucun backend requis : tout tourne dans le navigateur.
 */
import Papa from 'papaparse'
import type { NafRomeRecord } from '../types'

let cache: NafRomeRecord[] | null = null

//export async function loadData(csvUrl = '/data/sample_naf_rome.csv'): Promise<NafRomeRecord[]> {
export async function loadData(csvUrl = '/data/rome_with_naf__thenlper_gte-large.csv'): Promise<NafRomeRecord[]> {
  if (cache) return cache

  const response = await fetch(csvUrl)
  if (!response.ok) throw new Error(`Impossible de charger ${csvUrl} (${response.status})`)
  const text = await response.text()

  const result = Papa.parse<NafRomeRecord>(text, {
    header: true,
    skipEmptyLines: true,
    transformHeader: (h) => h.trim(),
    transform: (v) => v.trim(),
  })

  cache = result.data.map((row) => ({
    ...row,
    type: (row.type === 'rome' ? 'rome' : 'naf') as 'naf' | 'rome',
  }))

  return cache
}

export function search(
  data: NafRomeRecord[],
  keyword: string,
  code: string,
  typeFilter: 'all' | 'naf' | 'rome',
): NafRomeRecord[] {
  const kw = keyword.toLowerCase().trim()
  const cd = code.toLowerCase().replace('.', '').trim()

  return data.filter((row) => {
    // Filtre type
    if (typeFilter !== 'all' && row.type !== typeFilter) return false

    // Filtre code (NAF ou ROME, insensible à la casse et au point)
    if (cd) {
      const nafNorm = row.code_naf.toLowerCase().replace('.', '')
      const romeNorm = row.code_rome.toLowerCase()
      if (!nafNorm.includes(cd) && !romeNorm.includes(cd)) return false
    }

    // Filtre mot-clé dans name + desc
    if (kw) {
      const text = `${row.name} ${row.desc}`.toLowerCase()
      if (!kw.split(/\s+/).every((w) => text.includes(w))) return false
    }

    return true
  })
}

export function exportToCsv(rows: NafRomeRecord[], filename = 'resultats_naf_rome.csv'): void {
  const csv = Papa.unparse(rows)
  const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}
