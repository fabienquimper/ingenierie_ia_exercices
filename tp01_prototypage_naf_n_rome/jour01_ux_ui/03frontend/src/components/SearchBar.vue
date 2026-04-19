<template>
  <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Recherche par mot-clé -->
      <div class="md:col-span-2">
        <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1.5">
          Recherche par mot-clé
        </label>
        <div class="relative">
          <span class="absolute inset-y-0 left-3 flex items-center text-slate-400">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </span>
          <input
            :value="keyword"
            @input="$emit('update:keyword', ($event.target as HTMLInputElement).value)"
            type="text"
            placeholder="ex : informatique, médecin, agriculture…"
            class="input pl-10"
          />
        </div>
      </div>

      <!-- Recherche par code -->
      <div>
        <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1.5">
          Code NAF ou ROME
        </label>
        <input
          :value="code"
          @input="$emit('update:code', ($event.target as HTMLInputElement).value)"
          type="text"
          placeholder="ex : 62.01Z ou M1805"
          class="input font-mono"
        />
      </div>
    </div>

    <!-- Filtres type + reset -->
    <div class="flex flex-wrap items-center gap-3 mt-4">
      <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Type :</span>

      <button
        v-for="opt in typeOptions"
        :key="opt.value"
        @click="$emit('update:typeFilter', opt.value)"
        :class="[
          'px-3 py-1.5 rounded-full text-xs font-semibold transition-all',
          typeFilter === opt.value
            ? opt.activeClass
            : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
        ]"
      >
        {{ opt.label }}
      </button>

      <button
        v-if="keyword || code || typeFilter !== 'all'"
        @click="$emit('reset')"
        class="ml-auto text-xs text-slate-500 hover:text-red-500 flex items-center gap-1 transition-colors"
      >
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
        Réinitialiser
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  keyword: string
  code: string
  typeFilter: 'all' | 'naf' | 'rome' | 'matching'
}>()

defineEmits<{
  'update:keyword': [v: string]
  'update:code': [v: string]
  'update:typeFilter': [v: 'all' | 'naf' | 'rome' | 'matching']
  'reset': []
}>()

const typeOptions = [
  { value: 'all',      label: 'Tous',             activeClass: 'bg-slate-700 text-white' },
  { value: 'naf',      label: 'NAF',              activeClass: 'bg-blue-600 text-white' },
  { value: 'rome',     label: 'ROME',             activeClass: 'bg-violet-600 text-white' },
  { value: 'matching', label: 'Matching NAF↔ROME', activeClass: 'bg-emerald-600 text-white' },
] as const
</script>
