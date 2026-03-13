export interface NafRomeRecord {
  code_naf: string
  code_rome: string
  name: string
  desc: string
  type: 'naf' | 'rome'
}

export type SortField = 'code_naf' | 'code_rome' | 'name' | 'type'
export type SortDir = 'asc' | 'desc'

export interface SearchState {
  keyword: string
  code: string
  typeFilter: 'all' | 'naf' | 'rome'
  sortField: SortField
  sortDir: SortDir
  page: number
  perPage: number
}
