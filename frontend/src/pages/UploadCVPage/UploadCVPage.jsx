import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../../styles/pages.css'
import { uploadCVApi } from '../../services/apiService'

/**
 * Schema Tầng 2 — Structured Extraction theo AGENTS.md:
 * - skills: danh sách kỹ năng trích xuất
 * - years: số năm kinh nghiệm
 * - education: thông tin trường, ngành, năm tốt nghiệp
 * - responsibilities: danh sách trách nhiệm & kinh nghiệm công việc
 */
const DEFAULT_MOCK_PARSED_CV = {
  candidate_id: 'Ứng viên #AIT-01 (Ẩn danh)',
  target_title: 'Frontend Developer',
  years_of_experience: 1.0,
  education: {
    institution: 'Đại học Bách Khoa (ĐHQG)',
    degree: 'Cử nhân Công nghệ Thông tin',
    graduation_year: '2025',
    gpa: '3.4 / 4.0',
  },
  skills: [
    'JavaScript (ES6+)',
    'ReactJS',
    'HTML5/CSS3',
    'Git',
    'RESTful API',
    'Tailwind CSS',
    'Redux Toolkit',
  ],
  experience: [
    {
      id: 1,
      company: 'Công ty Công nghệ Alpha (Thực tập)',
      role: 'Frontend Developer Intern',
      period: '06/2024 – 12/2024 (6 tháng)',
      responsibilities: [
        'Phát triển và tối ưu hóa các component giao diện ReactJS theo thiết kế Figma.',
        'Kết nối RESTful API với backend FastAPI, xử lý phân trang và caching dữ liệu client.',
        'Sử dụng Git/GitHub để quản lý mã nguồn, tham gia review code trong nhóm 5 người.',
      ],
    },
    {
      id: 2,
      company: 'Dự án Khóa luận Tốt nghiệp',
      role: 'Frontend & UI Lead',
      period: '01/2025 – 05/2025 (5 tháng)',
      responsibilities: [
        'Xây dựng hệ thống web dashboard phân tích việc làm cho sinh viên bằng React và Vite.',
        'Tối ưu hiệu năng Web Vitals đạt điểm Google Lighthouse 92/100.',
      ],
    },
  ],
}

