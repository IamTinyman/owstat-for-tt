import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fetchModuleRegistry } from '@/api/bootstrap'
import type { ModuleSpec } from '@/types'

const REPLY_BUNDLE_MODULES = ['dashen-match-detail', 'dashen-sameplay-detail']

export const useModulesStore = defineStore('modules', () => {
  const modules = ref<ModuleSpec[]>([])
  const activeModuleId = ref<string>('')
  const loading = ref(false)
  const error = ref<string | null>(null)

  const activeModule = computed<ModuleSpec | null>(() =>
    modules.value.find((m) => m.id === activeModuleId.value) || modules.value[0] || null
  )

  const isReplyBundle = computed(() =>
    activeModule.value ? REPLY_BUNDLE_MODULES.includes(activeModule.value.id) : false
  )

  function queryEndpoint(): string {
    if (!activeModule.value) return ''
    if (REPLY_BUNDLE_MODULES.includes(activeModule.value.id)) {
      return activeModule.value.json_endpoint
    }
    return activeModule.value.image_endpoint
  }

  async function loadModules() {
    loading.value = true
    error.value = null
    try {
      const data = await fetchModuleRegistry()
      modules.value = data.modules || []
      if (data.default_module_id && modules.value.some((m) => m.id === data.default_module_id)) {
        activeModuleId.value = data.default_module_id
      } else if (modules.value.length > 0) {
        activeModuleId.value = modules.value[0].id
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err)
      error.value = `模块注册表加载失败: ${msg}`
    } finally {
      loading.value = false
    }
  }

  function setActiveModule(id: string) {
    if (modules.value.some((m) => m.id === id)) {
      activeModuleId.value = id
    }
  }

  return { modules, activeModuleId, loading, error, activeModule, isReplyBundle, queryEndpoint, loadModules, setActiveModule }
})
