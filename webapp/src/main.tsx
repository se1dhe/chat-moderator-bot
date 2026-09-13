import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './styles/index.css';
import { initTelegram } from './lib/telegram';
import { LangProvider } from './context/LangContext';
import { ThemeProvider } from './context/ThemeContext';
import { ErrorBoundary } from './components/ErrorBoundary';

initTelegram();

const rootElement = document.getElementById('root');
if (!rootElement) throw new Error("Root element not found");

createRoot(rootElement).render(
  <StrictMode>
    <BrowserRouter>
      <ThemeProvider>
        <LangProvider>
          <ErrorBoundary>
            <App />
          </ErrorBoundary>
        </LangProvider>
      </ThemeProvider>
    </BrowserRouter>
  </StrictMode>
);
