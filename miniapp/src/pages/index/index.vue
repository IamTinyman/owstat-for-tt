<template>
  <view class="home">
    <!-- Hero -->
    <view class="hero">
      <text class="hero-title">潼潼宝宝的数据小站</text>
      <text class="hero-sub">打开就能看到你的守望数据，Tinyman 为你打造</text>
    </view>

    <!-- Featured -->
    <view class="section">
      <text class="section-label">常用查询</text>
      <view class="featured-grid">
        <view
          v-for="mod in featuredModules"
          :key="mod.id"
          class="featured-card"
          :style="{ background: cardBg(mod.id) }"
          @tap="goModule(mod.id)"
        >
          <text class="card-icon">{{ cardEmoji(mod.id) }}</text>
          <view class="card-text">
            <text class="card-title">{{ mod.title }}</text>
            <text class="card-desc">{{ mod.description }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- Toolbox -->
    <view class="section">
      <view class="toolbox-toggle" @tap="expanded = !expanded">
        <text class="toggle-label">全部工具 · {{ otherModules.length }} 个</text>
        <text class="toggle-arrow" :class="{ expanded }">▾</text>
      </view>
      <view v-if="expanded" class="toolbox-grid">
        <view
          v-for="mod in otherModules"
          :key="mod.id"
          class="tool-chip"
          @tap="goModule(mod.id)"
        >
          <text>{{ mod.title }}</text>
        </view>
      </view>
    </view>

    <!-- State -->
    <view v-if="modulesStore.loading" class="state-wrap">
      <text>加载中...</text>
    </view>
    <view v-else-if="modulesStore.error" class="state-wrap">
      <text class="state-error">{{ modulesStore.error }}</text>
      <button class="retry-btn" @tap="modulesStore.loadModules()">重试</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useModulesStore } from '@/stores/modules'
import type { ModuleSpec } from '@/types'

const modulesStore = useModulesStore()
const expanded = ref(false)

const FEATURED_IDS = ['dashen-summary-today', 'dashen-profile', 'dashen-match', 'dashen-rank-history']

const featuredModules = computed(() =>
  FEATURED_IDS.map(id => modulesStore.modules.find(m => m.id === id)).filter(Boolean) as ModuleSpec[]
)

const otherModules = computed(() =>
  modulesStore.modules.filter(m => !FEATURED_IDS.includes(m.id))
)

function cardBg(id: string): string {
  const map: Record<string, string> = {
    'dashen-summary-today': 'linear-gradient(135deg, #2d1f14, #1d1418)',
    'dashen-profile': 'linear-gradient(135deg, #1a1d2e, #14182a)',
    'dashen-match': 'linear-gradient(135deg, #14202a, #111d1e)',
    'dashen-rank-history': 'linear-gradient(135deg, #201e1a, #1a1914)',
  }
  return map[id] || map['dashen-profile']
}

function cardEmoji(id: string): string {
  const map: Record<string, string> = { 'dashen-summary-today': '📅', 'dashen-profile': '👤', 'dashen-match': '🎮', 'dashen-rank-history': '📈' }
  return map[id] || '📌'
}

function goModule(id: string) {
  modulesStore.setActiveModule(id)
  uni.navigateTo({ url: `/pages/module/index?moduleId=${id}` })
}

onMounted(async () => {
  if (modulesStore.modules.length === 0) {
    await modulesStore.loadModules()
  }
})
</script>

<style lang="scss" scoped>
$bg-base: #131820;
$bg-surface: #19202b;
$text-primary: #f0ede6;
$text-secondary: #a8a39a;
$text-muted: #6b6560;
$accent: #e8924e;
$accent-light: #f0b878;
$hairline: rgba(255,255,255,0.06);
$line: rgba(255,255,255,0.08);

.home {
  min-height: 100vh;
  background: $bg-base;
  padding: 48rpx 28rpx 48rpx;
}

.hero {
  text-align: center;
  padding: 80rpx 32rpx 64rpx;
}

.hero-title {
  display: block;
  font-size: 52rpx;
  font-weight: 800;
  color: $text-primary;
  letter-spacing: -2rpx;
}

.hero-sub {
  display: block;
  margin-top: 20rpx;
  font-size: 30rpx;
  color: $text-secondary;
}

.section { margin-bottom: 48rpx; }

.section-label {
  display: block;
  font-size: 24rpx;
  font-weight: 600;
  color: $text-muted;
  text-transform: uppercase;
  letter-spacing: 4rpx;
  margin-bottom: 24rpx;
}

.featured-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16rpx;
}

.featured-card {
  border: 1px solid $hairline;
  border-radius: 32rpx;
  padding: 36rpx 28rpx;
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  transition: transform 0.15s ease;

  &:active { transform: scale(0.97); }
}

.card-icon { font-size: 48rpx; }

.card-title {
  display: block;
  font-size: 30rpx;
  font-weight: 700;
  color: $text-primary;
}

.card-desc {
  display: block;
  margin-top: 4rpx;
  font-size: 24rpx;
  color: $text-secondary;
  line-height: 1.4;
}

.toolbox-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 28rpx 32rpx;
  background: $bg-surface;
  border: 1px solid $hairline;
  border-radius: 20rpx;
}

.toggle-label { font-size: 28rpx; color: $text-secondary; }

.toggle-arrow {
  font-size: 24rpx; color: $text-muted;
  transition: transform 0.2s ease;
  &.expanded { transform: rotate(180deg); }
}

.toolbox-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12rpx;
  margin-top: 16rpx;
}

.tool-chip {
  padding: 24rpx 12rpx;
  background: $bg-surface;
  border: 1px solid $hairline;
  border-radius: 12rpx;
  text-align: center;
  font-size: 26rpx;
  color: $text-secondary;

  &:active { background: rgba(255,255,255,0.05); }
}

.state-wrap {
  text-align: center;
  padding: 60rpx 0;
  color: $text-muted;
}

.state-error { color: #dc5a4a; }

.retry-btn {
  margin-top: 24rpx;
  border: 1px solid $accent;
  border-radius: 20rpx;
  padding: 16rpx 40rpx;
  background: transparent;
  color: $accent;
  font-size: 28rpx;

  &::after { border: none; }
}
</style>
