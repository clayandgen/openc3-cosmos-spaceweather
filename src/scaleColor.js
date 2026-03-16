export function scaleColor(value) {
  const v = parseInt(value) || 0
  if (v === 0) return 'green'
  if (v === 1) return 'light-green'
  if (v === 2) return 'yellow-darken-2'
  if (v === 3) return 'orange'
  if (v === 4) return 'deep-orange'
  return 'red'
}
