<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { useRequestStore } from '@/stores/request'
import { useModulesStore } from '@/stores/modules'

const requestStore = useRequestStore()
const modulesStore = useModulesStore()

const lbRef = ref<HTMLDivElement | null>(null)
const lightboxIndex = ref<number | null>(null)

watch(lightboxIndex, async (val) => {
  if (val !== null) { await nextTick(); lbRef.value?.focus() }
})

const hasImages = computed(() => requestStore.images.length > 0)
const isMulti = computed(() => requestStore.images.length > 1)
const lightboxSrc = computed(() =>
  lightboxIndex.value !== null && requestStore.images[lightboxIndex.value]
    ? requestStore.images[lightboxIndex.value].url : ''
)
const lightboxTitle = computed(() =>
  lightboxIndex.value !== null && requestStore.images[lightboxIndex.value]
    ? requestStore.images[lightboxIndex.value].title : ''
)

function openLightbox(idx: number) { lightboxIndex.value = idx }
function closeLightbox() { lightboxIndex.value = null }
function prevImage() {
  if (lightboxIndex.value === null || requestStore.images.length === 0) return
  lightboxIndex.value = (lightboxIndex.value - 1 + requestStore.images.length) % requestStore.images.length
}
function nextImage() {
  if (lightboxIndex.value === null || requestStore.images.length === 0) return
  lightboxIndex.value = (lightboxIndex.value + 1) % requestStore.images.length
}
function onLightboxKey(e: KeyboardEvent) {
  if (e.key === 'Escape') closeLightbox()
  if (e.key === 'ArrowLeft') prevImage()
  if (e.key === 'ArrowRight') nextImage()
}
</script>

<template>
  <div class="result-card">
    <div class="card-head">
      <h3>查询结果</h3>
      <span v-if="hasImages" class="result-badge">{{ isMulti ? `${requestStore.images.length} 张图片` : '图片' }}</span>
    </div>

    <!-- Empty -->
    <div v-if="!hasImages && requestStore.status !== 'loading'" class="empty-state">
      <svg class="empty-icon" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2">
        <rect x="3" y="3" width="18" height="18" rx="3" />
        <circle cx="8.5" cy="8.5" r="1.5" />
        <path d="M21 15l-5-5L5 21" />
      </svg>
      <p class="empty-title">{{ requestStore.status === 'error' ? '查询失败' : '等待查询' }}</p>
      <p class="empty-desc">
        {{ requestStore.status === 'error' ? requestStore.errorMessage || '请检查参数后重试' : '选择模块并填写参数，点击"开始查询"获取数据图片' }}
      </p>
    </div>

    <!-- Loading -->
    <div v-else-if="requestStore.isLoading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>正在生成图片</p>
    </div>

    <!-- Single image -->
    <div v-else-if="hasImages && !isMulti" class="single-image-wrap" @click="openLightbox(0)">
      <img :src="requestStore.images[0].url" :alt="requestStore.images[0].title" class="result-image" />
      <div class="image-overlay"><span>点击放大</span></div>
    </div>

    <!-- Gallery -->
    <div v-else-if="hasImages && isMulti" class="gallery-grid">
      <div v-for="(img, idx) in requestStore.images" :key="idx" class="gallery-item" @click="openLightbox(idx)">
        <img :src="img.url" :alt="img.title" class="gallery-image" />
        <div class="gallery-caption">
          <span>{{ img.title }}</span>
        </div>
      </div>
    </div>

    <!-- Lightbox -->
    <Teleport to="body">
      <div v-if="lightboxIndex !== null" class="lightbox-backdrop"
        @click="closeLightbox" @keydown="onLightboxKey" tabindex="0" ref="lbRef">
        <button class="lightbox-close" @click="closeLightbox">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 5l10 10M15 5l-10 10"/>
          </svg>
        </button>
        <button v-if="isMulti" class="lightbox-nav lightbox-prev" @click.stop="prevImage">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 4l-6 6 6 6"/>
          </svg>
        </button>
        <button v-if="isMulti" class="lightbox-nav lightbox-next" @click.stop="nextImage">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M8 4l6 6-6 6"/>
          </svg>
        </button>
        <img :src="lightboxSrc" :alt="lightboxTitle" class="lightbox-image" @click.stop />
        <div v-if="isMulti" class="lightbox-footer">
          <span>{{ lightboxTitle }}</span>
          <span class="lightbox-counter">{{ (lightboxIndex ?? 0) + 1 }} / {{ requestStore.images.length }}</span>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.result-card {
  background: var(--bg-surface);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-lg);
  padding: 28px;
  min-height: 400px;
}

