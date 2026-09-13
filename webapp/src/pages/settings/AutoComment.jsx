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
      <div className="section-label">{t('sec.autocomment')}</div>
      <div className="card">
        <Row title={t('sec.autocomment.enable')} subtitle={t('sec.autocomment.enable.desc')}>
          <Toggle checked={c.enabled} onChange={(v) => s.updateSection('auto_comment', { enabled: v })} />
        </Row>
      </div>
      
      {c.enabled && (
        <>
          <div className="section-label">{t('sec.autocomment.text')}</div>
          <div className="card p-4">
            <textarea 
              className="w-full bg-transparent border-none outline-none text-[var(--tg-theme-text-color)] resize-none"
              rows={4}
              placeholder={t('sec.autocomment.text.ph')}
              value={c.text}
              onChange={(e) => s.updateSection('auto_comment', { text: e.target.value })}
            />
          </div>
          <div className="section-label">{t('sec.autocomment.media')}</div>
          <div className="card p-4 flex items-center justify-between">
            <div className="text-[13px] text-[var(--tg-theme-hint-color)] truncate mr-3">
              {c.media_url ? t('common.mediaAttached') : t('common.noMedia')}
            </div>
            <label className={`btn btn-secondary px-3 py-1 text-[13px] whitespace-nowrap cursor-pointer ${uploading ? 'opacity-50' : ''}`}>
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
          <p className="px-4 mt-2 text-[13px] text-[var(--tg-theme-hint-color)]">
            {t('sec.autocomment.media.desc')}
          </p>
        </>
      )}
    </>
  )
}
