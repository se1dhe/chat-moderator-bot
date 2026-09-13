import React from 'react';
import { AlertTriangle, RefreshCcw } from 'lucide-react';
import { haptic } from '../lib/telegram';
import { LOCALES } from '../i18n/translations';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
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
      const lang = LOCALES[c] ? c : 'en';
      const t = (k) => LOCALES[lang][k] || k;

      return (
        <div style={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '24px',
          background: 'var(--bg-base, #07070e)',
          color: 'var(--tg-theme-text-color, #fff)',
          textAlign: 'center'
        }}>
          <AlertTriangle size={64} style={{ color: '#ef4444', marginBottom: '16px' }} />
          <h2 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '12px' }}>{t('error.title')}</h2>
          <p style={{ color: 'var(--tg-theme-hint-color, #888)', fontSize: '14px', marginBottom: '24px', maxWidth: '300px' }}>
            {t('error.desc')}
          </p>
          <div style={{
            background: 'var(--tg-theme-secondary-bg-color, #1a1a1a)',
            padding: '12px',
            borderRadius: '12px',
            fontSize: '11px',
            color: '#ef4444',
            fontFamily: 'monospace',
            marginBottom: '24px',
            wordBreak: 'break-word',
            maxWidth: '100%',
            overflow: 'auto',
            maxHeight: '100px',
            textAlign: 'left'
          }}>
            {this.state.error?.toString()}
          </div>
          <button 
            className="btn btn-primary" 
            onClick={this.handleReload}
            style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '12px 24px', borderRadius: '12px' }}
          >
            <RefreshCcw size={18} /> {t('error.reload')}
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
