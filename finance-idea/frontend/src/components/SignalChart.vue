<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { echarts, baseOption, tokens } from '@/lib/echarts'
import type { SeriesPoint, ThresholdBand } from '@/lib/api'

const props = defineProps<{
  primary: SeriesPoint[]
  secondary?: SeriesPoint[] | null
  secondaryLabel?: string | null
  bands?: ThresholdBand[] | null
  unit?: string
}>()

const el = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null

function render() {
  if (!chart) return
  const t = tokens()
  const opt: any = baseOption()
  opt.grid = { left: 60, right: 60, top: 30, bottom: 40 }
  opt.legend = {
    textStyle: { color: t.text2 },
    top: 0, left: 10, itemWidth: 14, itemHeight: 8,
  }
  opt.tooltip.formatter = undefined
  opt.dataZoom = [
    { type: 'inside', start: 70, end: 100 },
    { type: 'slider', start: 70, end: 100, height: 18, bottom: 4,
      borderColor: t.border, fillerColor: 'rgba(47,114,255,0.15)',
      handleStyle: { color: t.accent }, textStyle: { color: t.text3 } },
  ]
  opt.xAxis = { ...opt.xAxis, type: 'time' }
  opt.yAxis = [
    { ...opt.yAxis, name: props.unit ?? '', nameTextStyle: { color: t.text3 } },
    props.secondary ? { type: 'value', position: 'right', name: props.secondaryLabel ?? '',
       nameTextStyle: { color: t.text3 },
       axisLine: { lineStyle: { color: t.border } },
       axisLabel: { color: t.text2 },
       splitLine: { show: false } } : null,
  ].filter(Boolean) as any

  const series: any[] = [{
    name: 'signal',
    type: 'line',
    showSymbol: false,
    lineStyle: { color: t.up, width: 1.4 },
    areaStyle: { color: 'rgba(240,72,72,0.10)' },
    data: props.primary.map(p => [p.date, p.value]),
  }]
  if (props.bands && props.bands.length) {
    series.push({
      name: 'p90',
      type: 'line',
      showSymbol: false,
      lineStyle: { color: t.warn, width: 0.8, type: 'dashed' },
      data: props.bands.map(b => [b.date, b.upper]),
    })
    series.push({
      name: 'p10',
      type: 'line',
      showSymbol: false,
      lineStyle: { color: t.down, width: 0.8, type: 'dashed' },
      data: props.bands.map(b => [b.date, b.lower]),
    })
  }
  if (props.secondary && props.secondary.length) {
    series.push({
      name: props.secondaryLabel ?? 'overlay',
      type: 'line',
      yAxisIndex: 1,
      showSymbol: false,
      lineStyle: { color: t.text3, width: 1.0 },
      data: props.secondary.map(p => [p.date, p.value]),
    })
  }
  opt.series = series
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

watch(() => [props.primary, props.secondary, props.bands], render, { deep: true })
</script>

<template>
  <div ref="el" class="w-full h-[420px]" />
</template>
