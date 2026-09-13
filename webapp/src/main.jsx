import React from 'react'
import { createRoot } from 'react-dom/client'
import { HashRouter } from 'react-router-dom'
import { LangProvider } from './context/LangContext'
import { ThemeProvider } from './context/ThemeContext'
import { initTelegram } from './lib/telegram'
import App from './App'
import { ErrorBoundary } from './components/ErrorBoundary'
import './styles/index.css'

initTelegram()

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ErrorBoundary>
      <ThemeProvider>
        <LangProvider>
          <HashRouter>
            <App />
          </HashRouter>
        </LangProvider>
      </ThemeProvider>
    </ErrorBoundary>
  </React.StrictMode>,
)