.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 20px;
}

.card-head h3 {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.result-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 14px;
  border-radius: 999px;
  background: var(--accent-glow);
  border: 1px solid rgba(232, 146, 78, 0.25);
  color: var(--accent-light);
  font-size: 0.78rem;
  font-weight: 600;
}

/* Empty */
.empty-state {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 60px 20px; text-align: center;
}
.empty-icon { color: var(--text-muted); opacity: 0.35; margin-bottom: 16px; }
.empty-title { margin: 0 0 8px; font-size: 1.05rem; font-weight: 600; color: var(--text-secondary); }
.empty-desc { margin: 0; max-width: 360px; color: var(--text-muted); line-height: 1.6; font-size: 0.88rem; }

/* Loading */
.loading-state {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 80px 20px; gap: 16px;
  color: var(--text-muted);
}
.loading-spinner {
  width: 40px; height: 40px;
  border: 2px solid var(--line-strong);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Single */
.single-image-wrap {
  position: relative;
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: zoom-in;
  border: 1px solid var(--hairline);
  background: var(--bg-base);
}
.result-image { display: block; width: 100%; max-height: 700px; object-fit: contain; }
.image-overlay {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  background: rgba(0,0,0,0); color: transparent;
  font-weight: 600; font-size: 0.9rem;
  transition: all 200ms var(--ease-out);
  pointer-events: none;
}
.single-image-wrap:hover .image-overlay {
  background: rgba(0,0,0,0.4); color: #fff;
}

/* Gallery */
.gallery-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; }
.gallery-item {
  border-radius: var(--radius-md); overflow: hidden;
  cursor: pointer; border: 1px solid var(--hairline);
  background: var(--bg-base);
  transition: transform 160ms var(--ease-out), box-shadow 160ms var(--ease-out);
}
.gallery-item:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
.gallery-image { display: block; width: 100%; height: 200px; object-fit: cover; }
.gallery-caption {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 14px; background: var(--bg-surface-raised);
  font-size: 0.84rem; color: var(--text-secondary);
}

/* Lightbox */
.lightbox-backdrop {
  position: fixed; inset: 0; z-index: 9999;
  background: rgba(0,0,0,0.92);
  display: flex; align-items: center; justify-content: center;
  outline: none;
}
.lightbox-image {
  max-width: 92vw; max-height: 88vh;
  object-fit: contain; border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
}
.lightbox-close, .lightbox-nav {
  position: fixed;
  border: 1px solid var(--hairline);
  background: var(--bg-surface);
  color: var(--text-primary);
  border-radius: 50%;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: background 140ms var(--ease-out);
  backdrop-filter: blur(12px);
}
.lightbox-close:hover, .lightbox-nav:hover { background: var(--bg-surface-raised); }
.lightbox-close { top: 16px; right: 20px; width: 44px; height: 44px; }
.lightbox-nav { top: 50%; transform: translateY(-50%); width: 48px; height: 48px; }
.lightbox-prev { left: 20px; }
.lightbox-next { right: 20px; }
.lightbox-footer {
  position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
  display: flex; align-items: center; gap: 16px;
  padding: 8px 20px;
  background: var(--bg-surface); border: 1px solid var(--hairline);
  color: var(--text-secondary); border-radius: 999px;
  font-size: 0.84rem; backdrop-filter: blur(12px);
}
.lightbox-counter { opacity: 0.6; }

@media (max-width: 640px) {
  .result-card { padding: 18px; min-height: 280px; }
  .gallery-grid { grid-template-columns: 1fr; }
  .lightbox-nav { width: 38px; height: 38px; }
  .lightbox-prev { left: 8px; }
  .lightbox-next { right: 8px; }
}
</style>
