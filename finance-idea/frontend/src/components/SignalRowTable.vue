<script setup lang="ts">
import type { SignalSnapshot } from '@/lib/api'
import { fmtNum, fmtSigned, dirColor, levelColor } from '@/lib/format'
import ThresholdPill from './ThresholdPill.vue'
import Sparkline from './Sparkline.vue'

defineProps<{ signals: SignalSnapshot[] }>()
</script>

<template>
  <div class="card overflow-hidden">
    <table class="w-full text-[12.5px]">
      <thead class="bg-bg-2 text-ink-3 text-[11.5px]">
        <tr>
          <th class="px-3 py-2 text-left font-medium">信号</th>
          <th class="px-3 py-2 text-right font-medium">数值</th>
          <th class="px-3 py-2 text-right font-medium">7d</th>
          <th class="px-3 py-2 text-right font-medium">30d</th>
          <th class="px-3 py-2 font-medium">60d 走势</th>
          <th class="px-3 py-2 font-medium">状态</th>
          <th class="px-3 py-2 text-left font-medium">解读</th>
          <th class="px-3 py-2 text-right font-medium text-ink-3">最新</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s in signals" :key="s.id"
            class="border-t border-line hover:bg-bg-2/60 cursor-pointer"
            @click="$router.push(`/idea/${s.id}`)">
          <td class="px-3 py-2">
            <div class="text-ink-1 font-medium">{{ s.name_cn }}</div>
            <div class="text-[10.5px] text-ink-3 tracking-wide">{{ s.id }}</div>
          </td>
          <td class="px-3 py-2 text-right num-mono font-semibold" :class="levelColor(s.level)">
            {{ fmtNum(s.value) }}<span class="text-[10.5px] text-ink-3 ml-0.5">{{ s.unit }}</span>
          </td>
          <td class="px-3 py-2 text-right num-mono" :class="dirColor(s.delta_7d)">{{ fmtSigned(s.delta_7d) }}</td>
          <td class="px-3 py-2 text-right num-mono" :class="dirColor(s.delta_30d)">{{ fmtSigned(s.delta_30d) }}</td>
          <td class="px-3 py-2"><Sparkline :points="s.spark" :width="120" :height="28" /></td>
          <td class="px-3 py-2"><ThresholdPill :level="s.level" /></td>
          <td class="px-3 py-2 text-ink-2 truncate max-w-[260px]">{{ s.interpretation }}</td>
          <td class="px-3 py-2 text-right text-[11px] text-ink-3 num-mono">{{ s.last_update ?? '—' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
