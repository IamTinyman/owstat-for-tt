<script setup lang="ts">
import { computed } from 'vue'
import type { FieldSpec } from '@/types'

const props = defineProps<{ field: FieldSpec }>()
const model = defineModel<string | boolean>()

function isChecked(): boolean { return typeof model.value === 'boolean' ? model.value : false }
function textValue(): string { return typeof model.value === 'string' ? model.value : String(props.field.default || '') }

const isBnetIdField = computed(() =>
  props.field.id.includes('bnet_id') || props.field.payload_key.includes('bnet_id')
)

function fillXiaoHuai() { model.value = '小坏蛋#53106' }
function fillZhiyi() { model.value = '意志坚强酱#5821' }
</script>

<template>
  <label class="field">
    <span>{{ field.label }}</span>

    <template v-if="field.control_type === 'checkbox'">
      <input type="checkbox" :checked="isChecked()"
        @change="model = ($event.target as HTMLInputElement).checked" />
    </template>

    <template v-else-if="field.control_type === 'select'">
      <select :value="textValue()"
        @change="model = ($event.target as HTMLSelectElement).value">
        <option v-for="opt in field.options" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>
    </template>

    <template v-else>
      <div class="input-row">
        <input
          :type="field.control_type === 'number' ? 'number' : 'text'"
          :placeholder="field.placeholder"
          :value="textValue()"
          @input="model = ($event.target as HTMLInputElement).value"
        />
        <template v-if="isBnetIdField && field.control_type !== 'number'">
          <button type="button" class="quick-fill-btn" @click="fillXiaoHuai">小坏蛋</button>
          <button type="button" class="quick-fill-btn" @click="fillZhiyi">意志坚强酱</button>
        </template>
      </div>
    </template>

    <small v-if="field.help_text">{{ field.help_text }}</small>
  </label>
</template>

<style scoped>
.field { display: grid; gap: 8px; }

.field span {
  font-size: 0.84rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.field small {
  color: var(--text-muted);
  line-height: 1.45;
  font-size: 0.78rem;
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

.field input[type="checkbox"] {
  width: auto;
  justify-self: start;
}

.input-row { display: flex; gap: 8px; }
.input-row input { flex: 1; }

.quick-fill-btn {
  flex-shrink: 0;
  border: 1px solid var(--accent-glow);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  background: var(--accent-glow);
  color: var(--accent-light);
  font-weight: 600;
  font-size: 0.78rem;
  cursor: pointer;
  white-space: nowrap;
  transition: background 140ms var(--ease-out), transform 100ms var(--ease-out);
}

.quick-fill-btn:hover {
  background: rgba(232, 146, 78, 0.22);
  transform: translateY(-1px);
}

.quick-fill-btn:active { transform: translateY(0); }
</style>
