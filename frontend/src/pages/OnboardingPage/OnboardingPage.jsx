import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import '../../styles/pages.css'

// Gợi ý vai trò phổ biến trong ngành CNTT
const POPULAR_ROLES = [
  'Frontend Developer',
  'Backend Developer',
  'Fullstack Developer',
  'Data Analyst',
  'AI / Machine Learning Engineer',
  'DevOps / Cloud Engineer',
]

// Gợi ý kỹ năng thường gặp từ taxonomy (data/taxonomy/skills_taxonomy.json)
const SUGGESTED_SKILLS = [
  'JavaScript',
  'ReactJS',
  'Python',
  'TypeScript',
  'SQL',
  'Node.js',
  'Git',
  'FastAPI',
  'Docker',
  'Tailwind CSS',
  'RESTful API',
  'PostgreSQL',
]

/**
 * Bước 1 — Onboarding / Định hướng nghề nghiệp
 *
 * User thiết lập Career Profile:
 * - Vị trí mong muốn (Role)
 * - Mức kinh nghiệm (Experience Level)
 * - Địa điểm làm việc (Location)
 * - Mức lương kỳ vọng (Salary Range)
 * - Ngành trọng tâm (Industry)
 * - Kỹ năng mục tiêu (Skills Tagging)
 */
