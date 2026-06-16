<script setup lang="ts">
import { useRequestStore } from '@/stores/request'

const requestStore = useRequestStore()

function fillXiaoHuai() { requestStore.targetValue = '小坏蛋#53106' }
function fillZhiyi() { requestStore.targetValue = '意志坚强酱#5821' }
</script>

<template>
  <template v-if="requestStore.targetType">
    <label class="field">
      <span>目标类型</span>
      <select v-model="requestStore.targetType">
        <option value="bnet_id">bnet_id</option>
        <option value="customer_token">customer_token</option>
      </select>
    </label>

    <label class="field field-span-2">
      <span>目标值</span>
      <div class="target-input-row">
        <input
          v-model="requestStore.targetValue"
          type="text"
          placeholder="Player#12345"
          autocomplete="off"
        />
        <button
          v-if="requestStore.targetType === 'bnet_id'"
          type="button"
          class="quick-fill-btn"
          @click="fillXiaoHuai"
        >小坏蛋</button>
        <button
          v-if="requestStore.targetType === 'bnet_id'"
          type="button"
          class="quick-fill-btn"
          @click="fillZhiyi"
        >意志坚强酱</button>
      </div>
    </label>
  </template>
</template>

<style scoped>
.field {
  display: grid;
  gap: 8px;
}

.field span {
  font-size: 0.84rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.field input,
.field select {
  width: 100%;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius-sm);
  padding: 11px 13px;
  background: var(--bg-base);
  color: var(--text-primary);
  font-size: 0.92rem;
  outline: none;
  transition: border-color 150ms var(--ease-out);
}

.field input:focus,
.field select:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-glow);
}

.field-span-2 { grid-column: span 2; }

.target-input-row { display: flex; gap: 8px; }
.target-input-row input { flex: 1; }

.quick-fill-btn {
  flex-shrink: 0;
  border: 1px solid var(--accent-glow);
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  background: var(--accent-glow);
  color: var(--accent-light);
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  white-space: nowrap;
  transition: background 140ms var(--ease-out), transform 100ms var(--ease-out);
}

.quick-fill-btn:hover {
  background: rgba(232, 146, 78, 0.22);
  transform: translateY(-1px);
}

.quick-fill-btn:active { transform: translateY(0); }

@media (max-width: 640px) {
  .field-span-2 { grid-column: auto; }
}
</style>
