import { useState } from 'react'
import { FileText, Sparkles, X } from 'lucide-react'
import { api } from '../lib/api'
import { useParams } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'

export function AISummary({ t }) {
  const { cid } = useParams<{ cid: string }>()
  const [loading, setLoading] = useState(false)
  const [summary, setSummary] = useState('')
  const [error, setError] = useState('')

  const handleGenerate = async () => {
    setLoading(true)
    setError('')
    try {
      const res = await api.get(`/api/chats/${cid}/summary`)
      setSummary(res.data.summary)
    } catch (e: any) {
      setError(e.response?.data?.reason || e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-gradient-to-r from-blue-500/10 to-indigo-500/10 border border-blue-500/20 dark:from-blue-500/20 dark:to-indigo-500/20 rounded-2xl p-4 mb-4 relative overflow-hidden flex flex-col items-start shadow-sm">
      <div className="flex items-center gap-2 font-semibold text-blue-600 dark:text-blue-400 mb-2">
        <Sparkles size={18} />
        {t('dashboard.ai_summary')}
      </div>
      
      {!summary && !loading && (
        <>
          <div className="text-sm text-neutral-600 dark:text-neutral-400 mb-4">
            {t('dashboard.ai_summary.desc')}
          </div>
          <button 
            onClick={handleGenerate}
            className="bg-blue-500 hover:bg-blue-600 text-white font-medium px-4 py-2 rounded-xl text-sm transition-colors active:scale-95 w-full flex items-center justify-center gap-2"
          >
            <FileText size={16} />
            {t('dashboard.ai_summary.btn')}
          </button>
        </>
      )}

      {loading && (
        <div className="flex items-center gap-3 text-sm text-neutral-600 dark:text-neutral-400 py-2">
          <div className="animate-spin rounded-full h-4 w-4 border-2 border-blue-500 border-t-transparent" />
          {t('dashboard.ai_summary.loading')}
        </div>
      )}

      {error && (
        <div className="text-sm text-red-500 bg-red-50 dark:bg-red-500/10 px-3 py-2 rounded-lg w-full mt-2">
          {error}
        </div>
      )}

      {summary && (
        <div className="w-full">
          <div className="bg-white/60 dark:bg-black/40 backdrop-blur-md border border-black/5 dark:border-white/5 rounded-xl p-3 text-sm leading-relaxed mb-3 whitespace-pre-wrap">
            {summary}
          </div>
          <button 
            onClick={() => setSummary('')}
            className="text-xs text-neutral-500 hover:text-neutral-700 dark:hover:text-neutral-300 font-medium px-2 py-1 rounded-lg w-full flex justify-center items-center gap-1"
          >
            <X size={14} /> {t('common.close')}
          </button>
        </div>
      )}
    </div>
  )
}
