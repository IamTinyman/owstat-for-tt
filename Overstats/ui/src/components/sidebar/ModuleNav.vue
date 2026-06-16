<script setup lang="ts">
import { ref, computed } from 'vue'
import { useModulesStore } from '@/stores/modules'
import type { ModuleSpec } from '@/types'

const emit = defineEmits<{ navigate: [] }>()
const modulesStore = useModulesStore()

interface ModuleGroup {
  id: string
  label: string
  moduleIds: string[]
}

const groups: ModuleGroup[] = [
  {
    id: 'player',
    label: '玩家查询',
    moduleIds: [
      'dashen-profile', 'dashen-match', 'dashen-match-detail',
      'dashen-sameplay', 'dashen-sameplay-detail', 'dashen-rank-history',
      'dashen-quick-strength', 'dashen-competitive-strength',
    ],
  },
  {
    id: 'summary',
    label: '总结报告',
    moduleIds: ['dashen-summary-today', 'dashen-summary-yesterday', 'dashen-summary-week'],
  },
  {
    id: 'leaderboard',
    label: '排行榜与数据',
    moduleIds: ['dashen-rank-leaderboard', 'dashen-hero-leaderboard', 'ow-hero-pick-rate', 'ow-hero-perk'],
  },
  {
    id: 'more',
    label: '更多',
    moduleIds: ['ow-esports', 'ow-shop', 'patch-notes'],
  },
]

const moduleMap = computed<Record<string, ModuleSpec>>(() => {
  const map: Record<string, ModuleSpec> = {}
  for (const m of modulesStore.modules) { map[m.id] = m }
  return map
})

const expandedGroups = ref<Set<string>>(new Set(groups.map(g => g.id)))

function toggleGroup(groupId: string) {
  if (expandedGroups.value.has(groupId)) {
    expandedGroups.value.delete(groupId)
  } else {
    expandedGroups.value.add(groupId)
  }
}

function selectModule(id: string) {
  modulesStore.setActiveModule(id)
  emit('navigate')
}
</script>

<template>
  <nav class="module-nav">
    <div v-for="group in groups" :key="group.id" class="module-group">
      <button type="button" class="group-header" @click="toggleGroup(group.id)">
        <span class="group-label">{{ group.label }}</span>
        <span class="group-arrow" :class="{ expanded: expandedGroups.has(group.id) }">
          <svg width="10" height="6" viewBox="0 0 10 6" fill="none">
            <path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </span>
      </button>
      <div v-show="expandedGroups.has(group.id)" class="group-items">
        <button
          v-for="modId in group.moduleIds"
          :key="modId"
          type="button"
          class="module-btn"
          :class="{ active: modId === modulesStore.activeModuleId }"
          @click="selectModule(modId)"
        >
          <span class="module-text">
            {{ moduleMap[modId]?.title || modId }}
          </span>
        </button>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.module-nav {
  display: grid;
  gap: 2px;
  overflow-y: auto;
  flex: 1;
  padding-right: 4px;
}

.module-group { display: grid; gap: 1px; }

.group-header {
  display: flex;
  align-items: center;
  gap: 6px;
  width: 100%;
  border: none;
  border-radius: var(--radius-sm);
  padding: 9px 10px;
  background: transparent;
  color: var(--text-muted);
  font-size: 0.74rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  cursor: pointer;
  transition: color 140ms var(--ease-out);
}

.group-header:hover { color: var(--text-secondary); }

.group-label { flex: 1; text-align: left; }

.group-arrow {
  opacity: 0.4;
  transition: transform 180ms var(--ease-out);
  display: flex;
}
.group-arrow.expanded { transform: rotate(180deg); }

.group-items { display: grid; gap: 1px; padding: 3px 0 8px; }

.module-btn {
  display: block;
  width: 100%;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  padding: 8px 12px;
  background: transparent;
  color: var(--text-secondary);
  font-size: 0.84rem;
  text-align: left;
  cursor: pointer;
  transition: all 140ms var(--ease-out);
}

.module-btn:hover {
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-primary);
  transform: translateX(2px);
}

.module-btn.active {
  background: var(--accent-glow);
  border-color: rgba(232, 146, 78, 0.30);
  color: var(--accent-light);
  font-weight: 500;
}

.module-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}
</style>
