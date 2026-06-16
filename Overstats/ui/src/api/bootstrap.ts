import apiClient from './client'
import type { BootstrapPayload } from '@/types'

export async function fetchModuleRegistry(): Promise<BootstrapPayload> {
  const { data } = await apiClient.get<BootstrapPayload>('/api/v2/ui/bootstrap')
  return data
}
