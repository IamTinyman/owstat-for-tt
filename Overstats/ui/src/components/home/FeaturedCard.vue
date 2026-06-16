<script setup lang="ts">
import type { ModuleSpec } from '@/types'
import { computed } from 'vue'

const props = defineProps<{
  module: ModuleSpec | null
  active: boolean
}>()

defineEmits<{ click: [] }>()

const cardTheme = computed(() => {
  const id = props.module?.id ?? ''
  const themes: Record<string, { gradient: string; icon: string }> = {
    'dashen-summary-today': {
      gradient: 'linear-gradient(135deg, #2d1f14 0%, #1d1418 100%)',
      icon: `<svg width="32" height="32" viewBox="0 0 32 32" fill="none"><circle cx="16" cy="16" r="6" stroke="#e8924e" stroke-width="2"/><path d="M16 4v3M16 25v3M4 16h3M25 16h3" stroke="#e8924e" stroke-width="1.5" stroke-linecap="round"/></svg>`,
    },
    'dashen-profile': {
      gradient: 'linear-gradient(135deg, #1a1d2e 0%, #14182a 100%)',
      icon: `<svg width="32" height="32" viewBox="0 0 32 32" fill="none"><circle cx="16" cy="11" r="5" stroke="#8b9cf7" stroke-width="2"/><path d="M6 28c0-5.5 4.5-10 10-10s10 4.5 10 10" stroke="#8b9cf7" stroke-width="2" stroke-linecap="round"/></svg>`,
    },
    'dashen-match': {
      gradient: 'linear-gradient(135deg, #14202a 0%, #111d1e 100%)',
      icon: `<svg width="32" height="32" viewBox="0 0 32 32" fill="none"><rect x="4" y="8" width="10" height="16" rx="2" stroke="#5ec4a0" stroke-width="2"/><rect x="18" y="8" width="10" height="16" rx="2" stroke="#5ec4a0" stroke-width="2"/><line x1="14" y1="14" x2="18" y2="14" stroke="#5ec4a0" stroke-width="2"/></svg>`,
    },
    'dashen-rank-history': {
      gradient: 'linear-gradient(135deg, #201e1a 0%, #1a1914 100%)',
      icon: `<svg width="32" height="32" viewBox="0 0 32 32" fill="none"><polyline points="4,24 12,14 18,18 28,6" stroke="#d4a853" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="28" cy="6" r="2" fill="#d4a853"/></svg>`,
    },
  }
  return themes[id] || themes['dashen-profile'] || { gradient: 'linear-gradient(135deg, #1a1d2e, #14182a)', icon: '' }
})
</script>

<template>
  <button
    v-if="module"
    type="button"
    class="card"
    @click="$emit('click')"
  >
    <div class="card-bg" :style="{ background: cardTheme.gradient }"></div>
    <div class="card-content">
      <div class="card-icon" v-html="cardTheme.icon"></div>
      <div class="card-text">
        <strong>{{ module.title }}</strong>
        <span>{{ module.description }}</span>
      </div>
      <div class="card-arrow">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M6 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
    </div>
  </button>
</template>

<style scoped>
.card {
  position: relative;
  border: 1px solid var(--hairline);
  border-radius: var(--radius-lg);
  padding: 0;
  cursor: pointer;
  text-align: left;
  overflow: hidden;
  transition: transform 200ms var(--ease-out), box-shadow 200ms var(--ease-out), border-color 200ms var(--ease-out);
  background: transparent;
  color: inherit;
  width: 100%;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
  border-color: var(--line);
}

.card:active { transform: translateY(-1px); }

.card-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
  opacity: 0.85;
  transition: opacity 200ms var(--ease-out);
}

.card:hover .card-bg { opacity: 1; }

.card-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 28px 24px;
}

.card-icon {
  flex-shrink: 0;
  width: 48px; height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-text {
  flex: 1;
  display: grid;
  gap: 4px;
  min-width: 0;
}

.card-text strong {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
}

.card-text span {
  font-size: 0.82rem;
  color: var(--text-secondary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-arrow {
  flex-shrink: 0;
  color: var(--text-muted);
  opacity: 0;
  transform: translateX(-4px);
  transition: all 200ms var(--ease-out);
}

.card:hover .card-arrow {
  opacity: 1;
  transform: translateX(0);
}

@media (max-width: 640px) {
  .card-content { padding: 22px 18px; }
}
</style>
