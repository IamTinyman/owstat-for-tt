import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { sendModuleRequest } from '@/api/request'
import { useModulesStore } from './modules'
import type { RequestStatus } from '@/types'

export interface ImageResult {
  url: string
  title: string
}

export interface ModuleSession {
  targetType: 'bnet_id' | 'customer_token'
  targetValue: string
  status: RequestStatus
  statusMessage: string
  images: ImageResult[]
  errorMessage: string
  fieldValues: Record<string, string | boolean>
}

function createSession(defaultKey: string): ModuleSession {
  return {
    targetType: (defaultKey || 'bnet_id') as 'bnet_id' | 'customer_token',
    targetValue: '',
    status: 'idle',
    statusMessage: '就绪',
    images: [],
    errorMessage: '',
    fieldValues: {},
  }
}

export const useRequestStore = defineStore('request', () => {
  const sessions = ref<Record<string, ModuleSession>>({})
  const modulesStore = useModulesStore()

  function getSession(): ModuleSession {
    const id = modulesStore.activeModuleId
    if (!id) return createSession('bnet_id')
    if (!sessions.value[id]) {
      sessions.value[id] = createSession(
        modulesStore.activeModule?.default_target_key || 'bnet_id'
      )
    }
    return sessions.value[id]
  }

  /** Direct access to a module's session (for sidebar indicators) */
  function sessionFor(moduleId: string): ModuleSession | undefined {
    return sessions.value[moduleId]
  }

  // Reactive proxies to current module's session
  const targetType = computed({
    get: () => getSession().targetType,
    set: (v) => { getSession().targetType = v },
  })
  const targetValue = computed({
    get: () => getSession().targetValue,
    set: (v) => { getSession().targetValue = v },
  })
  const status = computed(() => getSession().status)
  const statusMessage = computed({
    get: () => getSession().statusMessage,
    set: (v) => { getSession().statusMessage = v },
  })
  const images = computed({
    get: () => getSession().images,
    set: (v) => { getSession().images = v },
  })
  const errorMessage = computed({
    get: () => getSession().errorMessage,
    set: (v) => { getSession().errorMessage = v },
  })
  const fieldValues = computed({
    get: () => getSession().fieldValues,
    set: (v) => { getSession().fieldValues = v },
  })

  const isLoading = computed(() => status.value === 'loading')

  function resetForm() {
    const s = getSession()
    s.status = 'idle'
    s.statusMessage = '就绪'
    s.images = []
    s.errorMessage = ''
    s.fieldValues = {}
    const mod = modulesStore.activeModule
    if (mod) {
      s.targetType = (mod.default_target_key || 'bnet_id') as 'bnet_id' | 'customer_token'
      s.targetValue = ''
    }
  }

  function cleanupImages(list: ImageResult[]) {
    for (const img of list) {
      try { URL.revokeObjectURL(img.url) } catch { /* ignore */ }
    }
  }

  async function submitRequest(payload: Record<string, unknown>) {
    const mod = modulesStore.activeModule
    if (!mod) return

    const endpoint = modulesStore.queryEndpoint()
    if (!endpoint) return

    const session = getSession()
    const moduleId = modulesStore.activeModuleId

    session.status = 'loading'
    session.statusMessage = '查询中...'
    session.errorMessage = ''
    cleanupImages(session.images)
    session.images = []

    try {
      const result = await sendModuleRequest(endpoint, payload, modulesStore.isReplyBundle)

      // Ensure we still write to the same session even if module was switched mid-query
      const targetSession = sessions.value[moduleId]
      if (!targetSession) return

      if (result.images.length > 0) {
        targetSession.images = result.images
        targetSession.status = 'success'
        targetSession.statusMessage = result.images.length > 1
          ? `共 ${result.images.length} 张图片`
          : '查询完成'
      } else {
        targetSession.status = 'error'
        targetSession.statusMessage = '未返回图片'
        targetSession.errorMessage = '服务器未返回图片数据，请检查查询参数。'
      }
    } catch (err: unknown) {
      const targetSession = sessions.value[moduleId]
      if (!targetSession) return
      cleanupImages(targetSession.images)
      targetSession.images = []
      const msg = err instanceof Error ? err.message : String(err)
      targetSession.errorMessage = msg
      targetSession.statusMessage = '网络请求失败'
      targetSession.status = 'error'
    }
  }

  return {
    sessions,
    targetType, targetValue, status, statusMessage, images, errorMessage,
    fieldValues, isLoading,
    getSession, sessionFor,
    resetForm, cleanupImages, submitRequest,
  }
})
