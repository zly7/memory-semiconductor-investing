<script setup lang="ts">
import { computed } from 'vue'
import type { SparkPoint } from '@/lib/api'

const props = defineProps<{
  points: SparkPoint[]
  width?: number
  height?: number
  color?: string
}>()

const W = computed(() => props.width ?? 120)
const H = computed(() => props.height ?? 32)

const path = computed(() => {
  const p = props.points
  if (!p.length) return ''
  const vs = p.map(x => x.value).filter(Number.isFinite)
  if (!vs.length) return ''
  const min = Math.min(...vs)
  const max = Math.max(...vs)
  const span = max - min || 1
  const stepX = W.value / Math.max(1, p.length - 1)
  return p.map((pt, i) => {
    const x = i * stepX
    const y = H.value - ((pt.value - min) / span) * H.value
    return (i === 0 ? 'M' : 'L') + x.toFixed(1) + ',' + y.toFixed(1)
  }).join(' ')
})

const fillPath = computed(() => {
  if (!path.value) return ''
  return path.value + ` L${W.value},${H.value} L0,${H.value} Z`
})

const stroke = computed(() => {
  if (props.color) return props.color
  const p = props.points
  if (p.length < 2) return 'var(--text-3)'
  return p[p.length - 1].value >= p[0].value ? 'var(--up)' : 'var(--down)'
})
</script>

<template>
  <svg :width="W" :height="H" :viewBox="`0 0 ${W} ${H}`" class="block">
    <path :d="fillPath" :fill="stroke" fill-opacity="0.14" />
    <path :d="path" :stroke="stroke" stroke-width="1.4" fill="none" />
  </svg>
</template>
