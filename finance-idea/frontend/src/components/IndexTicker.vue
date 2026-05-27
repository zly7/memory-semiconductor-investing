<script setup lang="ts">
import { computed } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import { fmtNum, fmtPct, dirColor } from '@/lib/format'

const store = useDashboardStore()
const items = computed(() => store.ticker?.items ?? [])
</script>

<template>
  <div class="border-b border-line bg-bg-1 overflow-x-auto">
    <div class="px-4 lg:px-6 h-10 flex items-center gap-6 max-w-[1600px] mx-auto whitespace-nowrap">
      <template v-for="t in items" :key="t.key">
        <div class="flex items-center gap-2 text-[12.5px]">
          <span class="text-ink-2">{{ t.name }}</span>
          <span class="num-mono font-semibold" :class="dirColor(t.change_pct)">{{ fmtNum(t.value, t.value > 1000 ? 2 : 2) }}</span>
          <span class="num-mono text-[11.5px]" :class="dirColor(t.change_pct)">{{ fmtPct(t.change_pct) }}</span>
        </div>
        <span class="text-line">·</span>
      </template>
      <div v-if="!items.length" class="text-ink-3 text-[12px]">指数加载中…</div>
    </div>
  </div>
</template>
