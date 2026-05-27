import { defineStore } from 'pinia'
import { api, type IdeaDetail } from '@/lib/api'

interface State {
  byId: Record<string, IdeaDetail>
  loading: Record<string, boolean>
  error: Record<string, string | null>
}

export const useIdeaStore = defineStore('idea', {
  state: (): State => ({ byId: {}, loading: {}, error: {} }),
  actions: {
    async load(id: string, force = false) {
      if (!force && this.byId[id]) return this.byId[id]
      this.loading[id] = true
      this.error[id] = null
      try {
        const d = await api.idea(id)
        this.byId[id] = d
        return d
      } catch (e: any) {
        this.error[id] = String(e?.message ?? e)
        return null
      } finally {
        this.loading[id] = false
      }
    },
  },
})
