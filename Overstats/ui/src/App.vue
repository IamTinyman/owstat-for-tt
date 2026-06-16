<script setup lang="ts">
import { ref } from 'vue'
import AppShell from '@/components/layout/AppShell.vue'
import LoginView from '@/components/LoginView.vue'

const authed = ref(localStorage.getItem('overstats_auth') === '1')

function onLogin() {
  authed.value = true
}
</script>

<template>
  <LoginView v-if="!authed" @login="onLogin" />
  <AppShell v-else />
</template>
