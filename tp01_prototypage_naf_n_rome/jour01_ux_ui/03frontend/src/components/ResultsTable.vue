<template>
  <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
    <!-- Barre d'actions -->
    <div class="flex flex-wrap items-center justify-between gap-3 px-6 py-4 border-b border-slate-100">
      <div class="flex items-center gap-2 text-sm text-slate-600">
        <span class="font-semibold text-slate-800">{{ total }}</span> résultat{{ total > 1 ? 's' : '' }}
        <span v-if="total !== totalAll" class="text-slate-400">sur {{ totalAll }}</span>
      </div>

      <div class="flex items-center gap-3">
        <!-- Lignes par page -->
        <select
          :value="perPage"
          @change="$emit('update:perPage', Number(($event.target as HTMLSelectElement).value))"
          class="text-sm border border-slate-200 rounded-lg px-3 py-1.5 bg-white focus:outline-none focus:ring-2 focus:ring-brand-500"
        >
          <option v-for="n in [10, 25, 50, 100]" :key="n" :value="n">{{ n }} / page</option>
        </select>

        <!-- Export -->
        <button @click="$emit('export')" class="btn-success">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
          </svg>
          Exporter CSV
        </button>
      </div>
    </div>

    <!-- Tableau -->
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="bg-slate-50 text-left">
            <th
              v-for="col in columns"
              :key="col.field"
              @click="toggleSort(col.field)"
              class="px-4 py-3 font-semibold text-slate-600 cursor-pointer select-none whitespace-nowrap hover:text-slate-900 transition-colors"
              :class="col.class"
            >
              <div class="flex items-center gap-1.5">
                {{ col.label }}
                <span class="text-slate-300">
                  <svg v-if="sortField === col.field && sortDir === 'asc'" class="w-3.5 h-3.5 text-brand-600" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z"/>
                  </svg>
                  <svg v-else-if="sortField === col.field && sortDir === 'desc'" class="w-3.5 h-3.5 text-brand-600" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"/>
                  </svg>
                  <svg v-else class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M5 10a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z"/>
                  </svg>
                </span>
              </div>
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-if="rows.length === 0">
            <td colspan="5" class="px-4 py-12 text-center text-slate-400">
              <div class="flex flex-col items-center gap-2">
                <svg class="w-10 h-10 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span>Aucun résultat</span>
              </div>
            </td>
          </tr>
          <tr
            v-for="(row, i) in rows"
            :key="i"
            class="hover:bg-slate-50/80 transition-colors group"
          >
            <td class="px-4 py-3">
              <span :class="row.type === 'naf' ? 'badge-naf' : 'badge-rome'">
                {{ row.type.toUpperCase() }}
              </span>
            </td>
            <td class="px-4 py-3 font-mono text-xs text-blue-700 font-semibold whitespace-nowrap">
              {{ row.code_naf || '—' }}
            </td>
            <td class="px-4 py-3 font-mono text-xs text-violet-700 font-semibold whitespace-nowrap">
              {{ row.code_rome || '—' }}
            </td>
            <td class="px-4 py-3 font-medium text-slate-800 max-w-xs">
              <span v-html="highlight(row.name)" />
            </td>
            <td class="px-4 py-3 text-slate-500 max-w-sm">
              <span class="line-clamp-2" v-html="highlight(row.desc)" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex items-center justify-between px-6 py-4 border-t border-slate-100">
      <span class="text-sm text-slate-500">
        Page {{ page }} / {{ totalPages }}
      </span>
      <div class="flex items-center gap-2">
        <button
          @click="$emit('update:page', page - 1)"
          :disabled="page <= 1"
          class="btn-secondary px-3 py-1.5 text-xs"
        >
          ← Préc.
        </button>
        <button
          v-for="p in visiblePages"
          :key="p"
          @click="$emit('update:page', p)"
          :class="[
            'w-8 h-8 rounded-lg text-xs font-medium transition-all',
            p === page
              ? 'bg-brand-600 text-white'
              : 'text-slate-600 hover:bg-slate-100'
          ]"
        >
          {{ p }}
        </button>
        <button
          @click="$emit('update:page', page + 1)"
          :disabled="page >= totalPages"
          class="btn-secondary px-3 py-1.5 text-xs"
        >
          Suiv. →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { NafRomeRecord, SortField, SortDir } from '../types'

const props = defineProps<{
  rows: NafRomeRecord[]
  total: number
  totalAll: number
  page: number
  perPage: number
  totalPages: number
  sortField: SortField
  sortDir: SortDir
  keyword: string
}>()

const emit = defineEmits<{
  'update:page': [v: number]
  'update:perPage': [v: number]
  'update:sortField': [v: SortField]
  'update:sortDir': [v: SortDir]
  'export': []
}>()

const columns = [
  { field: 'type' as SortField,      label: 'Type',      class: 'w-20' },
  { field: 'code_naf' as SortField,  label: 'Code NAF',  class: 'w-28' },
  { field: 'code_rome' as SortField, label: 'Code ROME', class: 'w-28' },
  { field: 'name' as SortField,      label: 'Intitulé',  class: '' },
  { field: 'name' as SortField,      label: 'Description', class: '' },
]

function toggleSort(field: SortField) {
  if (props.sortField === field) {
    emit('update:sortDir', props.sortDir === 'asc' ? 'desc' : 'asc')
  } else {
    emit('update:sortField', field)
    emit('update:sortDir', 'asc')
  }
}

function highlight(text: string): string {
  if (!props.keyword) return text
  const words = props.keyword.trim().split(/\s+/).filter(Boolean)
  let result = text
  for (const w of words) {
    const re = new RegExp(`(${w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi')
    result = result.replace(re, '<mark class="bg-yellow-200 rounded px-0.5">$1</mark>')
  }
  return result
}

const visiblePages = computed(() => {
  const pages: number[] = []
  const delta = 2
  for (let p = Math.max(1, props.page - delta); p <= Math.min(props.totalPages, props.page + delta); p++) {
    pages.push(p)
  }
  return pages
})
</script>
