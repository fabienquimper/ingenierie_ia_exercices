<template>
  <div class="min-h-screen bg-slate-50">
    <!-- Header -->
    <header class="bg-white border-b border-slate-200 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-xl font-bold text-slate-900 flex items-center gap-2">
              <span class="text-2xl">🔍</span>
              Explorateur NAF ↔ ROME
            </h1>
            <p class="text-sm text-slate-500 mt-0.5">
              Correspondances entre codes d'activité (NAF) et codes métier (ROME)
              <span class="ml-2 text-xs bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-full font-medium">
                Source : API FastAPI — Jour 2
              </span>
            </p>
          </div>
          <div class="flex items-center gap-3">
            <span :class="['flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full font-medium', apiOnline ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700']">
              <span :class="['w-2 h-2 rounded-full', apiOnline ? 'bg-emerald-500 animate-pulse' : 'bg-red-500']" />
              API {{ apiOnline ? 'connectée' : 'hors ligne' }}
            </span>
            <div v-if="loading" class="flex items-center gap-2 text-sm text-slate-500">
              <svg class="animate-spin w-4 h-4 text-brand-600" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
              </svg>
              Chargement…
            </div>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      <!-- Erreur -->
      <div v-if="error" class="bg-red-50 border border-red-200 rounded-xl p-4 text-red-700 text-sm flex items-start gap-3">
        <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
        </svg>
        <div>
          <p class="font-semibold">Erreur de connexion à l'API</p>
          <p class="mt-0.5 text-red-600">{{ error }}</p>
          <p class="mt-1 text-xs text-red-500">
            Lancez l'API : <code class="bg-red-100 px-1 rounded">./run.sh</code> puis rechargez cette page.
          </p>
        </div>
      </div>

      <!-- Stats -->
      <StatsBar v-if="allData.length" :data="allData" />

      <!-- Recherche -->
      <SearchBar
        v-model:keyword="keyword"
        v-model:code="code"
        v-model:typeFilter="typeFilter"
        @reset="resetFilters"
      />

      <!-- Tableau -->
      <ResultsTable
        :rows="paginatedRows"
        :total="filteredRows.length"
        :totalAll="allData.length"
        :page="page"
        :perPage="perPage"
        :totalPages="totalPages"
        :sortField="sortField"
        :sortDir="sortDir"
        :keyword="keyword"
        @update:page="page = $event"
        @update:perPage="perPage = $event; page = 1"
        @update:sortField="sortField = $event; page = 1"
        @update:sortDir="sortDir = $event"
        @export="handleExport"
      />
    </main>

    <!-- Footer -->
    <footer class="text-center py-6 text-xs text-slate-400">
      TP 1.1 · Master IA · CreativeTech · API : {{ apiBase }}
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import SearchBar from './components/SearchBar.vue'
import ResultsTable from './components/ResultsTable.vue'
import StatsBar from './components/StatsBar.vue'
import { loadData, search, exportToCsv } from './services/apiService'
import type { NafRomeRecord, SortField, SortDir } from './types'

const apiBase = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

// --- State ---
const allData    = ref<NafRomeRecord[]>([])
const loading    = ref(true)
const error      = ref('')
const apiOnline  = ref(false)

const keyword    = ref('')
const code       = ref('')
const typeFilter = ref<'all' | 'naf' | 'rome' | 'matching'>('all')
const sortField  = ref<SortField>('type')
const sortDir    = ref<SortDir>('asc')
const page       = ref(1)
const perPage    = ref(25)

// --- Chargement initial ---
onMounted(async () => {
  try {
    allData.value = await loadData()
    apiOnline.value = true
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
    apiOnline.value = false
  } finally {
    loading.value = false
  }
})

// --- Filtrage ---
const filteredRows = computed(() =>
  search(allData.value, keyword.value, code.value, typeFilter.value)
)

// --- Tri ---
const sortedRows = computed(() => {
  const rows = [...filteredRows.value]
  rows.sort((a, b) => {
    const av = (a[sortField.value] ?? '').toLowerCase()
    const bv = (b[sortField.value] ?? '').toLowerCase()
    return sortDir.value === 'asc' ? av.localeCompare(bv) : bv.localeCompare(av)
  })
  return rows
})

// --- Pagination ---
const totalPages = computed(() => Math.max(1, Math.ceil(sortedRows.value.length / perPage.value)))

const paginatedRows = computed(() => {
  const start = (page.value - 1) * perPage.value
  return sortedRows.value.slice(start, start + perPage.value)
})

// Reset page quand les filtres changent
watch([keyword, code, typeFilter], () => { page.value = 1 })

// --- Actions ---
function resetFilters() {
  keyword.value    = ''
  code.value       = ''
  typeFilter.value = 'all'
  page.value       = 1
}

function handleExport() {
  exportToCsv(sortedRows.value)
}
</script>
