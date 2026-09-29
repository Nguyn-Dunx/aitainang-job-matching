import rawJds from '@data/processed/jds.json'

/**
 * Service nạp 450 JD thật từ data/processed/jds.json.
 * Chuẩn hóa các trường hiển thị cho MatchingPage và ResultsPage.
 */
export const ALL_REAL_JDS = rawJds.map((jd, idx) => {
  const metadata = jd.metadata || {}

  // Parse benefits thành danh sách ngắn gọn nếu có
  let benefitsList = []
  if (metadata.benefits && typeof metadata.benefits === 'string') {
    // Tách theo dấu chấm hoặc xuống dòng, lấy 2-3 ý đầu
    benefitsList = metadata.benefits
      .split(/[.\n;•]+/)
      .map((b) => b.trim())
      .filter((b) => b.length > 5 && b.length < 50)
      .slice(0, 3)
  }
  if (benefitsList.length === 0) {
    benefitsList = ['Chế độ đãi ngộ theo năng lực', 'Môi trường làm việc chuyên nghiệp']
  }

  // Tạo mock score (trong lúc chờ API B) dựa trên độ ưu tiên và vị trí
  // Điểm số dao động 60 - 92 điểm
  const baseScore = 65 + ((idx * 7) % 25)

  return {
    id: idx + 1,
    source_id: metadata.source_id || idx + 1,
    title: jd.title || 'Vị trí IT',
    company: metadata.company_name || 'Đơn vị tuyển dụng',
    location: jd.location_normalized || jd.location || 'Toàn quốc',
    raw_location: jd.location,
    level: jd.level_normalized || jd.level || 'Fresher / Junior',
    industry_group: jd.industry_group || 'IT General',
    salary: metadata.salary || 'Thỏa thuận',
    job_type: metadata.job_type && metadata.job_type !== 'Chưa xác định' ? metadata.job_type : 'Toàn thời gian',
    benefits: benefitsList,
    raw_benefits: metadata.benefits,
    requirements: jd.requirements || '',
    responsibilities: jd.responsibilities || '',
    education_level: metadata.education_level || 'Đại học / Cao đẳng',
    score: baseScore,
    is_mock: true, // Cờ nhận biết điểm số đang là demo mock
  }
})

/**
 * Lấy danh sách thống kê số lượng theo nhóm ngành
 */
export function getIndustryCounts() {
  const counts = {
    all: ALL_REAL_JDS.length,
    'Data/AI/ML': 0,
    'Software Engineering': 0,
    'IT General': 0,
    'Infra/DevOps': 0,
    'Product/Project Mgmt': 0,
    'Testing/QA': 0,
    'Game Dev': 0,
    'Security': 0,
  }

  ALL_REAL_JDS.forEach((j) => {
    if (counts[j.industry_group] !== undefined) {
      counts[j.industry_group]++
    }
  })

  return counts
}

/**
 * Lấy JD theo ID
 */
export function getJobById(id) {
  const numId = parseInt(id, 10)
  return ALL_REAL_JDS.find((j) => j.id === numId) || ALL_REAL_JDS[0]
}
