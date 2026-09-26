import { useNavigate } from 'react-router-dom'
import '../../styles/pages.css'

/**
 * Bước 4 — Kết quả & Giải thích
 *
 * Xếp hạng + điểm khớp + breakdown (kỹ năng cứng/mềm/kinh nghiệm/học vấn)
 * + evidence trích từ CV và JD.
 *
 * Hiện tại: chỉ khung UI, chưa nối API.
 */

// Mock breakdown data theo chuẩn dataset tinixai/vietnamese-job-descriptions
const MOCK_BREAKDOWN = {
  title: 'Frontend Developer (ReactJS / Tailwind)',
  company: 'VNG Corporation',
  location: 'Quận 7, TP. Hồ Chí Minh',
  jobType: 'Toàn thời gian (Hybrid)',
  salary: '15 – 22 triệu VNĐ/tháng',
  benefits: ['MacBook Pro M-series', 'Bảo hiểm PVI Care', 'Thưởng KPI & tháng 13', 'Hỗ trợ ăn trưa'],
  datasetLicense: 'tinixai/vietnamese-job-descriptions (CC BY-NC 4.0)',
  totalScore: 84,
  dimensions: [
    { name: 'Kỹ năng cứng (Tech Stack)', score: 88, weight: 0.35, icon: '🔧' },
    { name: 'Kinh nghiệm thực tế', score: 82, weight: 0.30, icon: '💼' },
    { name: 'Học vấn & Bằng cấp', score: 90, weight: 0.20, icon: '🎓' },
    { name: 'Kỹ năng mềm & Tiêu chuẩn', score: 75, weight: 0.15, icon: '🤝' },
  ],
  matchedSkills: ['JavaScript (ES6+)', 'ReactJS', 'HTML5/CSS3', 'Git', 'RESTful API', 'Tailwind CSS'],
  missingSkills: ['TypeScript', 'Next.js (SSR)', 'Jest / React Testing Library'],
  evidence: [
    {
      type: 'match',
      source: 'Trích xuất từ CV của bạn',
      quote: '“Thực tập sinh Frontend: Xây dựng dashboard giao diện web với ReactJS, tối ưu hóa tái sử dụng Component và kết nối REST API backend.”',
      evaluation: 'Khớp 100% yêu cầu về ReactJS, Javascript ES6+ và tích hợp API.',
    },
    {
      type: 'gap',
      source: 'Trích xuất từ JD (VNG)',
      quote: '“Yêu cầu: Ưu tiên ứng viên có kinh nghiệm viết Unit Test (Jest/RTL) và dự án thực tế bằng TypeScript.”',
      evaluation: 'Chưa tìm thấy từ khóa TypeScript và testing trong CV. Đề xuất bổ sung ở Bước 5 để tăng +12 điểm.',
    },
  ],
}

function ScoreBar({ score, label, icon, weight }) {
  const getScoreColor = (s) => {
    if (s >= 80) return 'var(--color-success)'
    if (s >= 60) return 'var(--color-warning)'
    return 'var(--color-error)'
  }

  return (
    <div style={{ marginBottom: 'var(--space-4)' }}>
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
          {icon} {label}
        </span>
        <span style={{
          fontSize: 'var(--font-size-sm)',
          fontWeight: 'var(--font-weight-semibold)',
          color: getScoreColor(score),
        }}>
          {score}/100
          <span style={{
            color: 'var(--color-text-muted)',
            fontWeight: 'var(--font-weight-normal)',
            marginLeft: 'var(--space-2)',
          }}>
            (Trọng số: {weight * 100}%)
          </span>
        </span>
      </div>
      <div className="progress-bar">
        <div
          className="progress-bar-fill"
          style={{
            width: `${score}%`,
            background: getScoreColor(score),
          }}
        />
      </div>
    </div>
  )
}

