<script setup lang="ts">
import { ref } from 'vue'
import MainApp from '@/components/MainApp.vue'
import LoginView from '@/components/LoginView.vue'

const authed = ref(localStorage.getItem('overstats_auth') === '1')

function onLogin() {
  authed.value = true
}
</script>

<template>
  <LoginView v-if="!authed" @login="onLogin" />
  <MainApp v-else />
</template>
