<script setup lang="ts">
import ModuleHero from '@/components/workspace/ModuleHero.vue'
import QueryForm from '@/components/workspace/QueryForm.vue'
import ImageResult from '@/components/preview/ImageResult.vue'
</script>

<template>
  <main class="workspace">
    <div class="mobile-header">
      <h1 class="mobile-title">数据查询</h1>
      <p class="mobile-desc">这是Tinyman（小笨蛋）给潼潼宝宝（小坏蛋）做的独享查询网站</p>
    </div>
    <ModuleHero />
    <section class="content-grid">
      <QueryForm />
      <ImageResult />
    </section>
  </main>
</template>

<style scoped>
.workspace {
  display: grid;
  gap: 24px;
  padding: 28px;
  background:
    radial-gradient(ellipse 70% 50% at 20% 0%, rgba(232, 146, 78, 0.04), transparent),
    var(--bg-base);
}

.mobile-header { display: none; }

.mobile-title {
  margin: 0;
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.mobile-desc {
  margin: 8px 0 0;
  font-size: 0.84rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

.content-grid {
  display: grid;
  grid-template-columns: minmax(340px, 400px) minmax(0, 1fr);
  gap: 24px;
  align-items: start;
}

@media (max-width: 1080px) {
  .content-grid { grid-template-columns: 1fr; }
}

@media (max-width: 800px) {
  .mobile-header { display: block; padding-top: 42px; }
}

@media (max-width: 640px) {
  .workspace { padding: 14px; gap: 14px; }
  .mobile-header { padding-top: 40px; }
}
</style>
