import { X, Lock } from 'lucide-react'
import { haptic } from '../lib/telegram'

export function Toggle({ checked, onChange, disabled, onDisabledClick }) {
  return (
    <button
      type="button"
      className={`toggle ${checked ? 'on' : ''} ${disabled ? 'is-disabled' : ''}`}
      onClick={() => {
        haptic('light')
        if (disabled) { onDisabledClick?.(); return }
        onChange(!checked)
      }}
      aria-pressed={checked}
      aria-disabled={disabled || undefined}
    />
  )
}

export function Row({ title, desc, value, children }) {
  return (
    <div className="row">
      <div className="row-body">
        <div className="row-title">{title}</div>
        {desc && <div className="row-desc">{desc}</div>}
      </div>
      {value !== undefined && <div className="row-value">{value}</div>}
      {children}
    </div>
  )
}

export function SectionLabel({ children }) {
  return <div className="section-label">{children}</div>
}

export function Segmented({ options, value, onChange, onLocked }) {
  return (
    <div className="segmented">
      {options.map((o) => (
        <button
          key={o.value}
          className={`${value === o.value ? 'active' : ''} ${o.locked ? 'is-locked' : ''}`}
          onClick={() => { haptic('light'); if (o.locked) { onLocked?.(o); return } onChange(o.value) }}
        >
          {o.locked && <Lock size={11} style={{ marginRight: 3, verticalAlign: '-1px' }} />}{o.label}
        </button>
      ))}
    </div>
  )
}

export function Stepper({ value, min, max, step = 1, onChange }) {
  const clamp = (v) => Math.max(min, Math.min(max, v))
  return (
    <div className="stepper">
      <button style={{ width: 44, height: 44, display: 'flex', alignItems: 'center', justifyContent: 'center' }} onClick={() => { haptic('light'); onChange(clamp(value - step)) }}>−</button>
      <span className="val">{value}</span>
      <button style={{ width: 44, height: 44, display: 'flex', alignItems: 'center', justifyContent: 'center' }} onClick={() => { haptic('light'); onChange(clamp(value + step)) }}>+</button>
    </div>
  )
}

export function Slider({ value, min, max, step = 1, onChange }) {
  return (
    <input
      type="range"
      className="slider"
      min={min}
      max={max}
      step={step}
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
    />
  )
}

export function Chips({ items, onRemove }) {
  if (!items.length) return null
  return (
    <div className="chips">
      {items.map((it) => (
        <span className="chip" key={it}>
          {it}
          {onRemove && <button onClick={() => { haptic('light'); onRemove(it) }}><X size={13} /></button>}
        </span>
      ))}
    </div>
  )
}

export function Spinner() {
  return (
    <div className="center-state">
      <div className="spinner" />
    </div>
  )
}
