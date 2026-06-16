<script setup lang="ts">
import { ref, provide } from 'vue'
import { useModulesStore } from '@/stores/modules'
import { useRequestStore } from '@/stores/request'
import HomeView from './home/HomeView.vue'
import QueryView from './query/QueryView.vue'

const modulesStore = useModulesStore()
const requestStore = useRequestStore()

type View = 'home' | 'query'
const currentView = ref<View>('home')
provide('currentView', currentView)

function navigateToModule(id: string) {
  modulesStore.setActiveModule(id)
  requestStore.resetForm()
  currentView.value = 'query'
}

function goHome() {
  currentView.value = 'home'
}
</script>

<template>
  <div v-if="modulesStore.loading" class="shell-state">
    <div class="state-spinner"></div>
    <p>正在加载模块配置</p>
  </div>

  <div v-else-if="modulesStore.error" class="shell-state">
    <p class="state-error">{{ modulesStore.error }}</p>
    <button class="retry-btn" @click="modulesStore.loadModules()">重新加载</button>
  </div>

  <template v-else>
    <Transition name="view-slide" mode="out-in">
      <HomeView
        v-if="currentView === 'home'"
        key="home"
        :modules="modulesStore.modules"
        :active-module-id="modulesStore.activeModuleId"
        @navigate="navigateToModule"
      />
      <QueryView
        v-else
        key="query"
        @back="goHome"
      />
    </Transition>
  </template>
</template>

<style scoped>
.shell-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  gap: 16px;
  color: var(--text-secondary);
  background: var(--bg-base);
}

.state-spinner {
  width: 36px; height: 36px;
  border: 2px solid var(--line-strong);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.state-error { color: var(--danger); font-weight: 500; }

.retry-btn {
  border: 1px solid var(--accent);
  border-radius: 999px;
  padding: 10px 28px;
  background: var(--bg-surface);
  color: var(--accent);
  font-weight: 600;
  cursor: pointer;
}

.retry-btn:hover { background: var(--accent-glow); }

.view-slide-enter-active,
.view-slide-leave-active {
  transition: opacity 240ms var(--ease-out), transform 240ms var(--ease-out);
}

.view-slide-enter-from {
  opacity: 0;
  transform: translateY(12px);
}

.view-slide-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}
</style>
