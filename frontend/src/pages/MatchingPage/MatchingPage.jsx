import { useNavigate } from 'react-router-dom'
import '../../styles/pages.css'

/**
 * Bước 3 — Matching CV–JD
 *
 * Hệ thống truy xuất top-K JD phù hợp từ vector store (pgvector),
 * chấm điểm từng cặp CV–JD bằng hybrid scoring.
 *
 * Hiện tại: chỉ khung UI với mock data, chưa nối API.
 */

// Mock data theo chuẩn dataset tinixai/vietnamese-job-descriptions
const MOCK_JOBS = [
  {
    id: 1,
    title: 'Frontend Developer (ReactJS / Tailwind)',
    company: 'VNG Corporation',
    location: 'TP. Hồ Chí Minh',
    level: 'Fresher / Junior',
    job_type: 'Toàn thời gian (Hybrid)',
    salary: '15 – 22 triệu',
    benefits: ['MacBook Pro M-series', 'Bảo hiểm PVI Care', 'Thưởng tháng 13'],
    score: 84,
    status: 'matched',
  },
  {
    id: 2,
    title: 'Data Analyst (SQL / Python / PowerBI)',
    company: 'FPT Software',
    location: 'Hà Nội',
    level: 'Fresher (0–1 năm)',
    job_type: 'Toàn thời gian (Tại văn phòng)',
    salary: '12 – 18 triệu',
    benefits: ['Đào tạo chứng chỉ AWS', 'Trợ cấp ăn trưa', 'Teambuilding'],
    score: 76,
    status: 'matched',
  },
  {
    id: 3,
    title: 'Fullstack Web Developer (Node.js & React)',
    company: 'One Mount Group',
    location: 'Hà Nội / Remote',
    level: 'Junior (1–2 năm)',
    job_type: 'Linh hoạt (Remote-first)',
    salary: '18 – 25 triệu',
    benefits: ['15 ngày phép/năm', 'Review lương 2 lần/năm', 'Trợ cấp thiết bị'],
    score: 68,
    status: 'matched',
  },
]

