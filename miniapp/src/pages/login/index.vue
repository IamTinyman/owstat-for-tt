<template>
  <view class="login-shell">
    <view class="login-card" :class="{ shake: shaking }">
      <text class="login-title">Overstats</text>
      <text class="login-desc">这是Tinyman（小笨蛋）给潼潼宝宝（小坏蛋）做的独享查询网站</text>
      <view class="login-form">
        <text class="pw-label">密码</text>
        <input
          v-model="password"
          type="number"
          :maxlength="4"
          password
          placeholder="····"
          class="pw-input"
          :class="{ 'input-error': shaking }"
          @confirm="handleSubmit"
        />
        <button class="login-btn" @tap="handleSubmit">进入</button>
      </view>
      <text v-if="shaking" class="error-msg">密码不对哦</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const password = ref('')
const shaking = ref(false)

function handleSubmit() {
  if (password.value === '0320') {
    uni.setStorageSync('overstats_auth', '1')
    uni.reLaunch({ url: '/pages/index/index' })
  } else {
    shaking.value = true
    password.value = ''
    setTimeout(() => { shaking.value = false }, 500)
  }
}
</script>

<style lang="scss" scoped>
$bg-base: #131820;
$bg-surface: #19202b;
$accent: #e8924e;
$accent-strong: #d07830;
$danger: #dc5a4a;
$hairline: rgba(255,255,255,0.06);
$line-strong: rgba(255,255,255,0.12);
$text-primary: #f0ede6;
$text-secondary: #a8a39a;
$text-muted: #6b6560;

.login-shell {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 48rpx;
  background: $bg-base;
}

.login-card {
  width: 100%;
  max-width: 600rpx;
  background: $bg-surface;
  border: 1px solid $hairline;
  border-radius: 48rpx;
  padding: 80rpx 60rpx 72rpx;
  text-align: center;

  &.shake {
    animation: shake 0.4s ease;
  }
}

.login-title {
  display: block;
  font-size: 56rpx;
  font-weight: 800;
  color: $text-primary;
  letter-spacing: -2rpx;
}

.login-desc {
  display: block;
  margin-top: 20rpx;
  font-size: 28rpx;
  color: $text-secondary;
  line-height: 1.6;
}

.login-form {
  margin-top: 56rpx;
}

.pw-label {
  display: block;
  font-size: 24rpx;
  font-weight: 600;
  color: $text-muted;
  text-transform: uppercase;
  letter-spacing: 4rpx;
  margin-bottom: 16rpx;
}

.pw-input {
  width: 280rpx;
  margin: 0 auto;
  border: 1px solid $line-strong;
  border-radius: 20rpx;
  padding: 28rpx 32rpx;
  background: $bg-base;
  text-align: center;
  font-size: 48rpx;
  letter-spacing: 16rpx;
  color: $text-primary;

  &.input-error {
    border-color: $danger;
  }
}

.login-btn {
  width: 100%;
  margin-top: 40rpx;
  border: none;
  border-radius: 20rpx;
  padding: 28rpx 0;
  background: linear-gradient(135deg, $accent, $accent-strong);
  color: $text-primary;
  font-weight: 600;
  font-size: 32rpx;

  &::after { border: none; }
}

.error-msg {
  display: block;
  margin-top: 20rpx;
  color: $danger;
  font-size: 28rpx;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-12rpx); }
  40% { transform: translateX(12rpx); }
  60% { transform: translateX(-8rpx); }
  80% { transform: translateX(6rpx); }
}
</style>
