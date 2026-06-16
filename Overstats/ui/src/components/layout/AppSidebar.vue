<script setup lang="ts">
import SidebarHeader from '@/components/sidebar/SidebarHeader.vue'
import ModuleNav from '@/components/sidebar/ModuleNav.vue'

defineEmits<{ navigate: [] }>()
</script>

<template>
  <aside class="sidebar">
    <SidebarHeader />
    <ModuleNav @navigate="$emit('navigate')" />
    <footer class="sidebar-footer">
      <span>Overstats</span>
    </footer>
  </aside>
</template>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 28px 20px 18px;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--hairline);
  min-height: 100vh;
}

.sidebar-footer {
  padding-top: 14px;
  border-top: 1px solid var(--hairline);
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--text-muted);
  letter-spacing: 0.04em;
}

@media (max-width: 640px) {
  .sidebar {
    padding: 18px 14px;
    min-height: auto;
  }
}
</style>
