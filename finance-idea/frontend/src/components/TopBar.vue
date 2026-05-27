<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()
const dark = ref(!document.documentElement.classList.contains('light'))

function toggleTheme() {
  dark.value = !dark.value
  document.documentElement.classList.toggle('light', !dark.value)
  localStorage.setItem('theme', dark.value ? 'dark' : 'light')
}

const asof = computed(() => store.dashboard?.asof?.slice(0, 19).replace('T', ' ') ?? '—')

onMounted(() => {
  dark.value = !document.documentElement.classList.contains('light')
})
</script>

<template>
  <header class="border-b border-line bg-bg-1">
    <div class="px-4 lg:px-6 h-12 flex items-center gap-6 max-w-[1600px] mx-auto">
      <router-link to="/" class="flex items-center gap-2 no-underline">
        <span class="inline-block w-6 h-6 rounded bg-up flex items-center justify-center text-white font-bold text-sm">F</span>
        <span class="font-semibold text-ink-1 tracking-tight">FinanceIdea</span>
      </router-link>
      <nav class="flex items-center gap-5 text-ink-2 text-[13px]">
        <router-link to="/" active-class="text-ink-1" class="hover:text-ink-1 no-underline">行情</router-link>
        <a class="hover:text-ink-1 cursor-pointer">指标</a>
        <a class="hover:text-ink-1 cursor-pointer">回测</a>
      </nav>
      <div class="flex-1" />
      <span class="text-ink-3 text-[12px]">数据时间 {{ asof }}</span>
      <button
        @click="store.load()"
        :disabled="store.loading"
        class="text-ink-2 hover:text-ink-1 text-[12px] flex items-center gap-1 border border-line px-2 h-7 rounded"
        :class="{ 'opacity-50 cursor-wait': store.loading }"
      >
        <span :class="{ 'animate-spin': store.loading }">↻</span>
        刷新
      </button>
      <button
        @click="toggleTheme"
        class="text-ink-2 hover:text-ink-1 text-[12px] w-7 h-7 rounded border border-line flex items-center justify-center"
        :title="dark ? '切换浅色' : '切换深色'"
      >
        <span v-if="dark">☾</span>
        <span v-else>☀</span>
      </button>
    </div>
  </header>
</template>
