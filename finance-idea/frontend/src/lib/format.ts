export function fmtNum(v: number | null | undefined, digits = 2): string {
  if (v == null || !isFinite(v)) return '—'
  return v.toLocaleString('en-US', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  })
}

export function fmtPct(v: number | null | undefined, digits = 2): string {
  if (v == null || !isFinite(v)) return '—'
  const s = v.toLocaleString('en-US', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  })
  return (v >= 0 ? '+' : '') + s + '%'
}

export function fmtSigned(v: number | null | undefined, digits = 2): string {
  if (v == null || !isFinite(v)) return '—'
  const s = v.toLocaleString('en-US', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  })
  return (v >= 0 ? '+' : '') + s
}

/** CN convention: red for up/positive, green for down/negative. */
export function dirColor(v: number | null | undefined): string {
  if (v == null || !isFinite(v) || v === 0) return 'text-ink-2'
  return v > 0 ? 'text-up' : 'text-down'
}

export function levelColor(level: string): string {
  switch (level) {
    case 'hot':  return 'text-up'
    case 'warm': return 'text-warn'
    case 'cold': return 'text-down'
    case 'neutral': return 'text-ink-2'
    default: return 'text-ink-3'
  }
}

export function levelBg(level: string): string {
  switch (level) {
    case 'hot':  return 'bg-up-soft text-up'
    case 'warm': return 'bg-warn-soft text-warn'
    case 'cold': return 'bg-down-soft text-down'
    case 'neutral': return 'bg-nu-soft text-ink-2'
    default: return 'bg-nu-soft text-ink-3'
  }
}

export function levelLabel(level: string): string {
  switch (level) {
    case 'hot':  return 'HOT'
    case 'warm': return 'WARM'
    case 'cold': return 'COLD'
    case 'neutral': return 'NEUTRAL'
    default: return 'N/A'
  }
}
