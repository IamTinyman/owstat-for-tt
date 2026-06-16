<script setup lang="ts">
import { useModulesStore } from '@/stores/modules'
import QueryTopBar from './QueryTopBar.vue'
import QueryForm from '@/components/workspace/QueryForm.vue'
import ImageResult from '@/components/preview/ImageResult.vue'

defineEmits<{ back: [] }>()

const modulesStore = useModulesStore()
</script>

<template>
  <div class="query-page" v-if="modulesStore.activeModule">
    <QueryTopBar
      :title="modulesStore.activeModule.title"
      :description="modulesStore.activeModule.description"
      @back="$emit('back')"
    />

    <div class="query-body">
      <div class="form-bar">
        <QueryForm />
      </div>
      <div class="result-area">
        <ImageResult />
      </div>
    </div>
  </div>
</template>

<style scoped>
.query-page {
  min-height: 100vh;
  background: var(--bg-base);
  display: grid;
  grid-template-rows: auto 1fr;
}

.query-body {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 0;
  overflow: hidden;
  height: calc(100vh - 72px);
}

.form-bar {
  padding: 20px;
  border-right: 1px solid var(--hairline);
  overflow-y: auto;
  background: var(--bg-surface);
}

.result-area {
  padding: 20px 24px;
  overflow-y: auto;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

@media (max-width: 900px) {
  .query-body {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr;
    height: auto;
    min-height: calc(100vh - 72px);
  }
  .form-bar {
    border-right: none;
    border-bottom: 1px solid var(--hairline);
    padding: 14px;
  }
  .result-area { padding: 14px; }
}
</style>
