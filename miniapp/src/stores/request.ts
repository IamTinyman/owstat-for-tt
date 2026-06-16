import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fetchModuleImage } from '@/api/client'
import { useModulesStore } from './modules'
import type { RequestStatus, ImageResultItem } from '@/types'

export const useRequestStore = defineStore('request', () => {
  const modulesStore = useModulesStore()

  const targetType = ref<'bnet_id' | 'customer_token'>('bnet_id')
  const targetValue = ref('')
  const status = ref<RequestStatus>('idle')
  const statusMessage = ref('就绪')
  const images = ref<ImageResultItem[]>([])
  const errorMessage = ref('')
  const fieldValues = ref<Record<string, string | boolean>>({})

  const isLoading = computed(() => status.value === 'loading')

  function resetForm() {
    status.value = 'idle'
    statusMessage.value = '就绪'
    images.value = []
    errorMessage.value = ''
    fieldValues.value = {}
    const mod = modulesStore.activeModule
    if (mod) {
      targetType.value = (mod.default_target_key || 'bnet_id') as 'bnet_id' | 'customer_token'
      targetValue.value = ''
    }
  }

  async function submitRequest(payload: Record<string, unknown>) {
    const mod = modulesStore.activeModule
    if (!mod) return

    const endpoint = modulesStore.queryEndpoint()
    if (!endpoint) return

    status.value = 'loading'
    statusMessage.value = '查询中...'
    errorMessage.value = ''
    images.value = []

    try {
      const result = await fetchModuleImage(endpoint, payload)
      if (result.length > 0) {
        images.value = result
        status.value = 'success'
        statusMessage.value = '查询完成'
      } else {
        status.value = 'error'
        errorMessage.value = '未返回图片'
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err)
      errorMessage.value = msg
      statusMessage.value = '请求失败'
      status.value = 'error'
    }
  }

  return {
    targetType, targetValue, status, statusMessage, images, errorMessage,
    fieldValues, isLoading,
    resetForm, submitRequest,
  }
})
