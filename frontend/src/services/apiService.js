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
