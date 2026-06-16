<script setup lang="ts">
import { ref, watch } from 'vue'
import { useModulesStore } from '@/stores/modules'
import { useRequestStore } from '@/stores/request'
import DynamicField from './DynamicField.vue'
import TargetInput from './TargetInput.vue'

const modulesStore = useModulesStore()
const requestStore = useRequestStore()

const fieldStates = ref<{ fieldId: string; payloadKey: string; value: string | boolean }[]>([])

function rebuildFields() {
  const mod = modulesStore.activeModule
  if (!mod) { fieldStates.value = []; return }
  const saved = requestStore.getSession().fieldValues
  fieldStates.value = mod.fields.map((f) => ({
    fieldId: f.id,
    payloadKey: f.payload_key,
    value: saved[f.payload_key] != null
      ? saved[f.payload_key]
      : f.control_type === 'checkbox'
        ? Boolean(f.default)
        : (f.default != null ? String(f.default) : ''),
  }))
}

rebuildFields()

watch(() => modulesStore.activeModuleId, (newId, oldId) => {
  if (oldId) {
    const oldSession = requestStore.sessionFor(oldId)
    if (oldSession) {
      const values: Record<string, string | boolean> = {}
      for (const s of fieldStates.value) { values[s.payloadKey] = s.value }
      oldSession.fieldValues = values
    }
  }
  rebuildFields()
})

function collectPayload(): Record<string, unknown> {
  const mod = modulesStore.activeModule
  if (!mod) return {}
  const payload: Record<string, unknown> = {}
  for (const s of fieldStates.value) {
    if (typeof s.value === 'boolean') { payload[s.payloadKey] = s.value; continue }
    const v = String(s.value).trim()
    if (v) payload[s.payloadKey] = v
  }
  if (mod.requires_target && requestStore.targetValue.trim()) {
    payload[mod.default_target_key] = requestStore.targetValue.trim()
  }
  const session = requestStore.getSession()
  const values: Record<string, string | boolean> = {}
  for (const s of fieldStates.value) { values[s.payloadKey] = s.value }
  session.fieldValues = values
  return payload
}

async function handleSubmit() {
  await requestStore.submitRequest(collectPayload())
}
</script>

<template>
  <div class="query-card">
    <div class="card-head">
      <h3>查询参数</h3>
      <span class="card-sub">填写后点击查询即可生成图片</span>
    </div>

    <form class="query-form" @submit.prevent="handleSubmit">
      <div class="field-grid">
        <TargetInput v-if="modulesStore.activeModule?.requires_target" />
        <DynamicField
          v-for="(s, idx) in fieldStates"
          :key="s.fieldId"
          :field="modulesStore.activeModule?.fields[idx]!"
          v-model="fieldStates[idx].value"
        />
      </div>

      <div class="form-actions">
        <button class="submit-btn" type="submit" :disabled="requestStore.isLoading">
          <span v-if="requestStore.isLoading" class="btn-spinner"></span>
          <span>{{ requestStore.isLoading ? '查询中' : '开始查询' }}</span>
        </button>
        <span class="status-text" :class="{ 'is-error': requestStore.status === 'error' }">
          {{ requestStore.statusMessage }}
        </span>
      </div>
    </form>
  </div>
</template>

<style scoped>
.query-card {
  background: var(--bg-surface);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-lg);
  padding: 28px;
}

.card-head { margin-bottom: 24px; }

.card-head h3 {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.card-sub {
  display: block;
  margin-top: 6px;
  color: var(--text-muted);
  font-size: 0.84rem;
}

.query-form { display: grid; gap: 22px; }

.field-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.form-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.submit-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border: none;
  border-radius: var(--radius-md);
  padding: 12px 32px;
  background: linear-gradient(135deg, var(--accent), var(--accent-strong));
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: transform 140ms var(--ease-out), box-shadow 140ms var(--ease-out);
  box-shadow: 0 4px 18px var(--accent-glow-strong);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 28px var(--accent-glow-strong);
}

.submit-btn:active:not(:disabled) { transform: translateY(0); }
.submit-btn:disabled { opacity: 0.6; cursor: not-allowed; }

.btn-spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,0.2);
  border-top-color: var(--text-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.status-text { color: var(--text-muted); font-size: 0.85rem; }
.status-text.is-error { color: var(--danger); }

@media (max-width: 640px) {
  .field-grid { grid-template-columns: 1fr; }
  .query-card { padding: 18px; }
}
</style>
