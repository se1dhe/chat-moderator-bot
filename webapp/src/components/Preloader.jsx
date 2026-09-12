import { motion } from 'framer-motion'
import { useLang } from '../context/LangContext'

export function Preloader() {
  const { t } = useLang()

  return (
    <motion.div 
      className="fixed inset-0 z-[999] bg-tg-bg flex flex-col items-center justify-center"
      initial={{ opacity: 1 }}
      exit={{ opacity: 0, scale: 1.1, filter: 'blur(10px)' }}
      transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
    >
      <div className="relative w-32 h-32 mb-8">
        {/* Glowing backdrop */}
        <motion.div
          className="absolute inset-0 rounded-full bg-red-600/30 blur-2xl"
          animate={{
            scale: [1, 1.4, 1],
            opacity: [0.3, 0.6, 0.3]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        
        {/* Logo Container */}
        <motion.div 
          className="relative w-full h-full rounded-3xl overflow-hidden border border-red-500/20 shadow-2xl shadow-red-500/10"
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5, type: 'spring', bounce: 0.4 }}
        >
          <img 
            src="/app/logo.jpg" 
            alt="Red Queen"
            className="w-full h-full object-cover"
          />
        </motion.div>
      </div>

      <motion.h1 
        className="text-2xl font-display font-bold text-tg-text tracking-tight mb-2"
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2, duration: 0.5, type: 'spring' }}
      >
        RedQueen Security
      </motion.h1>
      
      <motion.p 
        className="text-tg-hint text-sm uppercase tracking-[0.2em]"
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.5, type: 'spring' }}
      >
        {t('common.loading') || 'Инициализация...'}
      </motion.p>
    </motion.div>
  )
}
