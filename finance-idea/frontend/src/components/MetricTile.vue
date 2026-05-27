<script setup lang="ts">
const props = defineProps<{
  label: string
  value: string | number
  hint?: string
  tone?: 'up' | 'down' | 'warn' | 'neutral' | 'default'
}>()

const toneClass = {
  up: 'text-up', down: 'text-down', warn: 'text-warn',
  neutral: 'text-ink-2', default: 'text-ink-1',
}[props.tone ?? 'default']
</script>

<template>
  <div class="card px-3 py-2">
    <div class="text-[10.5px] text-ink-3 tracking-widest uppercase">{{ label }}</div>
    <div class="num-mono text-[18px] font-semibold mt-1" :class="toneClass">{{ value }}</div>
    <div v-if="hint" class="text-[11px] text-ink-3 mt-0.5">{{ hint }}</div>
  </div>
</template>
