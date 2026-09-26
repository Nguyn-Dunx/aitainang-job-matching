import { NavLink, Outlet, useLocation } from 'react-router-dom'
import './AppLayout.css'

/**
 * 6 bước luồng sản phẩm aitainang.
 * Mỗi bước tương ứng 1 route trong React Router.
 */
const STEPS = [
  {
    number: 1,
    path: '/onboarding',
    title: 'Định hướng nghề nghiệp',
    description: 'Mục tiêu, kinh nghiệm, kỳ vọng',
    icon: '🎯',
  },
  {
    number: 2,
    path: '/upload-cv',
    title: 'Upload & Parse CV',
    description: 'Tải lên, AI trích xuất, xác nhận',
    icon: '📄',
  },
  {
    number: 3,
    path: '/matching',
    title: 'Matching CV–JD',
    description: 'Truy xuất top-K JD phù hợp',
    icon: '🔍',
  },
  {
    number: 4,
    path: '/results',
    title: 'Kết quả & Giải thích',
    description: 'Điểm khớp, breakdown, evidence',
    icon: '📊',
  },
  {
    number: 5,
    path: '/improve',
    title: 'Cải thiện CV',
    description: 'Gap, gợi ý sửa, delta score',
    icon: '✏️',
  },
  {
    number: 6,
    path: '/dashboard',
    title: 'Dashboard',
    description: 'Lịch sử, tiến độ, job đã lưu',
    icon: '📈',
  },
]

export default function AppLayout() {
  const location = useLocation()

  // Determine current step index
  const currentStepIndex = STEPS.findIndex(s => location.pathname.startsWith(s.path))

  return (
    <div className="app-layout">
      {/* Sidebar */}
      <aside className="sidebar glass">
        {/* Brand */}
        <div className="sidebar-brand">
          <div className="sidebar-brand-icon">ai</div>
          <div className="sidebar-brand-text">
            <span className="sidebar-brand-name">aitainang</span>
            <span className="sidebar-brand-tagline">Trợ lý nghề nghiệp AI</span>
          </div>
        </div>

        {/* Step navigation */}
        <nav className="sidebar-stepper">
          <div className="stepper-label">Luồng sản phẩm</div>

          {STEPS.map((step, idx) => (
            <div key={step.path}>
              <NavLink
                to={step.path}
                className={({ isActive }) => {
                  let cls = 'step-item'
                  if (isActive) cls += ' active'
                  if (idx < currentStepIndex) cls += ' completed'
                  return cls
                }}
              >
                <div className="step-number">
                  {idx < currentStepIndex ? '✓' : step.number}
                </div>
                <div className="step-content">
                  <span className="step-title">{step.title}</span>
                  <span className="step-description">{step.description}</span>
                </div>
              </NavLink>
              {idx < STEPS.length - 1 && (
                <div className={`step-connector${idx < currentStepIndex ? ' completed' : ''}`} />
              )}
            </div>
          ))}
        </nav>

        {/* Footer disclaimer */}
        <div className="sidebar-footer">
          <p className="sidebar-footer-disclaimer">
            <strong>⚠ Lưu ý:</strong> Điểm số do AI tạo ra mang tính tham khảo,
            không đảm bảo kết quả tuyển dụng thực tế.
          </p>
        </div>
      </aside>

      {/* Main area */}
      <div className="main-area">
        {/* Header */}
        <header className="main-header">
          <div className="header-breadcrumb">
            <span>aitainang</span>
            <span>/</span>
            <span className="header-breadcrumb-current">
              {currentStepIndex >= 0
                ? STEPS[currentStepIndex].title
                : 'Trang chủ'}
            </span>
          </div>
          <div className="header-actions">
            <div className="header-avatar" title="Tài khoản">
              U
            </div>
          </div>
        </header>

        {/* Page outlet */}
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
