<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { echarts, baseOption, tokens } from '@/lib/echarts'
import type { EquityCurve } from '@/lib/api'

const props = defineProps<{ curves: EquityCurve[] }>()
const el = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null

const palette = ['var(--up)', 'var(--accent)', 'var(--warn)', 'var(--down)']

function render() {
  if (!chart) return
  const t = tokens()
  const colors = [t.up, t.accent, t.warn, t.down]
  const opt: any = baseOption()
  opt.grid = { left: 60, right: 30, top: 30, bottom: 40 }
  opt.legend = {
    textStyle: { color: t.text2 }, top: 0, left: 10, itemWidth: 14, itemHeight: 8,
  }
  opt.xAxis = { ...opt.xAxis, type: 'time' }
  opt.series = props.curves.map((c, i) => ({
    name: c.name,
    type: 'line',
    showSymbol: false,
    lineStyle: { color: colors[i % colors.length], width: 1.5 },
    data: c.points.map(p => [p.date, p.value]),
  }))
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
watch(() => props.curves, render, { deep: true })
</script>

<template>
  <div ref="el" class="w-full h-[300px]" />
</template>
