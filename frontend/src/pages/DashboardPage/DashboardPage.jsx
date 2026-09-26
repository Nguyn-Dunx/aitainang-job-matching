import { useNavigate } from 'react-router-dom'
import '../../styles/pages.css'

/**
 * Bước 6 — Dashboard
 *
 * Lịch sử phiên chấm, job đã lưu, tiến độ đóng gap kỹ năng theo thời gian.
 *
 * Hiện tại: chỉ khung UI, chưa nối API.
 */

const MOCK_HISTORY = [
  { id: 1, date: '2026-09-25', cv: 'CV v2.1', jobsMatched: 12, topScore: 82 },
  { id: 2, date: '2026-09-20', cv: 'CV v1.0', jobsMatched: 8, topScore: 65 },
]

const MOCK_SAVED_JOBS = [
  { id: 1, title: 'Frontend Developer', company: 'Công ty A', score: 82 },
  { id: 2, title: 'React Developer', company: 'Công ty D', score: 78 },
  { id: 3, title: 'Fullstack Developer', company: 'Công ty C', score: 71 },
]

const MOCK_SKILL_PROGRESS = [
  { skill: 'TypeScript', before: 0, after: 70 },
  { skill: 'Testing', before: 20, after: 65 },
  { skill: 'Next.js', before: 0, after: 40 },
  { skill: 'Docker', before: 30, after: 30 },
]