export default function ResultsPage() {
  const navigate = useNavigate()

  return (
    <div>
      {/* Page header */}
      <div className="page-header">
        <div className="page-step-badge">
          <span>📊</span>
          <span>Bước 4 / 6</span>
        </div>
        <h1 className="page-title">Kết quả & Giải thích</h1>
        <p className="page-subtitle">
          Chi tiết độ khớp CV–JD với breakdown 4 chiều, dẫn chứng minh bạch (explainability) và phân loại kỹ năng đạt / thiếu.
        </p>
      </div>

      {/* Top-level score + JD Overview */}
      <div className="card card-accent" style={{ marginBottom: 'var(--space-6)' }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--space-8)',
          flexWrap: 'wrap',
        }}>
          {/* Score circle */}
          <div style={{
            width: 108,
            height: 108,
            borderRadius: 'var(--radius-full)',
            background: 'var(--color-accent-bg)',
            border: '3px solid var(--color-success)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0,
            boxShadow: '0 0 24px rgba(52, 211, 153, 0.25)',
          }}>
            <div className="score-value" style={{ color: 'var(--color-success)', fontSize: '2rem' }}>
              {MOCK_BREAKDOWN.totalScore}
            </div>
            <div className="score-label" style={{ fontWeight: '600' }}>/ 100 ĐIỂM</div>
          </div>

          {/* Info */}
          <div style={{ flex: 1, minWidth: 260 }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: 'var(--space-2)',
              marginBottom: 'var(--space-2)',
              flexWrap: 'wrap',
            }}>
              <h2 style={{
                fontSize: 'var(--font-size-xl)',
                fontWeight: 'var(--font-weight-bold)',
                color: 'var(--color-text-primary)',
              }}>
                {MOCK_BREAKDOWN.title}
              </h2>
              <span className="tag tag-salary">💵 {MOCK_BREAKDOWN.salary}</span>
              <span className="tag tag-jobtype">{MOCK_BREAKDOWN.jobType}</span>
            </div>

            <div style={{
              fontSize: 'var(--font-size-sm)',
              color: 'var(--color-text-secondary)',
              display: 'flex',
              gap: 'var(--space-3)',
              marginBottom: 'var(--space-3)',
              flexWrap: 'wrap',
            }}>
              <span>🏢 <strong>{MOCK_BREAKDOWN.company}</strong></span>
              <span>•</span>
              <span>📍 {MOCK_BREAKDOWN.location}</span>
            </div>

            {/* Benefits */}
            <div style={{
              display: 'flex',
              gap: 'var(--space-2)',
              flexWrap: 'wrap',
              marginBottom: 'var(--space-3)',
            }}>
              {MOCK_BREAKDOWN.benefits.map((b) => (
                <span key={b} className="tag tag-benefit">✓ {b}</span>
              ))}
            </div>

            <div style={{
              fontSize: 'var(--font-size-xs)',
              color: 'var(--color-text-muted)',
              borderTop: '1px solid rgba(148, 163, 184, 0.1)',
              paddingTop: 'var(--space-2)',
            }}>
              Nguồn dữ liệu JD: <strong>{MOCK_BREAKDOWN.datasetLicense}</strong> — Điểm số có công thức trọng số minh bạch.
            </div>
          </div>
        </div>
      </div>

      {/* Breakdown by dimension & Skills */}
      <div className="grid-2" style={{ marginBottom: 'var(--space-6)' }}>
        <div className="card">
          <h3 style={{
            fontSize: 'var(--font-size-base)',
            fontWeight: 'var(--font-weight-semibold)',
            marginBottom: 'var(--space-4)',
            color: 'var(--color-text-primary)',
          }}>
            📊 Phân rã điểm 4 chiều (Breakdown)
          </h3>
          {MOCK_BREAKDOWN.dimensions.map(d => (
            <ScoreBar
              key={d.name}
              score={d.score}
              label={d.name}
              icon={d.icon}
              weight={d.weight}
            />
          ))}
        </div>

        {/* Skill match & gap */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
          <div className="card">
            <h3 style={{
              fontSize: 'var(--font-size-base)',
              fontWeight: 'var(--font-weight-semibold)',
              marginBottom: 'var(--space-3)',
              color: 'var(--color-text-primary)',
            }}>
              ✅ Kỹ năng đáp ứng ({MOCK_BREAKDOWN.matchedSkills.length})
            </h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-2)' }}>
              {MOCK_BREAKDOWN.matchedSkills.map(s => (
                <span key={s} className="tag tag-match">{s}</span>
              ))}
            </div>
          </div>

          <div className="card">
            <h3 style={{
              fontSize: 'var(--font-size-base)',
              fontWeight: 'var(--font-weight-semibold)',
              marginBottom: 'var(--space-3)',
              color: 'var(--color-text-primary)',
            }}>
              ❌ Khoảng trống kỹ năng ({MOCK_BREAKDOWN.missingSkills.length} Gap)
            </h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-2)' }}>
              {MOCK_BREAKDOWN.missingSkills.map(s => (
                <span key={s} className="tag tag-gap">{s}</span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Evidence section — Explainability */}
      <div className="card" style={{ marginBottom: 'var(--space-6)' }}>
        <h3 style={{
          fontSize: 'var(--font-size-base)',
          fontWeight: 'var(--font-weight-semibold)',
          marginBottom: 'var(--space-4)',
          color: 'var(--color-text-primary)',
        }}>
          📝 Bằng chứng đối chiếu (Evidence) — Trích dẫn trực tiếp
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
          {MOCK_BREAKDOWN.evidence.map((ev, i) => (
            <div
              key={i}
              style={{
                padding: 'var(--space-4)',
                borderRadius: 'var(--radius-lg)',
                background: 'var(--color-bg-primary)',
                borderLeft: `4px solid ${ev.type === 'match' ? 'var(--color-success)' : 'var(--color-warning)'}`,
              }}
            >
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: 'var(--space-2)',
              }}>
                <span style={{
                  fontSize: 'var(--font-size-xs)',
                  fontWeight: 'var(--font-weight-semibold)',
                  color: ev.type === 'match' ? 'var(--color-success)' : 'var(--color-warning)',
                  textTransform: 'uppercase',
                }}>
                  {ev.source}
                </span>
                <span className="tag tag-neutral" style={{ fontSize: '0.7rem' }}>
                  {ev.type === 'match' ? 'Khớp ngữ nghĩa' : 'Khoảng cách cần bù'}
                </span>
              </div>
              <p style={{
                fontSize: 'var(--font-size-sm)',
                color: 'var(--color-text-primary)',
                fontStyle: 'italic',
                marginBottom: 'var(--space-2)',
                lineHeight: 'var(--line-height-relaxed)',
              }}>
                {ev.quote}
              </p>
              <p style={{
                fontSize: 'var(--font-size-xs)',
                color: 'var(--color-text-muted)',
              }}>
                💡 <strong>Nhận định AI:</strong> {ev.evaluation}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Navigation */}
      <div className="page-navigation">
        <button
          type="button"
          className="btn btn-ghost"
          onClick={() => navigate('/matching')}
        >
          ← Danh sách JD
        </button>
        <button
          type="button"
          className="btn btn-primary btn-lg"
          onClick={() => navigate('/improve')}
        >
          Cải thiện CV →
        </button>
      </div>
    </div>
  )
}
