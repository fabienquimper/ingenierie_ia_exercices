import Papa from 'papaparse'
import type { NafRomeRecord } from '../types'

let cache: NafRomeRecord[] | null = null

async function loadCsv(url: string, type: NafRomeRecord['type']): Promise<NafRomeRecord[]> {
  const response = await fetch(url)
  if (!response.ok) throw new Error(`Impossible de charger ${url} (${response.status})`)
  const text = await response.text()
  const result = Papa.parse<Record<string, string>>(text, {
    header: true,
    skipEmptyLines: true,
    transformHeader: (h) => h.trim(),
    transform: (v) => v.trim(),
  })
  return result.data.map((row) => ({
    code_naf: row.code_naf ?? '',
    code_rome: row.code_rome ?? '',
    name: row.name ?? '',
    desc: row.desc ?? '',
    type,
  }))
}

export async function loadData(): Promise<NafRomeRecord[]> {
  if (cache) return cache

  const [nafData, romeData, matchingData] = await Promise.all([
    loadCsv('/naf_codes_001_desc.csv', 'naf'),
    loadCsv('/rome.csv', 'rome'),
    loadCsv('/data/rome_with_naf__thenlper_gte-large.csv', 'matching'),
  ])

  cache = [...nafData, ...romeData, ...matchingData]
  return cache
}

export function search(
  data: NafRomeRecord[],
  keyword: string,
  code: string,
  typeFilter: 'all' | 'naf' | 'rome' | 'matching',
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
