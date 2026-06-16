<script setup lang="ts">
defineProps<{
  title: string
  description: string
}>()

defineEmits<{ back: [] }>()
</script>

<template>
  <header class="topbar">
    <button type="button" class="back-btn" @click="$emit('back')">
      <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
        <path d="M11 4L6 9l5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
    <div class="topbar-info">
      <h2 class="topbar-title">{{ title }}</h2>
      <p class="topbar-desc">{{ description }}</p>
    </div>
  </header>
</template>

<style scoped>
.topbar {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--hairline);
  background: var(--bg-surface);
  height: 72px;
}

.back-btn {
  flex-shrink: 0;
  width: 38px; height: 38px;
  border: 1px solid var(--hairline);
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 140ms var(--ease-out);
}

.back-btn:hover {
  background: var(--bg-surface-raised);
  color: var(--text-primary);
}

.topbar-info {
  flex: 1;
  min-width: 0;
}

.topbar-title {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.topbar-desc {
  margin: 2px 0 0;
  font-size: 0.8rem;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

@media (max-width: 640px) {
  .topbar { padding: 12px 14px; height: 60px; }
  .topbar-desc { display: none; }
}
</style>
