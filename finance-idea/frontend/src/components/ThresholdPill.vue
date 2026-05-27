<script setup lang="ts">
import { computed } from 'vue'
import { levelBg, levelLabel } from '@/lib/format'

const props = defineProps<{ level: string }>()
const cls = computed(() => levelBg(props.level))
const label = computed(() => levelLabel(props.level))
</script>

<template>
  <span class="inline-flex items-center px-2 py-[2px] rounded text-[10.5px] font-semibold tracking-wider"
        :class="cls">{{ label }}</span>
</template>
