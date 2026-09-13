import { useState } from 'react';
import { ShieldCheck, Filter, Check, Rocket } from 'lucide-react';
import { useLang } from '../context/LangContext';
import { useChatSettings } from '../context/ChatSettingsContext';
import { haptic } from '../lib/telegram';
import { Toggle, Row, Spinner } from './ui';

export function OnboardingWizard() {
  const { t } = useLang();
  const { draft, updateSection, pro, openUpgrade, billing } = useChatSettings();
  const [step, setStep] = useState(1);
  
  if (!draft) return <div className="flex-1 flex items-center justify-center py-12"><Spinner /></div>;

  const next = () => {
    haptic('light');
    setStep(s => s + 1);
  };
  
  const finish = () => {
    haptic('success');
    updateSection('onboarding', { setup_completed: true });
  };

  const s1 = (
    <div className="flex-1 flex flex-col items-center justify-center text-center animate-in fade-in slide-in-from-bottom-2 px-2">
      <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mb-6 mt-4">
        <Rocket size={40} className="text-primary" />
      </div>
      <h3 className="text-2xl font-black tracking-tight text-neutral-900 dark:text-neutral-50 mb-3">{t('ob.title.1')}</h3>
      <p className="text-[15px] leading-relaxed text-neutral-500 mb-8 max-w-[280px]">
        {t('ob.desc.1')}
      </p>
      
      <div className="w-full bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-2 mb-8 shadow-sm text-left">
        <Row title={t('ob.card.1')} desc={t('ob.card.1.sub')}>
          <Toggle checked={draft.antiflood.enabled} onChange={v => updateSection('antiflood', { enabled: v })} />
        </Row>
      </div>

      <button className="w-full py-3.5 bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 text-white shadow-[0_4px_20px_-4px_rgba(220,38,38,0.5)] rounded-xl font-bold transition-all active:scale-95 text-base" onClick={next}>{t('ob.btn.continue')}</button>
    </div>
  );

  const s2 = (
    <div className="flex-1 flex flex-col items-center justify-center text-center animate-in fade-in slide-in-from-right-4 px-2">
      <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mb-6 mt-4">
        <Filter size={40} className="text-primary" />
      </div>
      <h3 className="text-2xl font-black tracking-tight text-neutral-900 dark:text-neutral-50 mb-3">{t('ob.title.2')}</h3>
      <p className="text-[15px] leading-relaxed text-neutral-500 mb-8 max-w-[280px]">
        {t('ob.desc.2')}
      </p>
      
      <div className="w-full bg-white dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800/60 rounded-2xl p-2 mb-8 shadow-sm text-left flex flex-col gap-1">
        <Row title={t('ob.card.2')} desc={t('ob.card.2.sub')}>
          <Toggle checked={draft.core.ai_mode !== 'off'} onChange={v => updateSection('core', { ai_mode: v ? 'quarantine' : 'off' })} />
        </Row>
        <Row title={t('ob.card.2.block')} desc={t('ob.card.2.block.sub')}>
          <Toggle checked={draft.filters.block_links} onChange={v => updateSection('filters', { block_links: v })} />
        </Row>
      </div>

      <button className="w-full py-3.5 bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 text-white shadow-[0_4px_20px_-4px_rgba(220,38,38,0.5)] rounded-xl font-bold transition-all active:scale-95 text-base" onClick={next}>{t('ob.btn.continue')}</button>
    </div>
  );

  const s3 = (
    <div className="flex-1 flex flex-col items-center justify-center text-center animate-in fade-in slide-in-from-right-4 px-2">
      <div className="w-20 h-20 bg-amber-500/10 rounded-full flex items-center justify-center mb-6 mt-4">
        <ShieldCheck size={40} className="text-amber-500" />
      </div>
      <h3 className="text-2xl font-black tracking-tight text-neutral-900 dark:text-neutral-50 mb-3">{t('ob.title.3')}</h3>
      <p className="text-[15px] leading-relaxed text-neutral-500 mb-8 max-w-[280px]">
        {t('ob.desc.3')}
      </p>
      
      {!pro ? (
        <div className="w-full flex flex-col gap-3">
          <button 
            className="w-full py-3.5 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-xl font-bold transition-all active:scale-95 text-base shadow-lg shadow-amber-500/20" 
            onClick={openUpgrade}
          >
            {t('ob.btn.pro', { stars: billing?.price_stars || 500 })}
          </button>
          <button 
            className="w-full py-3.5 bg-neutral-200 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 rounded-xl font-bold transition-all active:scale-95 text-base" 
            onClick={finish}
          >
            {t('ob.btn.skip')}
          </button>
        </div>
      ) : (
        <div className="w-full flex flex-col items-center">
          <div className="text-emerald-500 font-bold mb-8 flex items-center gap-2 text-lg">
            <Check size={24} /> {t('ob.pro.unlocked')}
          </div>
          <button className="w-full py-3.5 bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 text-white shadow-[0_4px_20px_-4px_rgba(220,38,38,0.5)] rounded-xl font-bold transition-all active:scale-95 text-base" onClick={finish}>{t('ob.btn.finish')}</button>
        </div>
      )}
    </div>
  );

  return (
    <div className="w-full flex-1 flex flex-col">
      {step === 1 && s1}
      {step === 2 && s2}
      {step === 3 && s3}
    </div>
  );
}
