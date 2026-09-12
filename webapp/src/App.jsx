import { Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from './components/Layout'
import { ChatPicker } from './pages/ChatPicker'
import { Dashboard } from './pages/Dashboard'
import { SettingsSection } from './pages/SettingsSection'
import { Members } from './pages/Members'
import { Quarantine } from './pages/Quarantine'
import { Audit } from './pages/Audit'
import { Stats } from './pages/Stats'
import { WhatsNewModal } from './components/WhatsNewModal'
import { Landing } from './pages/Landing'
import { isTelegram } from './lib/telegram'
import { TelegramBackButton } from './components/TelegramBackButton'

export default function App() {
  return (
    <>
      <TelegramBackButton />
      <Routes>
        <Route path="/" element={isTelegram ? <ChatPicker /> : <Landing />} />
        <Route path="/c/:cid" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="s/:section" element={<SettingsSection />} />
          <Route path="members" element={<Members />} />
          <Route path="quarantine" element={<Quarantine />} />
          <Route path="audit" element={<Audit />} />
          <Route path="stats" element={<Stats />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <WhatsNewModal />
    </>
  )
}
