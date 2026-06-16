<script setup lang="ts">
import { useModulesStore } from '@/stores/modules'

const modulesStore = useModulesStore()
</script>

<template>
  <section class="hero" v-if="modulesStore.activeModule">
    <div class="hero-content">
      <h2>{{ modulesStore.activeModule.title }}</h2>
      <p>{{ modulesStore.activeModule.description }}</p>
    </div>
  </section>
</template>

<style scoped>
.hero {
  padding: 24px 28px;
  background: var(--bg-surface);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-lg);
}

.hero-content h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

.hero-content p {
  margin: 8px 0 0;
  color: var(--text-secondary);
  line-height: 1.6;
  font-size: 0.92rem;
}

@media (max-width: 640px) {
  .hero { padding: 18px 20px; }
  .hero-content h2 { font-size: 1.25rem; }
}
</style>
