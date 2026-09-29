/**
 * API Service kết nối trực tiếp backend FastAPI (Tầng 1-4) của B.
 * Endpoint: POST /api/cv/upload
 */

export async function uploadCVApi(file, options = {}) {
  const { mode = 'llm', top_k = 10, location, level, industry_group } = options

  const formData = new FormData()
  formData.append('file', file)

  const params = new URLSearchParams()
  params.append('mode', mode)
  params.append('top_k', top_k.toString())
  if (location) params.append('location', location)
  if (level) params.append('level', level)
  if (industry_group) params.append('industry_group', industry_group)

  const url = `/api/cv/upload?${params.toString()}`

  try {
    const res = await fetch(url, {
      method: 'POST',
      body: formData,
    })

    if (!res.ok) {
      const errText = await res.text()
      throw new Error(`Backend trả lỗi ${res.status}: ${errText.slice(0, 200)}`)
    }

    const data = await res.json()
    return {
      success: true,
      data,
    }
  } catch (err) {
    console.error('Lỗi gọi API /api/cv/upload:', err)
    return {
      success: false,
      error: err.message,
    }
  }
}

/**
 * Tầng 6: Lịch sử phiên chấm THẬT từ DB (không mock).
 * Endpoint: GET /api/cv/history
 * @param {number} limit - số phiên gần nhất
 */
export async function getHistoryApi(limit = 5) {
  const url = `/api/cv/history?limit=${limit}`

  try {
    const res = await fetch(url)
    if (!res.ok) {
      const errText = await res.text()
      throw new Error(`Backend trả lỗi ${res.status}: ${errText.slice(0, 200)}`)
    }
    const data = await res.json()
    return { success: true, data }
  } catch (err) {
    console.error('Lỗi gọi API /api/cv/history:', err)
    return { success: false, error: err.message }
  }
}

/**
 * Tầng 5: Gợi ý cải thiện CV theo gap thật của 1 JD + delta score thật.
 * Endpoint: POST /api/cv/suggest-improvement
 * @param {Object} payload - { job_id, cv_skills, cv_experience, cv_text, accepted_skills, cv_id }
 * @param {boolean} useCache - true để lấy kết quả cache gần nhất (nếu có)
 */
export async function suggestImprovementApi(payload, useCache = false) {
  const params = new URLSearchParams()
  if (useCache) {
    params.append('use_cache', 'true')
  }

  const queryString = params.toString() ? `?${params.toString()}` : ''
  const url = `/api/cv/suggest-improvement${queryString}`

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })

    if (!res.ok) {
      const errText = await res.text()
      throw new Error(`Backend trả lỗi ${res.status}: ${errText.slice(0, 200)}`)
    }

    const data = await res.json()
    return {
      success: true,
      data,
    }
  } catch (err) {
    console.error('Lỗi gọi API /api/cv/suggest-improvement:', err)
    return {
      success: false,
      error: err.message,
    }
  }
}

