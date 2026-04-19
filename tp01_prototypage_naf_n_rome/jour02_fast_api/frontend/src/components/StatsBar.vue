<template>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
    <div
      v-for="stat in stats"
      :key="stat.label"
      class="bg-white rounded-xl border border-slate-200 px-5 py-4 shadow-sm"
    >
      <p class="text-xs font-semibold text-slate-500 uppercase tracking-wide">{{ stat.label }}</p>
      <p class="mt-1 text-2xl font-bold" :class="stat.color">{{ stat.value }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { NafRomeRecord } from '../types'

const props = defineProps<{ data: NafRomeRecord[] }>()

const stats = computed(() => [
  {
    label: 'Total enregistrements',
    value: props.data.length,
    color: 'text-slate-800',
  },
  {
    label: 'Codes NAF',
    value: props.data.filter((r) => r.type === 'naf').length,
    color: 'text-blue-600',
  },
  {
    label: 'Codes ROME',
    value: props.data.filter((r) => r.type === 'rome').length,
    color: 'text-violet-600',
  },
  {
    label: 'Correspondances NAF↔ROME',
    value: props.data.filter((r) => r.type === 'matching').length,
    color: 'text-emerald-600',
  },
])
</script>
