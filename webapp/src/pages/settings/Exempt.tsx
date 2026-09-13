import { useState, useEffect, useRef } from 'react'
import { Plus, Lock } from 'lucide-react'
import { Toggle, Row, Segmented, Stepper, Slider, Chips, Spinner } from '../../components/ui'
import { haptic, showAlert } from '../../lib/telegram'
import { api } from '../../lib/api'

export default function Exempt({ s, t }) {
  const ids = s.draft.exempt_user_ids
  const [val, setVal] = useState('')
  const add = () => {
    const n = parseInt(val.trim(), 10)
    if (Number.isFinite(n) && !ids.includes(n)) s.setSection('exempt_user_ids', [...ids, n])
    setVal('')
  }
  return (
    <>
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('sec.exempt')}</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60/60/60/60 rounded-2xl p-4 mb-4 shadow-sm w-full">
        {ids.length ? (
          <Chips items={ids.map(String)} onRemove={(x) => s.setSection('exempt_user_ids', ids.filter((i) => String(i) !== x))} />
        ) : (
          <div className="text-[13px] text-neutral-500 leading-snug">{t('exempt.empty')}</div>
        )}
        <div className="chip-input">
          <input className="w-full px-4 py-3 bg-neutral-50 dark:bg-black border border-neutral-200 dark:border-neutral-800/60/60/60/60 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px]" inputMode="numeric" value={val} placeholder={t('exempt.add')}
            onChange={(e) => setVal(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && add()} />
          <button className="w-full flex items-center justify-center gap-2 py-3 bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 text-white shadow-[0_4px_20px_-4px_rgba(220,38,38,0.5)] rounded-xl font-bold transition-all active:scale-95  text-[15px]" onClick={add}><Plus size={16} /></button>
        </div>
      </div>
    </>
  )
}
