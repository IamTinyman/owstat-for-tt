import apiClient from './client'
import type { ReplyItem } from '@/types'
import type { ImageResult } from '@/stores/request'

export interface RequestOutcome {
  images: ImageResult[]
}

function base64ToBlob(base64Text: string, mediaType?: string): Blob {
  const binary = atob(String(base64Text || ''))
  const bytes = new Uint8Array(binary.length)
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i)
  }
  return new Blob([bytes], { type: mediaType || 'image/png' })
}

function blobToUrl(blob: Blob): string {
  return URL.createObjectURL(blob)
}

function extractImageReplies(replies: ReplyItem[]): { base64: string; mediaType: string }[] {
  return replies
    .filter((r) => r && r.type === 'image' && r.base64)
    .map((r) => ({ base64: r.base64!, mediaType: r.media_type || 'image/png' }))
}

export async function sendModuleRequest(
  endpoint: string,
  payload: Record<string, unknown>,
  isReplyBundle: boolean
): Promise<RequestOutcome> {
  const response = await apiClient.post(endpoint, payload, {
    responseType: 'arraybuffer',
  })

  const contentType = String(response.headers['content-type'] || '').toLowerCase()

  // Direct image response
  if (contentType.startsWith('image/')) {
    const blob = new Blob([response.data], { type: contentType })
    return { images: [{ url: blobToUrl(blob), title: '查询结果' }] }
  }

  // JSON response - extract base64 images (reply bundles)
  const decoder = new TextDecoder('utf-8')
  const textBody = decoder.decode(response.data)
  let parsed: { replies?: ReplyItem[] } = {}
  try { parsed = textBody ? JSON.parse(textBody) : {} } catch { /* ignore */ }

  if (isReplyBundle && parsed.replies?.length) {
    const imgReplies = extractImageReplies(parsed.replies)
    if (imgReplies.length > 0) {
      const titles = imgReplies.length >= 3
        ? ['主面板', '详细信息', 'AI 总结']
        : imgReplies.length === 2
          ? ['主面板', '详细信息']
          : ['查询结果']
      const images: ImageResult[] = imgReplies.map((r, i) => ({
        url: blobToUrl(base64ToBlob(r.base64, r.mediaType)),
        title: titles[i] || `图片 ${i + 1}`,
      }))
      return { images }
    }
  }

  return { images: [] }
}
