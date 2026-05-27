<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { echarts, baseOption, tokens } from '@/lib/echarts'
import type { BucketRow } from '@/lib/api'

const props = defineProps<{ rows: BucketRow[]; horizons: string[] }>()
const el = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null

function render() {
  if (!chart || !props.rows.length) return
  const t = tokens()
  // Heatmap data: each cell is [horizon_index, bucket_index, value]
  const data: [number, number, number][] = []
  const minMax = { min: Infinity, max: -Infinity }
  props.rows.forEach((r, yi) => {
    props.horizons.forEach((h, xi) => {
      const v = r.fwd_means[h]
      if (v != null && isFinite(v)) {
        data.push([xi, yi, v])
        minMax.min = Math.min(minMax.min, v)
        minMax.max = Math.max(minMax.max, v)
      }
    })
  })
  const absMax = Math.max(Math.abs(minMax.min), Math.abs(minMax.max), 0.001)

  const opt: any = baseOption()
  opt.grid = { left: 70, right: 30, top: 30, bottom: 40 }
  opt.xAxis = { type: 'category', data: props.horizons,
                axisLine: { lineStyle: { color: t.border } },
                axisLabel: { color: t.text2 } }
  opt.yAxis = { type: 'category', data: props.rows.map(r => r.bucket),
                axisLine: { lineStyle: { color: t.border } },
                axisLabel: { color: t.text2 }, inverse: true }
  opt.tooltip = {
    trigger: 'item',
    backgroundColor: t.bg2,
    borderColor: t.border,
    textStyle: { color: t.text1, fontSize: 12 },
    formatter: (p: any) => {
      const r = props.rows[p.data[1]]
      const h = props.horizons[p.data[0]]
      const v = (p.data[2] * 100).toFixed(2) + '%'
      const win = r.fwd_winrates[h]
      const w = win != null ? (win * 100).toFixed(0) + '%' : '—'
      return `<b>${r.bucket}</b> &middot; ${h}<br/>` +
             `mean fwd return: <b>${v}</b><br/>` +
             `win rate: ${w}<br/>` +
             `samples: ${r.n}`
    },
  }
  opt.visualMap = {
    show: false,
    min: -absMax,
    max:  absMax,
    inRange: { color: [t.down, t.bg2, t.up] },
  }
  opt.series = [{
    type: 'heatmap',
    data,
    label: { show: true, color: t.text1, fontSize: 11,
             formatter: (p: any) => (p.data[2] * 100).toFixed(1) + '%' },
    itemStyle: { borderColor: t.border, borderWidth: 1 },
    progressive: 0,
  }]
  chart.setOption(opt, true)
}

function resize() { chart?.resize() }

onMounted(() => {
  if (!el.value) return
  chart = echarts.init(el.value, undefined, { renderer: 'canvas' })
  render()
  window.addEventListener('resize', resize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resize)
  chart?.dispose()
  chart = null
})

watch(() => [props.rows, props.horizons], render, { deep: true })
</script>

<template>
  <div ref="el" class="w-full h-[300px]" />
</template>
