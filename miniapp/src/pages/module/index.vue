<template>
  <view class="module-page" v-if="mod">
    <!-- Top Bar -->
    <view class="topbar">
      <view class="back-btn" @tap="goBack">
        <text class="back-arrow">‹</text>
      </view>
      <view class="topbar-info">
        <text class="topbar-title">{{ mod.title }}</text>
      </view>
    </view>

    <!-- Form -->
    <view class="form-area">
      <!-- Target input -->
      <view v-if="mod.requires_target" class="field">
        <text class="field-label">目标类型</text>
        <picker :value="targetTypeIndex" :range="['bnet_id', 'customer_token']" @change="onTargetTypeChange">
          <view class="picker-val">{{ requestStore.targetType }}</view>
        </picker>
      </view>
      <view v-if="mod.requires_target" class="field">
        <text class="field-label">目标值</text>
        <view class="input-row">
          <input class="field-input" v-model="requestStore.targetValue" placeholder="Player#12345" />
          <view v-if="requestStore.targetType === 'bnet_id'" class="quick-fill" @tap="requestStore.targetValue = '小坏蛋#53106'">
            <text>小坏蛋</text>
          </view>
          <view v-if="requestStore.targetType === 'bnet_id'" class="quick-fill" @tap="requestStore.targetValue = '意志坚强酱#5821'">
            <text>意志坚强酱</text>
          </view>
        </view>
      </view>

      <!-- Dynamic fields -->
      <view v-for="f in mod.fields" :key="f.id" class="field">
        <text class="field-label">{{ f.label }}</text>
        <template v-if="f.control_type === 'checkbox'">
          <switch :checked="fieldMap[f.payload_key] === true" @change="setField(f.payload_key, $event.detail.value)" />
        </template>
        <template v-else-if="f.control_type === 'select'">
          <picker :value="selectIndex(f)" :range="f.options.map(o => o.label)" @change="onSelectChange(f, $event.detail.value)">
            <view class="picker-val">{{ selectLabel(f) }}</view>
          </picker>
        </template>
        <template v-else>
          <view class="input-row">
            <input
              class="field-input"
              :type="f.control_type === 'number' ? 'number' : 'text'"
              :placeholder="f.placeholder"
              :value="fieldMap[f.payload_key] || ''"
              @input="setField(f.payload_key, ($event.detail as any).value)"
            />
            <template v-if="isBnetField(f)">
              <view class="quick-fill" @tap="setField(f.payload_key, '小坏蛋#53106')"><text>小坏蛋</text></view>
              <view class="quick-fill" @tap="setField(f.payload_key, '意志坚强酱#5821')"><text>意志坚强酱</text></view>
            </template>
          </view>
        </template>
      </view>

      <!-- Submit -->
      <button
        class="submit-btn"
        :disabled="requestStore.isLoading"
        @tap="handleSubmit"
      >
        {{ requestStore.isLoading ? '查询中...' : '开始查询' }}
      </button>
      <text v-if="requestStore.statusMessage" class="status-text" :class="{ error: requestStore.status === 'error' }">
        {{ requestStore.statusMessage }}
      </text>
    </view>

    <!-- Result -->
    <view class="result-area">
      <view v-if="requestStore.status === 'idle'" class="empty-state">
        <text class="empty-text">填写参数后点击查询</text>
      </view>
      <view v-else-if="requestStore.isLoading" class="loading-state">
        <text>生成图片中...</text>
      </view>
      <view v-else-if="requestStore.status === 'error'" class="empty-state">
        <text class="error-text">{{ requestStore.errorMessage }}</text>
      </view>
      <image
        v-else-if="requestStore.images.length > 0"
        :src="requestStore.images[0].url"
        mode="widthFix"
        class="result-image"
        @tap="previewImage"
      />
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useModulesStore } from '@/stores/modules'
import { useRequestStore } from '@/stores/request'
import type { FieldSpec } from '@/types'

const modulesStore = useModulesStore()
const requestStore = useRequestStore()

const mod = computed(() => modulesStore.activeModule)
const targetTypeIndex = computed(() => requestStore.targetType === 'customer_token' ? 1 : 0)

const fieldMap = reactive<Record<string, any>>({})

