<script setup lang="ts">
import TopBar from './components/TopBar.vue'
import IndexTicker from './components/IndexTicker.vue'
import { onMounted } from 'vue'
import { useDashboardStore } from './stores/dashboard'

const store = useDashboardStore()
onMounted(() => store.load())
</script>

<template>
  <div class="min-h-screen flex flex-col bg-bg-0 text-ink-1">
    <TopBar />
    <IndexTicker />
    <main class="flex-1 px-4 lg:px-6 py-4 max-w-[1600px] mx-auto w-full">
      <router-view />
    </main>
    <footer class="border-t border-line py-2 px-6 text-[11px] text-ink-3 flex justify-between">
      <span>finance-idea · 10 个市场情绪信号</span>
      <span>数据源: akshare / yfinance · 本地 parquet 缓存</span>
    </footer>
  </div>
</template>
