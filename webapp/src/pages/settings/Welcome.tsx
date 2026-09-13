import { useState, useEffect, useRef } from 'react'
import { Plus, Lock } from 'lucide-react'
import { Toggle, Row, Segmented, Stepper, Slider, Chips, Spinner } from '../../components/ui'
import { haptic, showAlert } from '../../lib/telegram'
import { api } from '../../lib/api'

export default function Welcome({ s, t }) {
  const text = s.draft.welcome_text || ''
  const fileId = s.draft.welcome_file_id || ''
  const [uploading, setUploading] = useState(false)
  const fileInputRef = useRef(null)

  const handleUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    setUploading(true)
    try {
      const res = await api.uploadMedia(s.chatId, file)
      if (res && res.file_id) {
        s.setSection('welcome_file_id', res.file_id)
      }
    } catch (err) {
      showAlert('Error uploading file')
    } finally {
      setUploading(false)
    }
  }

  return (
    <>
      <div className="text-sm font-semibold text-neutral-500 uppercase tracking-wider ml-1 mt-4 mb-2">{t('sec.welcome')}</div>
      <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-2xl p-4 mb-4 shadow-sm w-full" style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
        <div className="row-desc">{t('welcome.desc')}</div>
        
        <div style={{ fontWeight: 600, fontSize: '15px', marginTop: '0.5rem' }}>{t('welcome.text')}</div>
        <textarea
          className="w-full px-4 py-3 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-800 rounded-xl focus:outline-none focus:border-primary/50 transition-colors font-medium text-[15px]"
          style={{ minHeight: '120px', resize: 'vertical' }}
          value={text}
          placeholder={t('welcome.text.ph')}
          onChange={(e) => s.setSection('welcome_text', e.target.value)}
        ></textarea>

        <div style={{ fontWeight: 600, fontSize: '15px', marginTop: '0.5rem' }}>{t('welcome.media')}</div>
        {fileId && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div className="row-desc" style={{ color: 'var(--tg-theme-success-color)' }}>{t('welcome.media.uploaded')}</div>
            <button className="w-full flex items-center justify-center gap-2 py-3 bg-neutral-200 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 rounded-xl font-bold transition-all active:scale-95 text-[15px]" style={{ padding: '0.3rem 0.6rem', fontSize: '12px' }} onClick={() => s.setSection('welcome_file_id', null)}>{t('common.delete') || 'Delete'}</button>
          </div>
        )}
        <input 
          type="file" 
          accept="image/*,video/*" 
          ref={fileInputRef} 
          style={{ display: 'none' }} 
          onChange={handleUpload} 
        />
        <button 
          className="w-full flex items-center justify-center gap-2 py-3 bg-neutral-200 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 rounded-xl font-bold transition-all active:scale-95 text-[15px]" 
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
        >
          {uploading ? <Spinner /> : (fileId ? t('welcome.media.change') : t('welcome.media.upload'))}
        </button>
      </div>
    </>
  )
}
