<script setup lang="ts">
import { computed } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import SignalCard from '@/components/SignalCard.vue'
import SignalRowTable from '@/components/SignalRowTable.vue'

const store = useDashboardStore()
const signals = computed(() => store.dashboard?.signals ?? [])

// Sort: by level (hot > warm > cold > neutral > na) for "top movers" rail
const levelRank: Record<string, number> = { hot: 0, warm: 1, cold: 2, neutral: 3, na: 4 }
const topSignals = computed(() => {
  return [...signals.value].sort((a, b) => (levelRank[a.level] ?? 9) - (levelRank[b.level] ?? 9)).slice(0, 5)
})
</script>

<template>
  <div class="flex flex-col gap-4">
    <div class="flex items-baseline justify-between">
      <div>
        <h1 class="text-[18px] font-semibold text-ink-1 m-0">市场情绪 · 信号面板</h1>
        <div class="text-[12px] text-ink-3 mt-1">10 个 idea，按 quintile bucket 验证过的反指 / 顺势信号</div>
      </div>
      <div v-if="store.error" class="text-down text-[12px]">{{ store.error }}</div>
    </div>

    <!-- top movers -->
    <section v-if="topSignals.length">
      <h2 class="text-[12px] text-ink-3 tracking-widest font-medium uppercase mb-2">Today&nbsp;·&nbsp;按重要性</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-3">
        <SignalCard v-for="s in topSignals" :key="s.id" :signal="s" />
      </div>
    </section>

    <!-- full table -->
    <section>
      <h2 class="text-[12px] text-ink-3 tracking-widest font-medium uppercase mb-2 mt-2">All&nbsp;·&nbsp;全部 10 个信号</h2>
      <SignalRowTable :signals="signals" />
    </section>

    <div v-if="store.loading && !signals.length" class="text-ink-3 text-center py-12">加载中…</div>
  </div>
</template>