export default function DashboardPage() {
  const navigate = useNavigate()

  return (
    <div>
      {/* Page header */}
      <div className="page-header">
        <div className="page-step-badge">
          <span>📈</span>
          <span>Bước 6 / 6</span>
        </div>
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">
          Theo dõi hành trình cải thiện CV, lịch sử phiên chấm, và tiến độ
          đóng gap kỹ năng của bạn.
        </p>
      </div>

      {/* Stats overview */}
      <div className="grid-3" style={{ marginBottom: 'var(--space-8)' }}>
        <div className="card card-accent" style={{ textAlign: 'center' }}>
          <div style={{
            fontSize: 'var(--font-size-3xl)',
            fontWeight: 'var(--font-weight-bold)',
          }}>
            <span className="gradient-text">+17</span>
          </div>
          <div style={{
            fontSize: 'var(--font-size-sm)',
            color: 'var(--color-text-muted)',
            marginTop: 'var(--space-1)',
          }}>
            Tổng delta score
          </div>
        </div>

        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{
            fontSize: 'var(--font-size-3xl)',
            fontWeight: 'var(--font-weight-bold)',
            color: 'var(--color-text-primary)',
          }}>
            2
          </div>
          <div style={{
            fontSize: 'var(--font-size-sm)',
            color: 'var(--color-text-muted)',
            marginTop: 'var(--space-1)',
          }}>
            Phiên chấm
          </div>
        </div>

        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{
            fontSize: 'var(--font-size-3xl)',
            fontWeight: 'var(--font-weight-bold)',
            color: 'var(--color-text-primary)',
          }}>
            3
          </div>
          <div style={{
            fontSize: 'var(--font-size-sm)',
            color: 'var(--color-text-muted)',
            marginTop: 'var(--space-1)',
          }}>
            Job đã lưu
          </div>
        </div>
      </div>

      <div className="grid-2">
        {/* Session history */}
        <div className="card">
          <h3 style={{
            fontSize: 'var(--font-size-base)',
            fontWeight: 'var(--font-weight-semibold)',
            marginBottom: 'var(--space-4)',
            color: 'var(--color-text-primary)',
          }}>
            📅 Lịch sử phiên chấm
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
            {MOCK_HISTORY.map(session => (
              <div
                key={session.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: 'var(--space-3)',
                  background: 'var(--color-bg-primary)',
                  borderRadius: 'var(--radius-lg)',
                }}
              >
                <div>
                  <div style={{
                    fontSize: 'var(--font-size-sm)',
                    fontWeight: 'var(--font-weight-medium)',
                    color: 'var(--color-text-primary)',
                  }}>
                    {session.cv}
                  </div>
                  <div style={{
                    fontSize: 'var(--font-size-xs)',
                    color: 'var(--color-text-muted)',
                  }}>
                    {session.date} • {session.jobsMatched} JD matched
                  </div>
                </div>
                <span className="tag tag-match">Top: {session.topScore}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Saved jobs */}
        <div className="card">
          <h3 style={{
            fontSize: 'var(--font-size-base)',
            fontWeight: 'var(--font-weight-semibold)',
            marginBottom: 'var(--space-4)',
            color: 'var(--color-text-primary)',
          }}>
            ⭐ Job đã lưu
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
            {MOCK_SAVED_JOBS.map(job => (
              <div
                key={job.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: 'var(--space-3)',
                  background: 'var(--color-bg-primary)',
                  borderRadius: 'var(--radius-lg)',
                }}
              >
                <div>
                  <div style={{
                    fontSize: 'var(--font-size-sm)',
                    fontWeight: 'var(--font-weight-medium)',
                    color: 'var(--color-text-primary)',
                  }}>
                    {job.title}
                  </div>
                  <div style={{
                    fontSize: 'var(--font-size-xs)',
                    color: 'var(--color-text-muted)',
                  }}>
                    {job.company}
                  </div>
                </div>
                <span style={{
                  fontSize: 'var(--font-size-sm)',
                  fontWeight: 'var(--font-weight-bold)',
                  color: job.score >= 80
                    ? 'var(--color-success)'
                    : job.score >= 70
                      ? 'var(--color-warning)'
                      : 'var(--color-text-secondary)',
                }}>
                  {job.score}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Skill gap progress */}
      <div className="card" style={{ marginTop: 'var(--space-6)' }}>
        <h3 style={{
          fontSize: 'var(--font-size-base)',
          fontWeight: 'var(--font-weight-semibold)',
          marginBottom: 'var(--space-4)',
          color: 'var(--color-text-primary)',
        }}>
          📊 Tiến độ đóng gap kỹ năng
        </h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
          {MOCK_SKILL_PROGRESS.map(item => (
            <div key={item.skill}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                marginBottom: 'var(--space-2)',
              }}>
                <span style={{
                  fontSize: 'var(--font-size-sm)',
                  fontWeight: 'var(--font-weight-medium)',
                  color: 'var(--color-text-primary)',
                }}>
                  {item.skill}
                </span>
                <span style={{
                  fontSize: 'var(--font-size-xs)',
                  color: item.after > item.before
                    ? 'var(--color-success)'
                    : 'var(--color-text-muted)',
                }}>
                  {item.before}% → {item.after}%
                  {item.after > item.before && (
                    <span style={{ marginLeft: 'var(--space-2)' }}>
                      ↑{item.after - item.before}
                    </span>
                  )}
                </span>
              </div>
              <div style={{
                position: 'relative',
                height: 6,
                borderRadius: 'var(--radius-full)',
                background: 'rgba(148, 163, 184, 0.1)',
              }}>
                {/* Before */}
                <div style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  height: '100%',
                  width: `${item.before}%`,
                  borderRadius: 'var(--radius-full)',
                  background: 'rgba(148, 163, 184, 0.3)',
                }} />
                {/* After */}
                <div style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  height: '100%',
                  width: `${item.after}%`,
                  borderRadius: 'var(--radius-full)',
                  background: 'var(--gradient-accent)',
                  transition: 'width var(--transition-slow)',
                }} />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Navigation */}
      <div className="page-navigation">
        <button
          type="button"
          className="btn btn-ghost"
          onClick={() => navigate('/improve')}
        >
          ← Cải thiện CV
        </button>
        <button
          type="button"
          className="btn btn-primary btn-lg"
          onClick={() => navigate('/onboarding')}
        >
          🔄 Bắt đầu phiên mới
        </button>
      </div>
    </div>
  )
}
