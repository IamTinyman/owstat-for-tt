import type { BootstrapPayload, ImageResultItem } from '@/types'

const API_BASE = 'https://jetson.owstatfortt.xyz'

function request(opts: UniApp.RequestOptions): Promise<UniApp.RequestSuccessCallbackResult> {
  return new Promise((resolve, reject) => {
    uni.request({
      ...opts,
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res)
        } else {
          reject(new Error(`HTTP ${res.statusCode}`))
        }
      },
      fail: (err) => reject(new Error(err.errMsg || 'network error')),
    })
  })
}

export async function fetchBootstrap(): Promise<BootstrapPayload> {
  const res = await request({
    url: `${API_BASE}/api/v2/ui/bootstrap`,
    method: 'GET',
    timeout: 15000,
  })
  return res.data as BootstrapPayload
}

export async function fetchModuleImage(
  endpoint: string,
  payload: Record<string, unknown>
): Promise<ImageResultItem[]> {
  const res = await request({
    url: `${API_BASE}${endpoint}`,
    method: 'POST',
    header: { 'Content-Type': 'application/json' },
    data: payload,
    responseType: 'arraybuffer',
    timeout: 120000,
  })

  const arrayBuffer = res.data as ArrayBuffer
  const base64 = uni.arrayBufferToBase64(arrayBuffer)
  const mediaType = (res.header?.['content-type'] || 'image/png') as string
  const url = `data:${mediaType};base64,${base64}`

  return [{ url, title: '查询结果' }]
}
