import { defineStore } from 'pinia'
import { api, type DashboardResponse, type TickerResponse } from '@/lib/api'

interface State {
  dashboard: DashboardResponse | null
  ticker: TickerResponse | null
  loading: boolean
  error: string | null
}

export const useDashboardStore = defineStore('dashboard', {
  state: (): State => ({ dashboard: null, ticker: null, loading: false, error: null }),
  actions: {
    async load() {
      this.loading = true
      this.error = null
      try {
        const [d, t] = await Promise.all([api.dashboard(), api.ticker()])
        this.dashboard = d
        this.ticker = t
      } catch (e: any) {
        this.error = String(e?.message ?? e)
      } finally {
        this.loading = false
      }
    },
  },
})
