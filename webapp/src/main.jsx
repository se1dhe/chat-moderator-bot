import React from 'react'
import { createRoot } from 'react-dom/client'
import { HashRouter } from 'react-router-dom'
import { LangProvider } from './context/LangContext'
import { initTelegram } from './lib/telegram'
import App from './App'
import './styles/index.css'

initTelegram()

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <LangProvider>
      <HashRouter>
        <App />
      </HashRouter>
    </LangProvider>
  </React.StrictMode>,
)
