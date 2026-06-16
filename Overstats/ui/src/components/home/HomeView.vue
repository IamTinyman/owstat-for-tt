<script setup lang="ts">
import type { ModuleSpec } from '@/types'
import FeaturedCard from './FeaturedCard.vue'
import ToolboxPanel from './ToolboxPanel.vue'

defineProps<{
  modules: ModuleSpec[]
  activeModuleId: string
}>()

defineEmits<{ navigate: [id: string] }>()

const FEATURED_IDS = [
  'dashen-summary-today',
  'dashen-profile',
  'dashen-match',
  'dashen-rank-history',
]

const featuredIcons: Record<string, string> = {
  'dashen-summary-today': 'sun',
  'dashen-profile': 'user',
  'dashen-match': 'gamepad',
  'dashen-rank-history': 'chart-line',
}
</script>

<template>
  <div class="home">
    <!-- Hero -->
    <section class="hero">
      <div class="hero-glow"></div>
      <h1 class="hero-title">潼潼宝宝的数据小站</h1>
      <p class="hero-sub">打开就能看到你的守望数据，Tinyman 为你打造</p>
    </section>

    <!-- Featured Cards -->
    <section class="featured">
      <h2 class="section-label">常用查询</h2>
      <div class="featured-grid">
        <FeaturedCard
          v-for="id in FEATURED_IDS"
          :key="id"
          :module="modules.find(m => m.id === id) ?? null"
          :active="id === activeModuleId"
          @click="$emit('navigate', id)"
        />
      </div>
    </section>

    <!-- Toolbox -->
    <section class="toolbox-section">
      <ToolboxPanel
        :modules="modules"
        :featured-ids="FEATURED_IDS"
        :active-module-id="activeModuleId"
        @navigate="id => $emit('navigate', id)"
      />
    </section>

    <footer class="home-footer">
      <p>Overstats · Overwatch Data</p>
    </footer>
  </div>
</template>

<style scoped>
.home {
  min-height: 100vh;
  background: var(--bg-base);
  padding: 60px 24px 40px;
  max-width: 960px;
  margin: 0 auto;
}

/* ── Hero ── */
.hero {
  position: relative;
  text-align: center;
  padding: 56px 20px 48px;
  margin-bottom: 44px;
}

.hero-glow {
  position: absolute;
  top: -40px; left: 50%; transform: translateX(-50%);
  width: 500px; height: 200px;
  background: radial-gradient(ellipse, rgba(232,146,78,0.10) 0%, transparent 70%);
  pointer-events: none;
}

.hero-title {
  margin: 0;
  font-size: clamp(1.6rem, 4vw, 2.4rem);
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  line-height: 1.2;
}

.hero-sub {
  margin: 14px 0 0;
  font-size: 1.05rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

/* ── Section ── */
.section-label {
  margin: 0 0 18px;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* ── Featured Grid ── */
.featured { margin-bottom: 48px; }

.featured-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

/* ── Toolbox ── */
.toolbox-section { margin-bottom: 48px; }

/* ── Footer ── */
.home-footer {
  text-align: center;
  padding: 32px 0;
  border-top: 1px solid var(--hairline);
}

.home-footer p {
  margin: 0;
  font-size: 0.78rem;
  color: var(--text-muted);
}

@media (max-width: 640px) {
  .home { padding: 40px 14px 24px; }
  .hero { padding: 32px 16px 28px; margin-bottom: 28px; }
  .featured-grid { grid-template-columns: 1fr; }
}
</style>
