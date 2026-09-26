import { useNavigate } from 'react-router-dom'
import '../../styles/pages.css'

/**
 * Bước 5 — Cải thiện CV
 *
 * Gap có thứ tự ưu tiên, gợi ý viết lại bullet cụ thể,
 * chấm lại sau khi sửa → hiển thị delta score.
 *
 * Hiện tại: chỉ khung UI, chưa nối API.
 */

const MOCK_SUGGESTIONS = [
  {
    id: 1,
    priority: 'Cao',
    gap: 'Thiếu TypeScript',
    suggestion: 'Thêm kinh nghiệm sử dụng TypeScript vào phần kỹ năng và mô tả dự án',
    example: '"Phát triển ứng dụng web sử dụng React + TypeScript, xử lý type-safe API integration cho 5 endpoints"',
    deltaScore: '+8',
  },
  {
    id: 2,
    priority: 'Cao',
    gap: 'Chưa đề cập Testing',
    suggestion: 'Bổ sung kinh nghiệm viết unit test / integration test',
    example: '"Viết 50+ unit tests với Jest & React Testing Library, đạt coverage 85%"',
    deltaScore: '+5',
  },
  {
    id: 3,
    priority: 'Trung bình',
    gap: 'Next.js chưa có',
    suggestion: 'Nếu có kinh nghiệm SSR/SSG, hãy nêu cụ thể framework',
    example: '"Xây dựng landing page SEO-friendly với Next.js (SSG), đạt Lighthouse 95+"',
    deltaScore: '+3',
  },
]

function getPriorityColor(priority) {
  if (priority === 'Cao') return { bg: 'var(--color-error-bg)', color: 'var(--color-error)' }
  if (priority === 'Trung bình') return { bg: 'var(--color-warning-bg)', color: 'var(--color-warning)' }
  return { bg: 'rgba(148, 163, 184, 0.1)', color: 'var(--color-text-secondary)' }
}

export default function ImprovePage() {
  const navigate = useNavigate()

  return (
    <div>
      {/* Page header */}
      <div className="page-header">
        <div className="page-step-badge">
          <span>✏️</span>
          <span>Bước 5 / 6</span>
        </div>
        <h1 className="page-title">Cải thiện CV</h1>
        <p className="page-subtitle">
          Dựa trên gap giữa CV và JD đã chọn, AI gợi ý cụ thể cách sửa từng
          điểm. Sửa xong → chấm lại → thấy delta score ngay.
        </p>
      </div>

      {/* Delta score banner */}
      <div className="card card-accent" style={{
        marginBottom: 'var(--space-6)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
      }}>
        <div>
          <div style={{
            fontSize: 'var(--font-size-sm)',
            color: 'var(--color-text-muted)',
            marginBottom: 'var(--space-1)',
          }}>
            Điểm hiện tại → Mục tiêu sau cải thiện
          </div>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--space-4)',
          }}>
            <span style={{
              fontSize: 'var(--font-size-3xl)',
              fontWeight: 'var(--font-weight-bold)',
              color: 'var(--color-warning)',
            }}>
              72
            </span>
            <span style={{
              fontSize: 'var(--font-size-xl)',
              color: 'var(--color-text-muted)',
            }}>
              →
            </span>
            <span style={{
              fontSize: 'var(--font-size-3xl)',
              fontWeight: 'var(--font-weight-bold)',
              color: 'var(--color-success)',
            }}>
              88
            </span>
            <span className="tag tag-match" style={{ fontSize: 'var(--font-size-base)' }}>
              +16 điểm tiềm năng
            </span>
          </div>
        </div>
        <button className="btn btn-primary">
          🔄 Chấm lại CV đã sửa
        </button>
      </div>

      {/* Suggestions list */}
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: 'var(--space-4)',
      }}>
        {MOCK_SUGGESTIONS.map((item, idx) => {
          const priorityStyle = getPriorityColor(item.priority)
          return (
            <div
              key={item.id}
              className="card"
              style={{
                animation: `fadeIn 0.4s ease ${idx * 0.1}s forwards`,
              }}
            >
              <div style={{
                display: 'flex',
                alignItems: 'flex-start',
                justifyContent: 'space-between',
                marginBottom: 'var(--space-3)',
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                  <span
                    className="tag"
                    style={{
                      background: priorityStyle.bg,
                      color: priorityStyle.color,
                    }}
                  >
                    {item.priority}
                  </span>
                  <span style={{
                    fontWeight: 'var(--font-weight-semibold)',
                    color: 'var(--color-text-primary)',
                  }}>
                    {item.gap}
                  </span>
                </div>
                <span className="tag tag-match">
                  {item.deltaScore}
                </span>
              </div>

              <p style={{
                fontSize: 'var(--font-size-sm)',
                color: 'var(--color-text-secondary)',
                marginBottom: 'var(--space-3)',
                lineHeight: 'var(--line-height-relaxed)',
              }}>
                💡 {item.suggestion}
              </p>

              <div style={{
                background: 'var(--color-bg-primary)',
                borderRadius: 'var(--radius-lg)',
                padding: 'var(--space-4)',
                borderLeft: '3px solid var(--color-accent)',
              }}>
                <div style={{
                  fontSize: 'var(--font-size-xs)',
                  color: 'var(--color-text-muted)',
                  marginBottom: 'var(--space-2)',
                }}>
                  Ví dụ viết lại:
                </div>
                <div style={{
                  fontSize: 'var(--font-size-sm)',
                  color: 'var(--color-text-primary)',
                  fontStyle: 'italic',
                }}>
                  {item.example}
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Navigation */}
      <div className="page-navigation">
        <button
          type="button"
          className="btn btn-ghost"
          onClick={() => navigate('/results')}
        >
          ← Kết quả
        </button>
        <button
          type="button"
          className="btn btn-primary btn-lg"
          onClick={() => navigate('/dashboard')}
        >
          Xem Dashboard →
        </button>
      </div>
    </div>
  )
}