function isBnetField(f: FieldSpec): boolean {
  return f.id.includes('bnet_id') || f.payload_key.includes('bnet_id')
}

function setField(key: string, val: any) {
  fieldMap[key] = val
}

function selectIndex(f: FieldSpec): number {
  const v = fieldMap[f.payload_key] || f.default || ''
  return f.options.findIndex(o => o.value === v)
}

function selectLabel(f: FieldSpec): string {
  const idx = selectIndex(f)
  return idx >= 0 ? f.options[idx].label : '请选择'
}

function onTargetTypeChange(e: any) {
  requestStore.targetType = Number(e.detail.value) === 1 ? 'customer_token' : 'bnet_id'
}

function onSelectChange(f: FieldSpec, idx: number) {
  fieldMap[f.payload_key] = f.options[idx]?.value || ''
}

async function handleSubmit() {
  if (!mod.value) return
  const payload: Record<string, unknown> = {}
  for (const f of mod.value.fields) {
    const v = fieldMap[f.payload_key]
    if (v != null && v !== '') payload[f.payload_key] = v
  }
  if (mod.value.requires_target && requestStore.targetValue.trim()) {
    payload[mod.value.default_target_key] = requestStore.targetValue.trim()
  }
  await requestStore.submitRequest(payload)
}

function previewImage() {
  if (requestStore.images.length > 0) {
    uni.previewImage({ urls: [requestStore.images[0].url] })
  }
}

function goBack() {
  uni.navigateBack()
}

onMounted(() => {
  if (modulesStore.activeModule) {
    requestStore.resetForm()
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
$accent-strong: #d07830;
$accent-glow: rgba(232,146,78,0.15);
$danger: #dc5a4a;
$hairline: rgba(255,255,255,0.06);
$line: rgba(255,255,255,0.08);

.module-page {
  min-height: 100vh;
  background: $bg-base;
}

/* ── Topbar ── */
.topbar {
  display: flex;
  align-items: center;
  gap: 24rpx;
  padding: 24rpx 28rpx;
  border-bottom: 1px solid $hairline;
  background: $bg-surface;
}

.back-btn {
  width: 64rpx; height: 64rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid $hairline;
  border-radius: 16rpx;
}

.back-arrow { font-size: 52rpx; color: $text-secondary; line-height: 1; }

.topbar-title {
  font-size: 34rpx;
  font-weight: 700;
  color: $text-primary;
}

/* ── Form ── */
.form-area {
  padding: 28rpx;
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.field-label {
  font-size: 26rpx;
  font-weight: 600;
  color: $text-secondary;
}

.field-input {
  flex: 1;
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 12rpx;
  padding: 20rpx 24rpx;
  background: $bg-base;
  color: $text-primary;
  font-size: 28rpx;
}

.input-row {
  display: flex;
  gap: 12rpx;
  align-items: center;
}

.quick-fill {
  flex-shrink: 0;
  border: 1px solid $accent-glow;
  border-radius: 12rpx;
  padding: 16rpx 20rpx;
  background: $accent-glow;
  color: $accent-light;
  font-size: 24rpx;
  font-weight: 600;

  &:active { background: rgba(232,146,78,0.22); }
}

.picker-val {
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 12rpx;
  padding: 20rpx 24rpx;
  background: $bg-base;
  color: $text-primary;
  font-size: 28rpx;
}

.submit-btn {
  width: 100%;
  margin-top: 8rpx;
  border: none;
  border-radius: 20rpx;
  padding: 28rpx 0;
  background: linear-gradient(135deg, $accent, $accent-strong);
  color: $text-primary;
  font-weight: 600;
  font-size: 30rpx;

  &::after { border: none; }

  &[disabled] { opacity: 0.5; }
}

.status-text {
  font-size: 26rpx;
  color: $text-muted;
  text-align: center;
  &.error { color: $danger; }
}

/* ── Result ── */
.result-area {
  padding: 0 20rpx 40rpx;
}

.empty-state {
  padding: 120rpx 0;
  text-align: center;
}

.empty-text { color: $text-muted; font-size: 28rpx; }
.error-text { color: $danger; font-size: 28rpx; }

.loading-state {
  padding: 120rpx 0;
  text-align: center;
  color: $text-muted;
}

.result-image {
  width: 100%;
  border-radius: 16rpx;
}
</style>
