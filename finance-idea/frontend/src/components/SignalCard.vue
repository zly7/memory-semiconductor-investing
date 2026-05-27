<script setup lang="ts">
import { computed } from 'vue'
import type { SignalSnapshot } from '@/lib/api'
import { fmtNum, fmtSigned, levelColor, dirColor } from '@/lib/format'
import ThresholdPill from './ThresholdPill.vue'
import Sparkline from './Sparkline.vue'

const props = defineProps<{ signal: SignalSnapshot }>()
const s = computed(() => props.signal)
const valueColor = computed(() => {
  if (s.value.value == null) return 'text-ink-3'
  if (s.value.level === 'na') return 'text-ink-3'
  return levelColor(s.value.level)
})
</script>

<template>
  <router-link :to="`/idea/${s.id}`"
    class="card p-3.5 flex flex-col gap-2 no-underline hover:border-ink-3 transition-colors group">
    <div class="flex items-start justify-between gap-2">
      <div>
        <div class="text-[11.5px] text-ink-3 tracking-wide">{{ s.id.toUpperCase() }}</div>
        <div class="text-[14px] text-ink-1 font-medium leading-tight">{{ s.name_cn }}</div>
      </div>
      <ThresholdPill :level="s.level" />
    </div>

    <div class="flex items-end justify-between gap-2 mt-1">
      <div>
        <div class="num-mono text-[28px] leading-none font-semibold" :class="valueColor">
          {{ fmtNum(s.value, 2) }}<span class="text-[14px] text-ink-2 ml-1">{{ s.unit }}</span>
        </div>
        <div class="text-[11.5px] mt-1.5 flex gap-2">
          <span class="text-ink-3">7d</span>
          <span class="num-mono" :class="dirColor(s.delta_7d)">{{ fmtSigned(s.delta_7d) }}</span>
          <span class="text-ink-3 ml-2">30d</span>
          <span class="num-mono" :class="dirColor(s.delta_30d)">{{ fmtSigned(s.delta_30d) }}</span>
        </div>
      </div>
      <Sparkline :points="s.spark" :width="110" :height="36" />
    </div>

    <div class="text-[11.5px] text-ink-2 truncate group-hover:text-ink-1">
      {{ s.interpretation }}
    </div>
  </router-link>
</template>
