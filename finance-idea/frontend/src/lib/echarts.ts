// Centralized ECharts theme + helper to build a chart in a target div.
import * as echarts from 'echarts'

// Resolve CSS vars (computed at runtime so theme toggle reflects in charts).
export function tokens() {
  const css = getComputedStyle(document.documentElement)
  return {
    text1: css.getPropertyValue('--text-1').trim(),
    text2: css.getPropertyValue('--text-2').trim(),
    text3: css.getPropertyValue('--text-3').trim(),
    border: css.getPropertyValue('--border').trim(),
    bg1: css.getPropertyValue('--bg-1').trim(),
    bg2: css.getPropertyValue('--bg-2').trim(),
    up: css.getPropertyValue('--up').trim() || '#f04848',
    down: css.getPropertyValue('--down').trim() || '#1aaf60',
    warn: css.getPropertyValue('--warn').trim() || '#f5a623',
    accent: css.getPropertyValue('--accent').trim() || '#2f72ff',
  }
}

export function baseOption() {
  const t = tokens()
  return {
    backgroundColor: 'transparent',
    textStyle: { color: t.text1, fontFamily: 'JetBrains Mono, SF Mono, Menlo, monospace' },
    grid: { left: 50, right: 50, top: 20, bottom: 30, containLabel: false },
    tooltip: {
      trigger: 'axis',
      backgroundColor: t.bg2,
      borderColor: t.border,
      textStyle: { color: t.text1, fontSize: 12 },
      axisPointer: {
        type: 'cross',
        lineStyle: { color: t.text3, type: 'dashed' },
        crossStyle: { color: t.text3 },
        label: { backgroundColor: t.bg2, color: t.text1, borderColor: t.border },
      },
    },
    xAxis: {
      type: 'time',
      axisLine: { lineStyle: { color: t.border } },
      axisLabel: { color: t.text2 },
      splitLine: { show: false },
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: t.border } },
      axisLabel: { color: t.text2 },
      splitLine: { lineStyle: { color: t.border, type: 'dashed' } },
    },
  }
}

export { echarts }
