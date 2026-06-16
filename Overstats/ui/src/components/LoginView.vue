<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{ login: [] }>()
const password = ref('')
const shaking = ref(false)

function handleSubmit() {
  if (password.value === '0320') {
    localStorage.setItem('overstats_auth', '1')
    emit('login')
  } else {
    shaking.value = true
    password.value = ''
    setTimeout(() => { shaking.value = false }, 500)
  }
}
</script>

<template>
  <div class="login-shell">
    <div class="login-card" :class="{ shake: shaking }">
      <div class="login-mark">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
          <path d="M16 2C8.268 2 2 8.268 2 16s6.268 14 14 14 14-6.268 14-14S23.732 2 16 2z" stroke="var(--accent)" stroke-width="1.5" opacity="0.4"/>
          <path d="M16 6a4 4 0 00-4 4v2a6 6 0 00-6 6v2h20v-2a6 6 0 00-6-6v-2a4 4 0 00-4-4z" stroke="var(--accent)" stroke-width="1.5" fill="none"/>
        </svg>
      </div>
      <h1 class="login-title">Overstats</h1>
      <p class="login-desc">这是Tinyman（小笨蛋）给潼潼宝宝（小坏蛋）做的独享查询网站</p>
      <form class="login-form" @submit.prevent="handleSubmit">
        <label class="pw-label">密码</label>
        <input
          v-model="password"
          type="password"
          inputmode="numeric"
          maxlength="4"
          placeholder="····"
          autocomplete="off"
          class="pw-input"
          :class="{ 'input-error': shaking }"
        />
        <button type="submit" class="login-btn">进入</button>
      </form>
      <p v-if="shaking" class="error-msg">密码不对哦</p>
    </div>
  </div>
</template>

<style scoped>
.login-shell {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 24px;
  background:
    radial-gradient(ellipse 80% 60% at 30% 20%, rgba(232, 146, 78, 0.08), transparent),
    radial-gradient(ellipse 60% 70% at 80% 80%, rgba(232, 146, 78, 0.04), transparent),
    var(--bg-base);
}

.login-card {
  width: 100%;
  max-width: 360px;
  background: var(--bg-surface);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-xl);
  padding: 48px 36px 40px;
  text-align: center;
  box-shadow: var(--shadow-lg);
}

.login-card.shake {
  animation: shake 0.4s ease;
}

.login-mark { margin-bottom: 16px; }

.login-title {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.login-desc {
  margin: 12px 0 0;
  font-size: 0.88rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

.login-form {
  margin-top: 32px;
  display: grid;
  gap: 16px;
}

.pw-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.pw-input {
  width: 100%;
  max-width: 160px;
  margin: 0 auto;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  background: var(--bg-base);
  text-align: center;
  font-size: 1.4rem;
  letter-spacing: 0.3em;
  color: var(--text-primary);
  outline: none;
  transition: border-color 180ms var(--ease-out);
}

.pw-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-glow);
}

.pw-input.input-error {
  border-color: var(--danger);
  background: rgba(220, 90, 74, 0.06);
}

.login-btn {
  width: 100%;
  border: none;
  border-radius: var(--radius-md);
  padding: 14px 32px;
  background: linear-gradient(135deg, var(--accent), var(--accent-strong));
  color: var(--text-primary);
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 140ms var(--ease-out), box-shadow 140ms var(--ease-out);
  box-shadow: 0 4px 20px var(--accent-glow-strong);
  margin-top: 4px;
}

.login-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 30px var(--accent-glow-strong);
}

.login-btn:active { transform: translateY(0); }

.error-msg {
  margin: 12px 0 0;
  color: var(--danger);
  font-size: 0.85rem;
  font-weight: 500;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-6px); }
  40% { transform: translateX(6px); }
  60% { transform: translateX(-4px); }
  80% { transform: translateX(3px); }
}
</style>
