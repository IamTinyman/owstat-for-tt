<script setup lang="ts">
import { ref } from 'vue'
import { useModulesStore } from '@/stores/modules'
import AppSidebar from './AppSidebar.vue'
import AppWorkspace from './AppWorkspace.vue'

const modulesStore = useModulesStore()
const sidebarOpen = ref(false)

function closeSidebar() {
  sidebarOpen.value = false
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

  <div v-else class="app-shell">
    <button
      class="hamburger"
      @click="sidebarOpen = !sidebarOpen"
      aria-label="切换菜单"
    >
      <span></span><span></span><span></span>
    </button>

    <div class="overlay" :class="{ open: sidebarOpen }" @click="closeSidebar"></div>
    <div class="sidebar-wrap" :class="{ open: sidebarOpen }">
      <AppSidebar @navigate="closeSidebar" />
    </div>
    <AppWorkspace />
  </div>
</template>

<style scoped>
.app-shell {
  display: grid;
  grid-template-columns: 272px minmax(0, 1fr);
  min-height: 100vh;
  position: relative;
}

/* ── hamburger ── */
.hamburger {
  display: none;
  position: fixed;
  top: 14px; left: 14px;
  z-index: 1100;
  width: 42px; height: 42px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
  backdrop-filter: blur(12px);
  cursor: pointer;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 0;
}

.hamburger span {
  display: block;
  width: 18px; height: 2px;
  background: var(--text-secondary);
  border-radius: 1px;
}

/* ── overlay ── */
.overlay {
  display: none;
  position: fixed; inset: 0;
  z-index: 1050;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0; pointer-events: none;
  transition: opacity 220ms var(--ease-out);
}
.overlay.open { opacity: 1; pointer-events: auto; }

/* ── sidebar ── */
.sidebar-wrap { position: relative; z-index: 1; }

/* ── states ── */
.shell-state {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  min-height: 100vh; gap: 16px;
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
  transition: background 140ms var(--ease-out);
}
.retry-btn:hover { background: var(--accent-glow); }

@media (max-width: 800px) {
  .app-shell { grid-template-columns: 1fr; }
  .hamburger { display: flex; }
  .overlay { display: block; }

  .sidebar-wrap {
    position: fixed; top: 0; left: 0; bottom: 0;
    z-index: 1060;
    width: 276px; max-width: 85vw;
    transform: translateX(-100%);
    transition: transform 240ms var(--ease-out);
    overflow-y: auto;
  }
  .sidebar-wrap.open { transform: translateX(0); }
}
</style>
