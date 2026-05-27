<script setup lang="ts">
import { computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'
import { useIdeaStore } from '@/stores/idea'
import { useDashboardStore } from '@/stores/dashboard'
import { fmtNum, fmtSigned, dirColor, levelColor } from '@/lib/format'
import ThresholdPill from '@/components/ThresholdPill.vue'
import SignalChart from '@/components/SignalChart.vue'
import BucketHeatmap from '@/components/BucketHeatmap.vue'
import EquityCurveChart from '@/components/EquityCurveChart.vue'
import MetricTile from '@/components/MetricTile.vue'

const route = useRoute()
const router = useRouter()
const store = useIdeaStore()
const dashStore = useDashboardStore()

const id = computed(() => String(route.params.id))
const detail = computed(() => store.byId[id.value])
const snapshot = computed(() => detail.value?.snapshot)
const loading = computed(() => store.loading[id.value])
const err = computed(() => store.error[id.value])

const narrative = computed(() => detail.value
  ? marked.parse(detail.value.description_md || '', { breaks: true })
  : '')

onMounted(() => store.load(id.value))
watch(id, (v) => store.load(v))

const equityStats = computed(() => {
  if (!detail.value?.equity?.length) return []
  return detail.value.equity.map(e => ({
    name: e.name,
    cagr: e.stats.cagr != null ? (e.stats.cagr * 100).toFixed(2) + '%' : '—',
    sharpe: e.stats.sharpe?.toFixed(2) ?? '—',
    maxdd: e.stats.maxdd != null ? (e.stats.maxdd * 100).toFixed(1) + '%' : '—',
    total: e.stats.total != null ? (e.stats.total * 100).toFixed(0) + '%' : '—',
  }))
})

const sampleSize = computed(() => detail.value?.primary_series?.length ?? 0)
const sampleRange = computed(() => {
  const arr = detail.value?.primary_series
  if (!arr || arr.length === 0) return '—'
  return `${arr[0].date} → ${arr[arr.length - 1].date}`
})
</script>

<template>
  <div class="flex flex-col gap-4">
    <!-- header strip -->
    <div class="card px-5 py-4">
      <div class="flex items-start gap-4">
        <button @click="router.back()" class="text-ink-3 hover:text-ink-1 text-[12px] mt-0.5">← 返回</button>
        <div class="flex-1">
          <div class="text-[10.5px] text-ink-3 tracking-widest uppercase">{{ id }}</div>
          <h1 class="text-[20px] font-semibold text-ink-1 m-0 leading-tight">
            {{ snapshot?.name_cn || id }}
          </h1>
          <div v-if="snapshot" class="flex items-center gap-3 mt-2">
            <span class="num-mono text-[32px] font-semibold leading-none"
                  :class="levelColor(snapshot.level)">
              {{ fmtNum(snapshot.value, 2) }}<span class="text-[14px] text-ink-2 ml-1">{{ snapshot.unit }}</span>
            </span>
            <ThresholdPill :level="snapshot.level" />
            <span class="text-[12.5px] text-ink-2">{{ snapshot.interpretation }}</span>
          </div>
        </div>
        <div class="text-right text-[11.5px] text-ink-3 num-mono">
          <div>asof {{ snapshot?.last_update ?? '—' }}</div>
          <div class="mt-1">
            7d <span :class="dirColor(snapshot?.delta_7d ?? null)">{{ fmtSigned(snapshot?.delta_7d ?? null) }}</span>
            &nbsp;·&nbsp;
            30d <span :class="dirColor(snapshot?.delta_30d ?? null)">{{ fmtSigned(snapshot?.delta_30d ?? null) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading && !detail" class="text-ink-3 text-center py-12">加载中…</div>
    <div v-if="err" class="card p-4 text-down">{{ err }}</div>

    <template v-if="detail">
      <!-- main chart + right rail -->
      <div class="grid grid-cols-1 lg:grid-cols-[1fr,320px] gap-4">
        <div class="card p-3">
          <div class="flex items-center justify-between mb-2 px-1">
            <div class="text-[12.5px] text-ink-2">信号时序 ·
              <span v-if="detail.secondary_label" class="text-ink-3">+ {{ detail.secondary_label }} 覆盖</span>
            </div>
            <div class="text-[11px] text-ink-3 num-mono">{{ sampleSize.toLocaleString() }} obs · {{ sampleRange }}</div>
          </div>
          <SignalChart
            :primary="detail.primary_series"
            :secondary="detail.secondary_series"
            :secondary-label="detail.secondary_label"
            :bands="detail.bands"
            :unit="snapshot?.unit"
          />
        </div>

        <div class="flex flex-col gap-2">
          <div class="grid grid-cols-2 gap-2">
            <MetricTile label="latest" :value="fmtNum(snapshot?.value ?? null, 2) + ' ' + (snapshot?.unit ?? '')" :tone="snapshot?.level === 'hot' ? 'up' : snapshot?.level === 'cold' ? 'down' : snapshot?.level === 'warm' ? 'warn' : 'default'" />
            <MetricTile label="7d Δ" :value="fmtSigned(snapshot?.delta_7d ?? null)" :tone="(snapshot?.delta_7d ?? 0) > 0 ? 'up' : (snapshot?.delta_7d ?? 0) < 0 ? 'down' : 'neutral'" />
            <MetricTile label="30d Δ" :value="fmtSigned(snapshot?.delta_30d ?? null)" :tone="(snapshot?.delta_30d ?? 0) > 0 ? 'up' : (snapshot?.delta_30d ?? 0) < 0 ? 'down' : 'neutral'" />
            <MetricTile label="样本" :value="sampleSize.toLocaleString()" hint="trading days" />
          </div>
          <div class="card p-4 prose-sm max-w-none text-[12.5px] leading-relaxed text-ink-1"
               v-html="narrative" />
        </div>
      </div>

      <!-- bucket heatmap + equity curve -->
      <div v-if="detail.buckets?.length || detail.equity?.length"
           class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div class="card p-3" v-if="detail.buckets?.length">
          <div class="text-[12.5px] text-ink-2 mb-2 px-1">分位前向回报热力图 (mean fwd return by quintile × horizon)</div>
          <BucketHeatmap :rows="detail.buckets" :horizons="detail.bucket_horizons" />
        </div>
        <div class="card p-3" v-if="detail.equity?.length">
          <div class="text-[12.5px] text-ink-2 mb-2 px-1">净值曲线对比 (策略 vs benchmark)</div>
          <EquityCurveChart :curves="detail.equity" />
          <table class="w-full text-[11.5px] mt-2 num-mono">
            <thead class="text-ink-3">
              <tr>
                <th class="text-left font-normal px-2 py-1">strategy</th>
                <th class="text-right font-normal px-2 py-1">total</th>
                <th class="text-right font-normal px-2 py-1">CAGR</th>
                <th class="text-right font-normal px-2 py-1">Sharpe</th>
                <th class="text-right font-normal px-2 py-1">maxDD</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in equityStats" :key="s.name" class="border-t border-line">
                <td class="text-left text-ink-1 px-2 py-1 font-sans text-[12px]">{{ s.name }}</td>
                <td class="text-right text-ink-1 px-2 py-1">{{ s.total }}</td>
                <td class="text-right text-ink-1 px-2 py-1">{{ s.cagr }}</td>
                <td class="text-right text-ink-1 px-2 py-1">{{ s.sharpe }}</td>
                <td class="text-right text-down px-2 py-1">{{ s.maxdd }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<style>
.prose-sm h2 { font-size: 13px; margin: 8px 0 4px; color: var(--text-1); font-weight: 600; }
.prose-sm h3 { font-size: 12.5px; margin: 6px 0 4px; color: var(--text-2); font-weight: 600; }
.prose-sm p  { margin: 4px 0; }
.prose-sm strong { color: var(--up); }
.prose-sm code { background: var(--bg-2); padding: 1px 4px; border-radius: 3px; }
</style>
