import React, { ReactNode } from 'react';
import { AlertTriangle, RefreshCcw } from 'lucide-react';
import { haptic } from '../lib/telegram';
import { LOCALES, Locales } from '../i18n/translations';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("React ErrorBoundary caught an error:", error, errorInfo);
  }

  handleReload = () => {
    haptic('light');
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      const code = window.Telegram?.WebApp?.initDataUnsafe?.user?.language_code || 'en';
      const c = (code).toLowerCase().slice(0, 2);
      const lang: Locales = LOCALES[c as Locales] ? c as Locales : 'en';
      const t = (k: string) => LOCALES[lang][k] || k;

      return (
        <div className="min-h-screen w-full flex flex-col items-center justify-center p-6 bg-neutral-50 dark:bg-neutral-950 text-neutral-900 dark:text-neutral-50 text-center">
          <div className="w-20 h-20 bg-red-500/10 rounded-full flex items-center justify-center mb-6">
            <AlertTriangle size={40} className="text-red-500" />
          </div>
          <h2 className="text-xl font-bold tracking-tight mb-3">{t('error.title')}</h2>
          <p className="text-sm text-neutral-500 mb-6 max-w-[280px]">
            {t('error.desc')}
          </p>
          <div className="bg-neutral-100 dark:bg-neutral-900 p-3 rounded-xl text-[11px] text-red-500 font-mono mb-8 max-w-full overflow-auto max-h-[100px] text-left border border-red-500/20">
            {this.state.error?.toString()}
          </div>
          <button 
            className="flex items-center gap-2 px-6 py-3.5 bg-primary hover:bg-primary-dark text-white rounded-xl font-bold transition-all active:scale-95 shadow-lg shadow-primary/20" 
            onClick={this.handleReload}
          >
            <RefreshCcw size={18} /> {t('error.reload')}
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
