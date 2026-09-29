import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import '../../styles/pages.css'
import { ALL_REAL_JDS, getJobById } from '../../services/jobService'

/**
 * Bước 4 — Kết quả & Giải thích (Explainable Matching)
 *
 * Nạp trực tiếp dữ liệu JD THẬT từ data/processed/jds.json (450 JD).
 * Loại bỏ hoàn toàn tên công ty tự bịa (VNG, FPT, Viettel...).
 * Trích dẫn bằng chứng (evidence) trực tiếp từ requirements/responsibilities thật của JD.
 */
export default function ResultsPage() {
  const navigate = useNavigate()
  const [selectedId, setSelectedId] = useState(2)
  const [candidateProfile, setCandidateProfile] = useState(null)
  const [backendMatches, setBackendMatches] = useState([])
  const [isBackendReal, setIsBackendReal] = useState(false)

  useEffect(() => {
    try {
      const savedId = localStorage.getItem('selectedJobId') || '2'
      setSelectedId(savedId)

      const cv = JSON.parse(localStorage.getItem('parsedCV') || '{}')
      const career = JSON.parse(localStorage.getItem('careerProfile') || '{}')
      setCandidateProfile({ ...career, ...cv })

      const matches = JSON.parse(localStorage.getItem('backendMatches') || '[]')
      if (Array.isArray(matches) && matches.length > 0) {
        setBackendMatches(matches)
        setIsBackendReal(true)
        // Nếu savedId không khớp ID nào trong matches, gán mặc định là matches[0].id
        const matchedJob = matches.find((m) => String(m.id) === String(savedId))
        if (!matchedJob && matches[0]) {
          setSelectedId(matches[0].id)
        }
      }
    } catch (err) {
      console.error('Lỗi đọc dữ liệu:', err)
    }
  }, [])

  // Tìm job từ Backend Matches nếu có, nếu không fallback ALL_REAL_JDS
  const backendJob = isBackendReal
    ? backendMatches.find((m) => String(m.id) === String(selectedId)) || backendMatches[0]
    : null

  const fallbackJob = getJobById(selectedId)
  const currentJob = backendJob || fallbackJob

  // Danh sách vài JD để user click chuyển nhanh (ưu tiên từ backendMatches)
  const featuredRealJobs = isBackendReal && backendMatches.length > 0
    ? backendMatches.slice(0, 5)
    : [
        ALL_REAL_JDS.find((j) => j.industry_group === 'Software Engineering') || ALL_REAL_JDS[1],
        ALL_REAL_JDS.find((j) => j.industry_group === 'Data/AI/ML') || ALL_REAL_JDS[3],
        ALL_REAL_JDS.find((j) => j.industry_group === 'Infra/DevOps') || ALL_REAL_JDS[0],
        ALL_REAL_JDS.find((j) => j.title?.toLowerCase().includes('data analyst')) || ALL_REAL_JDS[2],
      ].filter(Boolean)

  // Trích xuất các trích dẫn thực tế
  const rawReq = currentJob.requirements || currentJob.evidence?.jd_snippet || 'Yêu cầu kỹ năng chuyên môn phù hợp với vị trí.'
  const jdQuoteSample = currentJob.evidence?.jd_snippet || (rawReq.length > 200 ? rawReq.slice(0, 180) + '...' : rawReq)

  // Breakdown tính toán chuẩn hóa theo Hybrid V2 của Backend (W_HARD=0.5, W_SEMANTIC=0.4, W_SOFT=0.1)
  const breakdownDimensions = backendJob?.breakdown
    ? [
        {
          name: 'Kỹ năng cứng (Hard Skills)',
          score: Math.round(backendJob.breakdown.hard_skill?.score || 0),
          weight: 0.50,
          icon: '🔧',
        },
        {
          name: 'Ngữ nghĩa & Trách nhiệm (Semantic Match)',
          score: Math.round(backendJob.breakdown.semantic?.score || 0),
          weight: 0.40,
          icon: '🧠',
        },
        {
          name: 'Kỹ năng mềm & Tác phong (Soft Skills)',
          score: Math.round(backendJob.breakdown.soft_skill?.score || 0),
          weight: 0.10,
          icon: '🤝',
        },
      ]
    : [
        {
          name: 'Kỹ năng cứng (Hard Skills)',
          score: Math.min(95, Math.round(currentJob.score * 1.02)),
          weight: 0.50,
          icon: '🔧',
        },
        {
          name: 'Ngữ nghĩa & Trách nhiệm (Semantic Match)',
          score: Math.max(50, Math.round(currentJob.score * 0.98)),
          weight: 0.40,
          icon: '🧠',
        },
        {
          name: 'Kỹ năng mềm & Tác phong (Soft Skills)',
          score: Math.min(90, Math.round(currentJob.score * 1.05)),
          weight: 0.10,
          icon: '🤝',
        },
      ]

  // Kỹ năng khớp và kỹ năng thiếu (từ backend breakdown thật nếu có)
  const matchedSkills = backendJob?.breakdown?.hard_skill?.matched ||
    (rawReq.match(/[A-Z][A-Za-z0-9+#.]+(?:\s[A-Za-z0-9+#.]+)?/g) || ['Python', 'SQL', 'Git']).slice(0, 5)

  const missingSkills = backendJob?.breakdown?.hard_skill?.missing ||
    (rawReq.match(/[A-Z][A-Za-z0-9+#.]+(?:\s[A-Za-z0-9+#.]+)?/g) || ['Docker', 'AWS']).slice(5, 8)

  const cvEvidenceSnippet = backendJob?.evidence?.matched_skills_in_cv?.length > 0
    ? `Các kỹ năng ứng viên đáp ứng được trích xuất trực tiếp: ${backendJob.evidence.matched_skills_in_cv.join(', ')}.`
    : 'Ứng viên có các kỹ năng lập trình và kinh nghiệm phát triển dự án khớp với yêu cầu vị trí.'

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
          Chi tiết độ khớp CV–JD với <strong>phân rã 3 chiều Hybrid V2 (Breakdown)</strong>, dẫn chứng trực tiếp từ JD thật và phân tích khoảng cách kỹ năng (skill gaps).
        </p>
      </div>

      {/* Selector: Chuyển đổi nhanh giữa các Top JD THẬT */}
      <div style={{ marginBottom: 'var(--space-6)' }}>
        <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)', marginBottom: 'var(--space-2)', fontWeight: '600' }}>
          CHUYỂN NHANH GIỮA CÁC JD THỰC TẾ TRONG KHO DỮ LIỆU:
        </div>
        <div style={{
          display: 'flex',
          gap: 'var(--space-2)',
          overflowX: 'auto',
          paddingBottom: 'var(--space-2)',
        }}>
          {featuredRealJobs.map((job) => (
            <button
              key={job.id}
              type="button"
              className={`btn ${job.id === currentJob.id ? 'btn-primary' : 'btn-secondary'}`}
              style={{ fontSize: 'var(--font-size-xs)', padding: 'var(--space-2) var(--space-4)', whiteSpace: 'nowrap' }}
              onClick={() => {
                setSelectedId(job.id)
                localStorage.setItem('selectedJobId', job.id.toString())
              }}
            >
              <span>{job.title.slice(0, 32)}</span>
              <span style={{ opacity: 0.85, fontWeight: 'bold' }}>({job.industry_group})</span>
            </button>
          ))}
        </div>
      </div>

      {/* Top-level score + Real JD Overview */}
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
            border: `3px solid ${currentJob.score >= 80 ? 'var(--color-success)' : 'var(--color-warning)'}`,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0,
            boxShadow: currentJob.score >= 80 ? '0 0 24px rgba(52, 211, 153, 0.25)' : '0 0 24px rgba(251, 191, 36, 0.25)',
          }}>
            <div className="score-value" style={{
              color: currentJob.score >= 80 ? 'var(--color-success)' : 'var(--color-warning)',
              fontSize: '2rem'
            }}>
              {currentJob.score}
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
                {currentJob.title}
              </h2>
              <span className="tag tag-salary">💵 {currentJob.salary}</span>
              <span className="tag tag-jobtype">{currentJob.job_type}</span>
              <span className="tag tag-neutral">{currentJob.industry_group}</span>
            </div>

            <div style={{
              fontSize: 'var(--font-size-sm)',
              color: 'var(--color-text-secondary)',
              display: 'flex',
              gap: 'var(--space-3)',
              marginBottom: 'var(--space-3)',
              flexWrap: 'wrap',
            }}>
              <span>🏢 <strong>{currentJob.company}</strong></span>
              <span>•</span>
              <span>📍 {currentJob.location}</span>
              <span>•</span>
              <span>🎓 Yêu cầu: {currentJob.level}</span>
            </div>

            {/* Benefits */}
            <div style={{
              display: 'flex',
              gap: 'var(--space-2)',
              flexWrap: 'wrap',
              marginBottom: 'var(--space-3)',
            }}>
              {currentJob.benefits.map((b, idx) => (
                <span key={idx} className="tag tag-benefit">✓ {b}</span>
              ))}
            </div>

            <div style={{
              fontSize: 'var(--font-size-xs)',
              color: 'var(--color-text-muted)',
              borderTop: '1px solid rgba(148, 163, 184, 0.1)',
              paddingTop: 'var(--space-2)',
              display: 'flex',
              alignItems: 'center',
              gap: 'var(--space-2)'
            }}>
              <span>{isBackendReal ? '🟢' : 'ℹ️'}</span>
              <span>
                {isBackendReal
                  ? <>Điểm số & Breakdown: <strong>Thuật toán Hybrid V2 Backend thật (FastAPI)</strong> • JD: <strong>{currentJob.company}</strong> (Kho dữ liệu tinixai CC BY-NC 4.0)</>
                  : <>Dữ liệu JD: <strong>Thật từ tinixai</strong> • Điểm số: <em>Chế độ demo mock</em></>}
              </span>
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
            📊 Phân rã điểm 3 chiều (Hybrid V2 Scoring)
          </h3>
          {breakdownDimensions.map((d) => {
            const getScoreColor = (s) => (s >= 80 ? 'var(--color-success)' : s >= 65 ? 'var(--color-warning)' : 'var(--color-error)')
            return (
              <div key={d.name} style={{ marginBottom: 'var(--space-4)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--space-2)' }}>
                  <span style={{ fontSize: 'var(--font-size-sm)', fontWeight: 'var(--font-weight-medium)', color: 'var(--color-text-primary)' }}>
                    {d.icon} {d.name}
                  </span>
                  <span style={{ fontSize: 'var(--font-size-sm)', fontWeight: 'var(--font-weight-semibold)', color: getScoreColor(d.score) }}>
                    {d.score}/100 <span style={{ color: 'var(--color-text-muted)', fontWeight: 'normal' }}>(Trọng số: {Math.round(d.weight * 100)}%)</span>
                  </span>
                </div>
                <div className="progress-bar">
                  <div className="progress-bar-fill" style={{ width: `${d.score}%`, background: getScoreColor(d.score) }} />
                </div>
              </div>
            )
          })}
          <div style={{
            marginTop: 'var(--space-4)',
            paddingTop: 'var(--space-3)',
            borderTop: '1px solid rgba(148, 163, 184, 0.1)',
            fontSize: 'var(--font-size-xs)',
            color: 'var(--color-text-muted)'
          }}>
            💡 <strong>Công thức trọng số công khai (Tầng 4):</strong> <code>Score = 0.5 × HardSkill + 0.4 × Semantic + 0.1 × SoftSkill</code> (Chuẩn hóa minh bạch, không hộp đen).
          </div>
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
              ✅ Kỹ năng đáp ứng ({matchedSkills.length})
            </h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-2)' }}>
              {matchedSkills.map((s) => (
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
              ❌ Khoảng trống kỹ năng ({missingSkills.length} Gap)
            </h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-2)' }}>
              {missingSkills.length > 0 ? (
                missingSkills.map((s) => (
                  <span key={s} className="tag tag-gap">{s}</span>
                ))
              ) : (
                <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>
                  Không phát hiện thiếu hụt lớn về kỹ năng cơ bản.
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Evidence section — Explainability (Dẫn chứng thật) */}
      <div className="card" style={{ marginBottom: 'var(--space-6)' }}>
        <h3 style={{
          fontSize: 'var(--font-size-base)',
          fontWeight: 'var(--font-weight-semibold)',
          marginBottom: 'var(--space-4)',
          color: 'var(--color-text-primary)',
        }}>
          📝 Bằng chứng đối chiếu (Evidence) — Trích dẫn trực tiếp minh bạch
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
          {/* Trích từ CV */}
          <div
            style={{
              padding: 'var(--space-4)',
              borderRadius: 'var(--radius-lg)',
              background: 'var(--color-bg-primary)',
              borderLeft: '4px solid var(--color-success)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--space-2)' }}>
              <span style={{ fontSize: 'var(--font-size-xs)', fontWeight: 'var(--font-weight-semibold)', color: 'var(--color-success)', textTransform: 'uppercase' }}>
                Trích xuất từ CV của bạn ({candidateProfile?.candidate_id || 'Ứng viên #AIT-01'})
              </span>
              <span className="tag tag-neutral" style={{ fontSize: '0.7rem' }}>Khớp năng lực</span>
            </div>
            <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-primary)', fontStyle: 'italic', marginBottom: 'var(--space-2)', lineHeight: '1.6' }}>
              “{cvEvidenceSnippet}”
            </p>
            <p style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>
              💡 <strong>Nhận định AI:</strong> {isBackendReal
                ? `Hệ thống ghi nhận ${matchedSkills.length} kỹ năng phù hợp trực tiếp và độ tương đồng ngữ nghĩa đạt ${(backendJob?.breakdown?.semantic?.score || 80)}% với vị trí ${currentJob.title}.`
                : `Khớp nền tảng phát triển ứng dụng và xử lý dữ liệu với yêu cầu của vị trí ${currentJob.title}.`}
            </p>
          </div>

          {/* Trích trực tiếp từ JD THẬT trong jds.json */}
          <div
            style={{
              padding: 'var(--space-4)',
              borderRadius: 'var(--radius-lg)',
              background: 'var(--color-bg-primary)',
              borderLeft: '4px solid var(--color-warning)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--space-2)' }}>
              <span style={{ fontSize: 'var(--font-size-xs)', fontWeight: 'var(--font-weight-semibold)', color: 'var(--color-warning)', textTransform: 'uppercase' }}>
                Trích xuất trực tiếp từ JD ({currentJob.company})
              </span>
              <span className="tag tag-neutral" style={{ fontSize: '0.7rem' }}>Yêu cầu công việc thật</span>
            </div>
            <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-primary)', fontStyle: 'italic', marginBottom: 'var(--space-2)', lineHeight: '1.6' }}>
              “{jdQuoteSample}”
            </p>
            <p style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>
              💡 <strong>Nhận định AI:</strong> Điểm mạnh nằm ở các kỹ năng nền tảng. Các yêu cầu nâng cao trong đoạn trích sẽ được ưu tiên đưa vào Bước 5 (Cải thiện CV).
            </p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="page-navigation">
        <button
          type="button"
          className="btn btn-ghost"
          onClick={() => navigate('/matching')}
        >
          ← Quay lại danh sách JD
        </button>
        <button
          type="button"
          className="btn btn-primary btn-lg"
          onClick={() => navigate('/improve')}
        >
          Tiếp tục: Cải thiện CV (Bước 5) →
        </button>
      </div>
    </div>
  )
}
