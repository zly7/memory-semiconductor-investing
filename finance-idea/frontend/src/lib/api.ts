// Typed fetch wrappers — keep in sync with backend/app/schemas.py

export interface SparkPoint { date: string; value: number }
export interface SeriesPoint { date: string; value: number }
export interface ThresholdBand { date: string; upper: number | null; lower: number | null }
export interface BucketRow {
  bucket: string
  n: number
  fwd_means: Record<string, number>
  fwd_winrates: Record<string, number>
}
export interface EquityCurve {
  name: string
  points: SeriesPoint[]
  stats: Record<string, number | null>
}
export interface SignalSnapshot {
  id: string
  name: string
  name_cn: string
  value: number | null
  unit: string
  level: 'hot' | 'warm' | 'neutral' | 'cold' | 'na'
  interpretation: string
  delta_7d: number | null
  delta_30d: number | null
  spark: SparkPoint[]
  last_update: string | null
}
export interface IdeaDetail {
  snapshot: SignalSnapshot
  description_md: string
  primary_series: SeriesPoint[]
  secondary_series: SeriesPoint[] | null
  secondary_label: string | null
  bands: ThresholdBand[] | null
  buckets: BucketRow[]
  bucket_horizons: string[]
  equity: EquityCurve[]
}
export interface DashboardResponse {
  asof: string
  signals: SignalSnapshot[]
}
export interface IndexTick {
  key: string
  name: string
  value: number
  change_pct: number
}
export interface TickerResponse { asof: string; items: IndexTick[] }
export interface MetaEntry {
  key: string; kind: string; rows: number; first: string | null; last: string | null
}
export interface MetaResponse { entries: MetaEntry[]; refreshed_at: string | null }
export interface IdeaSummary {
  id: string; name: string; name_cn: string; description: string; tags: string[]
}

async function get<T>(path: string): Promise<T> {
  const r = await fetch(path)
  if (!r.ok) throw new Error(`${r.status} ${path}`)
  return r.json() as Promise<T>
}

export const api = {
  dashboard: () => get<DashboardResponse>('/api/dashboard'),
  ideas:     () => get<IdeaSummary[]>('/api/ideas'),
  idea:      (id: string) => get<IdeaDetail>(`/api/ideas/${id}`),
  ticker:    () => get<TickerResponse>('/api/ticker'),
  meta:      () => get<MetaResponse>('/api/meta'),
}
