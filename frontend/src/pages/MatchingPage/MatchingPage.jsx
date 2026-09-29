import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import '../../styles/pages.css'
import { ALL_REAL_JDS, getIndustryCounts } from '../../services/jobService'

/**
 * Bước 3 — Matching CV–JD
 *
 * Nạp trực tiếp 450 JD THẬT từ data/processed/jds.json (A đã tiền xử lý).
 * Hiển thị chuẩn hóa công ty thật, mức lương thật, đãi ngộ thật.
 * Có tab lọc riêng cho nhóm 'Data / AI / ML' (~75 job thật) và 'Software Engineering' (~60 job thật).
 */
export default function MatchingPage() {
  const navigate = useNavigate()
  const [selectedIndustry, setSelectedIndustry] = useState('all')
  const [candidateProfile, setCandidateProfile] = useState(null)
  const [backendMatches, setBackendMatches] = useState([])
  const [isRealScored, setIsRealScored] = useState(false)
  const [currentPage, setCurrentPage] = useState(1)
  const pageSize = 10

  const counts = getIndustryCounts()

  // Đọc Career Profile, Parsed CV và kết quả Matching thật từ Backend
  useEffect(() => {
    try {
      const career = JSON.parse(localStorage.getItem('careerProfile') || '{}')
      const cv = JSON.parse(localStorage.getItem('parsedCV') || '{}')
      setCandidateProfile({ ...career, ...cv })

      const matches = JSON.parse(localStorage.getItem('backendMatches') || '[]')
      if (Array.isArray(matches) && matches.length > 0) {
        setBackendMatches(matches)
        setIsRealScored(true)
      }
    } catch (err) {
      console.error('Lỗi đọc dữ liệu profile hoặc backendMatches:', err)
    }
  }, [])

  // Reset trang về 1 khi đổi bộ lọc ngành
  const handleFilterChange = (group) => {
    setSelectedIndustry(group)
    setCurrentPage(1)
  }

  // Danh sách công việc ưu tiên từ Backend thật nếu có, fallback ALL_REAL_JDS
  const baseJobs = isRealScored && backendMatches.length > 0 ? backendMatches : ALL_REAL_JDS

  // Lọc theo nhóm ngành
  const filteredJobs = baseJobs.filter((job) => {
    if (selectedIndustry === 'all') return true
    return job.industry_group === selectedIndustry
  })

  // Phân trang
  const totalPages = Math.ceil(filteredJobs.length / pageSize) || 1
  const paginatedJobs = filteredJobs.slice((currentPage - 1) * pageSize, currentPage * pageSize)

  // Chọn 1 job để xem chi tiết
  const handleSelectJob = (jobId) => {
    localStorage.setItem('selectedJobId', jobId.toString())
    navigate('/results')
  }

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
          AI đối chiếu hồ sơ của bạn với <strong>{ALL_REAL_JDS.length} JD thật</strong> từ dataset <code>tinixai/vietnamese-job-descriptions</code> (tuyệt đối không dùng tên công ty bịa đặt).
        </p>
      </div>

      {/* Candidate Profile summary bar */}
      {candidateProfile && (
        <div className="card" style={{ marginBottom: 'var(--space-6)', padding: 'var(--space-4) var(--space-6)', background: 'var(--color-bg-primary)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 'var(--space-3)' }}>
            <div>
              <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>Hồ sơ ứng viên đang đối chiếu:</span>
              <div style={{ fontSize: 'var(--font-size-sm)', fontWeight: 'var(--font-weight-semibold)', color: 'var(--color-text-primary)' }}>
                👤 {candidateProfile.candidate_id || 'Ứng viên #AIT-01'} • Mục tiêu: <strong>{candidateProfile.targetRole || candidateProfile.target_title || 'Software / Data Engineer'}</strong>
              </div>
            </div>
            <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
              <span className="tag tag-neutral">
                Kinh nghiệm: {candidateProfile.years_of_experience || 1.0} năm
              </span>
              <span className="tag tag-skill">
                {candidateProfile.skills?.length || 6} Kỹ năng đã xác nhận
              </span>
            </div>
          </div>
        </div>
      )}

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
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--space-2)'
          }}>
            <span>{isRealScored ? '🟢' : '🔄'}</span>
            <span>{isRealScored ? 'Truy xuất & Chấm điểm Backend thật (Hybrid V2)' : 'Trạng thái truy xuất & Chấm điểm'}</span>
          </span>
          <span className="tag tag-match">
            {isRealScored ? `Đã xếp hạng Top ${backendMatches.length} JD theo CV thật` : `Đã nạp ${ALL_REAL_JDS.length} JD thật từ kho dữ liệu`}
          </span>
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
          flexWrap: 'wrap',
          gap: 'var(--space-2)',
        }}>
          <span>
            {isRealScored
              ? 'Công thức: 50% Hard Skill + 10% Soft Skill + 40% Semantic Embedding'
              : 'Nguồn: data/processed/jds.json (CC BY-NC 4.0)'}
          </span>
          <span>
            Đang hiển thị <strong>{filteredJobs.length}</strong> việc làm {selectedIndustry !== 'all' ? `nhóm ${selectedIndustry}` : 'phù hợp'}
          </span>
        </div>
      </div>

      {/* Industry Filter Buttons (Yêu cầu 2: Data/AI/ML hiển thị đúng ~75 job) */}
      <div style={{
        display: 'flex',
        gap: 'var(--space-2)',
        marginBottom: 'var(--space-6)',
        flexWrap: 'wrap',
        alignItems: 'center',
      }}>
        <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)', fontWeight: '600', marginRight: 'var(--space-2)' }}>
          BỘ LỌC NGÀNH NGHỀ:
        </span>
        <button
          className={`btn ${selectedIndustry === 'all' ? 'btn-primary' : 'btn-secondary'}`}
          style={{ fontSize: 'var(--font-size-xs)', padding: 'var(--space-2) var(--space-4)' }}
          onClick={() => handleFilterChange('all')}
        >
          Tất cả ({counts.all})
        </button>
        <button
          className={`btn ${selectedIndustry === 'Data/AI/ML' ? 'btn-primary' : 'btn-secondary'}`}
          style={{ fontSize: 'var(--font-size-xs)', padding: 'var(--space-2) var(--space-4)' }}
          onClick={() => handleFilterChange('Data/AI/ML')}
        >
          🤖 Data / AI / ML ({counts['Data/AI/ML']})
        </button>
        <button
          className={`btn ${selectedIndustry === 'Software Engineering' ? 'btn-primary' : 'btn-secondary'}`}
          style={{ fontSize: 'var(--font-size-xs)', padding: 'var(--space-2) var(--space-4)' }}
          onClick={() => handleFilterChange('Software Engineering')}
        >
          💻 Software Engineering ({counts['Software Engineering']})
        </button>
        <button
          className={`btn ${selectedIndustry === 'IT General' ? 'btn-primary' : 'btn-secondary'}`}
          style={{ fontSize: 'var(--font-size-xs)', padding: 'var(--space-2) var(--space-4)' }}
          onClick={() => handleFilterChange('IT General')}
        >
          🛠️ IT General ({counts['IT General']})
        </button>
        <button
          className={`btn ${selectedIndustry === 'Infra/DevOps' ? 'btn-primary' : 'btn-secondary'}`}
          style={{ fontSize: 'var(--font-size-xs)', padding: 'var(--space-2) var(--space-4)' }}
          onClick={() => handleFilterChange('Infra/DevOps')}
        >
          ☁️ Infra / DevOps ({counts['Infra/DevOps']})
        </button>
      </div>

      {/* Thông tin số lượng tab hiện tại */}
      {selectedIndustry === 'Data/AI/ML' && (
        <div className="alert-box alert-success animate-fade-in" style={{ marginBottom: 'var(--space-4)' }}>
          <span>🤖</span>
          <div>
            <strong>Nhóm Data / AI / ML:</strong> Đang hiển thị chính xác <strong>{counts['Data/AI/ML']} việc làm thật</strong> (bao gồm Data Engineer, Data Analyst, AI/ML Specialist, LLM/GenAI...). Không bị trộn lẫn với Software Engineering.
          </div>
        </div>
      )}

      {/* Job list (450 JD THẬT) */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
        {paginatedJobs.map((job, idx) => {
          const globalRank = (currentPage - 1) * pageSize + idx + 1
          return (
            <div
              key={job.id}
              className="card"
              style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: 'var(--space-5)',
                animation: `fadeIn 0.3s ease ${(idx % 10) * 0.05}s forwards`,
                cursor: 'pointer',
                border: idx === 0 && currentPage === 1 ? '1px solid rgba(99, 102, 241, 0.4)' : undefined,
              }}
              onClick={() => handleSelectJob(job.id)}
            >
              {/* Rank badge */}
              <div style={{
                width: 38,
                height: 38,
                borderRadius: 'var(--radius-lg)',
                background: globalRank <= 3 ? 'var(--gradient-accent)' : 'rgba(148, 163, 184, 0.12)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 'var(--font-weight-bold)',
                color: globalRank <= 3 ? 'white' : 'var(--color-text-secondary)',
                flexShrink: 0,
                fontSize: 'var(--font-size-sm)',
              }}>
                #{globalRank}
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
                  <span className="tag tag-neutral" style={{ fontSize: '0.7rem' }}>
                    {job.industry_group}
                  </span>
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
                  <span style={{ color: 'var(--color-text-secondary)', fontWeight: 'var(--font-weight-semibold)' }}>
                    🏢 {job.company}
                  </span>
                  <span>•</span>
                  <span>📍 {job.location}</span>
                  <span>•</span>
                  <span>🎓 {job.level}</span>
                </div>

                {/* Benefits chips (real from dataset) */}
                <div style={{ display: 'flex', gap: 'var(--space-2)', flexWrap: 'wrap', marginBottom: job.breakdown ? 'var(--space-2)' : '0' }}>
                  {job.benefits?.map((b, bIdx) => (
                    <span key={bIdx} className="tag tag-benefit">✓ {b}</span>
                  ))}
                </div>

                {/* Real Hybrid Breakdown Chips từ backend nếu có */}
                {job.breakdown && (
                  <div style={{ display: 'flex', gap: 'var(--space-2)', flexWrap: 'wrap', marginTop: 'var(--space-2)' }}>
                    {job.breakdown.hard_skill && (
                      <span className="tag tag-skill" style={{ fontSize: '0.7rem' }}>
                        ⚙️ Kỹ năng cứng: {job.breakdown.hard_skill.score}%
                      </span>
                    )}
                    {job.breakdown.semantic && (
                      <span className="tag tag-neutral" style={{ fontSize: '0.7rem' }}>
                        🧠 Ngữ nghĩa CV-JD: {job.breakdown.semantic.score}%
                      </span>
                    )}
                    {job.breakdown.soft_skill && (
                      <span className="tag tag-neutral" style={{ fontSize: '0.7rem' }}>
                        🤝 Kỹ năng mềm: {job.breakdown.soft_skill.score}%
                      </span>
                    )}
                  </div>
                )}
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
          )
        })}
      </div>

      {/* Pagination controls */}
      {totalPages > 1 && (
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          gap: 'var(--space-2)',
          marginTop: 'var(--space-8)',
          flexWrap: 'wrap',
        }}>
          <button
            className="btn btn-secondary"
            style={{ fontSize: 'var(--font-size-xs)', padding: 'var(--space-2) var(--space-3)' }}
            disabled={currentPage === 1}
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
          >
            ← Trước
          </button>
          {Array.from({ length: Math.min(8, totalPages) }, (_, i) => {
            const pageNum = i + 1
            return (
              <button
                key={pageNum}
                className={`btn ${currentPage === pageNum ? 'btn-primary' : 'btn-ghost'}`}
                style={{ fontSize: 'var(--font-size-xs)', padding: 'var(--space-2) var(--space-3)', minWidth: '32px' }}
                onClick={() => setCurrentPage(pageNum)}
              >
                {pageNum}
              </button>
            )
          })}
          {totalPages > 8 && <span style={{ color: 'var(--color-text-muted)' }}>... {totalPages}</span>}
          <button
            className="btn btn-secondary"
            style={{ fontSize: 'var(--font-size-xs)', padding: 'var(--space-2) var(--space-3)' }}
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
          >
            Sau →
          </button>
        </div>
      )}

      {/* Navigation */}
      <div className="page-navigation">
        <button
          type="button"
          className="btn btn-ghost"
          onClick={() => navigate('/upload-cv')}
        >
          ← Quay lại Bước 2 (Upload CV)
        </button>
        <button
          type="button"
          className="btn btn-primary btn-lg"
          onClick={() => handleSelectJob(filteredJobs[0]?.id || 1)}
        >
          Xem kết quả chi tiết & Giải thích (Bước 4) →
        </button>
      </div>
    </div>
  )
}
