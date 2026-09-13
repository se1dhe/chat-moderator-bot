import { showAlert } from '../../lib/telegram'
import { Toggle, Row, Segmented, Stepper } from '../../components/ui'

const mins = (sec: number | null | undefined) => Math.round((sec || 0) / 60)

export default function Defcon({ s, t }: { s: any, t: any }) {
  const d = s.draft.defcon || { enabled: false, threshold: 10, action: 'read_only', lock_seconds: 900 }
  return (
    <>
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('sec.defcon')}</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-2 mb-4 shadow-sm w-full">
        <Row title={t('defcon.enabled')} desc={t('defcon.enabled_desc')}>
          <Toggle checked={d.enabled} onChange={(v) => s.updateSection('defcon', { enabled: v })} />
        </Row>
        
        {d.enabled && (
          <>
            <Row title={t('defcon.threshold')} onInfo={() => showAlert(t('defcon.info.threshold'))} value={`${d.threshold} / min`}>
              <Stepper value={d.threshold} min={2} max={100} onChange={(v) => s.updateSection('defcon', { threshold: v })} />
            </Row>
            <Row title={t('defcon.lockSeconds')} value={`${mins(d.lock_seconds)} ${t('common.minutes')}`}>
              <Stepper value={mins(d.lock_seconds)} min={1} max={1440} step={5} onChange={(v) => s.updateSection('defcon', { lock_seconds: v * 60 })} />
            </Row>
          </>
        )}
      </div>

      {d.enabled && (
        <>
          <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2 flex items-center justify-between">{t('defcon.action')} <button onClick={() => showAlert(t('defcon.info.action'))} className="text-neutral-400 hover:text-blue-500 mr-1"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg></button></div>
          <Segmented value={d.action} onChange={(v) => s.updateSection('defcon', { action: v })}
            options={[
              { value: 'read_only', label: t('action.read_only') },
              { value: 'strict', label: t('action.strict') },
              { value: 'captcha', label: t('action.captcha') },
            ]} />
        </>
      )}
    </>
  )
}
