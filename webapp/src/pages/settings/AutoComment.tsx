import { useState, useEffect, useRef } from 'react'
import { Plus, Lock } from 'lucide-react'
import { Toggle, Row, Segmented, Stepper, Slider, Chips, Spinner } from '../../components/ui'
import { haptic, showAlert } from '../../lib/telegram'
import { api } from '../../lib/api'

export default function AutoComment({ s, t }) {
  const c = s.draft.auto_comment || { enabled: false, text: '', media_url: '' }
  const [uploading, setUploading] = useState(false)
  const mountedRef = useRef(true)
  useEffect(() => { return () => { mountedRef.current = false } }, [])
  
  const handleUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    setUploading(true)
    try {
      const { file_id } = await api.uploadMedia(s.chatId, file)
      s.updateSection('auto_comment', { media_url: file_id })
    } catch (err) {
      showAlert(t('common.error') + ': ' + err.message)
    } finally {
      if (mountedRef.current) setUploading(false)
      e.target.value = ''
    }
  }

  return (
    <>
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('sec.autocomment')}</div>
      <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-2 mb-4 shadow-sm w-full">
        <Row title={t('sec.autocomment.enable')} subtitle={t('sec.autocomment.enable.desc')}>
          <Toggle checked={c.enabled} onChange={(v) => s.updateSection('auto_comment', { enabled: v })} />
        </Row>
      </div>
      
      {c.enabled && (
        <>
          <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('sec.autocomment.text')}</div>
          <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-4 mb-4 shadow-sm w-full">
            <textarea 
              className="w-full bg-transparent border-none outline-none text-neutral-900 dark:text-neutral-50 resize-none"
              rows={4}
              placeholder={t('sec.autocomment.text.ph')}
              value={c.text}
              onChange={(e) => s.updateSection('auto_comment', { text: e.target.value })}
            />
          </div>
          <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('sec.autocomment.media')}</div>
          <div className="bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-4 mb-4 shadow-sm w-full flex items-center justify-between">
            <div className="text-[13px] text-neutral-500 truncate mr-3">
              {c.media_url ? t('common.mediaAttached') : t('common.noMedia')}
            </div>
            <label className={`px-4 py-2 bg-neutral-200 dark:bg-neutral-800 hover:bg-neutral-300 dark:hover:bg-neutral-700 text-neutral-900 dark:text-neutral-50 rounded-xl text-[13px] font-bold transition-colors whitespace-nowrap cursor-pointer ${uploading ? 'opacity-50' : ''}`}>
              {uploading ? t('common.uploading') : t('common.upload')}
              <input type="file" className="hidden" accept="image/*,video/mp4,image/gif" disabled={uploading} onChange={handleUpload} />
            </label>
          </div>
          {c.media_url && (
            <div className="px-4 mt-2 mb-1 text-right">
              <button className="text-[13px] text-red-500" onClick={() => s.updateSection('auto_comment', { media_url: '' })}>
                {t('settings.removeMedia')}
              </button>
            </div>
          )}
          <p className="px-4 mt-2 text-[13px] text-neutral-500">
            {t('sec.autocomment.media.desc')}
          </p>
        </>
      )}
    </>
  )
}
