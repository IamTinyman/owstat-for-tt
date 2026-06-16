<script setup lang="ts">
import { ref, computed } from 'vue'
import type { ModuleSpec } from '@/types'

const props = defineProps<{
  modules: ModuleSpec[]
  featuredIds: string[]
  activeModuleId: string
}>()

defineEmits<{ navigate: [id: string] }>()

const expanded = ref(false)

const allModules = computed(() =>
  props.modules.filter(m => !props.featuredIds.includes(m.id))
)
</script>

<template>
  <div class="toolbox">
    <button type="button" class="toolbox-toggle" @click="expanded = !expanded">
      <span class="toggle-label">全部工具 · {{ allModules.length }} 个</span>
      <span class="toggle-arrow" :class="{ expanded }">
        <svg width="12" height="8" viewBox="0 0 12 8" fill="none">
          <path d="M1 1.5l5 5 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </span>
    </button>
    <div v-show="expanded" class="toolbox-grid">
      <button
        v-for="m in allModules"
        :key="m.id"
        type="button"
        class="tool-chip"
        :class="{ active: m.id === activeModuleId }"
        @click="$emit('navigate', m.id)"
      >
        {{ m.title }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.toolbox { margin-top: 0; }

.toolbox-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  border: 1px solid var(--hairline);
  border-radius: var(--radius-md);
  padding: 14px 18px;
  background: var(--bg-surface);
  color: var(--text-secondary);
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 140ms var(--ease-out);
}

.toolbox-toggle:hover { background: var(--bg-surface-raised); }

.toggle-arrow {
  transition: transform 200ms var(--ease-out);
  opacity: 0.5;
  display: flex;
}

.toggle-arrow.expanded { transform: rotate(180deg); }

.toolbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 8px;
  margin-top: 12px;
}

.tool-chip {
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  padding: 11px 14px;
  background: var(--bg-surface);
  color: var(--text-secondary);
  font-size: 0.84rem;
  text-align: center;
  cursor: pointer;
  transition: all 140ms var(--ease-out);
}

.tool-chip:hover {
  background: var(--bg-surface-raised);
  color: var(--text-primary);
  border-color: var(--line);
}

.tool-chip.active {
  background: var(--accent-glow);
  border-color: rgba(232,146,78,0.3);
  color: var(--accent-light);
}

@media (max-width: 640px) {
  .toolbox-grid { grid-template-columns: repeat(3, 1fr); }
}
</style>
