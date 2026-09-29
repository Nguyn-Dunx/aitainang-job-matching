import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../../styles/pages.css'
import { getHistoryApi } from '../../services/apiService'

/**
 * Bước 6 — Dashboard
 *
 * Lịch sử phiên chấm, top JD khớp nhất, kỹ năng còn thiếu.
 *
 * Dữ liệu THẬT: GET /api/cv/history (đọc từ bảng cvs + match_results).
 * Không còn mock — nếu chưa có phiên nào thì hiện trạng thái rỗng rõ ràng.
 */
export default function DashboardPage() {
  const navigate = useNavigate()

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [data, setData] = useState(null)

  useEffect(() => {
    let alive = true
    getHistoryApi(5).then(res => {
      if (!alive) return
      if (res.success) {
        setData(res.data)
      } else {
        setError(res.error)
      }
      setLoading(false)
    })
    return () => { alive = false }
  }, [])

  const stats = data?.stats || { sessions: 0, jobs_matched: 0, top_score: null }
  const sessions = data?.sessions || []
  const latest = data?.latest
  const matches = latest?.matches || []
  const gapSkills = latest?.gap_skills || []

  const fmtDate = iso => (iso ? new Date(iso).toLocaleString('vi-VN') : '—')

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
          Theo dõi lịch sử phiên chấm, top JD khớp nhất và kỹ năng còn thiếu —
          dữ liệu thật từ các phiên bạn đã chạy.
        </p>
      </div>

      {loading && (
        <div className="card" style={{ textAlign: 'center', color: 'var(--color-text-muted)' }}>
          Đang tải lịch sử phiên chấm…
        </div>
      )}

      {!loading && error && (
        <div className="card" style={{ borderColor: 'var(--color-danger, #ef4444)' }}>
          <strong>Không tải được lịch sử.</strong>
          <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-muted)', marginTop: 'var(--space-2)' }}>
            {error}
          </div>
        </div>
      )}

      {!loading && !error && (
        <>
          {/* Stats overview — số thật từ DB */}
          <div className="grid-3" style={{ marginBottom: 'var(--space-8)' }}>
            <div className="card card-accent" style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 'var(--font-size-3xl)', fontWeight: 'var(--font-weight-bold)' }}>
                <span className="gradient-text">
                  {stats.top_score != null ? stats.top_score : '—'}
                </span>
              </div>
              <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-muted)', marginTop: 'var(--space-1)' }}>
                Điểm khớp cao nhất
              </div>
            </div>

            <div className="card" style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 'var(--font-size-3xl)', fontWeight: 'var(--font-weight-bold)', color: 'var(--color-text-primary)' }}>
                {stats.sessions}
              </div>
              <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-muted)', marginTop: 'var(--space-1)' }}>
                Phiên chấm
              </div>
            </div>

            <div className="card" style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 'var(--font-size-3xl)', fontWeight: 'var(--font-weight-bold)', color: 'var(--color-text-primary)' }}>
                {stats.jobs_matched}
              </div>
              <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-muted)', marginTop: 'var(--space-1)' }}>
                JD đã khớp
              </div>
            </div>
          </div>

          {sessions.length === 0 ? (
            <div className="card" style={{ textAlign: 'center' }}>
              <p style={{ color: 'var(--color-text-muted)' }}>
                Chưa có phiên chấm nào. Hãy tải CV lên để bắt đầu.
              </p>
              <button type="button" className="btn btn-primary" onClick={() => navigate('/upload')}>
                Tải CV lên
              </button>
            </div>
          ) : (
            <>
              <div className="grid-2">
                {/* Session history — thật */}
                <div className="card">
                  <h3 style={{ fontSize: 'var(--font-size-base)', fontWeight: 'var(--font-weight-semibold)', marginBottom: 'var(--space-4)', color: 'var(--color-text-primary)' }}>
                    📅 Lịch sử phiên chấm
                  </h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
                    {sessions.map(s => (
                      <div key={s.cv_id} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: 'var(--space-3)', background: 'var(--color-bg-primary)', borderRadius: 'var(--radius-lg)' }}>
                        <div>
                          <div style={{ fontSize: 'var(--font-size-sm)', fontWeight: 'var(--font-weight-medium)', color: 'var(--color-text-primary)' }}>
                            {s.filename}
                          </div>
                          <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>
                            {fmtDate(s.created_at)} • {s.jobs_matched} JD matched
                          </div>
                        </div>
                        <span className="tag tag-match">
                          Top: {s.top_score != null ? s.top_score : '—'}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Top JD khớp nhất — thật */}
                <div className="card">
                  <h3 style={{ fontSize: 'var(--font-size-base)', fontWeight: 'var(--font-weight-semibold)', marginBottom: 'var(--space-4)', color: 'var(--color-text-primary)' }}>
                    ⭐ Top JD khớp nhất (phiên gần nhất)
                  </h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
                    {matches.map(job => (
                      <div key={job.id} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: 'var(--space-3)', background: 'var(--color-bg-primary)', borderRadius: 'var(--radius-lg)' }}>
                        <div style={{ minWidth: 0 }}>
                          <div style={{ fontSize: 'var(--font-size-sm)', fontWeight: 'var(--font-weight-medium)', color: 'var(--color-text-primary)' }}>
                            {job.title}
                          </div>
                          <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>
                            {job.company}
                          </div>
                        </div>
                        <span style={{ fontSize: 'var(--font-size-sm)', fontWeight: 'var(--font-weight-bold)', color: job.score >= 80 ? 'var(--color-success)' : job.score >= 70 ? 'var(--color-warning)' : 'var(--color-text-secondary)' }}>
                          {job.score != null ? job.score : '—'}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Kỹ năng còn thiếu — thật (gap của top match) */}
              <div className="card" style={{ marginTop: 'var(--space-6)' }}>
                <h3 style={{ fontSize: 'var(--font-size-base)', fontWeight: 'var(--font-weight-semibold)', marginBottom: 'var(--space-4)', color: 'var(--color-text-primary)' }}>
                  📊 Kỹ năng còn thiếu (top JD phiên gần nhất)
                </h3>
                {gapSkills.length === 0 ? (
                  <p style={{ color: 'var(--color-text-muted)', fontSize: 'var(--font-size-sm)' }}>
                    Không có kỹ năng nào còn thiếu so với JD khớp nhất.
                  </p>
                ) : (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-2)' }}>
                    {gapSkills.map(skill => (
                      <span key={skill} className="tag" style={{ background: 'rgba(245, 158, 11, 0.12)', color: 'var(--color-warning)' }}>
                        {skill}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </>
          )}
        </>
      )}

      {/* Navigation */}
      <div className="page-navigation">
        <button type="button" className="btn btn-ghost" onClick={() => navigate('/improve')}>
          ← Cải thiện CV
        </button>
        <button type="button" className="btn btn-primary btn-lg" onClick={() => navigate('/onboarding')}>
          🔄 Bắt đầu phiên mới
        </button>
      </div>
    </div>
  )
}
