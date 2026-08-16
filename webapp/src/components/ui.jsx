import { X } from 'lucide-react'
import { haptic } from '../lib/telegram'

export function Toggle({ checked, onChange }) {
  return (
    <button
      type="button"
      className={`toggle ${checked ? 'on' : ''}`}
      onClick={() => { haptic('light'); onChange(!checked) }}
      aria-pressed={checked}
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

export function Segmented({ options, value, onChange }) {
  return (
    <div className="segmented">
      {options.map((o) => (
        <button
          key={o.value}
          className={value === o.value ? 'active' : ''}
          onClick={() => { haptic('light'); onChange(o.value) }}
        >
          {o.label}
        </button>
      ))}
    </div>
  )
}

export function Stepper({ value, min, max, step = 1, onChange }) {
  const clamp = (v) => Math.max(min, Math.min(max, v))
  return (
    <div className="stepper">
      <button onClick={() => { haptic('light'); onChange(clamp(value - step)) }}>−</button>
      <span className="val">{value}</span>
      <button onClick={() => { haptic('light'); onChange(clamp(value + step)) }}>+</button>
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