export default function MatchingPage() {
  const navigate = useNavigate()

  return (
    <div>
      {/* Page header */}
      <div className="page-header">
        <div className="page-step-badge">
          <span>🔍</span>
          <span>Bước 3 / 6</span>
        </div>
        <h1 className="page-title">Matching CV–JD</h1>
        <p className="page-subtitle">
          AI truy xuất top JD từ kho dữ liệu chuẩn hóa <code>tinixai/vietnamese-job-descriptions</code> và chấm điểm độ khớp dựa trên hồ sơ của bạn.
        </p>
      </div>

      {/* Progress / Status */}
      <div className="card card-accent" style={{ marginBottom: 'var(--space-6)' }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: 'var(--space-3)',
        }}>
          <span style={{
            fontSize: 'var(--font-size-sm)',
            fontWeight: 'var(--font-weight-medium)',
            color: 'var(--color-text-secondary)',
          }}>
            Trạng thái matching
          </span>
          <span className="tag tag-match">Đã hoàn tất (Top-3 JD)</span>
        </div>
        <div className="progress-bar">
          <div className="progress-bar-fill" style={{ width: '100%' }} />
        </div>
        <div style={{
          marginTop: 'var(--space-2)',
          fontSize: 'var(--font-size-xs)',
          color: 'var(--color-text-muted)',
          display: 'flex',
          justifyContent: 'space-between',
        }}>
          <span>Truy xuất 3 / 3 JD phù hợp nhất</span>
          <span>Kho dữ liệu: <strong>tinixai (CC BY-NC 4.0)</strong></span>
        </div>
      </div>

      {/* Filters */}
      <div style={{
        display: 'flex',
        gap: 'var(--space-3)',
        marginBottom: 'var(--space-6)',
        flexWrap: 'wrap',
      }}>
        <button className="btn btn-secondary" style={{ fontSize: 'var(--font-size-sm)' }}>
          📍 Địa điểm (TP.HCM, Hà Nội)
        </button>
        <button className="btn btn-secondary" style={{ fontSize: 'var(--font-size-sm)' }}>
          📊 Mức kinh nghiệm (Fresher/Junior)
        </button>
        <button className="btn btn-secondary" style={{ fontSize: 'var(--font-size-sm)' }}>
          💰 Mức lương
        </button>
        <div style={{ flex: 1 }} />
        <button className="btn btn-primary" onClick={() => navigate('/results')}>
          ▶ Chấm lại Top JD
        </button>
      </div>

      {/* Job list (rich cards) */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
        {MOCK_JOBS.map((job, idx) => (
          <div
            key={job.id}
            className="card"
            style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: 'var(--space-5)',
              animation: `fadeIn 0.4s ease ${idx * 0.1}s forwards`,
              cursor: 'pointer',
            }}
            onClick={() => navigate('/results')}
          >
            {/* Rank badge */}
            <div style={{
              width: 36,
              height: 36,
              borderRadius: 'var(--radius-lg)',
              background: idx === 0 ? 'var(--gradient-accent)' : 'rgba(148, 163, 184, 0.12)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 'var(--font-weight-bold)',
              color: idx === 0 ? 'white' : 'var(--color-text-secondary)',
              flexShrink: 0,
              fontSize: 'var(--font-size-sm)',
            }}>
              #{idx + 1}
            </div>

            {/* Job details */}
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--space-2)',
                flexWrap: 'wrap',
                marginBottom: 'var(--space-1)',
              }}>
                <span style={{
                  fontSize: 'var(--font-size-base)',
                  fontWeight: 'var(--font-weight-bold)',
                  color: 'var(--color-text-primary)',
                }}>
                  {job.title}
                </span>
                <span className="tag tag-salary">💵 {job.salary}</span>
                <span className="tag tag-jobtype">{job.job_type}</span>
              </div>

              <div style={{
                fontSize: 'var(--font-size-sm)',
                color: 'var(--color-text-muted)',
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--space-3)',
                marginBottom: 'var(--space-3)',
                flexWrap: 'wrap',
              }}>
                <span style={{ color: 'var(--color-text-secondary)', fontWeight: 'var(--font-weight-medium)' }}>
                  🏢 {job.company}
                </span>
                <span>•</span>
                <span>📍 {job.location}</span>
                <span>•</span>
                <span>🎓 {job.level}</span>
              </div>

              {/* Benefits chips */}
              <div style={{ display: 'flex', gap: 'var(--space-2)', flexWrap: 'wrap' }}>
                {job.benefits.map((b) => (
                  <span key={b} className="tag tag-benefit">✓ {b}</span>
                ))}
              </div>
            </div>

            {/* Score pill */}
            <div style={{
              textAlign: 'center',
              minWidth: 70,
              padding: 'var(--space-2) var(--space-3)',
              borderRadius: 'var(--radius-lg)',
              background: job.score >= 80 ? 'var(--color-success-bg)' : 'var(--color-accent-bg)',
              border: `1px solid ${job.score >= 80 ? 'rgba(52, 211, 153, 0.3)' : 'rgba(99, 102, 241, 0.3)'}`,
            }}>
              <div style={{
                fontSize: 'var(--font-size-xl)',
                fontWeight: 'var(--font-weight-extrabold)',
                color: job.score >= 80 ? 'var(--color-success)' : 'var(--color-accent-bright)',
              }}>
                {job.score}%
              </div>
              <div style={{
                fontSize: '0.7rem',
                color: 'var(--color-text-muted)',
                textTransform: 'uppercase',
                letterSpacing: '0.04em',
              }}>
                Độ khớp
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Navigation */}
      <div className="page-navigation">
        <button
          type="button"
          className="btn btn-ghost"
          onClick={() => navigate('/upload-cv')}
        >
          ← Quay lại
        </button>
        <button
          type="button"
          className="btn btn-primary btn-lg"
          onClick={() => navigate('/results')}
        >
          Xem kết quả chi tiết →
        </button>
      </div>
    </div>
  )
}