export default function UploadCVPage() {
  const navigate = useNavigate()

  // State quản lý luồng
  const [file, setFile] = useState(null)
  const [isParsing, setIsParsing] = useState(false)
  const [parseProgress, setParseProgress] = useState(0)
  const [parsedData, setParsedData] = useState(null)
  const [apiError, setApiError] = useState(null)
  const [isRealBackend, setIsRealBackend] = useState(false)
  const [newSkill, setNewSkill] = useState('')
  const [newBullet, setNewBullet] = useState({ expId: 1, text: '' })

  // Gọi API Backend thật: POST /api/cv/upload
  const handleUploadRealCV = async (fileObj) => {
    if (!fileObj) return
    setIsParsing(true)
    setApiError(null)
    setParseProgress(20)

    const timer1 = setTimeout(() => setParseProgress(50), 300)
    const timer2 = setTimeout(() => setParseProgress(80), 700)

    try {
      // Đọc metadata lọc từ Career Profile nếu có
      let options = { mode: 'llm', top_k: 20 }
      try {
        const career = JSON.parse(localStorage.getItem('careerProfile') || '{}')
        if (career.preferredLocation) options.location = career.preferredLocation
        if (career.experienceLevel) options.level = career.experienceLevel
      } catch (e) {
        console.warn('Không đọc được careerProfile:', e)
      }

      const res = await uploadCVApi(fileObj, options)

      clearTimeout(timer1)
      clearTimeout(timer2)

      if (res.success && res.data) {
        setParseProgress(100)
        setIsParsing(false)
        setIsRealBackend(true)

        const uiCv = res.data.parsed_cv
        setParsedData(uiCv)

        // Lưu vào localStorage
        localStorage.setItem('parsedCV', JSON.stringify(uiCv))
        localStorage.setItem('backendMatches', JSON.stringify(res.data.matches || []))
        localStorage.setItem('isMockMode', 'false')
        // Thông báo cho AppLayout tắt hẳn Demo Mode badge
        window.dispatchEvent(new Event('mockModeChanged'))
      } else {
        throw new Error(res.error || 'Backend không phản hồi thành công.')
      }
    } catch (err) {
      clearTimeout(timer1)
      clearTimeout(timer2)
      setIsParsing(false)
      setApiError(err.message)
      console.error('Lỗi upload CV tới backend thật:', err)
    }
  }

  // Xử lý khi người dùng chọn file thật từ máy
  const handleFileSelect = (selectedFile) => {
    if (!selectedFile) return
    setFile(selectedFile)
    handleUploadRealCV(selectedFile)
  }

  // Nạp CV mẫu kiểm thử nhanh (Quick Sample): dùng file cv_single_column.pdf thật
  const handleLoadSampleCV = async () => {
    try {
      setIsParsing(true)
      setParseProgress(10)
      const resp = await fetch('/samples/cv_single_column.pdf')
      if (!resp.ok) {
        throw new Error('Không tải được file mẫu /samples/cv_single_column.pdf')
      }
      const blob = await resp.blob()
      const sampleFile = new File([blob], 'cv_single_column.pdf', { type: 'application/pdf' })
      setFile(sampleFile)
      await handleUploadRealCV(sampleFile)
    } catch (err) {
      console.warn('Lỗi tải file mẫu thật, chuyển fallback mock:', err)
      // Fallback nếu không có file
      const mockFile = { name: 'cv_single_column.pdf', size: 1024 * 340 }
      setFile(mockFile)
      setParseProgress(100)
      setIsParsing(false)
      setParsedData({
        ...DEFAULT_MOCK_PARSED_CV,
        uploaded_filename: mockFile.name,
      })
      localStorage.setItem('isMockMode', 'true')
      window.dispatchEvent(new Event('mockModeChanged'))
    }
  }

  // Chuyển sang chế độ giả lập nếu backend lỗi
  const handleUseMockFallback = () => {
    setApiError(null)
    setParsedData({
      ...DEFAULT_MOCK_PARSED_CV,
      uploaded_filename: file?.name || 'cv_mock_fallback.pdf',
    })
    localStorage.setItem('isMockMode', 'true')
    window.dispatchEvent(new Event('mockModeChanged'))
  }

  // --- Human-in-the-loop: Chỉnh sửa kỹ năng ---
  const handleRemoveSkill = (skillToRemove) => {
    setParsedData({
      ...parsedData,
      skills: parsedData.skills.filter((s) => s !== skillToRemove),
    })
  }

  const handleAddSkill = (e) => {
    if ((e.key === 'Enter' || e.type === 'blur') && newSkill.trim()) {
      e.preventDefault()
      const val = newSkill.trim()
      if (!parsedData.skills.includes(val)) {
        setParsedData({
          ...parsedData,
          skills: [...parsedData.skills, val],
        })
      }
      setNewSkill('')
    }
  }

  // --- Human-in-the-loop: Chỉnh sửa số năm kinh nghiệm ---
  const handleYearsChange = (val) => {
    const num = parseFloat(val) || 0
    setParsedData({
      ...parsedData,
      years_of_experience: num,
    })
  }

  // --- Human-in-the-loop: Chỉnh sửa học vấn ---
  const handleEducationChange = (field, val) => {
    setParsedData({
      ...parsedData,
      education: {
        ...parsedData.education,
        [field]: val,
      },
    })
  }

  // --- Human-in-the-loop: Thêm/Xóa bullet point kinh nghiệm ---
  const handleRemoveBullet = (expId, bulletIdx) => {
    const updatedExp = parsedData.experience.map((item) => {
      if (item.id === expId) {
        return {
          ...item,
          responsibilities: item.responsibilities.filter((_, idx) => idx !== bulletIdx),
        }
      }
      return item
    })
    setParsedData({ ...parsedData, experience: updatedExp })
  }

  const handleAddBullet = (expId) => {
    if (!newBullet.text.trim()) return
    const updatedExp = parsedData.experience.map((item) => {
      if (item.id === expId) {
        return {
          ...item,
          responsibilities: [...item.responsibilities, newBullet.text.trim()],
        }
      }
      return item
    })
    setParsedData({ ...parsedData, experience: updatedExp })
    setNewBullet({ expId, text: '' })
  }

  // Xác nhận kết quả parse và chuyển sang Bước 3 (Matching)
  const handleConfirmAndProceed = () => {
    localStorage.setItem('parsedCV', JSON.stringify(parsedData))
    navigate('/matching')
  }

  return (
    <div>
      {/* Page header */}
      <div className="page-header">
        <div className="page-step-badge">
          <span>📄</span>
          <span>Bước 2 / 6</span>
        </div>
        <h1 className="page-title">Upload & Parse CV</h1>
        <p className="page-subtitle">
          Tải lên bản CV của bạn (PDF/DOCX). Hệ thống AI sử dụng mô hình trích xuất cấu trúc (Structured Extraction)
          và hỗ trợ <strong>cơ chế rà soát Human-in-the-loop</strong> để bạn chỉnh sửa thông tin trước khi đối chiếu.
        </p>
      </div>

      {/* Upload Zone (Hiện khi chưa có kết quả parse) */}
      {!parsedData && !isParsing && (
        <div>
          <div
            className="upload-zone"
            id="cv-upload-zone"
            onClick={() => document.getElementById('cv-file-input').click()}
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => {
              e.preventDefault()
              if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                handleFileSelect(e.dataTransfer.files[0])
              }
            }}
          >
            <div className="upload-zone-icon">📁</div>
            <div className="upload-zone-text">
              Kéo thả file CV vào đây, hoặc <strong style={{ color: 'var(--color-accent)' }}>nhấn để chọn file từ máy</strong>
            </div>
            <div className="upload-zone-hint">
              Hỗ trợ định dạng: <strong>.PDF, .DOCX</strong> (Tối đa 10MB) • Bảo mật thông tin & ẩn danh hoàn toàn
            </div>
            <input
              id="cv-file-input"
              type="file"
              accept=".pdf,.docx"
              style={{ display: 'none' }}
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) {
                  handleFileSelect(e.target.files[0])
                }
              }}
            />
          </div>

          <div style={{ textAlign: 'center', marginTop: 'var(--space-6)' }}>
            <span style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-muted)', marginRight: 'var(--space-3)' }}>
              Chưa có sẵn file CV?
            </span>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={handleLoadSampleCV}
            >
              ⚡ Dùng CV mẫu thử nghiệm (Quick Sample)
            </button>
          </div>
        </div>
      )}

      {/* Parsing progress animation */}
      {isParsing && (
        <div className="card card-accent" style={{ textAlign: 'center', padding: 'var(--space-12) var(--space-6)' }}>
          <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 'var(--space-4)' }}>
            <div className="spinner" />
          </div>
          <h3 style={{ fontSize: 'var(--font-size-lg)', fontWeight: 'var(--font-weight-semibold)', marginBottom: 'var(--space-2)' }}>
            Đang phân tích cấu trúc CV... ({parseProgress}%)
          </h3>
          <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-muted)', marginBottom: 'var(--space-6)' }}>
            File: <strong>{file?.name}</strong> • AI đang đọc nội dung thô và phân loại thực thể theo schema chuẩn hóa
          </p>
          <div className="progress-bar" style={{ maxWidth: '400px', margin: '0 auto' }}>
            <div className="progress-bar-fill" style={{ width: `${parseProgress}%` }} />
          </div>
        </div>
      )}

      {/* Lỗi gọi API backend */}
      {apiError && !isParsing && (
        <div className="alert-box alert-warning animate-fade-in" style={{ marginBottom: 'var(--space-6)' }}>
          <span style={{ fontSize: '1.25rem' }}>⚠️</span>
          <div style={{ flex: 1 }}>
            <div style={{ fontWeight: 'var(--font-weight-bold)', marginBottom: 'var(--space-1)' }}>
              Không thể kết nối API Backend thật (POST /api/cv/upload)
            </div>
            <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)', marginBottom: 'var(--space-3)' }}>
              Chi tiết lỗi: {apiError}
            </div>
            <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
              <button
                type="button"
                className="btn btn-primary"
                style={{ fontSize: 'var(--font-size-xs)' }}
                onClick={() => handleUploadRealCV(file)}
              >
                🔄 Thử lại
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                style={{ fontSize: 'var(--font-size-xs)' }}
                onClick={handleUseMockFallback}
              >
                ⚡ Tiếp tục bằng dữ liệu mẫu (Mock Mode)
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Màn hình Xác nhận kết quả parse (HUMAN-IN-THE-LOOP) */}
      {parsedData && !isParsing && (
        <div className="animate-fade-in">
          {/* Backend Status Notification */}
          {isRealBackend && (
            <div className="alert-box alert-success" style={{ marginBottom: 'var(--space-4)' }}>
              <span style={{ fontSize: '1.25rem' }}>🟢</span>
              <div>
                <strong>API Backend Thật (FastAPI Tầng 1–4) đã xử lý thành công:</strong> Kết quả trích xuất cấu trúc (Structured Extraction) và tính toán độ khớp ngữ nghĩa song ngữ với kho JD thật. Chế độ Mock Mode đã được <strong>tắt hoàn toàn</strong>.
              </div>
            </div>
          )}

          {/* Banner Human-in-the-loop */}
          <div className="alert-box alert-info">
            <span style={{ fontSize: '1.25rem' }}>💡</span>
            <div>
              <strong>Cơ chế Human-in-the-loop (Xác nhận & Chỉnh sửa):</strong> AI đã tự động trích xuất các trường từ CV của bạn.
              Hãy kiểm tra lại danh sách kỹ năng, năm kinh nghiệm và học vấn bên dưới. Bạn có thể <strong>thêm, bớt hoặc sửa trực tiếp</strong> trước khi bấm bắt đầu Matching.
            </div>
          </div>

          {/* Header file info */}
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: 'var(--space-6)',
            flexWrap: 'wrap',
            gap: 'var(--space-3)'
          }}>
            <div>
              <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>File đã đọc:</span>
              <div style={{ fontSize: 'var(--font-size-base)', fontWeight: 'var(--font-weight-semibold)', color: 'var(--color-accent-bright)' }}>
                📄 {parsedData.uploaded_filename}
              </div>
            </div>
            <button
              type="button"
              className="btn btn-secondary"
              style={{ fontSize: 'var(--font-size-xs)' }}
              onClick={() => {
                setParsedData(null)
                setFile(null)
              }}
            >
              🔄 Tải lên file khác
            </button>
          </div>

          {/* Grid 1: Thông tin ứng viên & Học vấn */}
          <div className="grid-2" style={{ marginBottom: 'var(--space-6)' }}>
            {/* Thẻ 1: Thông tin cơ bản & Số năm kinh nghiệm */}
            <div className="card">
              <h3 style={{
                fontSize: 'var(--font-size-base)',
                fontWeight: 'var(--font-weight-semibold)',
                marginBottom: 'var(--space-4)',
                color: 'var(--color-text-primary)',
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--space-2)'
              }}>
                <span>👤</span>
                <span>Thông tin ứng viên & Kinh nghiệm</span>
              </h3>

              <div className="form-group" style={{ marginBottom: 'var(--space-3)' }}>
                <label className="form-label">Mã định danh (Đã ẩn danh hóa theo Điều 5.7):</label>
                <input
                  className="form-input"
                  type="text"
                  value={parsedData.candidate_id}
                  disabled
                  style={{ opacity: 0.8, background: 'rgba(148, 163, 184, 0.05)' }}
                />
              </div>

              <div className="grid-2">
                <div className="form-group" style={{ marginBottom: 'var(--space-2)' }}>
                  <label className="form-label">Vị trí nhận diện:</label>
                  <input
                    className="form-input"
                    type="text"
                    value={parsedData.target_title}
                    onChange={(e) => setParsedData({ ...parsedData, target_title: e.target.value })}
                  />
                </div>
                <div className="form-group" style={{ marginBottom: 'var(--space-2)' }}>
                  <label className="form-label">Số năm kinh nghiệm (years):</label>
                  <input
                    className="form-input"
                    type="number"
                    step="0.5"
                    min="0"
                    max="10"
                    value={parsedData.years_of_experience}
                    onChange={(e) => handleYearsChange(e.target.value)}
                  />
                </div>
              </div>
            </div>

            {/* Thẻ 2: Học vấn (Education) */}
            <div className="card">
              <h3 style={{
                fontSize: 'var(--font-size-base)',
                fontWeight: 'var(--font-weight-semibold)',
                marginBottom: 'var(--space-4)',
                color: 'var(--color-text-primary)',
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--space-2)'
              }}>
                <span>🎓</span>
                <span>Trình độ học vấn (Education)</span>
              </h3>

              <div className="form-group" style={{ marginBottom: 'var(--space-3)' }}>
                <label className="form-label">Trường đào tạo:</label>
                <input
                  className="form-input"
                  type="text"
                  value={parsedData.education.institution}
                  onChange={(e) => handleEducationChange('institution', e.target.value)}
                />
              </div>

              <div className="grid-2">
                <div className="form-group" style={{ marginBottom: 'var(--space-2)' }}>
                  <label className="form-label">Bằng cấp / Ngành học:</label>
                  <input
                    className="form-input"
                    type="text"
                    value={parsedData.education.degree}
                    onChange={(e) => handleEducationChange('degree', e.target.value)}
                  />
                </div>
                <div className="form-group" style={{ marginBottom: 'var(--space-2)' }}>
                  <label className="form-label">Năm tốt nghiệp & GPA:</label>
                  <input
                    className="form-input"
                    type="text"
                    value={`${parsedData.education.graduation_year} • GPA: ${parsedData.education.gpa}`}
                    onChange={(e) => handleEducationChange('graduation_year', e.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Thẻ 3: Danh sách kỹ năng trích xuất (Skills) */}
          <div className="card" style={{ marginBottom: 'var(--space-6)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-2)' }}>
              <h3 style={{
                fontSize: 'var(--font-size-base)',
                fontWeight: 'var(--font-weight-semibold)',
                color: 'var(--color-text-primary)',
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--space-2)'
              }}>
                <span>⚡</span>
                <span>Kỹ năng AI trích xuất ({parsedData.skills.length})</span>
              </h3>
              <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>
                Bấm ✕ để loại bỏ kỹ năng sai, hoặc gõ bên dưới để thêm
              </span>
            </div>

            <div style={{
              display: 'flex',
              flexWrap: 'wrap',
              gap: 'var(--space-2)',
              padding: 'var(--space-3)',
              background: 'var(--color-bg-primary)',
              borderRadius: 'var(--radius-lg)',
              border: '1px solid rgba(148, 163, 184, 0.15)',
              alignItems: 'center',
              marginBottom: 'var(--space-3)'
            }}>
              {parsedData.skills.map((skill) => (
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
                value={newSkill}
                onChange={(e) => setNewSkill(e.target.value)}
                onKeyDown={handleAddSkill}
                placeholder="+ Thêm kỹ năng bị AI đọc sót (gõ & Enter)..."
                style={{
                  border: 'none',
                  outline: 'none',
                  background: 'transparent',
                  color: 'var(--color-text-primary)',
                  fontSize: 'var(--font-size-xs)',
                  padding: 'var(--space-1) var(--space-2)',
                  minWidth: '220px',
                  flex: 1
                }}
              />
            </div>
          </div>

          {/* Thẻ 4: Trách nhiệm & Dự án đã làm (Responsibilities) */}
          <div className="card" style={{ marginBottom: 'var(--space-6)' }}>
            <h3 style={{
              fontSize: 'var(--font-size-base)',
              fontWeight: 'var(--font-weight-semibold)',
              marginBottom: 'var(--space-4)',
              color: 'var(--color-text-primary)',
              display: 'flex',
              alignItems: 'center',
              gap: 'var(--space-2)'
            }}>
              <span>💼</span>
              <span>Dự án & Trách nhiệm công việc (Responsibilities)</span>
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
              {parsedData.experience.map((exp) => (
                <div
                  key={exp.id}
                  style={{
                    padding: 'var(--space-4)',
                    borderRadius: 'var(--radius-lg)',
                    background: 'var(--color-bg-primary)',
                    border: '1px solid rgba(148, 163, 184, 0.1)',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-2)' }}>
                    <div>
                      <span style={{ fontSize: 'var(--font-size-sm)', fontWeight: 'var(--font-weight-bold)', color: 'var(--color-text-primary)' }}>
                        {exp.role}
                      </span>
                      <span style={{ margin: '0 var(--space-2)', color: 'var(--color-text-muted)' }}>•</span>
                      <span style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-accent-bright)' }}>
                        {exp.company}
                      </span>
                    </div>
                    <span className="tag tag-neutral" style={{ fontSize: '0.7rem' }}>
                      {exp.period}
                    </span>
                  </div>

                  <ul style={{ paddingLeft: 'var(--space-4)', display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
                    {exp.responsibilities.map((resp, bIdx) => (
                      <li key={bIdx} style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)', lineHeight: '1.5' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 'var(--space-2)' }}>
                          <span>• {resp}</span>
                          <button
                            type="button"
                            className="tag-remove-btn"
                            onClick={() => handleRemoveBullet(exp.id, bIdx)}
                            title="Xóa bullet point này"
                          >
                            ✕
                          </button>
                        </div>
                      </li>
                    ))}
                  </ul>

                  {/* Add bullet point */}
                  <div style={{ display: 'flex', gap: 'var(--space-2)', marginTop: 'var(--space-3)' }}>
                    <input
                      className="form-input"
                      type="text"
                      placeholder="+ Thêm mô tả trách nhiệm / công nghệ sử dụng..."
                      style={{ fontSize: 'var(--font-size-xs)', padding: 'var(--space-1) var(--space-3)' }}
                      value={newBullet.expId === exp.id ? newBullet.text : ''}
                      onChange={(e) => setNewBullet({ expId: exp.id, text: e.target.value })}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault()
                          handleAddBullet(exp.id)
                        }
                      }}
                    />
                    <button
                      type="button"
                      className="btn btn-secondary"
                      style={{ fontSize: 'var(--font-size-xs)', padding: 'var(--space-1) var(--space-3)' }}
                      onClick={() => handleAddBullet(exp.id)}
                    >
                      Thêm
                    </button>
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
              onClick={() => navigate('/onboarding')}
            >
              ← Quay lại Onboarding
            </button>
            <button
              type="button"
              className="btn btn-primary btn-lg"
              onClick={handleConfirmAndProceed}
            >
              ✓ Xác nhận dữ liệu & Tiến hành Matching (Bước 3) →
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