export default function OnboardingPage() {
  const navigate = useNavigate()

  // Form State
  const [targetRole, setTargetRole] = useState('Frontend Developer')
  const [experienceLevel, setExperienceLevel] = useState('fresher')
  const [location, setLocation] = useState('hcm')
  const [expectedSalary, setExpectedSalary] = useState('12 – 18')
  const [industry, setIndustry] = useState('Công nghệ thông tin / Phần mềm')
  const [skills, setSkills] = useState(['JavaScript', 'ReactJS', 'HTML/CSS', 'Git'])
  const [newSkillInput, setNewSkillInput] = useState('')
  const [savedNotice, setSavedNotice] = useState(false)

  // Khôi phục từ localStorage nếu đã nhập trước đó
  useEffect(() => {
    const saved = localStorage.getItem('careerProfile')
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        if (parsed.targetRole) setTargetRole(parsed.targetRole)
        if (parsed.experienceLevel) setExperienceLevel(parsed.experienceLevel)
        if (parsed.location) setLocation(parsed.location)
        if (parsed.expectedSalary) setExpectedSalary(parsed.expectedSalary)
        if (parsed.industry) setIndustry(parsed.industry)
        if (Array.isArray(parsed.skills)) setSkills(parsed.skills)
      } catch (err) {
        console.error('Lỗi đọc careerProfile từ localStorage:', err)
      }
    }
  }, [])

  // Thêm kỹ năng từ input gõ phím
  const handleAddSkill = (e) => {
    if ((e.key === 'Enter' || e.type === 'blur') && newSkillInput.trim()) {
      e.preventDefault()
      const val = newSkillInput.trim()
      if (!skills.includes(val)) {
        setSkills([...skills, val])
      }
      setNewSkillInput('')
    }
  }

  // Thêm kỹ năng nhanh từ gợi ý
  const handleToggleSuggestedSkill = (skill) => {
    if (skills.includes(skill)) {
      setSkills(skills.filter((s) => s !== skill))
    } else {
      setSkills([...skills, skill])
    }
  }

  // Xóa kỹ năng khỏi danh sách
  const handleRemoveSkill = (skillToRemove) => {
    setSkills(skills.filter((s) => s !== skillToRemove))
  }

  // Submit Career Profile
  const handleSubmit = (e) => {
    e.preventDefault()

    const careerProfile = {
      targetRole,
      experienceLevel,
      location,
      expectedSalary,
      industry,
      skills,
      updatedAt: new Date().toISOString(),
    }

    localStorage.setItem('careerProfile', JSON.stringify(careerProfile))
    setSavedNotice(true)

    // Chuyển tiếp sang Bước 2: Upload CV
    setTimeout(() => {
      navigate('/upload-cv')
    }, 300)
  }

  return (
    <div>
      {/* Header */}
      <div className="page-header">
        <div className="page-step-badge">
          <span>🎯</span>
          <span>Bước 1 / 6</span>
        </div>
        <h1 className="page-title">Định hướng nghề nghiệp</h1>
        <p className="page-subtitle">
          Xây dựng <strong>Career Profile</strong> để hệ thống AI hiểu rõ mục tiêu, mức kinh nghiệm và kỳ vọng của bạn,
          từ đó truy xuất các tin tuyển dụng sát nhất trước khi đối chiếu CV.
        </p>
      </div>

      {savedNotice && (
        <div className="alert-box alert-success animate-fade-in">
          <span>✓</span>
          <span>Hồ sơ định hướng đã được lưu trữ thành công. Đang chuyển sang Bước 2...</span>
        </div>
      )}

      {/* Form Onboarding */}
      <form onSubmit={handleSubmit}>
        {/* Khối 1: Vị trí & Ngành */}
        <div className="card" style={{ marginBottom: 'var(--space-6)' }}>
          <h2 style={{
            fontSize: 'var(--font-size-base)',
            fontWeight: 'var(--font-weight-semibold)',
            marginBottom: 'var(--space-4)',
            color: 'var(--color-text-primary)',
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--space-2)'
          }}>
            <span>💼</span>
            <span>Mục tiêu vị trí & Ngành nghề</span>
          </h2>

          <div className="grid-2">
            <div className="form-group" style={{ marginBottom: 'var(--space-4)' }}>
              <label className="form-label" htmlFor="target-role">
                Vị trí mục tiêu <span style={{ color: 'var(--color-accent)' }}>*</span>
              </label>
              <input
                id="target-role"
                className="form-input"
                type="text"
                required
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                placeholder="VD: Frontend Developer, Data Analyst..."
              />
              {/* Quick suggestions */}
              <div style={{ marginTop: 'var(--space-2)', display: 'flex', gap: 'var(--space-2)', flexWrap: 'wrap' }}>
                {POPULAR_ROLES.map((role) => (
                  <button
                    key={role}
                    type="button"
                    className={`pill-option ${targetRole === role ? 'active' : ''}`}
                    onClick={() => setTargetRole(role)}
                  >
                    {role}
                  </button>
                ))}
              </div>
            </div>

            <div className="form-group" style={{ marginBottom: 'var(--space-4)' }}>
              <label className="form-label" htmlFor="industry">
                Lĩnh vực trọng tâm
              </label>
              <input
                id="industry"
                className="form-input"
                type="text"
                value={industry}
                onChange={(e) => setIndustry(e.target.value)}
                placeholder="VD: Công nghệ thông tin / Phần mềm, AI..."
              />
              <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)', marginTop: 'var(--space-1)', display: 'block' }}>
                Hệ thống ưu tiên bộ lọc ngành IT chuẩn từ dataset <code>tinixai</code>.
              </span>
            </div>
          </div>
        </div>

        {/* Khối 2: Kinh nghiệm, Địa điểm & Lương */}
        <div className="card" style={{ marginBottom: 'var(--space-6)' }}>
          <h2 style={{
            fontSize: 'var(--font-size-base)',
            fontWeight: 'var(--font-weight-semibold)',
            marginBottom: 'var(--space-4)',
            color: 'var(--color-text-primary)',
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--space-2)'
          }}>
            <span>📍</span>
            <span>Điều kiện làm việc & Kỳ vọng</span>
          </h2>

          <div className="grid-3">
            {/* Kinh nghiệm */}
            <div className="form-group" style={{ marginBottom: 'var(--space-2)' }}>
              <label className="form-label" htmlFor="experience-level">
                Mức kinh nghiệm hiện tại
              </label>
              <select
                id="experience-level"
                className="form-select"
                value={experienceLevel}
                onChange={(e) => setExperienceLevel(e.target.value)}
              >
                <option value="intern">Thực tập sinh (Intern)</option>
                <option value="fresher">Fresher (0 – 1 năm kinh nghiệm)</option>
                <option value="junior">Junior (1 – 3 năm kinh nghiệm)</option>
                <option value="mid">Mid-level (3 – 5 năm kinh nghiệm)</option>
              </select>
            </div>

            {/* Địa điểm */}
            <div className="form-group" style={{ marginBottom: 'var(--space-2)' }}>
              <label className="form-label" htmlFor="location">
                Khu vực làm việc
              </label>
              <select
                id="location"
                className="form-select"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
              >
                <option value="hcm">TP. Hồ Chí Minh</option>
                <option value="hanoi">Hà Nội</option>
                <option value="danang">Đà Nẵng</option>
                <option value="remote">Làm việc từ xa (Remote)</option>
                <option value="any">Linh hoạt / Toàn quốc</option>
              </select>
            </div>

            {/* Lương */}
            <div className="form-group" style={{ marginBottom: 'var(--space-2)' }}>
              <label className="form-label" htmlFor="salary">
                Mức lương mong muốn (triệu VNĐ)
              </label>
              <input
                id="salary"
                className="form-input"
                type="text"
                value={expectedSalary}
                onChange={(e) => setExpectedSalary(e.target.value)}
                placeholder="VD: 10 – 15 hoặc 15 – 22"
              />
            </div>
          </div>
        </div>

        {/* Khối 3: Kỹ năng định hướng */}
        <div className="card" style={{ marginBottom: 'var(--space-6)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-2)' }}>
            <h2 style={{
              fontSize: 'var(--font-size-base)',
              fontWeight: 'var(--font-weight-semibold)',
              color: 'var(--color-text-primary)',
              display: 'flex',
              alignItems: 'center',
              gap: 'var(--space-2)'
            }}>
              <span>⚡</span>
              <span>Kỹ năng cốt lõi (Skills)</span>
            </h2>
            <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>
              Đã chọn: <strong>{skills.length}</strong> kỹ năng
            </span>
          </div>

          <p style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)', marginBottom: 'var(--space-4)' }}>
            Nhập kỹ năng rồi bấm <strong>Enter</strong> hoặc chọn nhanh từ danh mục kỹ năng chuẩn hóa (Taxonomy):
          </p>

          {/* Active skills list */}
          <div style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: 'var(--space-2)',
            padding: 'var(--space-3)',
            background: 'var(--color-bg-primary)',
            borderRadius: 'var(--radius-lg)',
            border: '1px solid rgba(148, 163, 184, 0.15)',
            minHeight: '48px',
            alignItems: 'center',
            marginBottom: 'var(--space-4)'
          }}>
            {skills.map((skill) => (
              <span key={skill} className="tag-removable">
                <span>{skill}</span>
                <button
                  type="button"
                  className="tag-remove-btn"
                  onClick={() => handleRemoveSkill(skill)}
                  title={`Xóa ${skill}`}
                >
                  ✕
                </button>
              </span>
            ))}
            <input
              type="text"
              value={newSkillInput}
              onChange={(e) => setNewSkillInput(e.target.value)}
              onKeyDown={handleAddSkill}
              placeholder="+ Thêm kỹ năng (gõ & Enter)..."
              style={{
                border: 'none',
                outline: 'none',
                background: 'transparent',
                color: 'var(--color-text-primary)',
                fontSize: 'var(--font-size-xs)',
                padding: 'var(--space-1) var(--space-2)',
                minWidth: '180px',
                flex: 1
              }}
            />
          </div>

          {/* Gợi ý kỹ năng từ Taxonomy */}
          <div>
            <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)', marginBottom: 'var(--space-2)' }}>
              Gợi ý nhanh từ kho taxonomy CNTT:
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-2)' }}>
              {SUGGESTED_SKILLS.map((item) => {
                const isSelected = skills.includes(item)
                return (
                  <button
                    key={item}
                    type="button"
                    className={`pill-option ${isSelected ? 'active' : ''}`}
                    onClick={() => handleToggleSuggestedSkill(item)}
                  >
                    <span>{isSelected ? '✓' : '+'}</span>
                    <span>{item}</span>
                  </button>
                )
              })}
            </div>
          </div>
        </div>

        {/* Footer Navigation */}
        <div className="page-navigation">
          <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>
            Thông tin sẽ tự động đồng bộ sang Bước 2 & 3.
          </div>
          <button type="submit" className="btn btn-primary btn-lg">
            Tiếp tục → Upload CV (Bước 2)
          </button>
        </div>
      </form>
    </div>
  )
}
