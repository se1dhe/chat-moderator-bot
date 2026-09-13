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
      <div className="section-label">{t('sec.exempt')}</div>
      <div className="card card-pad">
        {ids.length ? (
          <Chips items={ids.map(String)} onRemove={(x) => s.setSection('exempt_user_ids', ids.filter((i) => String(i) !== x))} />
        ) : (
          <div className="row-desc">{t('exempt.empty')}</div>
        )}
        <div className="chip-input">
          <input className="input" inputMode="numeric" value={val} placeholder={t('exempt.add')}
            onChange={(e) => setVal(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && add()} />
          <button className="btn btn-primary" onClick={add}><Plus size={16} /></button>
        </div>
      </div>
    </>
  )
}
