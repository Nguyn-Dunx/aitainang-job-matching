import { Routes, Route, Navigate } from 'react-router-dom'
import AppLayout from './components/layout/AppLayout'
import OnboardingPage from './pages/OnboardingPage/OnboardingPage'
import UploadCVPage from './pages/UploadCVPage/UploadCVPage'
import MatchingPage from './pages/MatchingPage/MatchingPage'
import ResultsPage from './pages/ResultsPage/ResultsPage'
import ImprovePage from './pages/ImprovePage/ImprovePage'
import DashboardPage from './pages/DashboardPage/DashboardPage'

/**
 * App — root component
 *
 * Luồng 6 bước:
 * 1. /onboarding  → Định hướng nghề nghiệp
 * 2. /upload-cv   → Upload & Parse CV
 * 3. /matching    → Matching CV–JD
 * 4. /results     → Kết quả & Giải thích
 * 5. /improve     → Cải thiện CV
 * 6. /dashboard   → Dashboard theo dõi
 */
export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/onboarding" element={<OnboardingPage />} />
        <Route path="/upload-cv" element={<UploadCVPage />} />
        <Route path="/matching" element={<MatchingPage />} />
        <Route path="/results" element={<ResultsPage />} />
        <Route path="/improve" element={<ImprovePage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        {/* Redirect root → bước 1 */}
        <Route path="/" element={<Navigate to="/onboarding" replace />} />
        {/* Catch-all */}
        <Route path="*" element={<Navigate to="/onboarding" replace />} />
      </Route>
    </Routes>
  )
}
