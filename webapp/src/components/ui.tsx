import { X, Lock } from 'lucide-react';
import { haptic } from '../lib/telegram';
import { ReactNode } from 'react';

export function Toggle({ checked, onChange, disabled, onDisabledClick }: { checked: boolean, onChange: (v: boolean) => void, disabled?: boolean, onDisabledClick?: () => void }) {
  return (
    <button
      type="button"
      className={`relative w-12 h-7 rounded-full transition-colors flex items-center shrink-0 ${
        checked ? (disabled ? 'bg-primary/50' : 'bg-primary') : 'bg-neutral-200 dark:bg-neutral-700'
      } ${disabled ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'}`}
      onClick={() => {
        haptic('light');
        if (disabled) { onDisabledClick?.(); return; }
        onChange(!checked);
      }}
      aria-pressed={checked}
      aria-disabled={disabled || undefined}
    >
      <div 
        className={`w-6 h-6 rounded-full bg-white shadow-sm transition-transform ${
          checked ? 'translate-x-[22px]' : 'translate-x-0.5'
        }`}
      />
    </button>
  );
}

export function Row({ title, desc, value, children }: { title: string, desc?: string, value?: any, children?: ReactNode }) {
  return (
    <div className="flex items-center justify-between w-full p-2 gap-3 min-h-[44px]">
      <div className="flex flex-col flex-1 min-w-0 justify-center">
        <div className="text-sm font-semibold text-neutral-900 dark:text-neutral-50 truncate leading-tight">{title}</div>
        {desc && <div className="text-[13px] text-neutral-500 leading-snug mt-0.5 pr-2">{desc}</div>}
      </div>
      {value !== undefined && <div className="text-sm font-medium text-neutral-400 shrink-0">{value}</div>}
      {children && <div className="shrink-0">{children}</div>}
    </div>
  );
}

export function SectionLabel({ children }: { children: ReactNode }) {
  return <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{children}</div>;
}

export function Segmented({ options, value, onChange, onLocked }: { options: any[], value: any, onChange: (v: any) => void, onLocked?: (v: any) => void }) {
  return (
    <div className="flex items-center w-full p-1 bg-neutral-200/60 dark:bg-neutral-800 rounded-xl relative overflow-hidden">
      {options.map((o) => {
        const active = value === o.value;
        return (
          <button
            key={o.value}
            className={`flex-1 relative flex items-center justify-center py-2 text-[13px] font-bold rounded-lg transition-all z-10 ${
              active 
                ? 'text-neutral-900 dark:text-neutral-50 shadow-sm' 
                : 'text-neutral-500 hover:text-neutral-700 dark:hover:text-neutral-300'
            } ${o.locked ? 'opacity-80' : ''}`}
            onClick={() => { haptic('light'); if (o.locked) { onLocked?.(o); return; } onChange(o.value); }}
          >
            {active && (
              <div className="absolute inset-0 bg-white dark:bg-[#0a0a0a] rounded-lg shadow-sm -z-10" />
            )}
            {o.locked && <Lock size={12} className="mr-1 opacity-70" />}
            {o.label}
          </button>
        );
      })}
    </div>
  );
}

export function Stepper({ value, min, max, step = 1, onChange }: { value: number, min: number, max: number, step?: number, onChange: (v: number) => void }) {
  const clamp = (v: number) => Math.max(min, Math.min(max, v));
  return (
    <div className="flex items-center bg-neutral-100 dark:bg-neutral-800 rounded-xl border border-neutral-200 dark:border-neutral-700 overflow-hidden h-9">
      <button className="w-10 h-full flex items-center justify-center text-neutral-500 hover:bg-neutral-200 dark:hover:bg-neutral-700 active:bg-neutral-300 dark:active:bg-neutral-600 transition-colors" onClick={() => { haptic('light'); onChange(clamp(value - step)); }}>−</button>
      <span className="w-10 text-center font-bold text-neutral-900 dark:text-neutral-50 font-mono text-sm">{value}</span>
      <button className="w-10 h-full flex items-center justify-center text-neutral-500 hover:bg-neutral-200 dark:hover:bg-neutral-700 active:bg-neutral-300 dark:active:bg-neutral-600 transition-colors" onClick={() => { haptic('light'); onChange(clamp(value + step)); }}>+</button>
    </div>
  );
}

export function Slider({ value, min, max, step = 1, onChange }: { value: number, min: number, max: number, step?: number, onChange: (v: number) => void }) {
  return (
    <input
      type="range"
      className="w-full h-2 bg-neutral-200 dark:bg-neutral-700 rounded-full appearance-none cursor-pointer accent-primary"
      min={min}
      max={max}
      step={step}
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
    />
  );
}

export function Chips({ items, onRemove }: { items: string[], onRemove?: (v: string) => void }) {
  if (!items.length) return null;
  return (
    <div className="flex flex-wrap gap-2 pt-1 pb-2">
      {items.map((it) => (
        <span className="flex items-center gap-1.5 px-3 py-1.5 bg-neutral-100 dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700 text-neutral-700 dark:text-neutral-300 text-[13px] font-medium rounded-lg" key={it}>
          {it}
          {onRemove && (
            <button 
              className="text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 transition-colors -mr-1" 
              onClick={() => { haptic('light'); onRemove(it); }}
            >
              <X size={14} />
            </button>
          )}
        </span>
      ))}
    </div>
  );
}

export function Spinner() {
  return (
    <div className="w-8 h-8 rounded-full border-2 border-primary/20 border-t-primary animate-spin" />
  );
}
